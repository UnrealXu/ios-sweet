#!/usr/bin/env python3
"""Generate an initial ACE XNU ADT from a bounded FDT and explicit cold-boot policy.

Host only: no ADB, mapping, RAM write, boot or flash. A generated tree is not an
ownership proof. The native loader must revalidate its live source/stack ranges,
FDT, incoming MPIDR and hardware state before copying/jumping.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys

import adt
import fdt

PAGE, BLOCK, PHYS_LIMIT = 0x4000, 0x2000000, 1 << 40
GICD, GICD_BYTES, GICR, GICR_BYTES = 0xc000000, 0x40000, 0xc040000, 0x200000
TIMEBASE, VTIMER = 13000000, 27
PMSG, PMSG_BYTES = 0x48160000, 0x10000
CMA = {'/reserved-memory/ssmr-reserved-cma_memory': (0x6000000, 0x1000000),
       '/reserved-memory/ssheap-reserved-cma_memory': (0x400000, 0x200000)}
u32 = lambda *v: struct.pack('<%dI' % len(v), *v)
u64 = lambda *v: struct.pack('<%dQ' % len(v), *v)
text = lambda value: value.encode('ascii') + b'\0'


def span(base, size, name):
    if type(base) is not int or type(size) is not int or not 0 <= base < PHYS_LIMIT or not 0 < size <= PHYS_LIMIT - base:
        raise ValueError(f'{name}: invalid/overflowing physical range')
    return {'name': name, 'base': base, 'size': size}


def overlaps(a, b):
    return a['base'] < b['base'] + b['size'] and b['base'] < a['base'] + a['size']


def inside(a, b):
    return b['base'] <= a['base'] and a['base'] + a['size'] <= b['base'] + b['size']


def available(node):
    return node.text('status', ['okay']) in (['okay'], ['ok'])


def one(tree, compatible):
    found = [n for n in tree.root.walk() if compatible in n.text('compatible', [])]
    if len(found) != 1 or not available(found[0]):
        raise ValueError(f'expected one enabled {compatible}')
    return found[0]


def pairs(value, ac, sc, name):
    values = fdt.cells(value)
    if ac not in (1, 2) or sc not in (1, 2) or not values or len(values) % (ac + sc):
        raise ValueError(f'{name}: malformed address/size pairs')
    out = []
    for i in range(0, len(values), ac + sc):
        base = int.from_bytes(value[i*4:(i+ac)*4], 'big')
        size = int.from_bytes(value[(i+ac)*4:(i+ac+sc)*4], 'big')
        out.append(span(base, size, name))
    return out


def build(blob, *, ram_base, ram_size, fdt_pa, loader_ranges, boot_affinity,
          cold_native, seed=None, ufs_probe=False, ufs_read=False, ufs_root=False):
    if cold_native is not True:
        raise ValueError('requires cold-native stage before Linux, not running Android RAM')
    if type(boot_affinity) is not int or boot_affinity != 0:
        raise ValueError('initial ACE target supports only requested boot affinity0')
    ram = span(ram_base, ram_size, 'xnu-managed')
    if ram_base % BLOCK or ram_size % BLOCK:
        raise ValueError('initial XNU bootstrap requires 32MiB base and size alignment')
    if not loader_ranges or len(loader_ranges) > 128:
        raise ValueError('explicit loader/image/stack exclusion ranges required')
    tree = fdt.parse(blob)
    if 'mediatek,MT6895' not in tree.root.text('compatible', []):
        raise ValueError('not the MT6895 target FDT')
    if tree.root.u32('#address-cells') != 2 or tree.root.u32('#size-cells') != 2:
        raise ValueError('unsupported root address format')
    banks = [span(r['address'], r['size'], n.path) for n in tree.root.walk()
             if n.props.get('device_type') == b'memory\0' and available(n) for r in fdt.reg(n)]
    if not any(inside(ram, b) for b in banks):
        raise ValueError('whole requested RAM window must fit one declared bank')
    cpus = [n for n in tree.root.walk() if n.props.get('device_type') == b'cpu\0']
    affinities = [fdt.reg(n) for n in cpus]
    if len(cpus) != 8 or any(r != [{'address': i << 8, 'size': 0}] for i, r in enumerate(affinities)):
        raise ValueError('CPU affinity list differs from observed Ace topology')
    for i, cpu in enumerate(cpus):
        expected = 'arm,cortex-a55' if i < 4 else 'arm,cortex-a78'
        if not available(cpu) or expected not in cpu.text('compatible', []) or cpu.text('enable-method') != ['psci']:
            raise ValueError('CPU kind/enable-method differs from Ace')
    cpu_clock = cpus[0].u32('clock-frequency')
    if cpu_clock is None or cpu_clock == 0:
        raise ValueError('missing CPU0 firmware-declared clock')
    gic, timer, psci = one(tree, 'arm,gic-v3'), one(tree, 'arm,armv8-timer'), one(tree, 'arm,psci-1.0')
    if gic.parent is not tree.root or fdt.reg(gic) != [dict(address=GICD,size=GICD_BYTES), dict(address=GICR,size=GICR_BYTES)]:
        raise ValueError('GIC address space/regions differ from observed Ace')
    irq = fdt.interrupts(tree, timer)
    if timer.u32('clock-frequency') != TIMEBASE or len(irq) != 4 or irq[2].get('intid') != VTIMER or irq[2]['provider'] != gic.path:
        raise ValueError('architectural timer differs from observed 13MHz/PPI27')
    if psci.text('method') != ['smc']:
        raise ValueError('PSCI conduit differs from observed SMC')
    if type(ufs_root) is not bool or (ufs_root and not ufs_read):
        raise ValueError('ufs-root requires the command-read profile')
    if type(ufs_read) is not bool or (ufs_read and ufs_probe):
        raise ValueError('ufs-read and ufs-probe are exclusive boolean profiles')
    if type(ufs_probe) is not bool:
        raise ValueError('ufs-probe must be boolean')
    if ufs_probe or ufs_read:
        ufs = one(tree, 'mediatek,mt8183-ufshci')
        soc = tree.by_path('/soc')
        if soc is None or not available(soc) or ufs.path != '/soc/ufshci@112b0000' or ufs.parent is not soc or soc.parent is not tree.root or soc.u32('#address-cells') != 2 or soc.u32('#size-cells') != 2 or soc.props.get('ranges') != b'':
            raise ValueError('UFS address translation differs from observed Ace')
        if fdt.reg(ufs) != [dict(address=0x112b0000, size=0x2300)] or ufs.props.get('interrupts') != struct.pack('>4I',0,137,4,0) or 'interrupts-extended' in ufs.props:
            raise ValueError('UFS resources differ from observed Ace')
        irq = fdt.interrupts(tree, ufs)
        if len(irq) != 1 or irq[0].get('intid') != 169 or irq[0]['provider'] != gic.path:
            raise ValueError('UFS interrupt provider differs from observed Ace')
    reserves = [span(r['address'], r['size'], 'fdt-memreserve') for r in tree.reservations]
    incoming = span(fdt_pa, tree.total_size, 'incoming-fdt')
    if not any(inside(incoming, bank) for bank in banks):
        raise ValueError('incoming FDT range is outside declared RAM')
    reserves.append(incoming)
    chosen = tree.by_path('/chosen')
    if chosen is None:
        raise ValueError('missing /chosen and initrd handoff')
    initrd = [chosen.props.get('linux,initrd-'+part) for part in ('start', 'end')]
    if any(v is not None for v in initrd):
        if any(v is None or len(v) not in (4,8) for v in initrd):
            raise ValueError('incomplete/malformed initrd handoff')
        start, end = map(fdt.integer, initrd)
        image = span(start, end-start, 'incoming-initrd')
        if not any(inside(image, bank) for bank in banks):
            raise ValueError('incoming initrd range is outside declared RAM')
        reserves.append(image)
    reserved = tree.by_path('/reserved-memory')
    if reserved is None or reserved.props.get('ranges') != b'' or reserved.u32('#address-cells') != 2 or reserved.u32('#size-cells') != 2:
        raise ValueError('unsupported reserved-memory address space')
    deferred, bounded = [], []
    for n in reserved.children:
        if 'reg' in n.props:
            entries = fdt.reg(n)
            if not entries:
                raise ValueError('empty fixed reservation reg')
            for r in entries:
                reserves.append(span(r['address'], r['size'], n.path))
        elif n.path in CMA:
            size, align = CMA[n.path]
            known = {'compatible','reusable','size','alignment','phandle','linux,phandle','status'}
            if set(n.props) - known:
                raise ValueError('unknown property on deferred Linux CMA declaration')
            if n.props.get('size') != struct.pack('>Q',size) or n.props.get('alignment') != struct.pack('>Q',align) or n.text('compatible') != ['shared-dma-pool'] or 'reusable' not in n.props or 'no-map' in n.props or 'alloc-ranges' in n.props:
                raise ValueError('unrecognized Linux CMA declaration; no automatic waiver')
            deferred.append(n.path)
        elif 'alloc-ranges' in n.props:
            if 'size' not in n.props or len(n.props['size']) != 8 or not fdt.integer(n.props['size']):
                raise ValueError('bounded dynamic node has invalid size')
            domains = pairs(n.props['alloc-ranges'],2,2,n.path+'-allocation-domain')
            if not any(x['size'] >= fdt.integer(n.props['size']) for x in domains):
                raise ValueError('dynamic reservation cannot fit its allocation domain')
            reserves += domains
            bounded.append(n.path)
        else:
            raise ValueError(f'{n.path}: unresolved unbounded dynamic reservation')
    for name, base, size in loader_ranges:
        if not re.fullmatch(r'[a-zA-Z0-9_.-]{1,48}',name):
            raise ValueError('invalid caller exclusion name')
        claimed = span(base,size,'caller-'+name)
        if not any(inside(claimed, bank) for bank in banks):
            raise ValueError('caller loader range is outside declared RAM')
        reserves.append(claimed)
    if len(reserves) > 256:
        raise ValueError('exclusion count exceeds native loader policy capacity')
    for reserved_range in reserves:
        if overlaps(ram, reserved_range):
            raise ValueError('XNU RAM overlaps '+reserved_range['name'])
    pmsg = span(PMSG, PMSG_BYTES, 'pmsg')
    if not any(inside(pmsg, span(r['address'],r['size'],n.path)) for n in reserved.children
               if 'mediatek,pstore' in n.text('compatible',[]) for r in fdt.reg(n)):
        raise ValueError('observed pmsg is not covered by a pstore reservation')
    if seed is None:
        seed = os.urandom(64)
    if type(seed) is not bytes or len(seed) != 64:
        raise ValueError('random-seed must be exactly64bytes')
    counter = iter(range(1,100))
    def node(name, props=(), children=()):
        n = adt.Node()
        n.props = [('name',0,text(name)),('AAPL,phandle',0,u32(next(counter)))] + [(k,0,v) for k,v in props]
        n.children = list(children)
        return n
    cpu = node('cpu0', [('device_type',text('cpu')),('compatible',text('ace,armv8-cpu')+text('arm,cortex-a55')+text('ARM,v8')),
        ('reg',u32(0)),('cpu-id',u32(0)),('cluster-id',u32(0)),('cluster-type',u32(0)),('die-cluster-id',u32(0)),
        ('cluster-core-id',u32(0)),('l2-cache-id',u32(0)),('l3-cache-id',u32(0)),('state',text('running')),
        ('timebase-frequency',u32(TIMEBASE)),('fixed-frequency',u32(TIMEBASE)),('clock-frequency',u32(cpu_clock))])
    io = node('arm-io',[('device_type',text('ace-io')),('compatible',text('ace-io')+text('arm-io')),
        ('#address-cells',u32(2)),('#size-cells',u32(2)),('ranges',u64(0,GICD,GICR+GICR_BYTES-GICD))],
        [node('gic',[('compatible',text('arm,gic-v3')),('interrupt-controller',b''),('virtual-timer-intid',u32(VTIMER)),
                     ('reg',u64(0,GICD_BYTES,GICR-GICD,GICR_BYTES))])])
    chosen_adt = node('chosen',[('dram-base',u64(ram_base)),('dram-size',u64(ram_size)),('random-seed',seed)],
        [node('memory-map'),node('ace-pmsg',[('compatible',text('ace,ramoops-pmsg-v1')),
          ('reg',u64(PMSG,PMSG_BYTES)),('ecc-size',u32(0)),('type-signature',u32(0))])])
    children = [chosen_adt,node('defaults'),
                node('cpus',[('#address-cells',u32(1)),('#size-cells',u32(0))],[cpu]),io]
    if ufs_probe or ufs_read:
        children.append(node('ace-ufs',[('compatible',text('ace,mt6895-ufs-read-v1' if ufs_read else 'ace,mt6895-ufs-hci-probe-v1')),
            ('reg',u64(0x112b0000,0x2300)),('interrupt-intid',u32(169)),('ace,command-read-probe' if ufs_read else 'ace,read-only-probe',u32(1))] +
            ([('ace,root-read-probe',u32(1))] if ufs_root else [])))
    root = node('device-tree',[('compatible',text('oneplus,ace-mt6895')+text('mediatek,MT6895')+text('AppleARM')),
        ('model',text('PGKM10')),('manufacturer',text('OnePlus')),('target-type',text('ACE')),('target-sub-type',text('PGKM10')),
        ('#address-cells',u32(2)),('#size-cells',u32(2))], children)
    output = adt.serialize(root)
    report = {'schema_version':1,'target':'ACE','fdt_sha256':hashlib.sha256(blob).hexdigest(),
        'adt_sha256':hashlib.sha256(output).hexdigest(),'adt_bytes':len(output),'requested_ram':ram,'excluded_ranges':reserves,
        'cold_native_only':True,'requested_boot_affinity':boot_affinity,'incoming_boot_mpidr_verified':False,
        'linux_cma_not_instantiated':deferred,'bounded_dynamic_domains_excluded':bounded,
        'cpu_clock_hz':cpu_clock,'cpu_clock_meaning':'firmware declaration, not measured DVFS',
        'unknown_clocks_omitted':['bus-frequency','memory-frequency','peripheral-frequency'],
        'required_xnu_patches':['0082','0083','0084','0085'] + (['0090','0091'] if ufs_read else ['0090'] if ufs_probe else []) + (['0113'] if ufs_root else []),
        'ufs_read_only_probe':ufs_probe,'ufs_command_read_probe':ufs_read,'ufs_root_discovery_probe':ufs_root,
        'suggested_diagnostic_boot_args':'debug=0xc serial=3 cpus=1 keepsyms=1 ace_pmsg=1 -enable_kprintf_spam',
        'hardware_ram_ownership_verified':False,
        'ios_deployable':False,'scope':'host ADT candidate; no phone execution or RAM ownership grant'}
    return output, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fdt',type=Path); parser.add_argument('output_directory',type=Path)
    for name in ('ram-base','ram-size','fdt-pa','boot-affinity'):
        parser.add_argument('--'+name,required=True,type=lambda s:int(s,0))
    parser.add_argument('--reserve',action='append',required=True,metavar='NAME:BASE:SIZE')
    parser.add_argument('--cold-native',action='store_true')
    parser.add_argument('--ufs-probe',action='store_true')
    parser.add_argument('--ufs-read',action='store_true')
    parser.add_argument('--ufs-root',action='store_true',help='read and validate primary GPT userdata bounds; no BSD media')
    args = parser.parse_args()
    try:
        ranges = []
        for entry in args.reserve:
            name,base,size = entry.split(':')
            ranges.append((name,int(base,0),int(size,0)))
        blob, report = build(args.fdt.read_bytes(),ram_base=args.ram_base,ram_size=args.ram_size,
            fdt_pa=args.fdt_pa,boot_affinity=args.boot_affinity,loader_ranges=ranges,cold_native=args.cold_native,ufs_probe=args.ufs_probe,ufs_read=args.ufs_read,ufs_root=args.ufs_root)
        args.output_directory.mkdir()  # exclusive: no existing artifact overwrite
        (args.output_directory/'ace.adt').write_bytes(blob)
        (args.output_directory/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
        print(f'ACE ADT candidate: {len(blob)}bytes; hardware ownership and XNU boot NOT verified')
        return 0
    except (OSError,ValueError) as error:
        print('ACE ADT refused: '+str(error),file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
