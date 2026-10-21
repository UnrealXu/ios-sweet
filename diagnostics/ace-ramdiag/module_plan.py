#!/usr/bin/env python3
"""Offline Ace module dependency plan; never loads modules or contacts hardware.

Symbol/soft dependencies determine insertion order. DT provider edges are kept
separate: a successful insertion does not prove probe/binding or deferred-probe
completion. Unknown mappings remain explicit, never presumed built in.
"""
import argparse
import fnmatch
import hashlib
import heapq
import importlib.util
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import fdt

VENDOR_SHA = 'bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670'
FDT_SHA = '68c811fbaae657372d740c25ff81f03c9763eab3e897b0a7104d624ec598560b'
KERNEL_SHA = '8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'
SEEDS = ['/soc/ufshci@112b0000', '/soc/usb0@11201000',
         '/soc/watchdog@1c007000/reboot-mode']
RETURN_PREFIX = ['mtk_wdt.ko', 'reboot-mode.ko', 'syscon-reboot-mode.ko']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def module_name(value):
    if value.startswith('/lib/modules/'):
        value = value[len('/lib/modules/'):]
    require(re.fullmatch(r'[A-Za-z0-9_+-]+(?:\.ko)?', value), 'unsafe module name: ' + value)
    return value[:-3] if value.endswith('.ko') else value


class Dependencies:
    def __init__(self, filenames, dep_text, soft_text):
        self.names = {}
        for filename in filenames:
            key = module_name(filename).replace('-', '_')
            require(key not in self.names, 'ambiguous normalized module name: ' + key)
            self.names[key] = filename
        self.hard = {}
        for line in dep_text.splitlines():
            if not line.strip():
                continue
            require(line.count(':') == 1, 'malformed modules.dep line')
            name, values = line.split(':')
            name = self.resolve(name)
            require(name not in self.hard, 'duplicate modules.dep entry: ' + name)
            self.hard[name] = {self.resolve(v) for v in values.split()}
        require(set(self.hard) == set(filenames), 'modules.dep does not cover exact archive module set')
        self.pre, self.post = {}, {}
        for line in soft_text.splitlines():
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            words = line.replace('pre:', ' pre: ').replace('post:', ' post: ').split()
            require(len(words) >= 3 and words[0] == 'softdep', 'malformed modules.softdep line')
            name = self.resolve(words[1])
            require(name not in self.pre, 'duplicate soft dependency record')
            self.pre[name], self.post[name] = set(), set()
            target = None
            for word in words[2:]:
                if word in ('pre:', 'post:'):
                    target = self.pre[name] if word == 'pre:' else self.post[name]
                else:
                    require(target is not None, 'soft dependency without pre/post marker')
                    target.add(self.resolve(word))

    def resolve(self, name):
        key = module_name(name).replace('-', '_')
        require(key in self.names, 'unknown module: ' + name)
        return self.names[key]

    def ordered(self, seeds, *, before=(), first=()):
        selected = set()
        pending = [self.resolve(s) for s in seeds]
        while pending:
            name = pending.pop()
            if name in selected:
                continue
            selected.add(name)
            pending.extend(self.hard[name] | self.pre.get(name, set()) | self.post.get(name, set()))
        edges = {n: self.hard[n] | self.pre.get(n, set()) for n in selected}
        for name in selected:
            for post in self.post.get(name, set()):
                edges[post].add(name)
        for provider, consumer in before:
            provider, consumer = self.resolve(provider), self.resolve(consumer)
            require(provider in selected and consumer in selected, 'startup constraint module outside closure')
            edges[consumer].add(provider)
        early = {self.resolve(n) for n in first}
        require(early <= selected, 'early module outside closure')
        for name in early:
            require(edges[name] <= early, 'early module depends on later stage')
        for name in selected - early:
            edges[name].update(early)
        ready = [n for n in selected if not edges[n]]
        heapq.heapify(ready)
        ordered = []
        while ready:
            name = heapq.heappop(ready)
            ordered.append(name)
            for consumer in sorted(selected - set(ordered)):
                if name in edges[consumer]:
                    edges[consumer].remove(name)
                    if not edges[consumer]:
                        heapq.heappush(ready, consumer)
        require(len(ordered) == len(selected), 'module dependency cycle: ' + ','.join(sorted(selected - set(ordered))))
        return ordered


def provider_closure(tree, seeds):
    nodes = {n.path: n for n in tree.root.walk()}
    handles = {}
    for node in nodes.values():
        handle = node.u32('phandle')
        if handle is not None:
            require(handle not in handles and handle not in (0, 0xffffffff), 'duplicate/invalid DT phandle')
            handles[handle] = node
    # Known binding formats only. Vendor string references (e.g. tcpc name)
    # remain listed below; they must not be guessed to be integer phandles.
    tuples = {'clocks': '#clock-cells', 'power-domains': '#power-domain-cells',
              'resets': '#reset-cells', 'phys': '#phy-cells', 'iommus': '#iommu-cells',
              'interconnects': '#interconnect-cells', 'dmas': '#dma-cells',
              'mboxes': '#mbox-cells', 'io-channels': '#io-channel-cells',
              'interrupts-extended': '#interrupt-cells'}
    singles = {'remote-endpoint', 'interrupt-parent', 'extcon', 'charger', 'bootmode'}
    pending = list(seeds)
    visited, edges, unparsed = set(), [], []

    def edge(node, prop, handle, args):
        require(handle in handles, f'unknown phandle {handle:x} at {node.path}:{prop}')
        target = handles[handle]
        edges.append(dict(consumer=node.path, property=prop, provider=target.path, args=args))
        pending.append(target.path)
        return target

    while pending:
        path = pending.pop()
        require(path in nodes, 'missing seed/provider path: ' + path)
        if path in visited:
            continue
        visited.add(path)
        node = nodes[path]
        if node.parent is not None:
            edges.append(dict(consumer=path, property='parent', provider=node.parent.path, args=[]))
            pending.append(node.parent.path)
        # Include graph endpoints, not arbitrary functional children of providers.
        for child in node.children:
            if child.name in ('port', 'ports') or child.name.startswith(('port@', 'endpoint@')):
                pending.append(child.path)
        for prop, value in node.props.items():
            if prop in tuples:
                values, at = fdt.cells(value), 0
                while at < len(values):
                    handle = values[at]
                    if handle == 0:  # optional empty phandle-array slot
                        at += 1
                        continue
                    require(handle in handles, f'unknown tuple phandle at {path}:{prop}')
                    count = handles[handle].u32(tuples[prop])
                    require(count is not None and count <= 16 and at + 1 + count <= len(values), f'bad specifier at {path}:{prop}')
                    edge(node, prop, handle, values[at + 1:at + 1 + count])
                    at += count + 1
            elif prop in singles or prop.endswith('-supply'):
                values = fdt.cells(value)
                require(len(values) == 1, f'expected single phandle at {path}:{prop}')
                edge(node, prop, values[0], [])
            elif re.fullmatch(r'pinctrl-[0-9]+', prop):
                for handle in fdt.cells(value):
                    edge(node, prop, handle, [])
            elif prop == 'mediatek,syscon-wakeup':
                values = fdt.cells(value)
                require(len(values) == 3, 'unexpected syscon-wakeup format')
                edge(node, prop, values[0], values[1:])
            elif prop == 'gpio-ranges':
                values = fdt.cells(value)
                require(len(values) % 4 == 0, 'bad gpio-ranges')
                for at in range(0, len(values), 4):
                    edge(node, prop, values[at], values[at + 1:at + 4])
            elif prop == 'tcpc':
                # Explicit name identity used by extcon's tcpc_dev_get_by_name;
                # actual registration/probe remains a hardware acceptance gate.
                names = fdt.strings(value)
                require(len(names) == 1, 'ambiguous tcpc name')
                targets = [n for n in nodes.values() if n.text('tcpc,name', []) == names]
                require(len(targets) == 1, 'missing/ambiguous named tcpc provider')
                edges.append(dict(consumer=path, property='tcpc name -> tcpc,name', provider=targets[0].path, args=names))
                pending.append(targets[0].path)
            elif prop in ('regmap', 'mediatek,syscon') or prop.endswith(('-gpios', '-gpio')):
                unparsed.append(dict(node=path, property=prop, bytes=len(value), sha256=sha(value)))
    return {p: nodes[p] for p in sorted(visited)}, edges, unparsed


def match_modules(nodes, dep, alias_text, overrides):
    aliases = []
    for line in alias_text.splitlines():
        if not line or line.startswith('#'):
            continue
        words = line.split()
        require(len(words) == 3 and words[0] == 'alias', 'malformed module alias')
        aliases.append((words[1], dep.resolve(words[2])))
    matches = {}
    for path, node in nodes.items():
        compatible = node.text('compatible', [])
        modalias = 'of:N' + node.name.split('@')[0] + 'T' + ''.join(node.text('device_type', [])) + 'C' + 'C'.join(compatible)
        evidence = [{'module': m, 'kind': 'stock modules.alias', 'pattern': a}
                    for a, m in aliases if compatible and fnmatch.fnmatchcase(modalias, a)]
        for item in overrides:
            if set(compatible) & set(item['compatible']):
                record = dict(module=dep.resolve(item['module']), kind='matching official source table only',
                              source=item['source'], source_sha256=item['sha256'])
                if 'platform_cell' in item:
                    require(('platform:' + item['platform_cell'], record['module']) in aliases, 'MFD cell platform alias absent')
                    record.update(kind='official MFD child table + stock platform alias', platform_cell=item['platform_cell'])
                evidence.append(record)
        matches[path] = dict(compatible=compatible, status=node.text('status', ['okay']),
                             modules=sorted({r['module'] for r in evidence}), evidence=evidence)
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    require(not out.exists() and out.is_relative_to(ROOT / 'research'), 'new private research output required')
    vendor = (ROOT / 'research/ace-backup-20261019-wireless-v2/vendor_boot_b.img').read_bytes()
    blob = (ROOT / 'research/ace-native-fdt-20261020/live-fdt.dtb').read_bytes()
    kernel = (ROOT / 'research/ace-stock-qemu-20261019/Image').read_bytes()
    require(sha(vendor) == VENDOR_SHA and sha(blob) == FDT_SHA, 'exact vendor/FDT pin mismatch')
    require(sha(kernel) == KERNEL_SHA, 'exact refusal kernel pin mismatch')
    at = kernel.find(b'IKCFG_ST')
    require(at >= 0, 'pinned kernel config marker missing')
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    config = decoder.decompress(kernel[at + 8:], 1024 * 1024)
    require(decoder.eof and decoder.unused_data.startswith(b'IKCFG_ED'), 'invalid or oversized embedded config')
    spec = importlib.util.spec_from_file_location('cpio', ROOT / 'tools/ace-recovery-diag.py')
    cpio = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cpio)
    raw = subprocess.run(['lz4', '-dc'], input=cpio.read_vendor(vendor)['ramdisk'], capture_output=True, check=True).stdout
    archive = {}
    for name, fields, data in cpio.read_cpio(raw):
        require(name not in archive, 'duplicate CPIO member')
        archive[name] = (fields, data)
    modules = {n.removeprefix('lib/modules/'): d for n, (fields, d) in archive.items()
               if n.startswith('lib/modules/') and n.endswith('.ko') and stat.S_ISREG(fields[1])}
    metadata = {n: archive['lib/modules/' + n][1] for n in ['modules.dep', 'modules.alias', 'modules.softdep']}
    dep = Dependencies(modules, metadata['modules.dep'].decode(), metadata['modules.softdep'].decode())
    override_path = Path(__file__).with_name('provider_overrides.json')
    overrides = json.loads(override_path.read_text())
    startup_path = Path(__file__).with_name('startup_preconditions.json')
    preconditions = json.loads(startup_path.read_text())
    source_rows = overrides + preconditions + [s for r in preconditions for s in r.get('supporting_sources', [])]
    for row in source_rows:
        source = None
        for base in ['research/ace-ramdiag-20261020/provider-source', 'research/ace-driver-port-20261019/storage/official']:
            candidate = ROOT / base / row['source']
            if candidate.is_file():
                source = candidate.read_bytes()
                break
        require(source is not None and sha(source) == row['sha256'], 'provider source pin mismatch: ' + row['source'])
        observed = set(re.findall(r'\.compatible\s*=\s*"([^"]+)"', source.decode()))
        require(set(row.get('compatible', [])) <= observed, 'provider mapping absent from source table')
        if 'platform_cell' in row:
            require(row['platform_cell'] in re.findall(r'\.name\s*=\s*"([^"]+)"', source.decode()), 'MFD child name absent from source')
    nodes, edges, unparsed = provider_closure(fdt.parse(blob), SEEDS)
    matches = match_modules(nodes, dep, metadata['modules.alias'].decode(), overrides)
    direct = sorted({m for row in matches.values() for m in row['modules']})
    ordered = dep.ordered(direct, before=[(r['before'], r['consumer']) for r in preconditions], first=RETURN_PREFIX)
    source_files = [Path(__file__), override_path, startup_path, ROOT / 'tools/fdt.py', ROOT / 'tools/ace-recovery-diag.py']
    report = dict(status='offline proposal only; physical startup incomplete', hardware_tested=False,
                  ios_deployable=False, phone_io=False, vendor_sha256=sha(vendor), live_fdt_sha256=sha(blob),
                  kernel_sha256=sha(kernel), embedded_config_sha256=sha(config),
                  source_sha256={str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in source_files},
                  seeds=SEEDS, archive_module_count=len(modules), metadata_sha256={n: sha(d) for n, d in metadata.items()},
                  overrides_sha256=sha(override_path.read_bytes()), nodes=matches, provider_edges=edges,
                  startup_preconditions_sha256=sha(startup_path.read_bytes()),
                  runtime_preconditions_not_yet_implemented=preconditions,
                  unparsed_binding_properties=unparsed,
                  unmapped_compatible_nodes=[p for p, r in matches.items() if r['compatible'] and not r['modules']],
                  directly_matched_modules=direct,
                  return_prefix=ordered[:len(RETURN_PREFIX)],
                  insertion_order=[dict(module=n, sha256=sha(modules[n]), bytes=len(modules[n]),
                                        hard_dependencies=sorted(dep.hard[n]),
                                        soft_pre=sorted(dep.pre.get(n, set())), soft_post=sorted(dep.post.get(n, set()))) for n in ordered],
                  limitations=['DT reference closure covers only explicitly parsed binding formats',
                               'aliases/source tables do not prove binary/source equivalence or probe/binding',
                               'all driver instances may probe on insertion, including nodes outside this closure',
                               'unmapped nodes are not presumed built in; string lookups and generated MFD children need review',
                               'provider edges are not insertion constraints; deferred probe needs physical ready checks'])
    out.mkdir(parents=True, mode=0o700)
    (out / 'kernel.config').write_bytes(config)
    for path in source_files:
        snapshot = out / 'source-snapshot' / path.relative_to(ROOT)
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(path.read_bytes())
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: len(report[k]) for k in ['nodes', 'provider_edges', 'insertion_order', 'unmapped_compatible_nodes', 'unparsed_binding_properties']}, indent=2))


if __name__ == '__main__':
    main()
