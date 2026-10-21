#!/usr/bin/env python3
"""Bundle pinned original modules and compile their guarded RAM-only loader.

Offline output only. This does not enable a physical diagnostic profile.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import stat
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[1]
spec = importlib.util.spec_from_file_location('ace_module_plan', SOURCE / 'module_plan.py')
plan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plan)
require, sha = plan.require, plan.sha


def original_modules():
    vendor = (ROOT / 'research/ace-backup-20261019-wireless-v2/vendor_boot_b.img').read_bytes()
    kernel = (ROOT / 'research/ace-stock-qemu-20261019/Image').read_bytes()
    require(sha(vendor) == plan.VENDOR_SHA and sha(kernel) == plan.KERNEL_SHA, 'vendor/kernel pin mismatch')
    release = re.findall(rb'Linux version ([0-9][^ \x00\n]{1,63}) ', kernel)
    require(len(release) == 1, 'kernel release banner ambiguous')
    spec = importlib.util.spec_from_file_location('ace_cpio', ROOT / 'tools/ace-recovery-diag.py')
    cpio = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cpio)
    raw = subprocess.run(['lz4', '-dc'], input=cpio.read_vendor(vendor)['ramdisk'], capture_output=True, check=True).stdout
    archive = {}
    for name, fields, data in cpio.read_cpio(raw):
        require(name not in archive, 'duplicate original CPIO member')
        archive[name] = (fields, data)
    modules = {n.removeprefix('lib/modules/'): d for n, (f, d) in archive.items()
               if n.startswith('lib/modules/') and n.endswith('.ko') and stat.S_ISREG(f[1])}
    metadata = {n: archive['lib/modules/' + n][1].decode() for n in ['modules.dep', 'modules.softdep']}
    return modules, metadata, release[0].decode()


def module_info(data):
    with tempfile.TemporaryDirectory(prefix='ace-modinfo-') as temp:
        path = Path(temp) / 'input.ko'
        path.write_bytes(data)
        require(data[:4] == b'\x7fELF' and data[4:6] == b'\x02\x01' and data[16:18] == b'\x01\x00' and int.from_bytes(data[18:20], 'little') == 183,
                'module must be relocatable ELF64 little-endian AArch64')
        output = subprocess.run(['readelf', '-p', '.modinfo', str(path)], capture_output=True, text=True, check=True).stdout
    result = {}
    for key in ['name', 'vermagic']:
        values = re.findall(r'^\s*\[\s*[0-9a-f]+\]\s+' + key + r'=(.*)$', output, re.M)
        require(len(values) == 1, 'module metadata missing/ambiguous: ' + key)
        result[key] = values[0].strip()
    return result


def compile_bundle(out, items, *, expected_release, expected_serial, bindings=(), return_prefix_count=0, supervisor_timeout=90):
    """Compile fixed entries; caller supplies hash-pinned archive bytes.

    Used also by diskless QEMU fixtures. Does not execute the resulting loader.
    """
    require(1 <= len(items) <= 270, 'module count outside bound')
    require(re.fullmatch(r'[A-Za-z0-9_.+-]{1,64}', expected_serial), 'invalid serial identity')
    require(re.fullmatch(r'[A-Za-z0-9_.+-]{1,64}', expected_release), 'invalid kernel release')
    require(not out.exists() and out.is_relative_to(ROOT / 'research'), 'new private research directory required')
    require(type(return_prefix_count) is int and 0 <= return_prefix_count <= len(items), 'return prefix count bound')
    require(type(supervisor_timeout) is int and 1 <= supervisor_timeout <= 180, 'supervisor timeout bound')
    require(not return_prefix_count or any(b.get('early') for b in bindings), 'return prefix needs verified bindings')
    require(len(bindings) <= 64, 'binding count bound')
    for binding in bindings:
        require(re.fullmatch(r'/[A-Za-z0-9_./@:+-]+', binding['dt_path']) and '..' not in Path(binding['dt_path']).parts, 'unsafe DT binding path')
        require(re.fullmatch(r'[A-Za-z0-9_.+-]+', binding['driver']), 'unsafe binding driver')
        require(re.fullmatch(r'[A-Za-z0-9_]*', binding['module']), 'unsafe binding module')
        require(type(binding.get('early', False)) is bool, 'binding early stage must be boolean')
        require(not binding.get('early') or return_prefix_count > 0, 'early binding needs return prefix')
        gate = binding.get('class_path', '')
        require(not gate or re.fullmatch(r'/sys/[A-Za-z0-9_./@:+-]+', gate) and '..' not in Path(gate).parts, 'unsafe binding class path')
        properties = binding.get('properties', {})
        require(len(properties) <= 16, 'binding property count bound')
        for name, value in properties.items():
            require(re.fullmatch(r'[A-Za-z0-9_,#+.-]+', name) and name not in ('.', '..'), 'unsafe binding property')
            require(re.fullmatch(r'(?:[0-9a-f]{2}){1,64}', value), 'invalid binding property bytes')
    seen, rows = set(), []
    for item in items:
        name, data, gate = item['module'], item['data'], item.get('gate', '')
        require(re.fullmatch(r'[A-Za-z0-9_+-]+\.ko', name) and name not in seen, 'unsafe/duplicate module name')
        seen.add(name)
        require(0 < len(data) <= 2 * 1024 * 1024, 'module size bound')
        require(not gate or re.fullmatch(r'/sys/[A-Za-z0-9_./@:+-]+', gate) and '..' not in Path(gate).parts, 'unsafe gate path')
        info = module_info(data)
        require(info['name'] == name[:-3].replace('-', '_'), 'module internal name mismatch')
        require(info['vermagic'].split()[0] == expected_release, 'module release mismatch')
        rows.append(dict(module=name, sha256=sha(data), bytes=len(data), gate=gate, **info))
    early_names = {r['name'] for r in rows[:return_prefix_count]}
    for binding in bindings:
        require(not binding.get('early') or not binding['module'] or binding['module'] in early_names, 'early binding owner outside return prefix')
    identity = dict(expected_serial=expected_serial, expected_release=expected_release, modules=rows,
                    bindings=bindings, return_prefix_count=return_prefix_count, supervisor_timeout=supervisor_timeout,
                    policy_sha256={name: sha((SOURCE / name).read_bytes()) for name in
                                   ['module_bundle.py','module_loader.c','module_supervisor.c','sha256.h','slot_guard.h','aarch64_flags.h']})
    bundle_id = sha(json.dumps(identity, sort_keys=True, separators=(',', ':')).encode())
    out.mkdir(parents=True, mode=0o700)
    (out / 'modules').mkdir(mode=0o700)
    for row, item in zip(rows, items):
        p = out / 'modules' / row['module']
        p.write_bytes(item['data'])
        p.chmod(0o400)
    header = 'static const char expected_release[]=' + json.dumps(expected_release) + ';\n'
    header += 'static const char expected_serial[]=' + json.dumps(expected_serial) + ';\n'
    header += 'static const char expected_bundle_id[]=' + json.dumps(bundle_id) + ';\n'
    header += 'static const unsigned return_prefix_count=' + str(return_prefix_count) + ';\n'
    header += 'static const struct module_entry modules[]={\n'
    for row in rows:
        digest = ','.join('0x' + row['sha256'][i:i + 2] for i in range(0, 64, 2))
        header += '{' + json.dumps('/ace-ramdiag/modules/' + row['module']) + ',' + str(row['bytes']) + ',{' + digest + '},' + json.dumps(row['gate']) + '},\n'
    header += '};\n'
    for index, row in enumerate(bindings):
        header += 'static const struct property_entry properties_' + str(index) + '[]={\n'
        for name, value in sorted(row.get('properties', {}).items()):
            values = ','.join('0x' + value[i:i + 2] for i in range(0, len(value), 2))
            header += '{' + json.dumps(name) + ',' + str(len(value) // 2) + ',{' + values + '}},\n'
        header += '{0,0,{0}}};\n'
    header += 'static const struct binding_entry bindings[]={\n'
    for index, row in enumerate(bindings):
        header += '{' + ','.join(json.dumps(row.get(key, '')) for key in ['dt_path', 'driver', 'module', 'class_path']) + ',properties_' + str(index) + ',' + str(int(row.get('early', False))) + '},\n'
    header += '{0,0,0,0,0,0}};\n'
    (out / 'module_bundle.h').write_text(header)
    command = ['aarch64-linux-gnu-gcc', '-O2', '-static', '-nostdlib', '-ffreestanding', '-fno-builtin',
               '-fno-stack-protector', '-fno-pie', '-no-pie', '-Wall', '-Wextra', '-Werror',
               '-Wl,--build-id=none,-e,_start,--strip-all', '-I', str(out),
               str(ROOT / 'diagnostics/ace-irq-timer/qemu-start.S'), str(SOURCE / 'module_loader.c'), '-o', str(out / 'module-loader')]
    supervisor_header = 'static const char expected_bundle_id[]=' + json.dumps(bundle_id) + ';\n#define SUPERVISOR_TIMEOUT_SECONDS ' + str(supervisor_timeout) + '\n'
    (out / 'supervisor_config.h').write_text(supervisor_header)
    sources = [Path(__file__), SOURCE / 'module_loader.c', SOURCE / 'module_supervisor.c', SOURCE / 'sha256.h', SOURCE / 'slot_guard.h', SOURCE / 'aarch64_flags.h',
               SOURCE / 'module_plan.py', ROOT / 'tools/fdt.py', ROOT / 'tools/ace-recovery-diag.py',
               ROOT / 'diagnostics/ace-irq-timer/qemu-start.S']
    for path in sources:
        snapshot = out / 'source-snapshot' / path.relative_to(ROOT)
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(path.read_bytes())
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    (out / 'build.log').write_text(result.stdout + result.stderr)
    require(result.returncode == 0, 'module loader compile failed; inspect build.log')
    (out / 'module-loader').chmod(0o500)
    supervisor_command = command[:-3] + [str(SOURCE / 'module_supervisor.c'), '-o', str(out / 'module-supervisor')]
    result = subprocess.run(supervisor_command, capture_output=True, text=True, timeout=30)
    (out / 'supervisor-build.log').write_text(result.stdout + result.stderr)
    require(result.returncode == 0, 'supervisor compile failed; inspect supervisor-build.log')
    (out / 'module-supervisor').chmod(0o500)
    report = dict(status='compiled only; hardware startup unproven', phone_io=False, ios_deployable=False,
                  expected_serial=expected_serial, expected_release=expected_release, modules=rows, bindings=bindings,
                  bundle_id=bundle_id, return_prefix_count=return_prefix_count, supervisor_timeout=supervisor_timeout,
                  supervisor_sha256=sha((out / 'module-supervisor').read_bytes()), supervisor_build_command=supervisor_command,
                  supervisor_header_sha256=sha(supervisor_header.encode()),
                  loader_sha256=sha((out / 'module-loader').read_bytes()), header_sha256=sha(header.encode()),
                  source_sha256={str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sources}, build_command=command,
                  limitations=['release/vermagic check is not full ABI proof; kernel verifies module with flags zero',
                               'insertion does not prove hardware binding, power, interrupts or USB role'])
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def physical_bindings(module_names):
    """Source-observed driver identities plus bytes from the exact live FDT.

    These become runtime checks, never claims of probe/operation success.
    """
    path = SOURCE / 'binding_contract.json'
    raw = path.read_bytes()
    contract = json.loads(raw)
    blob = (ROOT / 'research/ace-native-fdt-20261020/live-fdt.dtb').read_bytes()
    require(sha(blob) == plan.FDT_SHA, 'binding FDT pin mismatch')
    tree = plan.fdt.parse(blob)
    bindings, source_hashes = [], {}
    for row in contract:
        require(row['module'] in module_names, 'binding owner module outside bundle')
        texts = []
        for entry in [row] + row.get('supporting_sources', []):
            relative = Path(entry['source'])
            require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe binding source path')
            data = None
            for base in ['research/ace-ramdiag-20261020/provider-source', 'research/ace-driver-port-20261019/storage/official']:
                candidate = ROOT / base / relative
                if candidate.is_file():
                    data = candidate.read_bytes()
                    break
            require(data is not None and sha(data) == entry['sha256'], 'binding source pin mismatch')
            source_hashes[str(relative)] = sha(data)
            texts.append(data.decode())
        macros = dict(re.findall(r'^\s*#define\s+(\w+)\s+"([^"]+)"', '\n'.join(texts), re.M))
        names = re.findall(r'\.name\s*=\s*"([^"]+)"', texts[0])
        names += [macros[m] for m in re.findall(r'\.name\s*=\s*(\w+)', texts[0]) if m in macros]
        require(row['driver'] in names, 'binding driver name absent from pinned source')
        node = tree.by_path(row['dt_path'])
        require(node is not None, 'binding DT node missing')
        properties = {}
        for name in row['check_properties']:
            require(name in node.props, 'binding DT property missing')
            properties[name] = node.props[name].hex()
        bindings.append({**{k: row[k] for k in ['dt_path', 'driver', 'module', 'class_path']}, 'properties': properties, 'early': row.get('early', False)})
    return bindings, dict(binding_contract_sha256=sha(raw), binding_source_sha256=source_hashes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--plan-sha256', required=True)
    parser.add_argument('--expected-serial', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = args.plan.read_bytes()
    require(re.fullmatch('[0-9a-f]{64}', args.plan_sha256) and sha(raw) == args.plan_sha256, 'explicit plan hash mismatch')
    report = json.loads(raw)
    require(report['vendor_sha256'] == plan.VENDOR_SHA and report['kernel_sha256'] == plan.KERNEL_SHA and report['live_fdt_sha256'] == plan.FDT_SHA, 'plan artifact pins mismatch')
    for path, pin in report['source_sha256'].items():
        require(not Path(path).is_absolute() and '..' not in Path(path).parts and sha((ROOT / path).read_bytes()) == pin, 'plan source changed')
    modules, metadata, release = original_modules()
    dep = plan.Dependencies(modules, metadata['modules.dep'], metadata['modules.softdep'])
    preconditions = json.loads((SOURCE / 'startup_preconditions.json').read_text())
    expected = dep.ordered(report['directly_matched_modules'], before=[(r['before'], r['consumer']) for r in preconditions], first=plan.RETURN_PREFIX)
    require([r['module'] for r in report['insertion_order']] == expected, 'independent dependency order mismatch')
    require(report['return_prefix'] == expected[:len(plan.RETURN_PREFIX)], 'return prefix report mismatch')
    gates = {r['consumer']: r['required_sysfs_path'] for r in preconditions}
    items = []
    for row in report['insertion_order']:
        name = dep.resolve(row['module'])
        require(sha(modules[name]) == row['sha256'] and len(modules[name]) == row['bytes'], 'module archive pin mismatch')
        items.append(dict(module=name, data=modules[name], gate=gates.get(name, '')))
    bindings, provenance = physical_bindings({module_info(item['data'])['name'] for item in items})
    result = compile_bundle(args.output.resolve(), items, expected_release=release, expected_serial=args.expected_serial,
                            bindings=bindings, return_prefix_count=len(plan.RETURN_PREFIX))
    result.update(provenance)
    result['input_plan_sha256'] = sha(raw)
    (args.output / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'module_count': len(items), 'loader_sha256': result['loader_sha256']}, indent=2))


if __name__ == '__main__':
    main()
