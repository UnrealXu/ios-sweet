#!/usr/bin/env python3
"""Host-only stock-kernel forwarding prefix; no transport or deploy operation."""
import hashlib
import json
from pathlib import Path
import secrets
import shutil
import struct
import subprocess
ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'ace/stock-chain'
OUT=ROOT/'research/ace-stock-chain-20261019'
STOCK=ROOT/'research/ace-stock-qemu-20261019/Image'
STOCK_SHA='8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if not __debug__:raise RuntimeError('Optimized build validation refused')
    if sha(STOCK)!=STOCK_SHA:raise ValueError('Exact current stock kernel Image changed')
    b=STOCK.read_bytes()
    if struct.unpack_from('<Q',b,8)[0]!=0 or struct.unpack_from('<Q',b,24)[0]!=0xa:raise ValueError('Stock header assumption changed')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'verification.json').write_text('{"status":"incomplete","reason":"build requested"}\n')
    shutil.copyfile(STOCK,OUT/'stock.Image')
    token=secrets.token_hex(12)
    commands={};images={}
    for mode,address in [('plain',None),('pmsg',0x48160000),('alias-test',0x41000000)]:
        flags=[] if address is None else ['-DCHAIN_PMSG=1',f'-DACE_ENTRY_PMSG_ADDRESS={address}', '-DACE_ENTRY_PMSG_BYTES=65536',f'-DCHAIN_TOKEN="{token}"']
        argv=[['aarch64-linux-gnu-gcc','-c','-I',str(OUT),*flags,str(HERE/'start.S'),'-o',str(OUT/(mode+'.o'))],
              ['aarch64-linux-gnu-ld','-T',str(HERE/'linker.ld'),str(OUT/(mode+'.o')),'-o',str(OUT/(mode+'.elf'))],
              ['aarch64-linux-gnu-objcopy','-O','binary',str(OUT/(mode+'.elf')),str(OUT/(mode+'.Image'))]]
        for i,cmd in enumerate(argv):
            with (OUT/f'{mode}-{i}-build.log').open('w') as log:subprocess.run(cmd,cwd=OUT,check=True,stdout=log,stderr=log,timeout=30)
        image=(OUT/(mode+'.Image')).read_bytes()
        assert image[0x200000:0x200000+len(b)]==b and not any(image[0x200000+len(b):])
        assert struct.unpack_from('<Q',image,8)[0]==0 and struct.unpack_from('<Q',image,16)[0]==len(image)
        images[mode]=dict(sha256=sha(OUT/(mode+'.Image')),bytes=len(image),pmsg_address=address)
        commands[mode]=argv
    report=dict(scope='Diagnostic stock-kernel forwarder only; not XNU/iOS; no hardware deployment',token=token,stock_sha256=STOCK_SHA,stock_bytes=len(b),stock_offset=0x200000,images=images,commands=commands,
                sources={str(p.relative_to(ROOT)):sha(p) for p in [HERE/'start.S',HERE/'linker.ld',HERE/'build.py',ROOT/'ace/entry/pmsg.S']},ios_deployable=False,hardware_tested=False)
    (OUT/'build.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Built three diagnostic variants; original kernel byte identity PASS; no device operation')

if __name__=='__main__':main()
