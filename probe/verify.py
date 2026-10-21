#!/usr/bin/env python3
"""Execute real probe instructions on QEMU; inspect only its own record via GDB."""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import socket
import struct
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'research/ace-offline/probe'
FIELDS = ('magic version stage entry_x0 current_el sctlr mpidr mmfr0 cntfrq tcr '
          'tgran16 esr far elr supports_16k').split()


def symbols():
    return {line.split()[2]: int(line.split()[0], 16)
            for line in subprocess.check_output(
                ['aarch64-linux-gnu-nm', str(OUT / 'probe.elf')], text=True).splitlines()
            if len(line.split()) == 3}


def run_case(name, virtualization, expected_stage, expected_el, address, fault=False, mmu=False):
    syms = symbols()
    # localhost only, with bounded process lifetime and unconditional cleanup.
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1', 0))
        port = reservation.getsockname()[1]
    dump = OUT / f'{name}-record.bin'
    dump.unlink(missing_ok=True)
    with (OUT / f'{name}-qemu.log').open('w') as log:
        q = subprocess.Popen([
            'qemu-system-aarch64', '-M', f'virt,virtualization={virtualization}',
            '-cpu', 'cortex-a76', '-m', '128M', '-smp', '1', '-nographic',
            '-monitor', 'none', '-serial', 'none', '-nic', 'none',
            '-kernel', str(OUT / 'probe.Image'), '-S',
            '-gdb', f'tcp:127.0.0.1:{port}'], stdout=log, stderr=log)
        try:
            # GDB retries opening QEMU's listener while it starts, at most 5 sec.
            commands = [
                'set pagination off', 'set confirm off',
                'set tcp connect-timeout 5', 'set tcp auto-retry on',
                f'target remote 127.0.0.1:{port}',
            ]
            # Relocation test: Linux header has no encoded absolute address.
            # QEMU initially loads at 0x40080000; copy bytes via GDB to another
            # RAM address and set PC only, retaining QEMU's actual entry EL/x0.
            if address != 0x40080000:
                commands += [f'hbreak *{0x40080000}', 'continue', 'delete breakpoints',
                             f'restore {OUT / "probe.Image"} binary {address}',
                             f'set $pc = {address}']
            if mmu:
                page = bytearray(4096)
                struct.pack_into('<Q', page, 8, 0x40000701)
                table_before = OUT / f'{name}-identity-l1.bin'
                table_after = OUT / f'{name}-identity-l1-after.bin'
                table_before.write_bytes(page)
                trampoline = 'qemu-el2-mmu-on.bin' if expected_el == 8 else 'qemu-mmu-on.bin'
                commands += [f'hbreak *{address}', 'continue', 'delete breakpoints',
                             f'restore {table_before} binary 0x41000000',
                             f'restore {OUT / trampoline} binary 0x41200000',
                             'set $pc = 0x41200000',
                             f'hbreak *{address + syms["probe_main"]}']
            if fault:
                commands += [f'set {{unsigned int}}{address + syms["probe_main"]} = 0xd4200000']
            halt = address + syms['probe_halt']
            record = address + syms['diagnostic_record']
            commands += [f'hbreak *{halt}', 'continue',
                         f'dump binary memory {dump} {record} {record + 120}',
                         'info registers pc cpsr sp']
            if mmu:
                register_names = (('SCTLR_EL2', 'TCR_EL2', 'TTBR0_EL2', 'MAIR_EL2')
                                  if expected_el == 8 else
                                  ('SCTLR', 'TCR_EL1', 'TTBR0_EL1', 'MAIR_EL1'))
                for label, register in zip(('SCTLR', 'TCR', 'TTBR0', 'MAIR'), register_names):
                    commands += [f'printf "FINAL_{label}=%#lx\\n", ${register}']
                commands += [f'dump binary memory {table_after} 0x41000000 0x41001000']
            commands += ['detach', 'quit']
            args = ['gdb-multiarch', '-q', '-nx', '-batch']
            for command in commands:
                args += ['-ex', command]
            r = subprocess.run(args, text=True, capture_output=True, timeout=20)
            (OUT / f'{name}-gdb.log').write_text(r.stdout + r.stderr)
            if r.returncode:
                raise RuntimeError(f'{name}: GDB failed: {r.stdout}\n{r.stderr}')
            raw = dump.read_bytes()
            values = dict(zip(FIELDS, struct.unpack('<15Q', raw)))
            assert raw[:8] == b'ACEPROBE', values
            assert values['version'] == 2, values
            assert values['stage'] == expected_stage, values
            assert values['current_el'] == expected_el, values
            if expected_stage == 5:
                assert values['sctlr'] & 1 == 0, values
                assert values['cntfrq'] > 0, values
                assert values['tgran16'] == (values['mmfr0'] >> 20) & 15
                assert values['supports_16k'] == 1, values
            if expected_stage in (5, 6):
                stack = re.search(r'^sp\s+(0x[0-9a-f]+)', r.stdout, re.MULTILINE)
                pstate = re.search(r'^cpsr\s+(0x[0-9a-f]+)', r.stdout, re.MULTILINE)
                assert stack and int(stack.group(1), 16) == address + syms['stack_top'], r.stdout
                assert pstate and int(pstate.group(1), 16) & 15 == (9 if expected_el == 8 else 5), r.stdout
            if fault:
                assert values['esr'] >> 26 == 0x3c, values
                assert values['elr'] == address + syms['probe_main'], values
            result = {'case': name, 'load_address': hex(address), 'pass': True,
                      'control_register_bank': 'EL2' if expected_el == 8 else 'EL1',
                      'record': {k: hex(v) for k, v in values.items()}}
            if mmu:
                live = {key: int(value, 16) for key, value in
                        re.findall(r'FINAL_(\w+)=(0x[0-9a-f]+)', r.stdout)}
                assert values['sctlr'] & 1 == 1, values
                assert live['SCTLR'] == values['sctlr'], live
                assert live['TCR'] == (0x80823019 if expected_el == 8 else 0x200803019), live
                assert live['TTBR0'] == 0x41000000, live
                assert live['MAIR'] == 0x44, live
                assert table_after.read_bytes() == page
                assert values['mpidr'] == values['mmfr0'] == values['cntfrq'] == 0
                result['mmu_setup_and_final'] = {key: hex(value) for key, value in live.items()}
                result['identity_table'] = {'pa': '0x41000000', 'size': 4096,
                                            'level': 1, 'entry_index': 1,
                                            'descriptor': '0x40000701',
                                            'translation_regime': 'EL2 stage-1' if expected_el == 8 else 'EL1 stage-1',
                                            'va_pa_range': '0x40000000..0x7fffffff',
                                            'unchanged_after_execution': True}
            return result
        finally:
            q.terminate()
            try:
                q.wait(timeout=3)
            except subprocess.TimeoutExpired:
                q.kill()
                q.wait(timeout=3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    # A failed rerun must not leave an earlier success looking current.
    report_path = OUT / 'verification.json'
    if report_path.exists():
        shutil.copyfile(report_path, OUT / 'verification.previous.json')
    report_path.write_text(json.dumps({'status': 'in-progress',
                                      'scope': 'QEMU only; this attempt has not passed'}) + '\n')
    for tool in ('qemu-system-aarch64', 'gdb-multiarch', 'aarch64-linux-gnu-nm'):
        if not shutil.which(tool):
            raise SystemExit(f'Missing required host tool: {tool}')
    subprocess.run([str(ROOT / 'probe/build.sh')], check=True)
    # QEMU's GDB interface exposes sysregs for reads, but writes were observed
    # to be ignored. Use architected MSR/TLBI/ISB in a separate test trampoline.
    for stem in ('qemu-mmu-on', 'qemu-el2-mmu-on'):
        subprocess.run(['aarch64-linux-gnu-gcc', '-march=armv8-a', '-nostdlib',
                        '-Wl,--build-id=none,-Ttext=0x41200000,-e,mmu_test_entry',
                        str(ROOT / 'probe' / (stem + '.S')), '-o',
                        str(OUT / (stem + '.elf'))], check=True)
        subprocess.run(['aarch64-linux-gnu-objcopy', '-O', 'binary', '-j', '.text',
                        str(OUT / (stem + '.elf')), str(OUT / (stem + '.bin'))], check=True)
    results = [run_case('el1', 'off', 5, 4, 0x40080000),
               run_case('el2', 'on', 5, 8, 0x40080000),
               run_case('el1-relocated', 'off', 5, 4, 0x40200000),
               run_case('el2-relocated', 'on', 5, 8, 0x40200000),
               run_case('el1-brk-exception', 'off', 6, 4, 0x40080000, fault=True),
               run_case('el2-brk-exception', 'on', 6, 8, 0x40080000, fault=True),
               run_case('el1-mmu-on-rejected', 'off', 3, 4, 0x40080000, mmu=True),
               run_case('el2-mmu-on-rejected', 'on', 3, 8, 0x40080000, mmu=True)]
    report = {'status': 'pass', 'scope': 'QEMU Cortex-A76 only; no Ace hardware evidence',
              'record_version': 2,
              'image_sha256': hashlib.sha256((OUT / 'probe.Image').read_bytes()).hexdigest(),
              'input_sha256': {name: hashlib.sha256((ROOT / 'probe' / name).read_bytes()).hexdigest()
                               for name in ('start.S', 'probe.c', 'linker.ld', 'build.sh',
                                            'verify.py', 'qemu-mmu-on.S', 'qemu-el2-mmu-on.S')},
              'cases': results,
              'not_tested': ['EL0/EL3',
                             'physical OnePlus Ace boot or debug record retrieval']}
    (OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
