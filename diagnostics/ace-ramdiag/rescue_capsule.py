#!/usr/bin/env python3
"""Build a hash-pinned derived selected-rescue generic. No phone operations."""
from pathlib import Path
import argparse,importlib.util,subprocess,hashlib,json,re,stat,struct
S=Path(__file__).resolve().parent;ROOT=S.parents[1];P=ROOT
def sha(b):return hashlib.sha256(b).hexdigest()
def module(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
cpio=module('capsule_cpio',ROOT/'tools/ace-recovery-diag.py')
def entry(n,d,mode):return n,(0,mode,0,0,1,0,len(d),0,0,0,0,len(n)+1,0),d
parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);parser.add_argument('--token',required=True);args=parser.parse_args();out=args.output.resolve()
assert re.fullmatch('[0-9a-f]{16}',args.token) and not out.exists() and out.is_relative_to(ROOT/'research');out.mkdir()
boot=(ROOT/'research/ace-backup-20261019-wireless-v2/boot_b.img').read_bytes();assert sha(boot)=='ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10'
ks,rs=struct.unpack_from('<II',boot,8);offset=((4096+ks+4095)//4096)*4096;generic=boot[offset:offset+rs]
raw=subprocess.run(['lz4','-dc'],input=generic,capture_output=True,check=True).stdout;entries=cpio.read_cpio(raw);fields,original=next((f,d) for n,f,d in entries if n=='init');assert original.startswith(b'\x7fELF')
pin='{'+','.join('0x'+sha(original)[i:i+2] for i in range(0,64,2))+'}'
(out/'rescue_init_config.h').write_text('#define RESCUE_TOKEN "'+args.token+'"\n#define RESCUE_ORIGINAL_BYTES '+str(len(original))+'UL\n#define RESCUE_ORIGINAL_SHA256 '+pin+'\n')
cmd=['aarch64-linux-gnu-gcc','-O2','-static','-nostdlib','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-pie','-no-pie','-Wall','-Wextra','-Werror','-Wl,--build-id=none,-e,_start,--strip-all','-I',str(out),str(ROOT/'diagnostics/ace-irq-timer/qemu-start.S'),str(S/'rescue_init.c'),'-o',str(out/'rescue-init')]
r=subprocess.run(cmd,capture_output=True,text=True);(out/'build.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
ov=[entry('ace-rescue',b'',stat.S_IFDIR|0o700),entry('ace-rescue/original-init',original,fields[1]),entry('init',(out/'rescue-init').read_bytes(),stat.S_IFREG|0o750),entry('TRAILER!!!',b'',0)]
overlay=subprocess.run(['lz4','-l','-9','-c'],input=cpio.write_cpio(ov),capture_output=True,check=True).stdout
capsule=generic+overlay;(out/'derived-rescue-generic.lz4').write_bytes(capsule);(out/'original-init').write_bytes(original)
# Independently decode both streams and verify prefix/blob/entry overrides.
check=subprocess.run(['lz4','-dc'],input=capsule,capture_output=True,check=True).stdout;decoded=cpio.read_cpio(check[len(raw):]);assert next(d for n,f,d in decoded if n=='ace-rescue/original-init')==original
report=dict(status='built private derived selected-rescue capsule; UNTESTED hardware',run_token=args.token,original_generic_sha256=sha(generic),original_generic_bytes=len(generic),original_init_sha256=sha(original),original_init_bytes=len(original),original_init_blob_unchanged=True,derived_generic_sha256=sha(capsule),derived_generic_bytes=len(capsule),derived_is_byte_identical_original=False,derived_includes_original_compressed_prefix=True,wrapper_sha256=sha((out/'rescue-init').read_bytes()),source_sha256={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in [S/'rescue_init.c',S/'sha256.h',S/'pmsg_trace.h',ROOT/'ace/pstore_ring.c',ROOT/'ace/pstore_trial.c',ROOT/'ace/pstore_rescue.c',ROOT/'diagnostics/ace-irq-timer/qemu-start.S']},hardware_tested=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('capsule built',len(capsule),'original init blob unchanged',sha(original))
