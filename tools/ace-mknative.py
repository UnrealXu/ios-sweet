#!/usr/bin/env python3
"""Build an UNTESTED native Ace EL1 Image containing the actual XNU payload.

No phone, flash, network or signing operations. Output must be a new directory
inside ignored research/. Entering the Image WOULD copy/jump to XNU after its
checks; building it grants no hardware RAM ownership or deployment approval.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import secrets
import struct
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ace_pack',ROOT/'tools/ace-mkpayload.py')
pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
SOURCES=['ace/native-loader/start.S','ace/native-loader/main.c','ace/native-loader/memory.c',
    'ace/native-loader/refusal_android.c','ace/native-loader/ram_rescue.c','ace/initrd_rescue.c','ace/pstore_rescue.c','ace/fdt_refusal.c','ace/xnu_cpu_capture.S',
    'ace/fdt.c','ace/xnu_fdt.c','ace/xnu_platform.c','ace/xnu_cpu.c','ace/xnu_handoff.c','ace/pstore_ring.c','ace/pstore_seed.c','ace/pstore_trial.c']
HEADERS=['ace/native-loader/ram_rescue.h','ace/initrd_rescue.h','ace/pstore_rescue.h','diagnostics/ace-ramdiag/sha256.h','ace/native-loader/linker.ld','ace/fdt.h','ace/fdt_refusal.h','ace/xnu_fdt.h','ace/xnu_platform.h',
    'ace/xnu_cpu.h','ace/xnu_handoff.h','ace/pstore_ring.h','ace/pstore_seed.h','ace/pstore_trial.h','ace/pstore_handoff.h','tools/ace-mkpayload.py','tools/ace-mknative.py']
CE_SOURCES=['ace/native-loader/sha_ce_core.S','ace/native-loader/sha_ce_guard.S','ace/native-loader/sha_ce_worker.c']
CE_HEADERS=['ace/sha_ce_update.h']
sha=lambda b:hashlib.sha256(b).hexdigest()
REFUSAL_ANDROID_SHA='8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'

def load_pmsg_reseed_snapshot(path,expected,*,pmsg,init_empty_pmsg,auto_readout_after_reset,refusal_android,diagnostic_readout):
    if path is None and expected is None:return None
    if path is None or not isinstance(expected,str) or not re.fullmatch('[0-9a-f]{64}',expected):
        raise ValueError('pmsg reseed requires capture path and exact lowercase expected SHA256')
    if not (pmsg is True and init_empty_pmsg is True and auto_readout_after_reset is True and refusal_android is not None and diagnostic_readout is False):
        raise ValueError('pmsg reseed requires explicit pmsg/init/automatic pinned Android trial, not readout-only')
    path=Path(path).resolve()
    if not path.is_relative_to(ROOT/'research'):
        raise ValueError('pmsg reseed capture must remain archived under private research/')
    snapshot=pack.read(path)
    if len(snapshot)!=65536 or sha(snapshot)!=expected:
        raise ValueError('pmsg reseed capture size/hash mismatch')
    signature,start,used=struct.unpack_from('<III',snapshot)
    if not any(snapshot) or (signature==0x43474244 and used<=65524 and start<=used):
        raise ValueError('pmsg reseed expects a nonzero invalid-header capture, never a valid ring')
    return snapshot

def build(kernel_path,adt_dir,out,expected,fdt_pa,pmsg=False,text_offset=0x80000,run_token=None,
          refusal_android=None,expected_android=None,init_empty_pmsg=False,diagnostic_readout=False,prior_run_token=None,auto_readout_after_reset=False,root_device=None,pmsg_reseed_from_snapshot=None,expected_pmsg_snapshot=None,ram_rescue_generic=None,ram_rescue_policy=None):
    out=Path(out).resolve();kernel_path=Path(kernel_path);adt_dir=Path(adt_dir)
    if not re.fullmatch('[0-9a-f]{64}',expected):raise ValueError('exact lowercase SHA256 required')
    if fdt_pa<0x44000000 or fdt_pa>0x7fe00000 or fdt_pa%8:raise ValueError('reviewed aligned low-DRAM FDT PA required')
    if text_offset not in (0,0x80000):raise ValueError('only reviewed Image text offsets0/0x80000')
    if type(init_empty_pmsg) is not bool or (init_empty_pmsg and not pmsg):
        raise ValueError('empty pmsg initialization requires explicit --pmsg')
    if type(diagnostic_readout) is not bool or (diagnostic_readout and (refusal_android is None or init_empty_pmsg)):
        raise ValueError('diagnostic readout requires Android handoff and forbids pmsg initialization')
    if prior_run_token is not None and (not diagnostic_readout or not isinstance(prior_run_token,str) or not re.fullmatch('[0-9a-f]{16}',prior_run_token)):
        raise ValueError('prior token must be 16 lowercase hex digits in diagnostic readout mode')
    if run_token is not None and (not isinstance(run_token,str) or not re.fullmatch('[0-9a-f]{16}',run_token)):
        raise ValueError('run token must be exactly16 lowercase hexadecimal digits')
    if type(auto_readout_after_reset) is not bool or (auto_readout_after_reset and
            (not pmsg or refusal_android is None or diagnostic_readout)):
        raise ValueError('automatic reset readout requires pmsg and Android handoff, not readout-only mode')
    if root_device is not None and (root_device!='aceufsroot0' or not auto_readout_after_reset or not pmsg):
        raise ValueError('Ace BSD root requires exact aceufsroot0 and automatic pmsg diagnostic recovery')
    rescue=None;rescue_policy=None
    if (ram_rescue_generic is None)!=(ram_rescue_policy is None):
        raise ValueError('RAM rescue requires immutable generic and explicit layout/pins together')
    if ram_rescue_generic is not None:
        if not (pmsg and auto_readout_after_reset and refusal_android is not None) or diagnostic_readout:
            raise ValueError('RAM rescue requires normal automatic/pmsg/pinned Android path')
        rescue=pack.read(ram_rescue_generic)
        rescue_policy=json.loads(Path(ram_rescue_policy).read_text())
        fields={'vendor_bytes','generic_offset','generic_bytes','vendor_sha256','generic_sha256','rescue_sha256','require_bootconfig'}
        if set(rescue_policy)!=fields or rescue_policy['require_bootconfig'] is not True:
            raise ValueError('exact explicit observed initrd policy and required bootconfig')
        for key in ['vendor_bytes','generic_offset','generic_bytes']:
            if type(rescue_policy[key]) is not int or not 0<rescue_policy[key]<=64*1024*1024:
                raise ValueError('bounded nonzero stream geometry required')
        if not (rescue_policy['vendor_bytes']<=rescue_policy['generic_offset']<=rescue_policy['vendor_bytes']+4095 and
                len(rescue)<=rescue_policy['generic_bytes'] and rescue_policy['generic_offset']+rescue_policy['generic_bytes']<=64*1024*1024):
            raise ValueError('stream geometry/replacement range mismatch')
        for key in ['vendor_sha256','generic_sha256','rescue_sha256']:
            if not isinstance(rescue_policy[key],str) or not re.fullmatch('[0-9a-f]{64}',rescue_policy[key]):
                raise ValueError('complete exact stream hashes required')
        if not rescue or sha(rescue)!=rescue_policy['rescue_sha256']:
            raise ValueError('embedded original generic hash mismatch')
    android=None
    if refusal_android is not None or expected_android is not None:
        if refusal_android is None or expected_android!=REFUSAL_ANDROID_SHA or text_offset!=0:
            raise ValueError('refusal fallback requires exact current Android SHA256 and text offset0')
        android=pack.read(refusal_android)
        if (sha(android)!=REFUSAL_ANDROID_SHA or android[56:60]!=b'ARM\x64' or
            struct.unpack_from('<Q',android,8)[0]!=0 or struct.unpack_from('<Q',android,24)[0]!=0xa):
            raise ValueError('refusal Android Image/hash/header mismatch')
    pmsg_reseed=load_pmsg_reseed_snapshot(pmsg_reseed_from_snapshot,expected_pmsg_snapshot,
        pmsg=pmsg,init_empty_pmsg=init_empty_pmsg,auto_readout_after_reset=auto_readout_after_reset,
        refusal_android=android,diagnostic_readout=diagnostic_readout)
    if not out.is_relative_to(ROOT/'research') or out.exists():raise ValueError('new ignored research/ directory required')
    if subprocess.run(['git','-C',str(ROOT),'check-ignore','--quiet','--',str(out.relative_to(ROOT))]).returncode:
        raise ValueError('output is not ignored')
    kernel=pack.read(kernel_path)
    if sha(kernel)!=expected:raise ValueError('kernel SHA256 mismatch')
    tree=pack.read(adt_dir/'ace.adt');metadata=json.loads((adt_dir/'manifest.json').read_text())
    if root_device is not None and metadata.get('ufs_root_discovery_probe') is not True:
        raise ValueError('Ace BSD root requires validated UFS root discovery ADT profile')
    run_token=run_token or secrets.token_hex(8)
    # BootArgs video is intentionally zero until a real framebuffer is reviewed.
    # XNU's OSX progress drawing otherwise asserts in pe_init.c on height0.
    command_line='debug=0xc serial=3 cpus=1 keepsyms=1 -noprogress'+(' ace_pmsg=1 ace_run='+run_token if pmsg else '')
    if root_device is not None: command_line+=' rd='+root_device
    payload,report=pack.build(kernel,tree,metadata,command_line)
    out.mkdir(parents=True) # exclusive final directory, validated inputs first
    (out/'status.json').write_text('{"status":"incomplete","ios_deployable":false}\n')
    (out/'ace.payload').write_bytes(payload)
    # Shipping LK reserves mb_kernel [0x40000000,0x47c80000) before decompression;
    # the optional larger image stays below0x45000000 and the pinned FDT. These
    # numeric guards do not establish firmware/DMA ownership on the phone.
    image_limit=0x45000000 if android is not None else 0x44000000
    config=('#define NATIVE_RAM_RESCUE '+str(int(rescue is not None))+'\n'
        '#define NATIVE_RAM_BASE '+hex(report['requested_ram']['base'])+'ULL\n'
        '#define NATIVE_RAM_BYTES '+hex(report['requested_ram']['size'])+'ULL\n'
        '#define NATIVE_FDT_PA '+hex(fdt_pa)+'\n#define NATIVE_TEXT_OFFSET '+hex(text_offset)+'\n'
        '#define NATIVE_PMSG '+str(int(pmsg))+'\n'
        '#define NATIVE_INIT_EMPTY_PMSG '+str(int(init_empty_pmsg))+'\n'
        '#define NATIVE_PMSG_RESEED_CAPTURE '+str(int(pmsg_reseed is not None))+'\n'
        '#define NATIVE_DIAGNOSTIC_READOUT '+str(int(diagnostic_readout))+'\n'
        '#define NATIVE_AUTO_READOUT '+str(int(auto_readout_after_reset))+'\n'
        '#define NATIVE_PRIOR_RUN_TOKEN "'+(prior_run_token or '')+'"\n'
        '#define NATIVE_IMAGE_LIMIT '+hex(image_limit)+'\n'
        '#define NATIVE_REFUSAL_ANDROID '+str(int(android is not None))+'\n'
        '#define NATIVE_RUN_TOKEN "'+run_token+'"\n')
    if rescue is not None:
        def digest_bytes(key):return '{'+','.join('0x'+rescue_policy[key][i:i+2] for i in range(0,64,2))+'}'
        config+='#ifdef ACE_INITRD_RESCUE_H\nstatic const struct ace_initrd_rescue_policy native_rescue_policy = {'+','.join(str(rescue_policy[k]) for k in ['vendor_bytes','generic_offset','generic_bytes'])+','+','.join(digest_bytes(k) for k in ['vendor_sha256','generic_sha256','rescue_sha256'])+',1};\n#endif\n'
    (out/'native_config.h').write_text(config)
    assembly='.file "ace-native-bundle.S"\n.section .rodata.bundle,"a"\n.balign 8\n.global bundle_start,bundle_end\nbundle_start:\n.incbin "ace.payload"\nbundle_end:\n'
    if android is not None:
        (out/'android.Image').write_bytes(android)
        assembly+='.section .rodata.android,"a"\n.balign 0x200000\n.global android_payload,android_payload_end\nandroid_payload:\n.incbin "android.Image"\nandroid_payload_end:\n'
    if pmsg_reseed is not None:
        (out/'pmsg-reseed.snapshot').write_bytes(pmsg_reseed)
        assembly+='.section .rodata.pmsg_reseed,"a"\n.balign 8\n.global pmsg_reseed_snapshot,pmsg_reseed_snapshot_end\npmsg_reseed_snapshot:\n.incbin "pmsg-reseed.snapshot"\npmsg_reseed_snapshot_end:\n'
    if rescue is not None:
        (out/'ram-rescue.lz4').write_bytes(rescue)
        assembly+='.section .rodata.rescue,"a"\n.balign 8\n.global ram_rescue_start,ram_rescue_end\nram_rescue_start:\n.incbin "ram-rescue.lz4"\nram_rescue_end:\n'
    (out/'bundle.S').write_text(assembly+'.section .note.GNU-stack,"",%progbits\n')
    commands=[]
    def run(command,name):
        commands.append(command)
        with (out/name).open('w') as log:subprocess.run(command,cwd=out,check=True,stdout=log,stderr=log,timeout=60)
    flags=['aarch64-linux-gnu-gcc','-std=c11','-mcpu=cortex-a55','-O2','-ffreestanding',
        '-fno-builtin','-fno-stack-protector','-fno-pie','-fno-pic','-mgeneral-regs-only',
        '-mstrict-align','-fno-asynchronous-unwind-tables','-fstack-usage','-Wall','-Wextra','-Werror','-I',str(out)]
    sources=SOURCES+(CE_SOURCES if rescue is not None else [])
    headers=HEADERS+(CE_HEADERS if rescue is not None else [])
    objects=[]
    for i,path in enumerate([*[ROOT/x for x in sources],out/'bundle.S']):
        obj=out/f'{i}.o';profile_flags=['-DACE_INITRD_NATIVE_CE=1'] if rescue is not None and path==ROOT/'ace/initrd_rescue.c' else []
        run(flags+profile_flags+['-c',str(path),'-o',str(obj)],f'{i}-compile.log');objects.append(str(obj))
    relocations=subprocess.check_output(['aarch64-linux-gnu-readelf','-Wr',*objects],text=True)
    (out/'relocations.txt').write_text(relocations)
    if re.search(r'R_AARCH64_(?:ABS(?:64|32|16)|MOVW_[US]ABS|GLOB_DAT|JUMP_SLOT)',relocations):
        raise ValueError('absolute image pointers require an actual relocation implementation')
    run(['aarch64-linux-gnu-ld','-T',str(ROOT/'ace/native-loader/linker.ld'),*objects,'-o',str(out/'native.elf')],'link.log')
    undefined=subprocess.check_output(['aarch64-linux-gnu-nm','-u',str(out/'native.elf')],text=True)
    if undefined.strip():raise ValueError('undefined runtime imports')
    run(['aarch64-linux-gnu-objcopy','-O','binary',str(out/'native.elf'),str(out/'native.Image')],'copy.log')
    symbols={a[2]:int(a[0],16) for line in subprocess.check_output(['aarch64-linux-gnu-nm','-n',str(out/'native.elf')],text=True).splitlines() if len(a:=line.split())==3}
    if symbols['_start']!=0 or symbols['image_end']>image_limit-0x40200000:raise ValueError('Image cannot fit reviewed low boot-program RAM')
    with (out/'native.Image').open('ab') as f:f.truncate(symbols['image_end'])
    (out/'symbols.json').write_text(json.dumps(symbols,indent=2)+'\n')
    (out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
    manifest={'status':'UNTESTED native EL1 Image','kernel_sha256':expected,'adt_sha256':sha(tree),
        'payload_sha256':sha(payload),'image_sha256':sha((out/'native.Image').read_bytes()),
        'image_bytes':symbols['image_end'],'entry':'EL1 only, masked DAIF, M/C/I/EE off',
        'image_load_window':[0x40000000,image_limit],'fdt_pa':fdt_pa,'text_offset':text_offset,
        'ram':report['requested_ram'],'entry_pa':report['entry_pa'],'args_pa':report['args_pa'],
        'adt_pa':report['adt_pa'],'auto_readout_after_reset':auto_readout_after_reset,'pmsg_enabled':pmsg,'run_token':run_token,'command_line':command_line,
        'pmsg_contract':'exclusive ordinary RAM, ECC0, valid DBGC; not inferred from header',
        'initialize_empty_pmsg':init_empty_pmsg,
        'pmsg_seed_failure_snapshot':bool(pmsg and init_empty_pmsg and not diagnostic_readout and android is not None),
        'diagnostic_readout_only':diagnostic_readout,
        'ram_rescue':{'enabled':rescue is not None,'sha_backend':'ce-guarded-aligned64-staging-scalar-fallback-v1' if rescue is not None else 'scalar','ce_cpu_trace':'phase-F-R-once-current-token-observed-sysregs-v1' if rescue is not None else None,'ce_permission_physical_verified':False,'policy':rescue_policy,'validation_budget_seconds':120 if rescue is not None else None,'validation_budget_ticks':1560000000 if rescue is not None else None,'sha_input_blocks':'direct64-with-tail-buffer-v1' if rescue is not None else None,'failure_trace_progress':'stream-completed-total-v1' if rescue is not None else None,'independent_of_userdata':False,'halt_diagnostic_version':2 if rescue is not None else 1,'fallback_guard_halt_stage':9 if rescue is not None else None,'halt_slot_groups':10 if rescue is not None else 9,'failure_trace':'current-token-once-no-eviction-v1' if rescue is not None else None},
        'root_device':root_device,'root_device_readonly':root_device is not None,
        'prior_run_token':prior_run_token,
        'pmsg_seed_contract':'explicit exclusive ECC0/type0 caller-owned RAM; initialize only entirely zero 64KiB, preserve valid, refuse nonzero corrupt',
        'kernel_provenance':'caller-supplied expected SHA256; verify CI/source evidence independently',
        'hardware_ram_ownership_verified':False,'xnu_hardware_boot':False,'ios_deployable':False,
        'source_sha256':{x:sha((ROOT/x).read_bytes()) for x in sources+headers}}
    if pmsg_reseed is not None:
        manifest['pmsg_reseed_from_snapshot']={
            'enabled':True,'capture_sha256':sha(pmsg_reseed),'capture_bytes':len(pmsg_reseed),
            'archived_capture_path':str(Path(pmsg_reseed_from_snapshot).resolve()),
            'scope':'only full runtime zone match after ordinary seed rejects invalid nonzero content; explicit caller-owned RAM lifecycle',
            'seed_result':2,'record_word':31,'does_not_prove_xnu_success':True}
    manifest['refusal_android']={'enabled':android is not None,'sha256':sha(android) if android is not None else None,
        'bytes':len(android) if android is not None else 0,'property':'/chosen/ace,native-refusal',
        'scope':'normal native_main refusal only; never early-entry/exception/XNU return; no boot partition restoration'}
    (out/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'status.json').write_text(json.dumps({'status':'built UNTESTED native Image','ios_deployable':False})+'\n')
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('kernel',type=Path);p.add_argument('adt_directory',type=Path);p.add_argument('output_directory',type=Path)
    p.add_argument('--expected-kernel-sha256',required=True);p.add_argument('--fdt-pa',required=True,type=lambda x:int(x,0))
    p.add_argument('--pmsg',action='store_true');p.add_argument('--text-offset',default=0x80000,type=lambda x:int(x,0))
    p.add_argument('--init-empty-pmsg',action='store_true',help='explicitly initialize wholly zero pmsg RAM only; requires --pmsg')
    p.add_argument('--auto-readout-after-reset',action='store_true',help='one token-bound XNU attempt; retained pending marker routes next reset to diagnostic Android')
    p.add_argument('--diagnostic-readout',action='store_true',help='intentional stage2/error-66 -> Android for prior-trial evidence; never attempts XNU')
    p.add_argument('--prior-run-token',help='prior physical trial token to search in preserved pmsg; readout only')
    p.add_argument('--run-token',help='16 lowercase hex digits; default generates a fresh build token')
    p.add_argument('--refusal-android-image',type=Path,help='optional hash-pinned current Android Image for normal-refusal diagnostics')
    p.add_argument('--expected-android-sha256',help='exact current Android SHA256; requires --text-offset0')
    p.add_argument('--ram-rescue-generic',type=Path,help='explicit immutable original generic rescue, not diskless proof')
    p.add_argument('--ram-rescue-policy',type=Path,help='observed actual firmware initrd stream geometry and full hashes')
    p.add_argument('--root-device',choices=['aceufsroot0'],help='explicit readonly BSD userdata root; requires root-discovery ADT and automatic pmsg recovery')
    p.add_argument('--pmsg-reseed-from-snapshot',type=Path,help='explicit exact-match reseed from an archived private full64KiB snapshot; requires pmsg/init/auto/pinned Android')
    p.add_argument('--expected-pmsg-snapshot-sha256',help='exact lowercase SHA256 of the archived reseed snapshot')
    a=p.parse_args()
    try:
        m=build(a.kernel,a.adt_directory,a.output_directory,a.expected_kernel_sha256,a.fdt_pa,a.pmsg,a.text_offset,a.run_token,
            a.refusal_android_image,a.expected_android_sha256,a.init_empty_pmsg,a.diagnostic_readout,a.prior_run_token,a.auto_readout_after_reset,a.root_device,a.pmsg_reseed_from_snapshot,a.expected_pmsg_snapshot_sha256,a.ram_rescue_generic,a.ram_rescue_policy)
        print(f'UNTESTED native Image: {m["image_bytes"]}bytes SHA256 {m["image_sha256"]}; no phone operation')
        return 0
    except (ValueError,OSError,subprocess.SubprocessError) as error:print('native Image refused: '+str(error),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
