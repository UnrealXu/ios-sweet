#!/usr/bin/env python3
"""Read firmware/live DTB configuration; never infer that hardware was tested."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import fdt


def describe(tree, node):
    item = {'path': node.path, 'compatible': node.text('compatible', []),
            'status': node.text('status', ['okay'])[0]}
    if 'reg' in node.props:
        item['reg'] = fdt.reg(node)
        item['reg_address_space'] = node.parent.path
    if 'interrupts' in node.props or 'interrupts-extended' in node.props:
        item['interrupts'] = fdt.interrupts(tree, node)
    return item


def audit(blob, source_kind='firmware-dtb'):
    tree = fdt.parse(blob)
    report = {'schema_version': 1, 'source_kind': source_kind,
              'source_sha256': hashlib.sha256(blob).hexdigest(),
              'bytes': len(blob), 'dtb_bytes': tree.total_size,
              'hardware_execution_verified': False,
              'memory_reservations': tree.reservations, 'cpus': [],
              'memory': [], 'reserved_memory': [], 'gic': [], 'timers': [],
              'psci': [], 'ufs': [], 'display_candidates': [],
              'limitations': ['DT values are configuration, not observed MMIO behavior',
                              'reg values are bus-relative; ranges are not translated',
                              'Firmware memory is not a complete boot-time memory map',
                              'Dynamic carve-outs and display handoff require live evidence']}
    for node in tree.root.walk():
        compat = node.text('compatible', [])
        if node.props.get('device_type') == b'cpu\0':
            item = describe(tree, node)
            item['enable_method'] = node.text('enable-method', [])
            report['cpus'].append(item)
        elif node.props.get('device_type') == b'memory\0':
            report['memory'].append(describe(tree, node))
        elif node.parent is not None and node.parent.path == '/reserved-memory':
            item = describe(tree, node)
            item.update(no_map='no-map' in node.props, reusable='reusable' in node.props,
                        dynamic='reg' not in node.props)
            for prop in ('size', 'alignment', 'alloc-ranges'):
                if prop in node.props:
                    item[prop.replace('-', '_') + '_cells'] = fdt.cells(node.props[prop])
            report['reserved_memory'].append(item)
        if 'arm,gic-v3' in compat:
            item = describe(tree, node)
            item['interrupt_cells'] = node.u32('#interrupt-cells')
            report['gic'].append(item)
        if 'arm,armv8-timer' in compat:
            item = describe(tree, node)
            item['frequency'] = node.u32('clock-frequency')
            report['timers'].append(item)
        if any(c.startswith('arm,psci') for c in compat):
            item = describe(tree, node)
            item['method'] = node.text('method', [])
            report['psci'].append(item)
        if any('ufs' in c for c in compat) and 'reg' in node.props:
            report['ufs'].append(describe(tree, node))
        if any(w in node.path.lower() for w in ('panel@', 'touch', 'framebuffer')) and compat:
            report['display_candidates'].append(describe(tree, node))
    return report


def check_profile(report, profile):
    errors = []
    if len(report['gic']) != 1 or len(report['timers']) != 1 or len(report['psci']) != 1:
        return ['expected exactly one GIC, architectural timer and PSCI node']
    gic, timer, psci = report['gic'][0], report['timers'][0], report['psci'][0]
    regs = gic.get('reg', [])
    if len(regs) < 2 or [r['address'] for r in regs[:2]] != [profile['gic']['distributor'], profile['gic']['redistributor']]:
        errors.append('GIC addresses differ from Ace profile')
    if timer['frequency'] != profile['timer']['frequency']:
        errors.append('timer frequency differs from Ace profile')
    specs = timer.get('interrupts', [])
    if len(specs) != 4 or specs[2].get('intid') != profile['timer']['virtual_intid']:
        errors.append('virtual timer interrupt differs from Ace profile')
    if psci['method'] != [profile['psci_conduit']]:
        errors.append('PSCI conduit differs from Ace profile')
    cpus = [r['address'] for c in report['cpus'] for r in c.get('reg', [])]
    if cpus != profile['cpu_affinities']:
        errors.append('CPU affinities differ from Ace profile')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dtb', type=Path)
    parser.add_argument('--source-kind', choices=['firmware-dtb', 'live-dtb'], default='firmware-dtb')
    parser.add_argument('--profile', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.dtb.read_bytes(), args.source_kind)
        if args.profile:
            report['profile_mismatches'] = check_profile(report, json.loads(args.profile.read_text()))
        text = json.dumps(report, indent=2) + '\n'
        if args.output:
            with args.output.open('x') as f:
                f.write(text)
        else:
            print(text, end='')
        return 2 if report.get('profile_mismatches') else 0
    except (ValueError, OSError) as exc:
        print(f'DT audit failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
