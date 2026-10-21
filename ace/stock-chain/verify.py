#!/usr/bin/env python3
"""Boot the exact stock kernel AFTER real diagnostic prefix execution in QEMU."""
import hashlib
import json
from pathlib import Path
import socket
import struct
import subprocess
import time
if not __debug__:raise RuntimeError('Optimized verification refused')
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'ace/stock-chain'
OUT=ROOT/'research/ace-stock-chain-20261019'
INITRD=ROOT/'research/ace-irq-timer-live-20261019/qemu/initramfs.cpio.gz'
INITRD_SHA='d652143893bec3a082b4fa8984e60827eee9aa9c1fdf28b72a8475171c3c4dfe'
RING=0x48160000

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def execute(name,mode,virt,seed=True,bad=False,relocated=False):
    build=json.loads((OUT/'build.json').read_text())
    assert sha(OUT/(mode+'.Image'))==build['images'][mode]['sha256']
    symbols={l.split()[2]:int(l.split()[0],16) for l in subprocess.check_output(['aarch64-linux-gnu-nm','-n',str(OUT/(mode+'.elf'))],text=True).splitlines() if len(l.split())==3}
    folder=OUT/name;folder.mkdir(exist_ok=True)
    for file in ['record.bin','ring.bin','stock.bin','serial.log','gdb.log','host.log']:(folder/file).unlink(missing_ok=True)
    ring=bytearray(65536);struct.pack_into('<III',ring,0,0x43474244 if not bad else 0,0,0)
    (folder/'seed.bin').write_bytes(ring)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    argv=['qemu-system-aarch64','-accel','tcg','-M','virt,gic-version=3,virtualization='+virt,'-cpu','max','-smp','1','-m','768M','-kernel',str(OUT/(mode+'.Image')),'-initrd',str(INITRD),'-append','console=ttyAMA0 earlycon=pl011,0x09000000 rdinit=/init nokaslr loglevel=8 panic=-1','-no-reboot','-display','none','-serial','file:'+str(folder/'serial.log'),'-monitor','none','-nic','none','-S','-gdb',f'tcp:127.0.0.1:{port}']
    start=time.monotonic()
    with (folder/'host.log').open('w') as log:
        q=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=log,stderr=log)
        try:
            cmds=['set pagination off','set confirm off','set tcp connect-timeout 5','set tcp auto-retry on',f'target remote 127.0.0.1:{port}',
                  # Exact QEMU virt boot stub has six instructions ending in BRx4.
                  'si 6','set $chainbase=$pc','set $incoming_x0=$x0']
            if relocated:
                cmds += [f'restore {OUT/(mode+".Image")} binary 0x44000000','set $pc=0x44000000','set $chainbase=$pc']
            if seed:cmds += [f'restore {folder/"seed.bin"} binary {RING}']
            cmds += [f'hbreak *($chainbase+{symbols["chain_jump"]})','continue',
                     f'dump binary memory {folder/"record.bin"} ($chainbase+{symbols["chain_record"]}) ($chainbase+{symbols["chain_record"]+80})',
                     f'dump binary memory {folder/"stock.bin"} ($chainbase+2097152) ($chainbase+2097152+{build["stock_bytes"]})',
                     'printf "CHAINREG %llu %llu %llu %llu %llu\\n",$chainbase,$incoming_x0,$x0,$x1|$x2|$x3,$pc',
                     'si','printf "STOCKPC %llu\\n",$pc']
            if seed:cmds += [f'dump binary memory {folder/"ring.bin"} {RING} {RING+65536}']
            cmds += ['detach','quit']
            g=['gdb-multiarch','-nx','-q','-batch']
            for c in cmds:g+=['-ex',c]
            result=subprocess.run(g,capture_output=True,text=True,timeout=30)
            (folder/'gdb.log').write_text(result.stdout+result.stderr)
            assert result.returncode==0,result.stderr
            q.wait(timeout=45)
        finally:
            if q.poll() is None:
                q.terminate()
                try:q.wait(timeout=3)
                except subprocess.TimeoutExpired:q.kill();q.wait(timeout=3)
    text=(folder/'gdb.log').read_text()
    line=next(l for l in text.splitlines() if l.startswith('CHAINREG '))
    base,incoming,x0,other,pc=map(int,line.split()[1:])
    assert base==(0x44000000 if relocated else 0x40200000)
    assert incoming==x0 and other==0 and pc==base+symbols['chain_jump']
    assert int(next(l for l in text.splitlines() if l.startswith('STOCKPC ')).split()[1])==base+0x200000
    assert sha(folder/'stock.bin')==build['stock_sha256']
    v=struct.unpack('<10Q',(folder/'record.bin').read_bytes())
    assert (folder/'record.bin').read_bytes()[:8]==b'ACECHN01'
    assert v[1]==2 and v[2]==incoming and v[3]==(8 if virt=='on' else 4) and v[4]&5==0
    assert v[7]==62500000 and v[9]==base+0x200000
    expected_status= -9 if mode=='plain' else -2 if mode=='alias-test' else -3 if bad else 0
    assert v[8]==expected_status%(2**64),v
    if seed:
        after=(folder/'ring.bin').read_bytes()
        if bad:assert after==ring
        else:
            marker=('ACECHAIN1:'+build['token']+': forwarding original Android kernel\n').encode()
            raw=list(v);raw[1]=1
            payload=marker+struct.pack('<10Q',*raw)
            expected=bytearray(ring);struct.pack_into('<II',expected,4,len(payload),len(payload));expected[12:12+len(payload)]=payload
            assert after==expected,'Ring bytes differ from exact marker + observed pre-handoff record'
    serial=(folder/'serial.log').read_text(errors='replace')
    required=['ACE_MODULE_QEMU: LOAD_PASS','ACE_MODULE_QEMU: UNLOAD_PASS','ACE_IRQ_TIMER: el=1','reboot: Power down']
    assert q.returncode==0 and all(m in serial for m in required)
    assert not any(m in serial for m in ['Kernel panic','BUG:','CFI failure','Unable to handle kernel'])
    report=dict(case=name,mode=mode,passed=True,incoming_el=v[3]//4,record=list(v),
                exact_stock_kernel_unchanged=True,stock_kernel_booted=True,module_normal_load_unload=True,
                logger_status=expected_status,exit_code=q.returncode,duration_s=round(time.monotonic()-start,3),qemu_argv=argv,gdb_argv=g)
    (folder/'case.json').write_text(json.dumps(report,indent=2)+'\n')
    print(name+': prefix -> byte-identical stock kernel -> normal module load/unload -> poweroff PASS',flush=True)
    return report

def main():
    OUT.mkdir(exist_ok=True)
    (OUT/'verification.json').write_text('{"status":"incomplete"}\n')
    assert sha(INITRD)==INITRD_SHA
    build=json.loads((OUT/'build.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in build['sources'].items())
    cases=[execute('plain-el2','plain','on',seed=False),
           execute('pmsg-el1','pmsg','off'),execute('pmsg-el2','pmsg','on'),
           execute('pmsg-relocated','pmsg','on',relocated=True),
           execute('bad-header-forward','pmsg','on',bad=True),
           execute('full-image-alias-refused','alias-test','on',seed=False)]
    sources=[HERE/'start.S',HERE/'linker.ld',HERE/'build.py',HERE/'verify.py',ROOT/'ace/entry/pmsg.S']
    paths=[OUT/'build.json',INITRD]
    for case in cases:paths += [p for p in (OUT/case['case']).iterdir() if p.is_file()]
    for mode in ['plain','pmsg','alias-test']:paths += [OUT/(mode+'.Image'),OUT/(mode+'.elf')]
    result=dict(status='pass',scope='Actual QEMU prefix plus original stock Linux execution; NOT Ace hardware/XNU/iOS',
                cases=cases,token=build['token'],stock_sha256=build['stock_sha256'],
                sources={str(p.relative_to(ROOT)):sha(p) for p in sources},
                artifacts_sha256={str(p.relative_to(ROOT)):sha(p) for p in paths},hardware_tested=False,ios_deployable=False)
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
