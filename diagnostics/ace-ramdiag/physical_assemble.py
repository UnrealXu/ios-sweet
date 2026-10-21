#!/usr/bin/env python3
"""Assemble private physical RAM diagnostics offline. Never flash or reboot.

The result is a generic ramdisk, not a native-token boot candidate or approved
physical loop. The enclosing native/boot preparation must bind its source/image
hashes and produce a matching host contract before the one-time writer is used.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import stat
import subprocess

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).resolve().parent

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

base=module('ace_ram_base',SOURCE/'qemu_stage2.py')
ram=module('ace_ram_profile',ROOT/'tools/ace_ram_readout.py')
require,sha=base.require,base.sha


def geometry(raw):
    parts=json.loads(raw)
    require(set(parts)==set(ram.PARTITIONS),'partition contract set')
    for value in parts.values():
        require(set(value)=={'start_512','sectors_512','number'},'partition contract fields')
        require(all(type(v) is int and v>0 for v in value.values()),'partition geometry types')
        require(value['sectors_512']==131072 and value['start_512']%8==0,'full64MiB aligned geometry required')
    first,second=sorted(parts.values(),key=lambda p:p['start_512'])
    require(first['start_512']+first['sectors_512']<=second['start_512'] and first['number']!=second['number'],'overlapping/repeated partitions')
    return parts


def assemble(out,plan,plan_sha,serial,token,public_key,key_sha,parts):
    require(not out.exists() and out.is_relative_to(ROOT/'research'),'new private output required')
    require(re.fullmatch('[A-Za-z0-9_.+-]{1,64}',serial) and serial!='RAMDIAG_QEMU_FIXTURE','physical serial required')
    require(re.fullmatch('[0-9a-f]{16}',token),'fresh native token format')
    require(sha(plan.read_bytes())==plan_sha and ram.digest(plan_sha),'module plan pin mismatch')
    base.wire.validate_public_key(public_key,key_sha)
    # Revalidate geometry even for programmatic callers.
    parts=geometry(json.dumps(parts).encode())
    out.mkdir(mode=0o700,parents=True)
    try:
        command=['python3',str(SOURCE/'module_bundle.py'),str(plan),'--plan-sha256',plan_sha,
                 '--expected-serial',serial,'--output',str(out/'bundle')]
        result=subprocess.run(command,capture_output=True,text=True,timeout=120)
        (out/'bundle-build.log').write_text(result.stdout+result.stderr)
        require(result.returncode==0,'physical bundle build failed')
        bundle=json.loads((out/'bundle/report.json').read_text())
        require(len(bundle['modules'])==48 and bundle['return_prefix_count']==3 and bundle['supervisor_timeout']==90,'physical bundle closure/stage/deadline mismatch')
        expected=['mtk_wdt.ko','reboot-mode.ko','syscon-reboot-mode.ko']
        require([r['module'] for r in bundle['modules'][:3]]==expected,'return-first module order mismatch')
        core=out/'base';core.mkdir(mode=0o700)
        report=base.assemble(core,trusted_public_key=public_key,trusted_public_key_sha256=key_sha,vendor_overlay_test=True)
        generic=subprocess.run(['lz4','-dc'],input=(core/'generic-ramdisk.lz4').read_bytes(),capture_output=True,check=True).stdout
        entries={n:(f,d) for n,f,d in base.cpio.read_cpio(generic) if n!='TRAILER!!!'}
        del entries['ace-ramdiag/probe.sh']
        def put(name,data,mode=stat.S_IFREG|0o400):entries[name]=(base.entry(name,data,mode)[1],data)
        put('system/etc/init/hw/init.rc',(SOURCE/'physical-init.rc').read_bytes(),stat.S_IFREG|0o644)
        put('ace-ramdiag/physical-usb.rc',(SOURCE/'physical-usb.rc').read_bytes(),stat.S_IFREG|0o644)
        put('ace-ramdiag/physical-startup.sh',(SOURCE/'physical-startup.sh').read_bytes())
        put('prop.default',b'ro.secure=0\nro.adb.secure=1\nro.debuggable=1\nro.build.version.sdk=31\nro.product.first_api_level=31\nro.build.type=userdebug\nservice.adb.tcp.port=-1\n',stat.S_IFREG|0o644)
        original=subprocess.run(['lz4','-dc'],input=base.cpio.read_vendor(base.VENDOR.read_bytes())['ramdisk'],capture_output=True,check=True).stdout
        vendor={n:(f,d) for n,f,d in base.cpio.read_cpio(original) if n!='TRAILER!!!'}
        for name in ['cmp','grep']:
            path='system/bin/'+name;entries[path]=vendor[path]
        for name in ['module-loader','module-supervisor']:
            data=(out/'bundle'/name).read_bytes()
            pin=bundle['loader_sha256' if name=='module-loader' else 'supervisor_sha256']
            require(sha(data)==pin,'bundle executable changed')
            put('ace-ramdiag/'+name,data,stat.S_IFREG|0o500)
        for row in bundle['modules']:
            data=(out/'bundle/modules'/row['module']).read_bytes()
            require(sha(data)==row['sha256'] and len(data)==row['bytes'],'bundle module changed')
            put('ace-ramdiag/modules/'+row['module'],data)
        profile=dict(format='ACE_RAMDIAG_GUEST_V1',serial=serial,run_token=token,bundle_id=bundle['bundle_id'],kernel_sha256=ram.KERNEL_SHA)
        profile_raw=(json.dumps(profile,sort_keys=True,separators=(',',':'))+'\n').encode()
        put('ace-ramdiag/profile.json',profile_raw)
        put('ace-ramdiag/trace-token',(token+'\n').encode())
        env=dict(EXPECTED_SERIAL=serial,BUNDLE_ID=bundle['bundle_id'],VENDOR_SHA=ram.VENDOR_SHA,
                 BOOT_START=parts['boot_b']['start_512'],BOOT_NUMBER=parts['boot_b']['number'],
                 VENDOR_START=parts['vendor_boot_b']['start_512'],VENDOR_NUMBER=parts['vendor_boot_b']['number'])
        put('ace-ramdiag/startup.env',(''.join(k+"='"+str(v)+"'\n" for k,v in env.items())).encode())
        (out/'native_config.h').write_text('static const char expected_native_token[]='+json.dumps(token)+';\n')
        compile_command=report['build_command'][:-3]+['-I',str(out),str(SOURCE/'native_gate.c'),'-o',str(out/'native-gate')]
        built=subprocess.run(compile_command,capture_output=True,text=True,timeout=30)
        (out/'native-build.log').write_text(built.stdout+built.stderr);require(built.returncode==0,'native gate build failed')
        put('ace-ramdiag/native-gate',(out/'native-gate').read_bytes(),stat.S_IFREG|0o500)
        for name in list(entries):
            for parent in Path(name).parents:
                if str(parent)!='.' and str(parent) not in entries:put(str(parent),b'',stat.S_IFDIR|0o755)
        payload=[(n,f,d) for n,(f,d) in sorted(entries.items(),key=lambda item:(item[0].count('/'),item[0]))]
        payload.append(base.entry('TRAILER!!!',b'',0))
        raw=base.cpio.write_cpio(payload)
        compressed=subprocess.run(['lz4','-l','-9','-c'],input=raw,capture_output=True,check=True).stdout
        require(subprocess.run(['lz4','-dc'],input=compressed,capture_output=True,check=True).stdout==raw,'ramdisk roundtrip')
        (out/'physical-generic.lz4').write_bytes(compressed)
        prefix=base.cpio.read_vendor(base.VENDOR.read_bytes())['ramdisk']
        (out/'vendor-plus-physical.initrd').write_bytes(prefix+compressed)
        # Exclude all QEMU workload/observer/proxy/fault assets from physical payload.
        forbidden={'probe.sh','usb-probe.sh','module-probe.sh','module-fixture','supervisor-test','observe-pid1','tcp-auth-test','usb-fixture','usb-proxy','dummy-usb-proxy','usb-boundary.bin'}
        require(not any(Path(n).name in forbidden for n in entries),'QEMU fixture in physical payload')
        sources=[Path(__file__),SOURCE/'physical-startup.sh',SOURCE/'physical-init.rc',SOURCE/'physical-usb.rc',SOURCE/'native_gate.c',SOURCE/'native_record_guard.h',SOURCE/'aarch64_flags.h',ROOT/'tools/ace_ram_readout.py']
        for path in sources:
            dest=out/'source-snapshot'/path.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes())
        manifest=dict(format='ACE_PHYSICAL_RAMDISK_V1',status='assembled offline; physical startup unproven',phone_io=False,ios_usable=False,
                      run_token=token,serial=serial,bundle_id=bundle['bundle_id'],guest_profile_sha256=sha(profile_raw),partitions=parts,
                      vendor_sha256=ram.VENDOR_SHA,kernel_sha256=ram.KERNEL_SHA,host_adb_public_key_sha256=sha(public_key),
                      generic_sha256=sha(compressed),combined_initrd_sha256=sha(prefix+compressed),native_gate_sha256=sha((out/'native-gate').read_bytes()),
                      source_sha256={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sources},base_report=report,
                      files={n:dict(sha256=sha(d),bytes=len(d),mode=oct(f[1])) for n,(f,d) in entries.items()})
        (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        return manifest
    except Exception:
        (out/'FAILED').write_text('Assembly failed; retain evidence, never use this output\n');raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--plan',type=Path,required=True);p.add_argument('--plan-sha256',required=True)
    p.add_argument('--transport-json',type=Path,required=True);p.add_argument('--run-token',required=True)
    p.add_argument('--host-adb-public-key',type=Path,required=True);p.add_argument('--host-adb-public-key-sha256',required=True)
    p.add_argument('--partitions-json',type=Path,required=True);p.add_argument('--partitions-sha256',required=True)
    a=p.parse_args();raw=a.partitions_json.read_bytes();require(sha(raw)==a.partitions_sha256 and ram.digest(a.partitions_sha256),'private partition contract pin mismatch')
    result=assemble(a.output.resolve(),a.plan,a.plan_sha256,json.loads(a.transport_json.read_text())['usb_adb'],a.run_token,
                    a.host_adb_public_key.read_bytes(),a.host_adb_public_key_sha256,geometry(raw))
    print(json.dumps({k:result[k] for k in ['status','generic_sha256','combined_initrd_sha256']},indent=2))

if __name__=='__main__':main()
