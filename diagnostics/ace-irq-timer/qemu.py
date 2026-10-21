#!/usr/bin/env python3
"""QEMU-only compatibility check. Never calls ADB or touches phone partitions."""
import argparse,gzip,hashlib,json,stat,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
if not __debug__: raise RuntimeError('Verification requires Python without optimization')
p=argparse.ArgumentParser();p.add_argument('module',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
module=a.module.resolve(); out=a.output.resolve()
if not out.is_relative_to(ROOT/'research/ace-irq-timer-live-20261019'): p.error('output must be a new child directory')
if module.stat().st_size>1024*1024: p.error('diagnostic module too large')
out.mkdir(mode=0o700,parents=True,exist_ok=False)
image=ROOT/'research/ace-stock-qemu-20261019/Image'
if not image.exists(): image=ROOT/'research/ace-stock-qemu-20261019/stock-kernel.Image'
assert hashlib.sha256(image.read_bytes()).hexdigest()=='8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'
build=['aarch64-linux-gnu-gcc','-march=armv8-a','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-pie','-O2','-nostdlib','-static','-no-pie','-Wl,-e,_start,--build-id=none','-o',str(out/'init'),str(HERE/'qemu-start.S'),str(HERE/'qemu-init.c')]
(out/'build-command.json').write_text(json.dumps(build,indent=2)+'\n')
with (out/'build.log').open('w') as f:subprocess.run(build,check=True,stdout=f,stderr=f,timeout=20)
entries=[('.',stat.S_IFDIR|0o755,b'',0,0),('dev',stat.S_IFDIR|0o755,b'',0,0),('dev/console',stat.S_IFCHR|0o600,b'',5,1),('init',stat.S_IFREG|0o755,(out/'init').read_bytes(),0,0),('ace_irq_timer.ko',stat.S_IFREG|0o600,module.read_bytes(),0,0),('TRAILER!!!',0,b'',0,0)]
archive=bytearray()
for i,(name,mode,data,major,minor) in enumerate(entries,1):
 name=name.encode()+b'\0';values=[i,mode,0,0,1,0,len(data),0,0,major,minor,len(name),0]
 archive.extend(b'070701'+b''.join(f'{v:08x}'.encode() for v in values)+name);archive.extend(bytes(-len(archive)%4));archive.extend(data);archive.extend(bytes(-len(archive)%4))
(out/'initramfs.cpio.gz').write_bytes(gzip.compress(archive,mtime=0))
command=['qemu-system-aarch64','-accel','tcg','-M','virt,gic-version=3,virtualization=on','-cpu','max','-smp','1','-m','768M','-kernel',str(image),'-initrd',str(out/'initramfs.cpio.gz'),'-append','console=ttyAMA0 earlycon=pl011,0x09000000 rdinit=/init nokaslr loglevel=8 panic=-1','-no-reboot','-display','none','-serial','file:'+str(out/'serial.log'),'-monitor','none','-nic','none']
(out/'command.json').write_text(json.dumps(command,indent=2)+'\n')
t=time.monotonic();expired=False
with (out/'host.log').open('w') as f:
 q=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=f,stderr=f)
 try:q.wait(timeout=45)
 except subprocess.TimeoutExpired:
  expired=True;q.terminate()
  try:q.wait(timeout=3)
  except subprocess.TimeoutExpired:q.kill();q.wait(timeout=3)
serial=(out/'serial.log').read_text(errors='replace')
markers=['ACE_MODULE_QEMU: LOAD_PASS','ACE_MODULE_QEMU: UNLOAD_PASS','ACE_IRQ_TIMER: el=1','reboot: Power down']
passed=not expired and q.returncode==0 and all(x in serial for x in markers) and not any(x in serial for x in ['Kernel panic','BUG:','CFI failure','CFI failure'])
result=dict(source_sha256={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['qemu.py','qemu-init.c','qemu-start.S']},passed=passed,exit_code=q.returncode,timed_out=expired,duration_s=round(time.monotonic()-t,3),module=str(module.relative_to(ROOT)),module_sha256=hashlib.sha256(module.read_bytes()).hexdigest(),markers={m:m in serial for m in markers},scope='QEMU stock kernel module compatibility only; no phone or iOS validation')
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if passed else 1)
