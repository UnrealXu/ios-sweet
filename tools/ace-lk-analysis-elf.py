#!/usr/bin/env python3
"""Wrap exact LK bytes in an ANALYSIS-ONLY ELF; never executes or patches LK.

ELF symbols are analyst labels at independently decoded function prologues.
The imposed virtual base is inferred from original static pointer tables, not
an assertion about physical placement. No synthetic BSS size is invented.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]
PIN='9e3f9fd53316fe7d64a5ed70eea5374489f9aed3e33b20511437f21e269e8511'
VBASE=0xffff000050f00000
LABELS={0x5b58:'analyst_command_register',0x5f04:'analyst_fastboot_okay',
        0x5f38:'analyst_fastboot_stop',0x5f50:'analyst_fastboot_dispatcher',
        0x6620:'analyst_fastboot_worker',0x6ea8:'analyst_continue_handler',
        0x8558:'analyst_download_flash_register',0xde78:'analyst_boot_from_storage',
        0xe240:'analyst_notify_boot_linux',0xec9c:'analyst_boot_linux_thread',
        0xecac:'analyst_wait_boot_linux'}


def wrap(data):
    if hashlib.sha256(data).hexdigest()!=PIN:
        raise ValueError('Not the exact previously identified Ace LK component')
    strings=bytearray(b'\0'); symbols=bytearray(24)
    for offset,name in LABELS.items():
        noff=len(strings);strings+=name.encode()+b'\0'
        symbols+=struct.pack('<IBBHQQ',noff,0x12,0,1,VBASE+offset,0)
    shstr=b'\0.image\0.symtab\0.strtab\0.shstrtab\0'
    image_off=4096; sym_off=(image_off+len(data)+7)&~7
    str_off=sym_off+len(symbols);shstr_off=str_off+len(strings)
    shoff=(shstr_off+len(shstr)+7)&~7
    ident=b'\x7fELF\x02\x01\x01'+bytes(9)
    header=ident+struct.pack('<HHIQQQIHHHHHH',2,183,1,VBASE+0x5f50,64,shoff,0,64,56,1,64,5,4)
    phdr=struct.pack('<IIQQQQQQ',1,5,image_off,VBASE,0,len(data),len(data),4096)
    result=bytearray(header+phdr);result+=bytes(image_off-len(result));result+=data
    result+=bytes(sym_off-len(result));result+=symbols;result+=strings;result+=shstr
    result+=bytes(shoff-len(result));result+=bytes(64)
    for sh in [(1,1,6,VBASE,image_off,len(data),0,0,4096,0),
               (8,2,0,0,sym_off,len(symbols),3,1,8,24),
               (16,3,0,0,str_off,len(strings),0,0,1,0),
               (24,3,0,0,shstr_off,len(shstr),0,0,1,0)]:
        result+=struct.pack('<IIQQQQIIQQ',*sh)
    # Header and section payload must preserve the exact parent bytes.
    if result[image_off:image_off+len(data)]!=data:
        raise ValueError('Analysis wrapper changed payload')
    return bytes(result), {'parent_sha256':PIN,'payload_file_offset':image_off,
                          'payload_bytes':len(data),'virtual_base':hex(VBASE),
                          'entry':hex(VBASE+0x5f50),'labels':{hex(k):v for k,v in LABELS.items()},
                          'labels_provenance':'analyst labels at observed GNU-decoded prologues, not original symbols',
                          'virtual_mapping_provenance':'inferred original linker VA; no physical placement claim',
                          'no_synthetic_bss':True,'analysis_only':True,'firmware_deployable':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=ROOT/'research/ace-20261019/images/lk-first-component-arm64.bin')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();out=a.output.resolve()
    if (not out.is_relative_to(ROOT/'research') or a.output.is_symlink() or
            out.exists() or out.with_suffix('.json').exists() or out.with_suffix('.json').is_symlink()):
        p.error('Choose a new analysis output under research/')
    with a.input.open('rb') as source:
        data=source.read(1362784+1)
    if len(data)!=1362784:
        p.error('Unexpected LK component length')
    wrapped,manifest=wrap(data)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(wrapped);out.chmod(0o600)
    manifest['wrapper_sha256']=hashlib.sha256(wrapped).hexdigest()
    manifest['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out.with_suffix('.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
