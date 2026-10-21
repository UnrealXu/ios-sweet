#!/usr/bin/env python3
"""Execute the real C loader in QEMU; receiver is synthetic, not XNU/iOS."""
import hashlib
import json
from pathlib import Path
import socket
import struct
import subprocess

if not __debug__: raise RuntimeError('Optimized verification is refused')
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'ace/xnu-loader'
OUT=ROOT/'research/ace-xnu-handoff-20261019'
RAM=0x41000000
MEM=0x40000
VA=0xffffff0000000000


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run_cmd(argv,log):
    with log.open('w') as f:
        subprocess.run(argv,check=True,stdout=f,stderr=f,timeout=30)

def symbols(path):
    return {line.split()[2]:int(line.split()[0],16) for line in subprocess.check_output(['aarch64-linux-gnu-nm','-n',str(path)],text=True).splitlines() if len(line.split())==3}

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'verification.json').write_text('{"status":"incomplete"}\n')
    flags=['aarch64-linux-gnu-gcc','-O2','-ffreestanding','-fno-builtin','-fno-pic','-fno-stack-protector','-mgeneral-regs-only','-mstrict-align','-Wall','-Wextra','-Werror']
    run_cmd(flags+['-c',str(HERE/'payload.S'),'-o',str(OUT/'receiver.o')],OUT/'receiver-build.log')
    run_cmd(['aarch64-linux-gnu-ld','-Ttext=0','-e','payload_entry',str(OUT/'receiver.o'),'-o',str(OUT/'receiver.elf')],OUT/'receiver-link.log')
    run_cmd(['aarch64-linux-gnu-objcopy','-O','binary',str(OUT/'receiver.elf'),str(OUT/'receiver.bin')],OUT/'receiver-copy.log')
    data=(OUT/'receiver.bin').read_bytes()
    adt=struct.pack('<II32sI',1,0,b'name',12)+b'device-tree\0'
    off=744
    extra=(off+len(data)+7)&~7
    dto=extra+16
    bundle=bytearray(dto+len(adt))
    struct.pack_into('<8sII7Q',bundle,0,b'ACEXNU01',1,2,VA,VA,dto,len(adt),VA+0x8000,RAM,MEM)
    bundle[72:75]=b'-v\0'
    struct.pack_into('<4Q',bundle,680,VA,len(data)+19,off,len(data))
    struct.pack_into('<4Q',bundle,712,VA+0x4000,32,extra,13)
    bundle[off:off+len(data)]=data
    bundle[extra:extra+13]=b'tail-13-bytes'
    bundle[dto:]=adt
    variants={}
    for name in ['normal','bad-entry','overlap']:
        folder=OUT/name;folder.mkdir(exist_ok=True)
        b=bytearray(bundle)
        if name=='bad-entry':struct.pack_into('<Q',b,24,VA+len(data)+4)
        if name=='overlap':struct.pack_into('<Q',b,712,VA+16)
        (folder/'payload.bin').write_bytes(b)
        (folder/'bundle.S').write_text('.section .rodata,"a"\n.balign 8\n.global bundle_start,bundle_end\nbundle_start:\n.incbin "'+str(folder/'payload.bin')+'"\nbundle_end:\n.section .note.GNU-stack,"",%progbits\n')
        objects=[];commands=[]
        for i,src in enumerate([HERE/'start.S',HERE/'main.c',ROOT/'ace/xnu_handoff.c',folder/'bundle.S']):
            obj=folder/f'{i}.o';command=flags+['-c',str(src),'-o',str(obj)]
            run_cmd(command,folder/f'{i}-compile.log');objects.append(str(obj));commands.append(command)
        command=['aarch64-linux-gnu-ld','-T',str(HERE/'linker.ld'),*objects,'-o',str(folder/'loader.elf')]
        run_cmd(command,folder/'link.log');commands.append(command)
        command=['aarch64-linux-gnu-objcopy','-O','binary',str(folder/'loader.elf'),str(folder/'loader.Image')]
        run_cmd(command,folder/'copy.log');commands.append(command)
        n=symbols(folder/'loader.elf')['image_end']
        with (folder/'loader.Image').open('ab') as f:f.truncate(n)
        (folder/'build-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        variants[name]=folder
    return variants,bundle,data,adt,extra,dto


def execute(name,folder,virt,receiver_symbols,base=0x40080000):
    syms=symbols(folder/'loader.elf')
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    record=OUT/(name+'-record.bin');ram=OUT/(name+'-ram.bin')
    for p in [record,ram]:p.unlink(missing_ok=True)
    qlog=OUT/(name+'-qemu.log');glog=OUT/(name+'-gdb.log')
    command=['qemu-system-aarch64','-M','virt,virtualization='+virt,'-cpu','cortex-a76','-m','128M','-smp','1','-display','none','-serial','none','-monitor','none','-nic','none','-kernel',str(folder/'loader.Image'),'-S','-gdb',f'tcp:127.0.0.1:{port}']
    with qlog.open('w') as log:
        q=subprocess.Popen(command,stdout=log,stderr=log,stdin=subprocess.DEVNULL)
        try:
            cmds=['set pagination off','set confirm off','set tcp connect-timeout 5','set tcp auto-retry on',f'target remote 127.0.0.1:{port}']
            if base!=0x40080000:
                cmds+=['hbreak *0x40080000','continue','delete breakpoints',f'restore {folder/"loader.Image"} binary {base}',f'set $pc={base}']
            cmds += [f'hbreak *{base+syms["harness_halt"]}']
            if folder.name=='normal':cmds += [f'hbreak *{RAM+receiver_symbols["payload_halt"]}']
            cmds += ['continue',f'dump binary memory {record} {base+syms["harness_record"]} {base+syms["harness_record"]+32}',f'dump binary memory {ram} {RAM} {RAM+MEM}','info registers pc cpsr','detach','quit']
            g=['gdb-multiarch','-nx','-q','-batch']
            for c in cmds:g+=['-ex',c]
            r=subprocess.run(g,capture_output=True,text=True,timeout=20)
            glog.write_text(r.stdout+r.stderr)
            if r.returncode:raise RuntimeError(r.stdout+r.stderr)
        finally:
            q.terminate()
            try:q.wait(timeout=3)
            except subprocess.TimeoutExpired:q.kill();q.wait(timeout=3)
    words=struct.unpack('<4Q',record.read_bytes())
    assert words[0] in [1,2],words
    return dict(case=name,record=list(words),qemu_argv=command,gdb_argv=g,ram=ram.name)


def main():
    variants,bundle,data,adt,extra,dto=build()
    receiver_symbols=symbols(OUT/'receiver.elf')
    cases=[execute('el1',variants['normal'],'off',receiver_symbols),
           execute('el2',variants['normal'],'on',receiver_symbols),
           execute('relocated-el2',variants['normal'],'on',receiver_symbols,0x40200000),
           execute('bad-entry',variants['bad-entry'],'on',receiver_symbols),
           execute('overlap',variants['overlap'],'off',receiver_symbols)]
    for case in cases:
        ram=(OUT/case['ram']).read_bytes()
        if case['case'] in ['bad-entry','overlap']:
            assert case['record']==[2,2**64-(5 if case['case']=='bad-entry' else 4),0,0],case
            assert ram==b'\xa5'*MEM, 'Invalid payload modified target RAM'
        else:
            assert case['record']==[1,0,RAM,RAM+0xc000],case
            received=struct.unpack_from('<8Q',ram,receiver_symbols['payload_record'])
            assert received[:5]==(RAM+0xc000,0,0,0,4),received
            assert received[5]&5==0 and received[6:]==(VA+0x8000,RAM+0x10000),received
            expected=bytearray(b'\xa5'*MEM)
            expected[:len(data)]=data;expected[len(data):len(data)+19]=bytes(19)
            expected[0x4000:0x4020]=b'tail-13-bytes'+bytes(19)
            expected[0x8000:0x8000+len(adt)]=adt
            args=bytearray(16384)
            struct.pack_into('<HH4x4Q',args,0,2,2,VA,RAM,MEM,RAM+0x10000)
            struct.pack_into('<QI',args,96,VA+0x8000,len(adt))
            args[108:111]=b'-v\0';struct.pack_into('<Q',args,728,MEM)
            expected[0xc000:0x10000]=args
            at=receiver_symbols['payload_record']
            expected[at:at+64]=struct.pack('<8Q',*received)
            assert ram==expected, 'Whole-RAM comparison failed'
            case['receiver_record']=list(received)
        case['passed']=True
    paths=[p for p in OUT.rglob('*') if p.is_file() and p.name!='verification.json']
    source_paths=[ROOT/'ace/xnu_handoff.c',ROOT/'ace/xnu_handoff.h',*[p for p in HERE.iterdir() if p.is_file()]]
    result=dict(status='pass',scope='QEMU real C loader and synthetic entry receiver; NOT XNU, Ace or iOS execution',cases=cases,
                sources={str(p.relative_to(ROOT)):sha(p) for p in source_paths},
                artifacts_sha256={str(p.relative_to(OUT)):sha(p) for p in paths},ios_deployable=False,hardware_tested=False)
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 3 actual loader/jump cases; 2 refusal cases; whole target RAM compared in all5')

if __name__=='__main__':main()
