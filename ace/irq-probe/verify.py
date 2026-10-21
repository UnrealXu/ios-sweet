#!/usr/bin/env python3
"""Execute isolated QEMU GICv3/timer experiments; never access a device."""
import hashlib
import json
from pathlib import Path
import socket
import struct
import subprocess

if not __debug__:
    raise RuntimeError('Optimized verification is refused')
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research/ace-irq-probe-20261019'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, virt, variant='normal', base=0x40080000):
    folder = OUT / variant
    symbols = dict((line.split()[2], int(line.split()[0], 16))
                   for line in subprocess.check_output(['aarch64-linux-gnu-nm', '-n', str(folder / 'probe.elf')], text=True).splitlines()
                   if len(line.split()) == 3)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    raw = OUT / (name + '.bin')
    raw.unlink(missing_ok=True)
    qlog = OUT / (name + '-qemu.log')
    glog = OUT / (name + '-gdb.log')
    command = ['qemu-system-aarch64', '-M', 'virt,gic-version=3,virtualization=' + virt,
               '-cpu', 'cortex-a76', '-m', '128M', '-smp', '1', '-nographic',
               '-monitor', 'none', '-serial', 'none', '-nic', 'none', '-kernel',
               str(folder / 'probe.Image'), '-S', '-gdb', 'tcp:127.0.0.1:' + str(port)]
    with qlog.open('w') as log:
        q = subprocess.Popen(command, stdout=log, stderr=log, stdin=subprocess.DEVNULL)
        try:
            cmds = ['set pagination off', 'set confirm off', 'set tcp connect-timeout 5',
                    'set tcp auto-retry on', f'target remote 127.0.0.1:{port}']
            if base != 0x40080000:
                cmds += ['hbreak *0x40080000', 'continue', 'delete breakpoints',
                         f'restore {folder / "probe.Image"} binary {base}', f'set $pc={base}']
            cmds += [f'hbreak *{base + symbols["halt"]}', 'continue',
                     f'dump binary memory {raw} {base + symbols["record"]} {base + symbols["record"] + 176}',
                     'info registers pc cpsr', 'detach', 'quit']
            argv = ['gdb-multiarch', '-nx', '-q', '-batch']
            for cmd in cmds:
                argv += ['-ex', cmd]
            result = subprocess.run(argv, capture_output=True, text=True, timeout=15)
            glog.write_text(result.stdout + result.stderr)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            values = struct.unpack('<22Q', raw.read_bytes())
            assert raw.read_bytes()[:8] == b'ACEIRQ01', values
            assert values[2] == (8 if virt == 'on' else 4) and values[3] == 4, values
            if variant == 'exception':
                assert values[1] == 9 and values[9] >> 26 == 0x3c and values[4] == 0, values
            else:
                assert values[5] > 0 and values[7] > values[6], values
                assert values[13] & 1 and (not virt == 'on' or values[14] & 9 == 9), values
                if variant == 'timeout':
                    assert values[1] == 6 and values[4] == 0, values
                    assert values[7] - values[6] >= values[5] // 6, values
                else:
                    assert values[1] == 5 and values[4] == 3 and values[8] == 27 and values[21] == 3, values
                    assert values[6] < values[18] < values[19] < values[20] <= values[7], values
                    assert values[19] - values[18] >= values[5] // 100, values
                    assert values[20] - values[19] >= values[5] // 100, values
                    assert values[7] - values[6] >= 3 * (values[5] // 100), values
            q.terminate()
            q.wait(timeout=3)
            paths = [raw, qlog, glog, folder / 'probe.Image', folder / 'probe.elf', folder / 'disassembly.txt']
            return dict(case=name, passed=True, variant=variant, base=hex(base),
                        record=list(values), qemu_argv=command, gdb_argv=argv,
                        artifacts_sha256={str(p.relative_to(OUT)): sha(p) for p in paths})
        finally:
            if q.poll() is None:
                q.kill()
                q.wait(timeout=3)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = OUT / 'verification.json'
    report.write_text('{"status":"incomplete"}\n')
    for variant in ('normal', 'timeout', 'exception'):
        subprocess.run([str(ROOT / 'ace/irq-probe/build.sh'), variant], check=True)
    cases = [run('el1-three-irqs', 'off'), run('el2-three-irqs', 'on'),
             run('el2-relocated', 'on', base=0x40200000),
             run('timer-disabled-timeout', 'on', variant='timeout'),
             run('brk-exception', 'off', variant='exception')]
    artifacts = {}
    for item in cases:
        artifacts.update(item['artifacts_sha256'])
    result = dict(status='pass', scope='QEMU virt cold boot only; NOT Ace or iOS',
                  sources={p.name: sha(p) for p in sorted((ROOT / 'ace/irq-probe').iterdir()) if p.is_file()},
                  cases=cases, artifacts_sha256=artifacts,
                  hardware_tested=False, ios_deployable=False)
    report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='pass', cases=len(cases))))


if __name__ == '__main__':
    main()
