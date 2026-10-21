"""Bounded, read-only flattened device tree parser (DTB version 17).

Values remain bytes. No device properties are executed or treated as paths.
"""
from dataclasses import dataclass, field
import struct


class FDTError(ValueError):
    pass


def cells(value):
    if len(value) % 4:
        raise FDTError('property is not a whole number of cells')
    return list(struct.unpack('>%dI' % (len(value) // 4), value))


def integer(value):
    return int.from_bytes(value, 'big')


def strings(value):
    if not value or value[-1] != 0:
        raise FDTError('unterminated string property')
    return value[:-1].decode('utf-8', errors='strict').split('\0')


@dataclass
class Node:
    name: str
    parent: 'Node | None' = None
    props: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    @property
    def path(self):
        return '/' if self.parent is None else self.parent.path.rstrip('/') + '/' + self.name

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()

    def u32(self, name, default=None):
        value = self.props.get(name)
        if value is None:
            return default
        if len(value) != 4:
            raise FDTError(f'{self.path}:{name} must contain one cell')
        return integer(value)

    def text(self, name, default=None):
        return strings(self.props[name]) if name in self.props else default

    def inherited(self, name):
        node = self
        while node is not None:
            if name in node.props:
                return node.props[name]
            node = node.parent
        return None


@dataclass
class Tree:
    root: Node
    reservations: list
    total_size: int

    def by_path(self, path):
        return next((n for n in self.root.walk() if n.path == path), None)


def parse(blob):
    if not 40 <= len(blob) <= 64 * 1024 * 1024:
        raise FDTError('DTB length outside 40-byte..64-MiB bound')
    magic, total, st, ss, rv, ver, compat, _, strings_size, struct_size = struct.unpack_from('>10I', blob)
    if magic != 0xd00dfeed or not 40 <= total <= len(blob) or ver != 17 or compat > 17:
        raise FDTError('invalid or unsupported DTB header')
    if st % 4 or rv % 8 or min(st, ss, rv) < 40:
        raise FDTError('invalid block alignment/offset')
    if st + struct_size > total or ss + strings_size > total or rv + 16 > total:
        raise FDTError('block exceeds totalsize')
    if max(st, ss) < min(st + struct_size, ss + strings_size):
        raise FDTError('structure and strings blocks overlap')
    reservations = []
    r = rv
    reserve_end = min(x for x in (st, ss, total) if x > rv)
    while r + 16 <= reserve_end:
        address, size = struct.unpack_from('>QQ', blob, r)
        r += 16
        if address == size == 0:
            break
        if address + size > 1 << 64:
            raise FDTError('reservation overflows 64 bits')
        reservations.append({'address': address, 'size': size})
    else:
        raise FDTError('unterminated reservation block')
    if any(max(rv, off) < min(r, off + size) for off, size in
           ((st, struct_size), (ss, strings_size))):
        raise FDTError('reservation block overlaps another block')
    stack, root, i = [], None, st
    node_count = 0
    while i + 4 <= st + struct_size:
        token = struct.unpack_from('>I', blob, i)[0]
        i += 4
        if token == 1:
            node_count += 1
            if node_count > 100000:
                raise FDTError('too many nodes')
            end = blob.find(b'\0', i, st + struct_size)
            if end < 0 or len(stack) >= 128:
                raise FDTError('invalid node name/depth')
            name = blob[i:end].decode('utf-8', errors='strict')
            if '/' in name or (not stack and (root is not None or name)):
                raise FDTError('invalid root/node name')
            node = Node(name, stack[-1] if stack else None)
            if stack:
                if any(c.name == name for c in stack[-1].children):
                    raise FDTError('duplicate node name')
                stack[-1].children.append(node)
            else:
                root = node
            stack.append(node)
            i = (end + 4) & ~3
        elif token == 2:
            if not stack:
                raise FDTError('unmatched END_NODE')
            stack.pop()
        elif token == 3:
            if not stack or i + 8 > st + struct_size:
                raise FDTError('property outside node/truncated header')
            size, off = struct.unpack_from('>II', blob, i)
            i += 8
            if off >= strings_size or i + size > st + struct_size:
                raise FDTError('property/string outside declared blocks')
            end = blob.find(b'\0', ss + off, ss + strings_size)
            if end < 0:
                raise FDTError('unterminated property name')
            name = blob[ss + off:end].decode('utf-8', errors='strict')
            if not name or name in stack[-1].props:
                raise FDTError('empty/duplicate property name')
            stack[-1].props[name] = blob[i:i + size]
            i = (i + size + 3) & ~3
        elif token == 4:
            continue
        elif token == 9:
            if stack or root is None:
                raise FDTError('unclosed/missing root')
            handles = set()
            for node in root.walk():
                phandle = node.u32('phandle', node.u32('linux,phandle'))
                if phandle is not None:
                    if not phandle or phandle in handles:
                        raise FDTError('invalid/duplicate phandle')
                    handles.add(phandle)
            return Tree(root, reservations, total)
        else:
            raise FDTError(f'unknown token {token}')
    raise FDTError('missing FDT_END')


def reg(node):
    if 'reg' not in node.props:
        return []
    if node.parent is None:
        raise FDTError('root cannot have reg')
    ac, sc = node.parent.u32('#address-cells', 2), node.parent.u32('#size-cells', 1)
    if ac not in (1, 2) or sc not in (0, 1, 2):
        raise FDTError('unsupported address/size cell count')
    values = cells(node.props['reg'])
    stride = ac + sc
    if len(values) % stride:
        raise FDTError(f'{node.path}: malformed reg')
    join = lambda c: sum(v << (32 * (len(c) - j - 1)) for j, v in enumerate(c))
    return [{'address': join(values[i:i + ac]), 'size': join(values[i + ac:i + stride])}
            for i in range(0, len(values), stride)]


def interrupts(tree, node):
    providers = {n.u32('phandle', n.u32('linux,phandle')): n for n in tree.root.walk()
                 if 'phandle' in n.props or 'linux,phandle' in n.props}
    items = []
    if 'interrupts-extended' in node.props:
        values = cells(node.props['interrupts-extended'])
        while values:
            provider = providers.get(values.pop(0))
            if provider is None:
                raise FDTError('unknown interrupt provider')
            count = provider.u32('#interrupt-cells')
            if count is None or not 1 <= count <= 16 or len(values) < count:
                raise FDTError('invalid interrupt provider cell count')
            items.append((provider, values[:count]))
            del values[:count]
    elif 'interrupts' in node.props:
        # Walk the interrupt-parent chain. A physical parent with
        # #interrupt-cells takes precedence over an ancestor's default.
        current, provider, visited = node, None, set()
        while current is not None:
            if id(current) in visited:
                raise FDTError('cyclic interrupt parent chain')
            visited.add(id(current))
            parent = current.props.get('interrupt-parent')
            if parent is not None:
                if len(parent) != 4 or integer(parent) not in providers:
                    raise FDTError('unknown interrupt provider')
                current = providers[integer(parent)]
            else:
                current = current.parent
            if current is not None and '#interrupt-cells' in current.props:
                provider = current
                break
        if provider is None:
            raise FDTError(f'{node.path}: interrupt parent unresolved')
        count = provider.u32('#interrupt-cells')
        values = cells(node.props['interrupts'])
        if count is None or not 1 <= count <= 16 or len(values) % count:
            raise FDTError('interrupt specifier size mismatch')
        items = [(provider, values[i:i + count]) for i in range(0, len(values), count)]
    out = []
    for provider, spec in items:
        record = {'provider': provider.path, 'cells': spec}
        if 'arm,gic-v3' in provider.text('compatible', []) and len(spec) in (3, 4):
            if spec[0] not in (0, 1) or (spec[0] == 1 and spec[1] >= 16) or (spec[0] == 0 and spec[1] >= 988):
                raise FDTError('invalid GIC SPI/PPI type/number')
            record.update(kind='SPI' if spec[0] == 0 else 'PPI',
                          intid=spec[1] + (32 if spec[0] == 0 else 16), flags=spec[2])
        out.append(record)
    return out
