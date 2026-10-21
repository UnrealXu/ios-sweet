#!/usr/bin/env python3
"""Pack a linked plain-arm64 Mach-O and hash-bound Ace ADT for the native loader.

Host only. Output is an ACEXNU01 candidate, not Android boot.img or deployable
iOS. Kernel platform provenance, exclusive RAM ownership and hardware boot
remain independent requirements. No transport, partition or phone operations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

PAGE, BLOCK, HEADER, MAX_FILE = 0x4000, 0x2000000, 680, 256 * 1024 * 1024
U64 = (1 << 64) - 1


def need(ok, message):
    if not ok: raise ValueError(message)


def inside(offset, size, limit):
    return 0 <= offset <= limit and 0 <= size <= limit - offset


def read(path):
    path = Path(path)
    need(path.is_file() and not path.is_symlink(), 'ordinary input file required')
    need(path.stat().st_size <= MAX_FILE, 'input exceeds size bound')
    with path.open('rb') as stream:
        data = stream.read(MAX_FILE + 1)
    need(len(data) <= MAX_FILE, 'input grew beyond size bound')
    return data


def sha(data): return hashlib.sha256(data).hexdigest()


def macho(data):
    need(32 <= len(data) <= MAX_FILE, 'Mach-O size')
    magic, cpu, sub, kind, count, size, flags, reserved = struct.unpack_from('<8I', data)
    need((magic, cpu, sub, kind, reserved) == (0xfeedfacf, 0x100000c, 0, 2, 0),
         'requires thin little-endian MH_EXECUTE plain arm64, not arm64e/IMG4/fileset')
    need(flags & 1 and not flags & 0x80000000, 'requires MH_NOUNDEFS, not a kernelcache')
    need(0 < count <= 4096 and inside(32, size, len(data)), 'load command bounds')
    end, off, segments, entry, commands = 32 + size, 32, [], None, set()
    local_relocations = None
    total_sections = 0
    for _ in range(count):
        need(inside(off, 8, end), 'truncated load command')
        cmd, length = struct.unpack_from('<2I', data, off)
        need(length >= 8 and length % 8 == 0 and inside(off, length, end), 'load command size')
        need(cmd == 0x19 or cmd not in commands, 'duplicate load command')
        if cmd == 0x19:
            need(length >= 72, 'short segment')
            raw_name = data[off+8:off+24]
            name = raw_name.split(b'\0', 1)[0].decode('ascii')
            va, memory, fileoff, files, maximum, initial, sections, segflags = struct.unpack_from('<4Q4I', data, off+24)
            total_sections += sections
            need(length == 72 + sections*80 and maximum & ~7 == 0 and initial & ~maximum == 0,
                 'segment sections/protections')
            need(inside(fileoff, files, len(data)) and memory <= U64-va, 'segment range')
            # XNU can emit a nonloaded __CTF/debug segment with filesize > 0.
            need(memory == 0 or files <= memory, 'file data exceeds mapped segment')
            for index in range(sections):
                section = off+72+index*80
                section_name = data[section:section+16].split(b'\0',1)[0]
                if section_name in (b'__thread_starts', b'__chain_starts'):
                    need(struct.unpack_from('<Q',data,section+40)[0] == 0, 'threaded pointer starts require a verified resolver')
                relocation_count = struct.unpack_from('<I', data, section+60)[0]
                need(relocation_count == 0, 'unresolved section relocations')
            if memory:
                need(va % PAGE == 0, 'segment VA must be 16KiB aligned')
                segments.append(dict(name=name, va=va, memory=memory, fileoff=fileoff,
                                     files=files, protection=initial))
        elif cmd == 5:
            need(entry is None and length == 288, 'duplicate/unsupported LC_UNIXTHREAD')
            need(struct.unpack_from('<2I', data, off+8) == (6, 68), 'arm_thread_state64 required')
            entry = struct.unpack_from('<Q', data, off+16+32*8)[0]
        elif cmd == 0xb:
            need(cmd not in commands and length == 80, 'LC_DYSYMTAB layout')
            fields = struct.unpack_from('<18I', data, off+8)
            need(fields[5] == 0 and fields[15] == 0, 'undefined symbols or external relocations')
            need(inside(fields[16],fields[17]*8,len(data)), 'local relocation table bounds')
            local_relocations = fields[16:18]
        elif cmd in (0x80000034, 0x22, 0x80000022, 0x80000028):
            raise ValueError('chained/dyld fixups or LC_MAIN require a separate verified resolver')
        elif cmd not in (2, 0x1b, 0x32, 0x2a, 0x26, 0x29, 0x24, 0x25, 0x80000033):
            raise ValueError('unsupported load command: '+hex(cmd))
        commands.add(cmd)
        off += length
    need(off == end and 0 < len(segments) <= 32, 'command count or loaded segment count')
    text = segments[0]
    need(text['name'] == '__TEXT' and text['fileoff'] == 0 and text['files'] >= end,
         '__TEXT must contain the complete Mach-O header/commands')
    for index, segment in enumerate(segments):
        for other in segments[:index]:
            need(not (segment['va'] < other['va']+other['memory'] and other['va'] < segment['va']+segment['memory']),
                 'overlapping mapped segments')
            if segment['files'] and other['files']:
                need(not (segment['fileoff'] < other['fileoff']+other['files'] and
                          other['fileoff'] < segment['fileoff']+segment['files']), 'overlapping segment file data')
    need(entry is not None and entry % 4 == 0 and any(s['protection'] & 4 and
         s['va'] <= entry and inside(entry-s['va'], 4, s['files']) for s in segments),
         'entry must have four executable file-backed bytes')
    va = text['va'] & ~(BLOCK-1)
    need(va >= 0xffff000000000000 and all(s['va'] >= va for s in segments), 'kernel virtual range')
    top = max(s['va']+s['memory'] for s in segments)
    need(top <= U64-(PAGE-1), 'kernel end overflow')
    # With unchanged linked VAs the virtual slide is zero. Local UNSIGNED
    # relocations already contain resolved plain pointers; retain bytes/table.
    # Do not confuse this with decoding chained/authenticated pointers.
    if local_relocations:
        rel_off, rel_count = local_relocations
        need(rel_count <= MAX_FILE//8, 'local relocation count')
        need(not rel_count or any(s['name'] == '__LINKEDIT' and
             s['fileoff'] <= rel_off and inside(rel_off-s['fileoff'],rel_count*8,s['files'])
             for s in segments), 'relocation table must remain in loaded LINKEDIT')
        sites = set()
        for index in range(rel_count):
            address, bits = struct.unpack_from('<iI',data,rel_off+index*8)
            need(address >= 0 and address % 4 == 0 and bits >> 24 == 6 and
                 0 < (bits & 0xffffff) <= total_sections, 'unsupported local relocation')
            site = text['va']+address
            need(site not in sites, 'duplicate local relocation')
            sites.add(site)
            owner = [s for s in segments if s['va'] <= site and inside(site-s['va'],8,s['files'])]
            need(len(owner) == 1, 'local relocation site must be file backed')
            s = owner[0]
            target = struct.unpack_from('<Q',data,s['fileoff']+site-s['va'])[0]
            need(any(s['va'] <= target <= s['va']+s['memory'] for s in segments),
                 'local relocation target outside linked image')
        ordered = sorted(sites)
        need(all(b-a >= 8 for a,b in zip(ordered,ordered[1:])), 'overlapping local relocation sites')
    return segments, va, entry, (top+PAGE-1) & ~(PAGE-1), local_relocations[1] if local_relocations else 0


def adt_ram(data, root_probe=False):
    """Bounded semantic read of the small generated ADT, no IM4P/decompression."""
    need(0 < len(data) <= 1024*1024, 'ADT size')
    nodes = 0
    def visit(off, depth):
        nonlocal nodes
        nodes += 1
        need(depth <= 32 and nodes <= 4096 and inside(off, 8, len(data)), 'ADT node bounds')
        props, children = struct.unpack_from('<2I', data, off); off += 8
        need(props <= 256 and children <= 256, 'ADT count bounds')
        values = {}
        for _ in range(props):
            need(inside(off, 36, len(data)), 'ADT property header')
            raw = data[off:off+32]
            need(b'\0' in raw, 'unterminated ADT property name')
            key = raw.split(b'\0',1)[0].decode('ascii')
            size = struct.unpack_from('<I', data, off+32)[0]; off += 36
            need(key and key not in values and not size & 0x80000000 and inside(off, (size+3)&~3, len(data)),
                 'ADT property bounds/duplicates/placeholders')
            values[key] = data[off:off+size]; off += (size+3)&~3
        need('name' in values and values['name'].endswith(b'\0'), 'ADT node name')
        items = {}
        for _ in range(children):
            child, off = visit(off, depth+1); name = child[0]['name']
            need(name not in items, 'duplicate ADT child')
            items[name] = child
        return (values, items), off
    (root, children), end = visit(0,0)
    need(end == len(data) and root['name'] == b'device-tree\0' and
         b'oneplus,ace-mt6895' in root.get('compatible',b'').split(b'\0'), 'Ace ADT root')
    need(root.get('target-type') == b'ACE\0' and root.get('model') == b'PGKM10\0', 'Ace ADT identity')
    need(b'chosen\0' in children, 'ADT chosen missing')
    chosen = children[b'chosen\0'][0]
    need(all(len(chosen.get(k,b'')) == 8 for k in ('dram-base','dram-size')), 'ADT RAM properties')
    ufs = children.get(b'ace-ufs\0')
    props = ufs[0] if ufs else {}
    need((root_probe and props.get('ace,root-read-probe') == struct.pack('<I',1) and
          props.get('ace,command-read-probe') == struct.pack('<I',1)) or
         (not root_probe and 'ace,root-read-probe' not in props), 'ADT root-discovery profile mismatch')
    return struct.unpack('<Q',chosen['dram-base'])[0], struct.unpack('<Q',chosen['dram-size'])[0]


def build(kernel, tree, manifest, command_line):
    need(isinstance(manifest,dict) and manifest.get('target') == 'ACE' and
         manifest.get('adt_sha256') == sha(tree), 'hash-bound Ace ADT manifest required')
    need(manifest.get('cold_native_only') is True and
         type(manifest.get('ufs_read_only_probe',False)) is bool and
         type(manifest.get('ufs_command_read_probe',False)) is bool and
         type(manifest.get('ufs_root_discovery_probe',False)) is bool and
         (not manifest.get('ufs_root_discovery_probe') or manifest.get('ufs_command_read_probe')) and
         not (manifest.get('ufs_command_read_probe') and manifest.get('ufs_read_only_probe')) and
         manifest.get('required_xnu_patches') == ['0082','0083','0084','0085'] +
         (['0090','0091'] if manifest.get('ufs_command_read_probe') else ['0090'] if manifest.get('ufs_read_only_probe') else []) +
         (['0113'] if manifest.get('ufs_root_discovery_probe') else []), 'ADT policy version')
    segments, va, entry, top, relocation_count = macho(kernel)
    physical, memory = adt_ram(tree, manifest.get('ufs_root_discovery_probe',False))
    need(manifest.get('requested_ram',{}).get('base') == physical and
         manifest.get('requested_ram',{}).get('size') == memory, 'manifest/ADT RAM disagreement')
    need(physical > 0 and physical % BLOCK == 0 and memory > 0 and memory % BLOCK == 0 and
         inside(physical,memory,1<<40), 'managed physical range')
    need(isinstance(manifest.get('excluded_ranges'),list) and manifest['excluded_ranges'], 'exclusions missing')
    for excluded in manifest['excluded_ranges']:
        need(isinstance(excluded,dict), 'excluded range object')
        base, size = excluded['base'], excluded['size']
        need(isinstance(base,int) and isinstance(size,int) and size > 0 and inside(base,size,1<<40), 'excluded range')
        need(not (physical < base+size and base < physical+memory), 'managed RAM overlaps exclusion')
    line = command_line.encode('ascii')
    need(b'\0' not in line and len(line) < 608, 'command line must fit without truncation or embedded NUL')
    need(top-va < memory and memory <= U64-va, 'kernel does not fit RAM/VA window')
    adt_pa = physical+top-va
    args_pa = (adt_pa+len(tree)+PAGE-1)&~(PAGE-1)
    need(inside(args_pa,PAGE,physical+memory), 'ADT/BootArgs do not fit RAM')
    output = bytearray(HEADER+32*len(segments))
    for i, segment in enumerate(segments):
        off = len(output)
        output.extend(kernel[segment['fileoff']:segment['fileoff']+segment['files']])
        output.extend(bytes(-len(output)%16))
        struct.pack_into('<4Q',output,HEADER+i*32,segment['va'],segment['memory'],off,segment['files'])
    tree_offset = len(output); output.extend(tree)
    need(len(output) <= MAX_FILE, 'payload exceeds size bound')
    struct.pack_into('<8sII7Q',output,0,b'ACEXNU01',1,len(segments),va,entry,tree_offset,len(tree),top,physical,memory)
    output[72:72+len(line)] = line
    report = dict(schema_version=1,format='ACEXNU01/v1',kernel_sha256=sha(kernel),adt_sha256=sha(tree),
                  payload_sha256=sha(output),payload_bytes=len(output),segments=segments,virt_base=va,
                  entry_va=entry,entry_pa=physical+entry-va,adt_pa=adt_pa,args_pa=args_pa,
                  top_of_kernel_data=args_pa+PAGE,requested_ram=manifest['requested_ram'],
                  local_relocations_checked=relocation_count,
                  relocation_mode='zero virtual slide; checked plain local pointers retained; no chained/dyld rebases',
                  kernel_ace_platform_verified=False,hardware_ram_ownership_verified=False,ios_deployable=False,
                  scope='host flat bundle only; no transport, image signing, storage or execution')
    return bytes(output), report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kernel',type=Path);parser.add_argument('adt_directory',type=Path)
    parser.add_argument('output_directory',type=Path)
    parser.add_argument('--cmdline',default='debug=0xc serial=3 cpus=1 keepsyms=1 ace_pmsg=1 -enable_kprintf_spam')
    args = parser.parse_args()
    try:
        manifest=json.loads(read(args.adt_directory/'manifest.json'))
        blob,report=build(read(args.kernel),read(args.adt_directory/'ace.adt'),manifest,args.cmdline)
        args.output_directory.mkdir()
        (args.output_directory/'ace.payload').write_bytes(blob)
        (args.output_directory/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
        print(f'ACE host payload candidate: {len(blob)}bytes; platform provenance/ownership/boot NOT verified')
        return 0
    except (ValueError,KeyError,TypeError,OSError,struct.error,UnicodeError) as error:
        print('ACE payload refused: '+str(error),file=sys.stderr)
        return 1


if __name__ == '__main__':sys.exit(main())
