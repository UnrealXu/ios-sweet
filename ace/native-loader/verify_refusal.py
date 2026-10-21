#!/usr/bin/env python3
"""QEMU-only real native refusals -> unchanged Android -> PID1 FDT readback.

No phone/flash operation. A passing test is not XNU or iOS hardware success.
All output is a fresh ignored research directory; failures retain raw evidence.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import socket
import struct
import subprocess
import sys

if not __debug__:raise RuntimeError('optimized verification refused')
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import fdt
spec=importlib.util.spec_from_file_location('cpio',ROOT/'tools/ace-recovery-diag.py')
cpio=importlib.util.module_from_spec(spec);spec.loader.exec_module(cpio)
INITRD=ROOT/'research/ace-irq-timer-live-20261019/qemu/initramfs.cpio.gz'
INITRD_SHA='d652143893bec3a082b4fa8984e60827eee9aa9c1fdf28b72a8475171c3c4dfe'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def pack(tree):
    strings=bytearray();body=bytearray();offsets={}
    u32=lambda *v:struct.pack('>'+len(v)*'I',*v)
    def visit(n):
        body.extend(u32(1)+n.name.encode()+b'\0');body.extend(bytes(-len(body)%4))
        for name,value in n.props.items():
            if name not in offsets:offsets[name]=len(strings);strings.extend(name.encode()+b'\0')
            body.extend(u32(3,len(value),offsets[name])+value);body.extend(bytes(-len(body)%4))
        for child in n.children:visit(child)
        body.extend(u32(2))
    visit(tree.root);body.extend(u32(9))
    reserves=b''.join(struct.pack('>QQ',*r) for r in tree.reservations)+bytes(16)
    st=40+len(reserves);ss=st+len(body)
    return u32(0xd00dfeed,ss+len(strings),st,ss,40,17,16,0,len(strings),len(body))+reserves+body+strings

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('image_directory',type=Path);p.add_argument('output_directory',type=Path)
    p.add_argument('--case',dest='selected_cases',action='append',help='run only the named case; repeat for multiple cases, default runs every case')
    a=p.parse_args();image=a.image_directory.resolve();out=a.output_directory.resolve()
    if out.exists() or not out.is_relative_to(ROOT/'research'):raise ValueError('new private output required')
    for path in (image,out):
        if not re.fullmatch(r'[A-Za-z0-9_./+-]+',str(path)):raise ValueError('restricted debugger paths required')
    m=json.loads((image/'build-manifest.json').read_text());s=json.loads((image/'symbols.json').read_text())
    assert m['refusal_android']['enabled'] and m['text_offset']==0
    assert sha(image/'native.Image')==m['image_sha256'] and sha(INITRD)==INITRD_SHA
    assert sha(image/'android.Image')==m['refusal_android']['sha256']
    assert re.fullmatch('[0-9a-f]{16}',m['run_token'])
    for name,h in m['source_sha256'].items():assert sha(ROOT/name)==h,'stale source '+name
    out.mkdir();(out/'verification.json').write_text('{"status":"incomplete","hardware_tested":false}\n')
    entries=cpio.read_cpio(gzip.decompress(INITRD.read_bytes()));cases=[]
    normal=('readout',2,66,13000000,0) if m.get('diagnostic_readout_only') else ('fdt-policy',3,33,13000000,0)
    profiles=[('frequency',1,22,62500000,0),normal,
            ('unaligned-android',1,22,62500000,-94),('firmware-alias',1,22,62500000,-62)]
    if m.get('auto_readout_after_reset'):
        profiles.append(('pending-handoff-fixture',5,67,62500000,0))
    if m.get('pmsg_seed_failure_snapshot'):
        profiles.append(('pmsg-snapshot-fixture',5,64,62500000,0))
    if m.get('diagnostic_readout_only') and m.get('prior_run_token'):
        profiles.append(('readout-marker-fixture',2,66,13000000,0))
    available_cases=[profile[0] for profile in profiles]
    if a.selected_cases is not None:
        if len(set(a.selected_cases))!=len(a.selected_cases) or not set(a.selected_cases)<=set(available_cases):
            raise ValueError('duplicate or unavailable Android refusal case')
        profiles=[profile for profile in profiles if profile[0] in a.selected_cases]
    for name,stage,code,frequency,guard in profiles:
        base=0x40080000 if name=='unaligned-android' else 0x40200000
        folder=out/name;folder.mkdir();init=folder/'init'
        command=['aarch64-linux-gnu-gcc','-march=armv8-a','-ffreestanding','-fno-builtin','-fno-stack-protector',
            '-fno-pie','-O2','-nostdlib','-static','-no-pie','-Wl,-e,_start,--build-id=none',
            '-DREFUSAL_TOKEN="'+m['run_token']+'"',f'-DEXPECT_STAGE={stage}',f'-DEXPECT_CODE={code}',f'-DEXPECT_PMSG_SNAPSHOT={int(name=="pmsg-snapshot-fixture")}',
            str(ROOT/'diagnostics/ace-irq-timer/qemu-start.S'),str(ROOT/'diagnostics/ace-native-refusal/qemu-init.c'),'-o',str(init)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=30)
        (folder/'init-build.log').write_text(result.stdout+result.stderr);assert result.returncode==0
        (folder/'init-build-command.json').write_text(json.dumps(command,indent=2)+'\n')
        modified=[(n,fields,init.read_bytes() if n=='init' else data) for n,fields,data in entries]
        initrd=folder/'initramfs.cpio.gz';initrd.write_bytes(gzip.compress(cpio.write_cpio(modified),mtime=0))
        base_argv=['qemu-system-aarch64','-M','virt,virtualization=off,gic-version=3',
            '-cpu',f'cortex-a55,cntfrq={frequency}','-m','2G','-smp','1','-kernel',str(image/'native.Image'),
            '-initrd',str(initrd),'-append','console=ttyAMA0 earlycon=pl011,0x09000000 rdinit=/init nokaslr loglevel=8 panic=-1',
            '-no-reboot','-display','none','-monitor','none','-nic','none']
        generated=folder/'qemu.dtb'
        dump_argv=base_argv.copy();dump_argv[2]+=',dumpdtb='+str(generated)
        result=subprocess.run(dump_argv+['-serial','none'],capture_output=True,text=True,timeout=15)
        (folder/'dtb-generation.log').write_text(result.stdout+result.stderr);assert result.returncode==0
        tree=fdt.parse(generated.read_bytes())
        assert tree.by_path('/reserved-memory') is None
        reserved=fdt.Node('reserved-memory',parent=tree.root,props={'#address-cells':struct.pack('>I',2),
            '#size-cells':struct.pack('>I',2),'ranges':b''})
        tree.root.children.append(reserved)
        if m.get('diagnostic_readout_only'):
            reserved.children.append(fdt.Node('pstore',parent=reserved,props={
                'compatible':b'mediatek,pstore\0','reg':struct.pack('>QQ',0x48090000,0xe0000),'no-map':b''}))
        if name=='firmware-alias':tree.reservations.append((base,4096))
        fixture=folder/'input.dtb';fixture.write_bytes(pack(tree))
        pstore=folder/'pstore-before.bin'
        pstore.write_bytes((b'ACE_PRIOR_TRIAL'+bytes(range(256))*256)[:65536])
        if name=='pmsg-snapshot-fixture':pstore.write_bytes(bytes(128)+b'\x71'+bytes(65536-129))
        if name=='readout-marker-fixture':
            marker=('ACEXNU1:'+m['prior_run_token']+': entry EL1\n').encode()
            pstore.write_bytes(struct.pack('<III',0x43474244,len(marker),len(marker))+marker+bytes(65524-len(marker)))
        if name=='pending-handoff-fixture':
            marker=('\nACETRIAL1:'+m['run_token']+': armed\n').encode()
            pstore.write_bytes(struct.pack('<III',0x43474244,len(marker),len(marker))+marker+bytes(65524-len(marker)))
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        argv=base_argv+['-serial','file:'+str(folder/'serial.log'),'-S','-gdb',f'tcp:127.0.0.1:{port}']
        commands=['set pagination off','set confirm off','set tcp connect-timeout 5','set tcp auto-retry on',
            f'target remote 127.0.0.1:{port}','si 6']
        if base!=0x40200000:commands += [f'restore {image/"native.Image"} binary {base}',f'set $pc={base}']
        commands += ['printf "NATIVE_BASE %lx\\n",$pc',
            f'restore {fixture} binary {m["fdt_pa"]}',f'set $x0={m["fdt_pa"]}',
            f'restore {pstore} binary 0x48160000',
            f'hbreak *{base+s["native_jump"]}',f'hbreak *{base+s["native_halt"]}',
            f'hbreak *{base+s["native_early_halt"]}','continue',
            'printf "ANDROID_HANDOFF %lx %lx %lx\\n",$pc,$x0,$x1',
            f'dump binary memory {folder/"record.bin"} {base+s["native_record"]} {base+s["native_record"]+256}',
            f'dump binary memory {folder/"stock.bin"} {base+s["android_payload"]} {base+s["android_payload_end"]}',
            f'dump binary memory {folder/"input-after.dtb"} {m["fdt_pa"]} {m["fdt_pa"]+len(fixture.read_bytes())}',
            f'dump binary memory {folder/"pstore-after.bin"} 0x48160000 0x48170000',
            f'dump binary memory {folder/"output.dtb"} {base+s["android_dtb"]} {base+s["android_dtb"]+len(fixture.read_bytes())+12+288+len(b"ace,native-refusal\0")+(12+65536+len(b"ace,pmsg-before-seed\0") if name=="pmsg-snapshot-fixture" else 0)}',
            'delete breakpoints','detach','quit']
        if name=='pending-handoff-fixture':
            # Synthetic refusal state, explicitly not the physical latch proof.
            # Execute the real fallback code and then the unchanged Android.
            index=commands.index('continue')
            commands[index:index]=[f'hbreak *{base+s["native_refusal_android"]}',
                'continue',f'set {{unsigned long long}}{base+s["native_record"]+16}=5',
                f'set {{unsigned long long}}{base+s["native_record"]+24}=0xffffffffffffffbd',
                'delete breakpoint 4']
        if name=='pmsg-snapshot-fixture':
            # The real capture is separately verified by verify.py's failed
            # seed case. Here exercise FDT/Android readback with that exact
            # pattern, using a synthetic failed-seed state at the fallback.
            index=commands.index('continue')
            commands[index:index]=[f'hbreak *{base+s["native_refusal_android"]}',
                'continue',f'set {{unsigned long long}}{base+s["native_record"]+16}=5',
                f'set {{unsigned long long}}{base+s["native_record"]+24}=0xffffffffffffffc0',
                f'set {{unsigned long long}}{base+s["native_record"]+19*8}=0xfffffffffffffffd',
                f'set {{unsigned long long}}{base+s["native_record"]+23*8}=0',
                f'set {{unsigned long long}}{base+s["native_record"]+25*8}=1',
                f'set {{unsigned long long}}{base+s["native_record"]+31*8}=0xfffffffffffffffd',
                f'restore {pstore} binary {base+s["native_pmsg_snapshot"]}',
                f'set {{unsigned int}}{base+s["native_pmsg_snapshot_ready"]}=1',
                'delete breakpoint 4']
        g=['gdb-multiarch','-nx','-q','-batch']
        for command in commands:g+=['-ex',command]
        with (folder/'qemu.log').open('w') as log:
            q=subprocess.Popen(argv,stdout=log,stderr=log,stdin=subprocess.DEVNULL)
            try:
                r=subprocess.run(g,capture_output=True,text=True,timeout=45)
                (folder/'gdb.log').write_text(r.stdout+r.stderr);assert r.returncode==0,'GDB failed; retained logs'
                if not guard:q.wait(timeout=55)
            finally:
                if q.poll() is None:
                    q.terminate()
                    try:q.wait(timeout=3)
                    except subprocess.TimeoutExpired:q.kill();q.wait(timeout=3)
        log=(folder/'gdb.log').read_text();match=re.search(r'ANDROID_HANDOFF ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+)',log)
        assert match
        registers=[int(x,16) for x in match.groups()]
        assert registers[0]==base+s['native_halt' if guard else 'native_jump']
        assert sha(folder/'stock.bin')==m['refusal_android']['sha256']
        record=(folder/'record.bin').read_bytes();words=struct.unpack('<32Q',record)
        assert words[2]==stage and words[3]==2**64-code and words[20]==guard%(2**64)
        if name=='readout':assert words[23]==2**64-3 and words[24]==0 and words[31]>0
        if name=='readout-marker-fixture':
            assert words[23]==0 and words[24]==1 and words[25]==0
            assert record[26*8:26*8+len(marker)]==marker
        assert (folder/'input-after.dtb').read_bytes()==fixture.read_bytes()
        after=(folder/'pstore-after.bin').read_bytes()
        if name=='pending-handoff-fixture':
            expected=marker+('\nACEANDROID1:'+m['run_token']+': pending handoff\n').encode()+b'ACEFALL1'+m['run_token'].encode()+bytes(8)+record
            assert after==struct.pack('<III',0x43474244,len(expected),len(expected))+expected+bytes(65524-len(expected))
        else:assert after==pstore.read_bytes()
        serial=(folder/'serial.log').read_text(errors='replace')
        if not guard:
            assert registers[1:]==[base+s['android_payload'],base+s['android_dtb']]
            copied=fdt.parse((folder/'output.dtb').read_bytes())
            prop=copied.by_path('/chosen').props['ace,native-refusal']
            assert len(prop)==288 and prop[:8]==b'ACEFALL1' and prop[8:25]==m['run_token'].encode()+b'\0' and prop[32:]==record
            if name=='pmsg-snapshot-fixture':
                assert copied.by_path('/chosen').props['ace,pmsg-before-seed']==pstore.read_bytes()
                assert 'ACE_REFUSAL_QEMU: SNAPSHOT_PASS' in serial and 'SNAPSHOT_FAIL' not in serial
            else:assert 'ace,pmsg-before-seed' not in copied.by_path('/chosen').props
            assert q.returncode==0 and all(x in serial for x in ['ACE_REFUSAL_QEMU: RECORD_PASS token='+m['run_token'],
                'ACE_MODULE_QEMU: LOAD_PASS','ACE_MODULE_QEMU: UNLOAD_PASS','reboot: Power down'])
            assert not any(x in serial for x in ['RECORD_FAIL','Kernel panic','Unable to handle kernel','CFI failure'])
        else:
            assert not any((folder/'output.dtb').read_bytes())
            assert 'ACE_STOCK_QEMU' not in serial
        cases.append(dict(case=name,stage=stage,error=-code,passed=True,original_kernel_booted=not bool(guard),
            fallback_guard_error=guard,guest_record_readback_verified=not bool(guard),qemu_argv=argv,gdb_argv=g,
            marker_fixture_is_synthetic=name=='readout-marker-fixture',
            pending_handoff_fixture_is_synthetic=name=='pending-handoff-fixture',
            durable_handoff_record_verified=name=='pending-handoff-fixture',
            seed_snapshot_fixture_is_synthetic=name=='pmsg-snapshot-fixture',
            guest_pmsg_snapshot_verified=name=='pmsg-snapshot-fixture',
            dumps_sha256={f.name:sha(f) for f in folder.iterdir() if f.is_file()}))
        print(name+(': refused fallback safely PASS' if guard else ': native refusal -> byte-identical Android -> guest record readback PASS'),flush=True)
    (out/'verification.json').write_text(json.dumps(dict(status='PASS QEMU normal-refusal Android diagnostics only',
        image_sha256=m['image_sha256'],kernel_sha256=m['kernel_sha256'],android_sha256=m['refusal_android']['sha256'],
        case_selection=a.selected_cases,available_cases=available_cases,cases=cases,verifier_sha256=sha(Path(__file__)),
        source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'diagnostics/ace-native-refusal/qemu-init.c',
            ROOT/'diagnostics/ace-irq-timer/qemu-init.c',ROOT/'diagnostics/ace-irq-timer/qemu-start.S',
            ROOT/'tools/fdt.py',ROOT/'tools/ace-recovery-diag.py']},
        hardware_tested=False,ios_deployable=False),indent=2)+'\n')

if __name__=='__main__':main()
