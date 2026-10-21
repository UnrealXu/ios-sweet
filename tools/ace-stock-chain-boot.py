#!/usr/bin/env python3
"""Prepare a reviewable diagnostic boot_b candidate. Never uses ADB/fastboot."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/ace-stock-chain-20261019'
BACKUP=ROOT/'research/ace-backup-20261019-wireless-v2/boot_b.img'
BACKUP_SHA='ee817627cbf0c90622135fcc857feb564904e60bdb00f35ace52dea9d0deed10'
STOCK_SHA='8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'
SOURCES={'ace/stock-chain/start.S','ace/stock-chain/linker.ld','ace/stock-chain/build.py','ace/stock-chain/verify.py','ace/entry/pmsg.S'}
CASES={'plain-el2','pmsg-el1','pmsg-el2','pmsg-relocated','bad-header-forward','full-image-alias-refused'}
spec=importlib.util.spec_from_file_location('boot',ROOT/'tools/ace-probe-boot.py')
boot=importlib.util.module_from_spec(spec);spec.loader.exec_module(boot)

def require(ok,msg):
    if not ok:raise ValueError(msg)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def private_file(name):
    require(isinstance(name,str) and not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe evidence path')
    p=(ROOT/name).resolve()
    require(p.is_relative_to(ROOT/'research/ace-stock-chain-20261019') or p==ROOT/'research/ace-irq-timer-live-20261019/qemu/initramfs.cpio.gz','Unexpected artifact location')
    return p

def validate(report):
    require(report.get('status')=='pass' and report.get('hardware_tested') is False and report.get('ios_deployable') is False,'Invalid evidence status/scope')
    require(set(report.get('sources',{}))==SOURCES,'Incomplete source evidence')
    for n,h in report['sources'].items():require(sha(ROOT/n)==h,'Changed source: '+n)
    cases=report.get('cases',[])
    require(len(cases)==6 and {c.get('case') for c in cases}==CASES,'Missing/duplicate QEMU cases')
    require(report.get('stock_sha256')==STOCK_SHA,'Wrong forwarded kernel')
    artifacts=report.get('artifacts_sha256',{})
    required={str((OUT/n).relative_to(ROOT)) for n in ['build.json','pmsg.Image','pmsg.elf']}
    for name in CASES:
        required.update(str((OUT/name/n).relative_to(ROOT)) for n in ['record.bin','stock.bin','serial.log','case.json','gdb.log','host.log'])
    require(required<=set(artifacts),'Missing raw evidence artifacts')
    for n,h in artifacts.items():require(sha(private_file(n))==h,'Changed raw evidence: '+n)
    build=json.loads((OUT/'build.json').read_text())
    require(build['token']==report['token'] and len(report['token'])==24 and all(c in '0123456789abcdef' for c in report['token']),'Invalid marker token')
    for c in cases:
        name=c['case'];folder=OUT/name
        require(c.get('passed') is True and c.get('exit_code')==0 and c.get('stock_kernel_booted') is True and c.get('exact_stock_kernel_unchanged') is True,'Case did not boot stock kernel')
        raw=(folder/'record.bin').read_bytes();require(len(raw)==80 and raw[:8]==b'ACECHN01','Invalid prefix record')
        v=struct.unpack('<10Q',raw)
        require(list(v)==c['record'] and v[1]==2 and v[3] in [4,8] and v[4]&5==0,'Invalid prefix state')
        expected= -9 if name=='plain-el2' else -2 if name=='full-image-alias-refused' else -3 if name=='bad-header-forward' else 0
        require(c['logger_status']==expected and v[8]==expected%(2**64),'Unexpected logger result')
        require(sha(folder/'stock.bin')==STOCK_SHA,'Runtime stock payload changed')
        serial=(folder/'serial.log').read_text(errors='replace')
        require(all(m in serial for m in ['ACE_MODULE_QEMU: LOAD_PASS','ACE_MODULE_QEMU: UNLOAD_PASS','ACE_IRQ_TIMER: el=1','reboot: Power down']),'Missing actual stock boot markers')
        require(not any(m in serial for m in ['Kernel panic','BUG:','CFI failure','Unable to handle kernel']),'Kernel failure in case')
    image=(OUT/'pmsg.Image').read_bytes()
    require(sha(OUT/'pmsg.Image')==build['images']['pmsg']['sha256'],'Selected Image changed')
    require(64<len(image)<64*1024*1024 and image[56:60]==b'ARM\x64','Invalid chain Image')
    require(struct.unpack_from('<3Q',image,8)==(0,len(image),0xa),'Chain Image header changed')
    stock_bytes=build['stock_bytes']
    require(hashlib.sha256(image[0x200000:0x200000+stock_bytes]).hexdigest()==STOCK_SHA,'Embedded stock not exact')
    require(not any(image[0x200000+stock_bytes:]),'Unexpected trailing payload')
    return image,build

def package(current,compressed,*,diagnostic_ramdisk=None,diagnostic_ramdisk_sha256=None):
    """Package bytes offline; a replacement ramdisk requires its explicit hash pin.

    This opt-in does not validate init/ADB, native trial evidence or authorize a
    device operation. Callers must separately validate the diagnostic payload.
    The default path retains the exact installed-backup Magisk ramdisk.
    """
    require(hashlib.sha256(current).hexdigest()==BACKUP_SHA,'Current boot backup changed')
    layout=boot.boot_v4(current)
    header=bytearray(current[:4096]);struct.pack_into('<I',header,8,len(compressed))
    ramdisk=current[layout['ramdisk_offset']:layout['ramdisk_offset']+layout['ramdisk_bytes']]
    replace_ramdisk=diagnostic_ramdisk is not None
    require(replace_ramdisk==(diagnostic_ramdisk_sha256 is not None),'Diagnostic ramdisk bytes and SHA256 pin must be supplied together')
    if replace_ramdisk:
        require(isinstance(diagnostic_ramdisk,bytes) and 0<len(diagnostic_ramdisk)<len(current),'Invalid diagnostic ramdisk size/type')
        require(isinstance(diagnostic_ramdisk_sha256,str) and len(diagnostic_ramdisk_sha256)==64 and
                all(c in '0123456789abcdef' for c in diagnostic_ramdisk_sha256),'Invalid diagnostic ramdisk SHA256 pin')
        require(hashlib.sha256(diagnostic_ramdisk).hexdigest()==diagnostic_ramdisk_sha256,'Diagnostic ramdisk hash mismatch')
        ramdisk=diagnostic_ramdisk
        struct.pack_into('<I',header,12,len(ramdisk))
    output=bytes(header)+compressed+bytes(-len(compressed)%4096)+ramdisk+bytes(-len(ramdisk)%4096)+bytes(4096)
    # Match the already-booting Magisk footer relocation pattern: preserve
    # the exact (obsolete payload hash) signed vbmeta bytes, move them after
    # the new payload, update footer geometry, and overwrite the FULL partition.
    # This is NOT a signature/authentication claim; current unlocked boot has
    # already accepted this same metadata with its modified ramdisk payload.
    bare=boot.boot_v4(output,avb_required=False)
    avb=layout['avb']
    metadata=current[avb['vbmeta_offset']:avb['vbmeta_offset']+avb['vbmeta_size']]
    end=len(output)
    require(end+len(metadata)+64<=len(current),'AVB relocation exceeds partition')
    output+=metadata+bytes(len(current)-end-len(metadata)-64)
    output+=struct.pack('>4sIIQQQ28s',b'AVBf',1,0,end,end,len(metadata),bytes(28))
    checked=boot.boot_v4(output)
    require(checked['payload_end']==end and len(output)==len(current)<=64*1024*1024,'Candidate geometry out of bounds')
    h=bytearray(header);struct.pack_into('<I',h,8,layout['kernel_bytes'])
    if replace_ramdisk:struct.pack_into('<I',h,12,layout['ramdisk_bytes'])
    require(bytes(h)==current[:4096],'Unexpected header modification')
    require(output[checked['kernel_offset']:checked['kernel_offset']+checked['kernel_bytes']]==compressed,'Packaged kernel changed')
    require(output[checked['ramdisk_offset']:checked['ramdisk_offset']+checked['ramdisk_bytes']]==ramdisk,'Packaged ramdisk changed')
    require(output[end:end+len(metadata)]==metadata,'Preserved AVB metadata changed')
    return output,layout,checked,ramdisk

def main():
    if not __debug__:raise RuntimeError('Optimized candidate validation refused')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    dest=a.output.resolve();require(dest.is_relative_to(OUT) and dest!=OUT and not dest.exists(),'Output must be new private child')
    report_path=OUT/'verification.json';image,build=validate(json.loads(report_path.read_text()))
    compressed=boot.deterministic_gzip(image);require(boot.inflate(compressed,64*1024*1024)==image,'Gzip roundtrip failed')
    current=BACKUP.read_bytes();candidate,old,new,ramdisk=package(current,compressed)
    dest.mkdir(parents=True,exist_ok=False)
    (dest/'chain.Image.gz').write_bytes(compressed);(dest/'diagnostic-boot-b.img').write_bytes(candidate)
    extracted=boot.inflate(candidate[4096:4096+new['kernel_bytes']],64*1024*1024)
    require(extracted==image,'Independent candidate extraction mismatch')
    manifest=dict(purpose='Diagnostic prefix then unchanged current Android kernel; NOT iOS',hardware_tested=False,ios_deployable=False,
                  destructive_write_requires_individual_user_confirmation=True,
                  candidate_sha256=sha(dest/'diagnostic-boot-b.img'),candidate_bytes=len(candidate),
                  backup_path=str(BACKUP),backup_sha256=BACKUP_SHA,backup_bytes=len(current),
                  kernel_image_sha256=hashlib.sha256(image).hexdigest(),original_kernel_sha256=STOCK_SHA,
                  original_magisk_ramdisk_sha256=hashlib.sha256(ramdisk).hexdigest(),marker_token=build['token'],
                  qemu_verification_sha256=sha(report_path),old_geometry=old,new_geometry=new,
                  footer='Exact current obsolete-payload AVB metadata preserved and relocated; full partition sized; no authentication claim',
                  preserved_avb_metadata_sha256=hashlib.sha256(current[old['avb']['vbmeta_offset']:old['avb']['vbmeta_offset']+old['avb']['vbmeta_size']]).hexdigest(),
                  source_sha256=sha(Path(__file__)),packaging_helper_sha256=sha(ROOT/'tools/ace-probe-boot.py'),
                  rollback='Restore exact pinned boot_b backup through verified unlocked USB fastboot; no vendor_boot/vbmeta/GPT/userdata writes',
                  limitations=['Not yet accepted by physical LK','Hardware RAM ownership/cache/reset logging unverified','Manual bootloader recovery and actual restore write untested','XNU and all MTK iOS drivers still incomplete'])
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ['purpose','candidate_sha256','candidate_bytes','marker_token','hardware_tested','ios_deployable']},indent=2))

if __name__=='__main__':main()
