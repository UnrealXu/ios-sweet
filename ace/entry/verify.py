#!/usr/bin/env python3
"""Execute EL2->EL1 bridge on QEMU. No device/partition access."""
import hashlib
import json
import pathlib
import re
import shutil
import socket
import struct
import subprocess

if not __debug__:
    raise RuntimeError('Verification requires Python assertions; optimized execution is refused')

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'research/ace-entry-20261019'
REPORT_ROOT = None
SOURCE_NAMES = ('README.md', 'start.S', 'pmsg.S', 'linker.ld', 'build.sh',
                'verify.py', 'verify_pmsg.py')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes():
    return {n: sha(ROOT / 'ace/entry' / n) for n in SOURCE_NAMES}


def artifact_hashes(paths):
    root = REPORT_ROOT or OUT
    return {str(p.relative_to(root)): sha(p) for p in paths}


def symbols(path):
    return {p[2]: int(p[0], 16) for line in subprocess.check_output(
        ['aarch64-linux-gnu-nm', str(path)], text=True).splitlines()
        if len(p := line.split()) == 3}


def case(name, virtualization, base=0x40080000, mmu=False, memory_fixture=None, qemu_mib=128):
    own = symbols(OUT / 'entry.elf')
    probe = symbols(OUT / 'probe.elf')
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    record = OUT / (name + '-bridge.bin')
    payload = OUT / (name + '-probe.bin')
    record.unlink(missing_ok=True)
    payload.unlink(missing_ok=True)
    paths = [record]
    command = ['qemu-system-aarch64', '-M', 'virt,virtualization=' + virtualization,
               '-cpu', 'cortex-a76', '-m', f'{qemu_mib}M', '-smp', '1', '-nographic',
               '-monitor', 'none', '-serial', 'none', '-nic', 'none', '-kernel',
               str(OUT / 'entry.Image'), '-S', '-gdb', 'tcp:127.0.0.1:' + str(port)]
    qlog = OUT / (name + '-qemu.log')
    glog = OUT / (name + '-gdb.log')
    paths += [qlog, glog]
    with qlog.open('w') as log:
        q = subprocess.Popen(command, stdout=log, stderr=log, stdin=subprocess.DEVNULL)
        try:
            g = ['set pagination off', 'set confirm off', 'set tcp connect-timeout 5',
                 'set tcp auto-retry on', f'target remote 127.0.0.1:{port}']
            if memory_fixture:
                ring_address, fixture = memory_fixture
                before = OUT / (name + '-ring-before.bin')
                after = OUT / (name + '-ring-after.bin')
                after.unlink(missing_ok=True)
                before.write_bytes(fixture)
                paths += [before, after]
                g += [f'restore {before} binary {ring_address}']
            if base != 0x40080000:
                g += ['hbreak *0x40080000', 'continue', 'delete breakpoints',
                      f'restore {OUT / "entry.Image"} binary {base}', f'set $pc={base}']
            if mmu:
                table = bytearray(4096)
                struct.pack_into('<Q', table, 8, 0x40000701)
                table_before = OUT / (name + '-table.bin')
                table_after = OUT / (name + '-table-after.bin')
                table_after.unlink(missing_ok=True)
                table_before.write_bytes(table)
                paths += [table_before, table_after]
                stem = 'qemu-el2-mmu-on.bin' if virtualization == 'on' else 'qemu-mmu-on.bin'
                trampoline = OUT / (name + '-' + stem)
                shutil.copyfile(ROOT / 'research/ace-offline/probe' / stem, trampoline)
                paths.append(trampoline)
                g += [f'hbreak *{base}', 'continue', 'delete breakpoints',
                      f'restore {table_before} binary 0x41000000',
                      f'restore {trampoline} binary 0x41200000', 'set $pc=0x41200000']
            halt = (base + own['bridge_halt'] if mmu else
                    base + own['bridge_payload'] + probe['probe_halt'])
            active = 'SCTLR_EL2' if virtualization == 'on' else 'SCTLR'
            g += [f'hbreak *{halt}', 'continue',
                  f'dump binary memory {record} {base + own["bridge_record"]} {base + own["bridge_record"] + 64}',
                  'info registers pc cpsr', f'printf "ACTIVE_SCTLR=%#lx\\n", ${active}']
            if not mmu:
                addr = base + own['bridge_payload'] + probe['diagnostic_record']
                g += [f'dump binary memory {payload} {addr} {addr + 120}']
                paths += [payload]
            else:
                g += [f'dump binary memory {table_after} 0x41000000 0x41001000']
            if memory_fixture:
                g += [f'dump binary memory {after} {ring_address} {ring_address + len(fixture)}']
            status = None
            if 'bridge_pmsg_results' in own:
                status_path = OUT / (name + '-pmsg-status.bin')
                status_path.unlink(missing_ok=True)
                addr = base + own['bridge_pmsg_results']
                g += [f'dump binary memory {status_path} {addr} {addr + 8}']
                paths += [status_path]
            g += ['detach', 'quit']
            args = ['gdb-multiarch', '-nx', '-q', '-batch']
            for item in g:
                args += ['-ex', item]
            result = subprocess.run(args, capture_output=True, text=True, timeout=20)
            glog.write_text(result.stdout + result.stderr)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            b = struct.unpack('<8Q', record.read_bytes())
            assert record.read_bytes()[:8] == b'ACEENTRY' and b[1] == 1
            assert b[4] == (8 if virtualization == 'on' else 4), b
            if mmu:
                assert b[2] == 3 and b[5] & 1 == 1 and b[6] == 0, b
                live = int(re.search(r'ACTIVE_SCTLR=(0x[0-9a-f]+)', result.stdout)[1], 16)
                assert live == b[5]
                assert table_after.read_bytes() == table
                values = None
            else:
                assert b[2] == 4 and b[6] == 4 and b[7] & 5 == 0, b
                values = struct.unpack('<15Q', payload.read_bytes())
                assert payload.read_bytes()[:8] == b'ACEPROBE'
                assert values[1] == 2 and values[2] == 5 and values[3] == b[3] and values[4] == 4 and values[14] == 1, values
                pstate = int(re.search(r'^cpsr\s+(0x[0-9a-f]+)', result.stdout, re.M)[1], 16)
                assert pstate & 15 == 5
            if 'bridge_pmsg_results' in own:
                status = list(struct.unpack('<2i', status_path.read_bytes()))
            # QEMU appends its shutdown notice: stop before hashing its log.
            q.terminate()
            try:
                q.wait(timeout=3)
            except subprocess.TimeoutExpired:
                q.kill()
                q.wait(timeout=3)
            artifacts = artifact_hashes(paths)
            return {'case': name, 'pass': True, 'base': hex(base),
                    'bridge_record': [hex(v) for v in b],
                    'probe_record': [hex(v) for v in values] if values else None,
                    'pmsg_status': status, 'qemu_argv': command,
                    'gdb_argv': args, 'artifact_paths': list(artifacts),
                    'artifacts_sha256': artifacts}
        finally:
            q.terminate()
            try:
                q.wait(timeout=3)
            except subprocess.TimeoutExpired:
                q.kill()
                q.wait(timeout=3)


def build_artifacts():
    return artifact_hashes([OUT / n for n in ['entry.Image', 'entry.elf', 'probe.Image',
                           'probe.elf', 'entry_config.h', 'pmsg-config.json', 'build-manifest.json']])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    result = OUT / 'verification.json'
    if result.exists():
        result.replace(OUT / 'verification.previous.json')
    result.write_text(json.dumps({'status': 'incomplete'}) + '\n')
    subprocess.run([str(ROOT / 'ace/entry/build.sh')], check=True)
    cases = [case('el1-pass', 'off'), case('el2-to-el1', 'on'),
             case('el2-relocated', 'on', 0x40200000), case('el2-mmu-rejected', 'on', mmu=True)]
    artifacts = build_artifacts()
    for item in cases:
        artifacts.update(item['artifacts_sha256'])
    report = {'status': 'pass', 'scope': 'QEMU execution of independent EL entry bridge with diagnostic payload; NOT XNU or physical Ace',
              'image_sha256': sha(OUT / 'entry.Image'), 'probe_sha256': sha(OUT / 'probe.Image'),
              'sources': source_hashes(), 'build_manifest_sha256': sha(OUT / 'build-manifest.json'),
              'pmsg_enabled': False, 'cases': cases, 'artifacts_sha256': artifacts,
              'not_tested': ['EL3 refusal', 'D-cache-on refusal', 'physical Ace', 'XNU payload',
                             'hardware log retrieval', 'bootloader gzip/AVB acceptance']}
    result.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'cases': len(cases), 'image_sha256': report['image_sha256']}))


if __name__ == '__main__':
    main()
