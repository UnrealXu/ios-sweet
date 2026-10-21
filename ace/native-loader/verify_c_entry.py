#!/usr/bin/env python3
"""QEMU-only actual XNU16K bootstrap through one instruction of arm_init.

No phone operations or complete iOS/controller boot claim. Run the separate
whole-copy/refusal/relocation preflight too; kernel RAM legitimately changes
during page-table initialization, so this test does not compare it to Mach-O.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import socket
import subprocess

if not __debug__:raise RuntimeError('optimized verification refused')
from verify import debugger_numbers
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('pack',ROOT/'tools/ace-mkpayload.py')
pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
sha=lambda b:hashlib.sha256(b).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('image_directory',type=Path);p.add_argument('kernel',type=Path);p.add_argument('fdt',type=Path);p.add_argument('output_directory',type=Path)
    a=p.parse_args();image=a.image_directory.resolve();out=a.output_directory.resolve()
    if out.exists() or not out.is_relative_to(ROOT/'research'):raise ValueError('new ignored research/ output required')
    for x in [image,a.kernel.resolve(),a.fdt.resolve(),out]:
        if not re.fullmatch(r'[A-Za-z0-9_./+-]+',str(x)):raise ValueError('restricted GDB fixture paths required')
    m=json.loads((image/'build-manifest.json').read_text());s=json.loads((image/'symbols.json').read_text())
    debugger_numbers(m,s,len((image/'native.Image').read_bytes()))
    if sha((image/'native.Image').read_bytes())!=m['image_sha256'] or m['text_offset'] not in (0,0x80000):raise ValueError('Image/profile mismatch')
    kernel=pack.read(a.kernel);dtb=pack.read(a.fdt)
    if sha(kernel)!=m['kernel_sha256']:raise ValueError('kernel mismatch')
    for name,digest in m['source_sha256'].items():
        if sha((ROOT/name).read_bytes())!=digest:raise ValueError('stale native source: '+name)
    _,va,_,_,_=pack.macho(kernel)
    symbols=[x.split() for x in subprocess.check_output(['llvm-nm',str(a.kernel)],text=True).splitlines()]
    target=[int(x[0],16) for x in symbols if len(x)==3 and x[2]=='_arm_init']
    if len(target)!=1:raise ValueError('one actual arm_init symbol required')
    arm_init=target[0];base=0x40200000 if m['text_offset']==0 else 0x40080000
    has_marker=any(len(x)==3 and x[2]=='_ace_early_bootargs_ready' for x in symbols)
    if has_marker and not re.fullmatch('[0-9a-f]{16}',m.get('run_token','')):raise ValueError('bound run token required')
    out.mkdir(parents=True);(out/'verification.json').write_text('{"status":"incomplete","xnu_hardware_boot":false}\n')
    ring=out/'ring.bin';ring.write_bytes(bytes.fromhex('44424743')+bytes(65532))
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    qcmd=['qemu-system-aarch64','-M','virt,virtualization=off,gic-version=3','-cpu','cortex-a55,cntfrq=13000000','-m','8G','-smp','1','-display','none','-serial','none','-monitor','none','-nic','none','-kernel',str(image/'native.Image'),'-S','-gdb',f'tcp:127.0.0.1:{port}']
    commands=['set pagination off','set confirm off','set tcp connect-timeout 5','set tcp auto-retry on',
        f'target remote 127.0.0.1:{port}',f'hbreak *{base}','continue','delete breakpoints',
        f'restore {a.fdt.resolve()} binary {m["fdt_pa"]}',f'restore {ring} binary 0x48160000',f'set $x0={m["fdt_pa"]}',
        f'hbreak *{base+s["native_halt"]}',f'hbreak *{base+s["native_early_halt"]}',f'hbreak *{arm_init}','continue',
        'printf "ARM_C_ENTRY %lx %lx %lx\\n",$pc,$sp,$x0','stepi 1','printf "ARM_C_AFTER %lx\\n",$pc',
        'maintenance print raw-registers',
        # XNU has enabled its page tables: this PA is no longer a mapped VA.
        # QEMU's documented gdbstub switch changes debugger reads only.
        'maintenance packet Qqemu.PhyMemMode:1','maintenance packet qqemu.PhyMemMode',
        f'dump binary memory {out/"ring-after.bin"} 0x48160000 0x48170000',
        'maintenance packet Qqemu.PhyMemMode:0','detach','quit']
    g=['gdb-multiarch','-nx','-q','-batch']
    for cmd in commands:g+=['-ex',cmd]
    with (out/'qemu.log').open('w') as log:
        q=subprocess.Popen(qcmd,stdout=log,stderr=log,stdin=subprocess.DEVNULL)
        try:
            result=subprocess.run(g,capture_output=True,text=True,timeout=30)
            text=result.stdout+result.stderr;(out/'gdb.log').write_text(text)
            if result.returncode:raise RuntimeError('GDB failed; inspect retained log')
        finally:
            q.terminate()
            try:q.wait(timeout=3)
            except subprocess.TimeoutExpired:q.kill();q.wait(timeout=3)
    entry=re.search(r'ARM_C_ENTRY ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+)',text)
    after=re.search(r'ARM_C_AFTER ([0-9a-f]+)',text)
    assert entry and after,'missing actual C-entry evidence'
    regs=[int(x,16) for x in entry.groups()]
    assert regs[0]==arm_init and int(after.group(1),16)==arm_init+4,regs
    assert regs[2]==va+m['args_pa']-m['ram']['base'],regs
    if has_marker:
        marker=('ACEXNU1:'+m['run_token']+': entry EL1\n').encode()
        captured=(out/'ring-after.bin').read_bytes()
        assert len(captured)==65536 and captured.count(marker)==1,'bound kernel entry marker missing/duplicated'
    def register(name):
        found=re.search(r'^\s*'+re.escape(name)+r'\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+0x([0-9a-f]+)',text,re.M)
        assert found is not None,'missing debugger register '+name
        return int(found.group(1),16)
    tcr=register('TCR_EL1');sctlr=register('SCTLR');ttbr0=register('TTBR0_EL1');ttbr1=register('TTBR1_EL1')
    assert (tcr>>14)&3==2 and (tcr>>30)&3==1 and (tcr>>32)&7==2,hex(tcr)
    assert sctlr&1 and not (ttbr0&0x3fff) and not (ttbr1&0x3fff)
    assert all(m['ram']['base']<=x<m['ram']['base']+m['ram']['size'] for x in [ttbr0,ttbr1])
    report={'status':'PASS QEMU actual XNU C-entry only','kernel_sha256':m['kernel_sha256'],'image_sha256':m['image_sha256'],
        'fdt_sha256':sha(dtb),'arm_init_va':arm_init,'first_c_instruction_executed':True,'entry_registers':regs,
        'tcr_el1':hex(tcr),'sctlr_debugger_alias':hex(sctlr),'ttbr0_el1':hex(ttbr0),'ttbr1_el1':hex(ttbr1),
        'granule_bytes':16384,'qemu_argv':qcmd,'gdb_argv':g,'log_sha256':sha((out/'gdb.log').read_bytes()),
        'token_bound_kernel_marker_checked':has_marker,
        'ring_read_address_space':'QEMU gdbstub physical memory after C-entry step',
        'verifier_sha256':sha(Path(__file__).read_bytes()),'xnu_hardware_boot':False,'ios_deployable':False,
        'limitations':'QEMU13MHz CPU and real-FDT fixture; no physical phone XNU, IRQ/storage/display/touch/iOS userspace boot'}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: actual XNU16K bootstrap and first arm_init instruction in QEMU; NOT phone/iOS boot')
if __name__=='__main__':main()
