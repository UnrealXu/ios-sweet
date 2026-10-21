#!/usr/bin/env python3
"""QEMU-only stock-kernel module and pmsg-layout check. No device operations."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL_SHA = '8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('module', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    out = a.output.resolve()
    if not out.is_relative_to(ROOT / 'research/ace-pmsg-header-20261019'):
        p.error('output must be under ignored research/ace-pmsg-header-20261019')
    out.mkdir(parents=True, exist_ok=False)
    image = ROOT / 'research/ace-stock-qemu-20261019/Image'
    if hashlib.sha256(image.read_bytes()).hexdigest() != KERNEL_SHA:
        p.error('stock kernel hash mismatch')
    module = a.module.resolve()
    if module.stat().st_size > 1024 * 1024:
        p.error('module exceeds diagnostic bound')
    def run(label, command):
        (out / (label + '-command.json')).write_text(json.dumps(command, indent=2)+'\n')
        with (out / (label + '.log')).open('w') as f:
            subprocess.run(command, check=True, stdout=f, stderr=f, timeout=30)
    machine = ['qemu-system-aarch64', '-accel', 'tcg', '-M', 'virt,gic-version=3,virtualization=on',
               '-cpu', 'max', '-smp', '1', '-m', '768M']
    run('dump-dtb', machine + ['-machine', 'dumpdtb='+str(out/'virt.dtb'), '-display', 'none', '-nic', 'none'])
    run('decode-dtb', ['dtc', '-I', 'dtb', '-O', 'dts', '-o', str(out/'virt.dts'), str(out/'virt.dtb')])
    dts = (out/'virt.dts').read_text()
    assert 'reserved-memory' not in dts and '\n/ {\n' in dts
    reserved = '''
    reserved-memory {
        #address-cells = <2>;
        #size-cells = <2>;
        ranges;
        ramoops@48090000 {
            compatible = "ramoops";
            reg = <0 0x48090000 0 0xe0000>;
            no-map;
            record-size = <0x1000>;
            console-size = <0x40000>;
            ftrace-size = <0x1000>;
            pmsg-size = <0x10000>;
            mem-type = <0>;
        };
    };
'''
    (out/'reserved.dts').write_text(dts[:dts.rfind('};')] + reserved + dts[dts.rfind('};'):])
    run('encode-dtb', ['dtc', '-I', 'dts', '-O', 'dtb', '-o', str(out/'reserved.dtb'), str(out/'reserved.dts')])
    run('build-init', ['aarch64-linux-gnu-gcc', '-march=armv8-a', '-ffreestanding', '-fno-builtin',
                      '-fno-stack-protector', '-fno-pie', '-O2', '-nostdlib', '-static', '-no-pie',
                      '-Wall', '-Wextra', '-Werror', '-Wl,-e,_start,--build-id=none', '-o', str(out/'init'),
                      str(HERE/'qemu-start.S'), str(HERE/'qemu-init.c')])
    entries = [('.', stat.S_IFDIR|0o755, b'',0,0), ('dev', stat.S_IFDIR|0o755,b'',0,0),
               ('proc', stat.S_IFDIR|0o755,b'',0,0), ('dev/console',stat.S_IFCHR|0o600,b'',5,1),
               ('init',stat.S_IFREG|0o755,(out/'init').read_bytes(),0,0),
               ('ace_pmsg_header.ko',stat.S_IFREG|0o600,module.read_bytes(),0,0), ('TRAILER!!!',0,b'',0,0)]
    archive = bytearray()
    for i,(name,mode,data,major,minor) in enumerate(entries,1):
        name = name.encode()+b'\0'
        fields = [i,mode,0,0,1,0,len(data),0,0,major,minor,len(name),0]
        archive += b'070701'+b''.join(f'{v:08x}'.encode() for v in fields)+name
        archive += bytes(-len(archive)%4);archive += data;archive += bytes(-len(archive)%4)
    (out/'initramfs.cpio.gz').write_bytes(gzip.compress(archive,mtime=0))
    command = machine + ['-kernel',str(image),'-dtb',str(out/'reserved.dtb'),'-initrd',str(out/'initramfs.cpio.gz'),
                         '-append','console=ttyAMA0 earlycon=pl011,0x09000000 rdinit=/init nokaslr loglevel=8 panic=-1',
                         '-no-reboot','-display','none','-serial','file:'+str(out/'serial.log'),'-monitor','none','-nic','none']
    (out/'command.json').write_text(json.dumps(command,indent=2)+'\n')
    start = time.monotonic(); expired = False
    with (out/'host.log').open('w') as f:
        proc = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=f, stderr=f)
        try: proc.wait(timeout=45)
        except subprocess.TimeoutExpired:
            expired=True;proc.terminate()
            try: proc.wait(timeout=3)
            except subprocess.TimeoutExpired: proc.kill();proc.wait(timeout=3)
    serial = (out/'serial.log').read_text(errors='replace')
    headers = re.findall(r'ACE_PMSG_HEADER: sig=([0-9a-f]+) start=(\d+) size=(\d+) capacity=(\d+) stable=(\d+) valid=(\d+) attempts=(\d+)',serial)
    expected = len(b'ACE_PMSG_QEMU_NORMAL_WRITE\n')
    passed = (not expired and proc.returncode==0 and len(headers)==2 and
              headers[0][:6]==('43474244','0','0','65524','1','1') and
              headers[1][:6]==('43474244',str(expected),str(expected),'65524','1','1') and
              serial.count('ACE_PMSG_QEMU: LOAD_PASS')==2 and serial.count('ACE_PMSG_QEMU: UNLOAD_PASS')==2 and
              'ACE_PMSG_QEMU: ALL_PASS' in serial and 'reboot: Power down' in serial and
              not any(x in serial for x in ['Kernel panic','BUG:','CFI failure']))
    result = dict(passed=passed, exit_code=proc.returncode, timed_out=expired,
                  duration_s=round(time.monotonic()-start,3), kernel_sha256=KERNEL_SHA,
                  module_sha256=hashlib.sha256(module.read_bytes()).hexdigest(), headers=headers,
                  source_sha256={x:hashlib.sha256((HERE/x).read_bytes()).hexdigest() for x in
                                 ['ace_pmsg_header.c','Makefile','qemu-init.c','qemu-start.S','qemu.py']},
                  scope='Stock kernel QEMU: normal load/unload and header before/after normal pmsg write; no phone or baremetal validation')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));raise SystemExit(0 if passed else 1)


if __name__=='__main__': main()
