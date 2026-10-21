#!/usr/bin/env python3
"""Execute the patch's stackless XNU entry marker in QEMU ordinary RAM only.

No phone commands, partition operations or hardware/iOS success claim.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import socket
import struct
import subprocess

if not __debug__:raise RuntimeError('optimized verification refused')
ROOT=Path(__file__).resolve().parents[2]
TOKEN='0123456789abcdef'
MARKER=('ACEXNU1:'+TOKEN+': entry EL1\n').encode()

def verify(out):
    out=out.resolve()
    if out.exists() or not out.is_relative_to(ROOT/'research') or not re.fullmatch(r'[A-Za-z0-9_./+-]+',str(out)):
        raise ValueError('new restricted ignored research/ output required')
    patch=(ROOT/'xnu/patches/0087-ace-earliest-entry-marker.patch').read_text()
    added=patch.split('+++ b/osfmk/arm64/ace_early_entry.h\n',1)[1]
    header=''.join(line[1:] for line in added.splitlines(True) if line.startswith('+'))
    out.mkdir(parents=True)
    (out/'header.h').write_text(header)
    source='''#define ARM64_BOARD_CONFIG_ACE 1
#define BA_REVISION 0
#define BA_COMMAND_LINE 108
#define BA_COMMAND_LINE_BYTES 608
#define BA_SIZE 736
#define BA_PHYS_BASE 16
#define BA_MEM_SIZE 24
#define EXT(x) x
#define LEXT(x) x:
.text
.global _start,run,stop
_start:
 b run
 .space 52
 .word 0x644d5241,0
run:
#include "header.h"
stop:
 b stop
'''
    (out/'fixture.S').write_text(source)
    subprocess.run(['aarch64-linux-gnu-gcc','-c','-mcpu=cortex-a55',str(out/'fixture.S'),'-o',str(out/'fixture.o')],check=True,capture_output=True)
    subprocess.run(['aarch64-linux-gnu-ld','-Ttext=0x40080000',str(out/'fixture.o'),'-o',str(out/'fixture.elf')],check=True,capture_output=True)
    subprocess.run(['aarch64-linux-gnu-objcopy','-O','binary',str(out/'fixture.elf'),str(out/'fixture.Image')],check=True,capture_output=True)
    syms={x[2]:int(x[0],16) for line in subprocess.check_output(['aarch64-linux-gnu-nm',str(out/'fixture.elf')],text=True).splitlines() if len(x:=line.split())==3}
    args_pa=0x140100000;capacity=65524
    valid='debug=0xc ace_pmsg=1 ace_run='+TOKEN
    cases=[('empty',valid,True,0,0),('partial',valid,True,10,10),('wrap',valid,True,capacity-4,capacity),
        ('reverse-options','ace_run='+TOKEN+' ace_pmsg=1',True,0,0),
        ('missing-optin','ace_run='+TOKEN,False,0,0),('missing-token','ace_pmsg=1',False,0,0),
        ('optin-substring','xace_pmsg=1 ace_run='+TOKEN,False,0,0),
        ('optin-suffix',valid.replace('ace_pmsg=1','ace_pmsg=10'),False,0,0),
        ('conflict',valid+' ace_pmsg=0',False,0,0),('duplicate-token',valid+' ace_run='+TOKEN,False,0,0),
        ('uppercase',valid.replace(TOKEN,TOKEN.upper()),False,0,0),('short',valid[:-1],False,0,0),
        ('unterminated','x'*608,False,0,0),('bad-header',valid,False,0,0),
        ('bad-cursor',valid,False,capacity,capacity),('noncanonical',valid,False,5,10),
        ('bad-revision',valid,False,0,0),('overlap',valid,False,0,0),('overflow',valid,False,0,0)]
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    qcmd=['qemu-system-aarch64','-M','virt,virtualization=off','-cpu','cortex-a55,cntfrq=13000000','-m','8G','-smp','1','-display','none','-serial','none','-monitor','none','-nic','none','-kernel',str(out/'fixture.Image'),'-S','-gdb',f'tcp:127.0.0.1:{port}']
    commands=['set pagination off','set confirm off','set tcp connect-timeout 5','set tcp auto-retry on',f'target remote 127.0.0.1:{port}',f'hbreak *{syms["stop"]}']
    for name,cmd,success,cursor,size in cases:
        folder=out/name;folder.mkdir();args=bytearray(736)
        struct.pack_into('<HH',args,0,1 if name=='bad-revision' else 2,2)
        bank,length=(0x40000000,0x100000000) if name=='overlap' else ((1<<64)-0x1000,0x2000) if name=='overflow' else (0x140000000,0xc0000000)
        struct.pack_into('<QQ',args,16,bank,length);args[108:108+len(cmd)]=cmd.encode()
        ring=struct.pack('<III',0 if name=='bad-header' else 0x43474244,cursor,size)+b'\xa5'*capacity
        (folder/'args.bin').write_bytes(args);(folder/'initial.bin').write_bytes(ring)
        commands += [f'restore {folder/"args.bin"} binary {args_pa}',f'restore {folder/"initial.bin"} binary 0x48160000',f'set $x0={args_pa}',f'set $pc={syms["run"]}']
        for reg in [*range(17,31)]:commands += [f'set $x{reg}={0x12340000+reg}']
        commands += ['continue',f'printf "REG {name} %lx %lx %lx %lx %lx\\n",$pc,$x0,$x17,$x20,$x30',f'dump binary memory {folder/"result.bin"} 0x48160000 0x48170000',f'dump binary memory {folder/"args-after.bin"} {args_pa} {args_pa+736}']
    commands+=['detach','quit'];g=['gdb-multiarch','-nx','-q','-batch']
    for c in commands:g+=['-ex',c]
    with (out/'qemu.log').open('w') as log:
        q=subprocess.Popen(qcmd,stdin=subprocess.DEVNULL,stdout=log,stderr=log)
        try:
            r=subprocess.run(g,capture_output=True,text=True,timeout=45);(out/'gdb.log').write_text(r.stdout+r.stderr)
            if r.returncode:raise RuntimeError('GDB failed: inspect retained logs')
        finally:
            q.terminate()
            try:q.wait(timeout=3)
            except subprocess.TimeoutExpired:q.kill();q.wait(timeout=3)
    for name,cmd,success,cursor,size in cases:
        folder=out/name;before=(folder/'initial.bin').read_bytes();expected=bytearray(before)
        if success:
            for i,byte in enumerate(MARKER):expected[12+(cursor+i)%capacity]=byte
            struct.pack_into('<II',expected,4,(cursor+len(MARKER))%capacity,min(capacity,size+len(MARKER)))
        assert (folder/'result.bin').read_bytes()==expected,name+' ring mismatch'
        assert (folder/'args-after.bin').read_bytes()==(folder/'args.bin').read_bytes(),name+' BootArgs modified'
        match=re.search(r'REG '+name+r' ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+)',r.stdout)
        assert match and [int(x,16) for x in match.groups()]==[syms['stop'],args_pa,0x12340011,0x12340014,0x1234001e],name+' preserved registers/PC'
    report={'status':'PASS QEMU entry-marker RAM fixtures','cases':len(cases),'patch_sha256':hashlib.sha256(patch.encode()).hexdigest(),'header_sha256':hashlib.sha256(header.encode()).hexdigest(),'qemu_argv':qcmd,'gdb_argv':g,'phone_xnu_boot':False,'ios_deployable':False}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output_directory',type=Path);a=p.parse_args()
    r=verify(a.output_directory);print('PASS:',r['cases'],'QEMU entry-marker cases; no phone execution')
