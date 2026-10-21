#!/usr/bin/env python3
"""QEMU preflight of the native Image and REAL linked XNU's early BootArgs load.

Actual phone FDT/ADT declarations are fixtures; QEMU controllers are different.
No synthetic receiver, phone command, flash or claim of iOS/native-phone boot.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import socket
import struct
import subprocess

if not __debug__:raise RuntimeError('optimized verification refused')
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('pack',ROOT/'tools/ace-mkpayload.py')
pack=importlib.util.module_from_spec(spec);spec.loader.exec_module(pack)
sha=lambda b:hashlib.sha256(b).hexdigest()

def debugger_numbers(m,s,length):
    # Metadata becomes debugger command operands: never accept strings/bools.
    for key in ['fdt_pa','text_offset','entry_pa','args_pa','adt_pa','image_bytes']:
        if type(m.get(key)) is not int or not 0<=m[key]<(1<<40):raise ValueError('invalid numeric Image metadata')
    if type(m.get('ram')) is not dict:raise ValueError('invalid RAM metadata')
    for key in ['base','size']:
        if type(m['ram'].get(key)) is not int or not 0<m['ram'][key]<(1<<40):raise ValueError('invalid RAM range')
    if not isinstance(s,dict) or any(type(x) is not int or not 0<=x<=length for x in s.values()):raise ValueError('invalid symbol offsets')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('image_directory',type=Path);p.add_argument('kernel',type=Path);p.add_argument('fdt',type=Path);p.add_argument('output_directory',type=Path)
    p.add_argument('--case',dest='selected_cases',action='append',help='run only the named case; repeat for multiple cases, default runs every case')
    a=p.parse_args();image=a.image_directory.resolve();out=a.output_directory.resolve()
    if out.exists() or not out.is_relative_to(ROOT/'research'):raise ValueError('new ignored research/ output required')
    for path in [image,a.kernel.resolve(),a.fdt.resolve(),out]:
        if not re.fullmatch(r'[A-Za-z0-9_./+-]+',str(path)):raise ValueError('restricted GDB fixture paths required')
    m=json.loads((image/'build-manifest.json').read_text());syms=json.loads((image/'symbols.json').read_text())
    data=(image/'native.Image').read_bytes();kernel=pack.read(a.kernel);fdt=pack.read(a.fdt)
    debugger_numbers(m,syms,len(data))
    if sha(data)!=m['image_sha256'] or sha(kernel)!=m['kernel_sha256'] or not m['pmsg_enabled']:raise ValueError('input/hash/profile mismatch')
    if m['text_offset'] not in (0,0x80000):raise ValueError('unsupported QEMU Image text offset')
    initial=0x40200000 if m['text_offset']==0 else 0x40080000
    fallback=m.get('refusal_android',{}).get('enabled',False)
    for name,digest in m['source_sha256'].items():
        if sha((ROOT/name).read_bytes())!=digest:raise ValueError('stale source binding: '+name)
    payload=(image/'ace.payload').read_bytes()
    if sha(payload)!=m['payload_sha256'] or data[syms['bundle_start']:syms['bundle_end']]!=payload:raise ValueError('embedded payload mismatch')
    segments,va,entry,top,relocs=pack.macho(kernel)
    ram=m['ram']['base'];mem=m['ram']['size'];start=min(s['va'] for s in segments)-va+ram
    end=max(s['va']+s['memory'] for s in segments)-va+ram
    entry_offset=next(s['fileoff']+entry-s['va'] for s in segments if s['va']<=entry<s['va']+s['files'])
    opcode=struct.unpack_from('<I',kernel,entry_offset)[0]
    if opcode>>26!=5:raise ValueError('preflight expects reviewed actual XNU B trampoline')
    delta=opcode&0x3ffffff
    if delta&(1<<25):delta-=1<<26
    after_pc=m['entry_pa']+delta*4+40
    kernel_symbols=[x.split() for x in subprocess.check_output(['llvm-nm',str(a.kernel)],text=True).splitlines()]
    ready=[int(x[0],16) for x in kernel_symbols if len(x)==3 and x[2]=='_ace_early_bootargs_ready']
    if len(ready)>1:raise ValueError('ambiguous kernel entry symbol')
    if ready:
        after_pc=ready[0]-va+ram
        if not re.fullmatch('[0-9a-f]{16}',m.get('run_token','')):raise ValueError('new kernel requires bound run token')
    out.mkdir(parents=True);(out/'verification.json').write_text('{"status":"incomplete","xnu_hardware_boot":false}\n')
    (out/'target-a5.bin').write_bytes(b'\xa5'*(end-start))
    (out/'bss-a5.bin').write_bytes(b'\xa5'*(syms['__bss_end']-syms['__bss_start']))
    (out/'old-image-poison.bin').write_bytes(b'\x5a'*len(data))
    valid_ring=struct.pack('<III',0x43474244,0,0)+bytes(65524)
    seed_empty=m.get('initialize_empty_pmsg',False)
    # Real failed trial had zero signature/start but some nonzero bytes remain.
    # A zero header never licenses clearing opaque old data.
    invalid_ring=(bytes(128)+b'\x71'+bytes(65536-129)) if seed_empty else bytes(65536)
    (out/'ring-valid.bin').write_bytes(valid_ring);(out/'ring-invalid.bin').write_bytes(invalid_ring)
    (out/'ring-zero.bin').write_bytes(bytes(65536))
    trial_marker=('\nACETRIAL1:'+m['run_token']+': armed\n').encode()
    pending_ring=struct.pack('<III',0x43474244,len(trial_marker),len(trial_marker))+trial_marker+bytes(65524-len(trial_marker))
    (out/'ring-pending.bin').write_bytes(pending_ring)
    cases=[]
    names=['el2-refusal','wrong-fdt-refusal','frequency-refusal','pmsg-refusal','actual-xnu-entry','relocated-actual-xnu-entry','phone-address-actual-xnu-entry']
    if seed_empty:names.append('zero-ring-actual-xnu-entry')
    if m.get('auto_readout_after_reset'):names.append('auto-reset-refusal')
    archived=m.get('pmsg_reseed_from_snapshot',{})
    if archived.get('enabled') is True:
        capture=(image/'pmsg-reseed.snapshot').read_bytes()
        if len(capture)!=65536 or sha(capture)!=archived['capture_sha256']:
            raise ValueError('archived pmsg capture identity mismatch')
        if data[syms['pmsg_reseed_snapshot']:syms['pmsg_reseed_snapshot_end']]!=capture:
            raise ValueError('embedded archived pmsg capture mismatch')
        (out/'ring-approved.bin').write_bytes(capture)
        # Reject a near-identical capture differing only at its final byte.
        changed=bytearray(capture);changed[-1]^=1;invalid_ring=bytes(changed)
        (out/'ring-invalid.bin').write_bytes(invalid_ring)
        names+=['approved-reseed-actual-xnu-entry','phone-address-approved-reseed-actual-xnu-entry']
    available_cases=list(names)
    if a.selected_cases is not None:
        if len(set(a.selected_cases))!=len(a.selected_cases) or not set(a.selected_cases)<=set(names):
            raise ValueError('duplicate or unavailable preflight case')
        names=[name for name in names if name in a.selected_cases]
    for name in names:
        # An optional rescue capsule can leave less than2MiB above initial.
        # Keep this XNU relocation fixture inside the SAME reviewed window.
        relocated=(0x40400000 if 0x40400000+len(data)<=m['image_load_window'][1] else 0x40100000) if fallback else 0x42000000
        base=relocated if name.startswith('relocated') else 0x40000000 if name.startswith('phone-address') else initial
        success=name.endswith('actual-xnu-entry') or name=='actual-xnu-entry'
        early=name in ['el2-refusal','wrong-fdt-refusal']
        virt='on' if name=='el2-refusal' else 'off'
        folder=out/name;folder.mkdir()
        with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
        cpu='cortex-a55' if name=='frequency-refusal' else 'cortex-a55,cntfrq=13000000'
        command=['qemu-system-aarch64','-M','virt,virtualization='+virt+',gic-version=3','-cpu',cpu,'-m','8G','-smp','1','-display','none','-serial','none','-monitor','none','-nic','none','-kernel',str(image/'native.Image'),'-S','-gdb',f'tcp:127.0.0.1:{port}']
        commands=['set pagination off','set confirm off','set tcp connect-timeout 5','set tcp auto-retry on',f'target remote 127.0.0.1:{port}',
            f'hbreak *{initial}','continue','delete breakpoints']
        if base!=initial:
            commands += [f'restore {image/"native.Image"} binary {base}']
            if base>=initial+len(data) or base+len(data)<=initial:
                commands += [f'restore {out/"old-image-poison.bin"} binary {initial}']
            commands += [f'set $pc={base}']
        commands += [f'restore {out/"bss-a5.bin"} binary {base+syms["__bss_start"]}',
            f'restore {out/"target-a5.bin"} binary {start}',f'restore {a.fdt.resolve()} binary {m["fdt_pa"]}',
            f'restore {out/("ring-approved.bin" if "approved-reseed" in name else "ring-invalid.bin" if name=="pmsg-refusal" else "ring-zero.bin" if name=="zero-ring-actual-xnu-entry" else "ring-pending.bin" if name=="auto-reset-refusal" else "ring-valid.bin")} binary 0x48160000',
            f'set $x0={m["fdt_pa"]+(8 if name=="wrong-fdt-refusal" else 0)}']
        commands += [f'hbreak *{base+syms["native_halt"]}',f'hbreak *{base+syms["native_early_halt"]}',
            f'hbreak *{m["entry_pa"]}']
        if fallback and not success and not early:
            commands += [f'hbreak *{base+syms["native_refusal_android"]}']
        commands += ['continue',
            'printf "ACE_ENTRY_REGS %lx %lx %lx %lx %lx\\n",$pc,$x0,$x1,$x2,$x3',
            f'dump binary memory {folder/"record.bin"} {base+syms["native_record"]} {base+syms["native_record"]+256}']
        if success:
            commands += ([f'hbreak *{after_pc}','continue'] if ready else ['stepi 11'])
            commands += ['printf "ACE_AFTER_REGS %lx %lx %lx %lx %lx\\n",$pc,$x20,$x22,$x23,$x24']
        elif not early and not fallback:
            stage,code=(1,22) if name=='frequency-refusal' else (5,64)
            halt_slot=base+syms['native_halt_slots']+(stage*128+code)*8
            commands += [f'hbreak *{halt_slot}','continue',
                'printf "ACE_HALT_REGS %lx %lx\\n",$pc,$sp']
        commands += [f'dump binary memory {folder/"target.bin"} {start} {end}',
            f'dump binary memory {folder/"bss.bin"} {base+syms["__bss_start"]} {base+syms["__bss_end"]}',
            f'dump binary memory {folder/"ring.bin"} 0x48160000 0x48170000']
        if name=='pmsg-refusal' and m.get('pmsg_seed_failure_snapshot'):
            commands += [f'dump binary memory {folder/"pmsg-snapshot.bin"} {base+syms["native_pmsg_snapshot"]} {base+syms["native_pmsg_snapshot"]+65536}',
                f'dump binary memory {folder/"snapshot-ready.bin"} {base+syms["native_pmsg_snapshot_ready"]} {base+syms["native_pmsg_snapshot_ready"]+4}']
        if success:
            commands += [f'dump binary memory {folder/"args.bin"} {m["args_pa"]} {m["args_pa"]+16384}',
                f'dump binary memory {folder/"adt.bin"} {m["adt_pa"]} {m["adt_pa"]+struct.unpack_from("<Q",payload,40)[0]}']
        commands += ['detach','quit']
        gdb=['gdb-multiarch','-nx','-q','-batch']
        for c in commands:gdb+=['-ex',c]
        with (folder/'qemu.log').open('w') as log:
            q=subprocess.Popen(command,stdout=log,stderr=log,stdin=subprocess.DEVNULL)
            try:
                result=subprocess.run(gdb,capture_output=True,text=True,timeout=50)
                (folder/'gdb.log').write_text(result.stdout+result.stderr)
                if result.returncode:raise RuntimeError(name+': GDB failed; inspect private log')
            finally:
                q.terminate()
                try:q.wait(timeout=3)
                except subprocess.TimeoutExpired:q.kill();q.wait(timeout=3)
        rec=(folder/'record.bin').read_bytes();words=list(struct.unpack('<32Q',rec))
        regs=re.search(r'ACE_ENTRY_REGS ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+)',result.stdout)
        if not regs:raise AssertionError(name+': missing entry registers')
        entry_regs=[int(x,16) for x in regs.groups()]
        target=(folder/'target.bin').read_bytes();ring=(folder/'ring.bin').read_bytes()
        if early:
            assert entry_regs[0]==base+syms['native_early_halt'],(name,entry_regs,words)
            assert rec==b'\xa5'*256 and (folder/'bss.bin').read_bytes()==(out/'bss-a5.bin').read_bytes()
        elif not success:
            assert entry_regs[0]==base+syms['native_refusal_android' if fallback else 'native_halt'],(name,entry_regs,words)
            assert words[0]==0x313054414e454341 and words[2]==(1 if name=='frequency-refusal' else 5),(name,words)
            assert words[3]==(1<<64)-(22 if name=='frequency-refusal' else 67 if name=='auto-reset-refusal' else 64),(name,words)
            if not fallback:
                halted=re.search(r'ACE_HALT_REGS ([0-9a-f]+) ([0-9a-f]+)',result.stdout)
                assert halted is not None,name+': missing watchdog-visible diagnostic slot'
                assert [int(x,16) for x in halted.groups()]==[halt_slot,base+syms['stack_top']],(name,halted.groups())
            assert syms['native_halt_slots_end']-syms['native_halt_slots']==(10 if m.get('ram_rescue',{}).get('enabled') else 9)*128*8
        if not success:
            assert target==(out/'target-a5.bin').read_bytes(),name+': refused Image changed destination'
            assert ring==(invalid_ring if name=='pmsg-refusal' else pending_ring if name=='auto-reset-refusal' else valid_ring),name+': refused Image changed ring'
            if name=='pmsg-refusal' and seed_empty:
                assert words[23]==0 and words[25]==sum(byte!=0 for byte in invalid_ring) and words[31]==2**64-3,(name,'readonly seed observation',words)
                if m.get('pmsg_seed_failure_snapshot'):
                    assert (folder/'pmsg-snapshot.bin').read_bytes()==invalid_ring
                    assert (folder/'snapshot-ready.bin').read_bytes()==struct.pack('<I',1)
        else:
            assert words[2:4]==[7,0] and words[19]==0 and words[25]==1,(name,words)
            assert words[31]==(2 if 'approved-reseed' in name else 1 if name=='zero-ring-actual-xnu-entry' else 0),(name,'seed outcome',words[31])
            if 'approved-reseed' in name:
                assert b'ACENATIVE1 pmsg rebuilt from exact archived snapshot; seed=2\n' in ring
            assert words[5]==base and words[24]==53 and words[28]==len(segments),(name,words)
            assert entry_regs==[m['entry_pa'],m['args_pa'],0,0,0],(name,entry_regs)
            after=re.search(r'ACE_AFTER_REGS ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+) ([0-9a-f]+)',result.stdout)
            assert after is not None,name
            assert [int(x,16) for x in after.groups()]==[after_pc,m['args_pa'],va,ram,mem],(name,after.groups())
            for s in segments:
                off=s['va']-va+ram-start;f=s['files'];n=s['memory']
                assert target[off:off+f]==kernel[s['fileoff']:s['fileoff']+f],(name,s['name'],'file mismatch')
                assert target[off+f:off+n]==bytes(n-f),(name,s['name'],'BSS not zero')
            adto,adtn=struct.unpack_from('<QQ',payload,32)
            assert (folder/'adt.bin').read_bytes()==payload[adto:adto+adtn]
            args=(folder/'args.bin').read_bytes();assert struct.unpack_from('<HH',args)==(2,2)
            assert struct.unpack_from('<QQQ',args,8)==(va,ram,mem) and args[736:]==bytes(16384-736)
            expected=bytearray(b'\xa5'*(end-start))
            for s in segments:
                off=s['va']-va+ram-start
                expected[off:off+s['files']]=kernel[s['fileoff']:s['fileoff']+s['files']]
                expected[off+s['files']:off+s['memory']]=bytes(s['memory']-s['files'])
            assert target==expected,name+': segment span/gaps mismatch'
            expected_args=bytearray(16384);struct.pack_into('<HH',expected_args,0,2,2)
            struct.pack_into('<QQQQ',expected_args,8,va,ram,mem,m['args_pa']+16384)
            struct.pack_into('<QI',expected_args,96,va+m['adt_pa']-ram,adtn)
            expected_args[108:716]=payload[72:680];struct.pack_into('<Q',expected_args,728,mem)
            assert args==expected_args,name+': complete BootArgs page mismatch'
            _,cursor,n=struct.unpack_from('<III',ring)
            assert cursor==n and n<65524 and b'ACENATIVE1 prepared' in ring[12:12+n] and b'ACENATIVE1 branching' in ring[12:12+n]
            assert rec in ring[12:12+n],name+': native record missing from ring'
            if m.get('auto_readout_after_reset'):
                assert ring[12:12+n].count(trial_marker)==1,name+': pending trial not armed exactly once'
            if ready:
                marker=('ACEXNU1:'+m['run_token']+': entry EL1\n').encode()
                assert ring[12:12+n].count(marker)==1,name+': bound XNU entry marker missing or duplicated'
        case={'case':name,'passed':True,'native_record':words,'entry_registers':entry_regs,'qemu_argv':command,
            'gdb_argv':gdb,'dumps_sha256':{p.name:sha(p.read_bytes()) for p in folder.glob('*.bin')},
            'actual_xnu_instructions_stepped':(None if ready else 11) if success else 0,
            'bootargs_ready_pa':after_pc if success else None,
            'token_bound_kernel_marker_checked':bool(success and ready),'phone_execution':False}
        case['normal_refusal_stopped_before_optional_android']=bool(fallback and not success and not early)
        (folder/'result.json').write_text(json.dumps(case,indent=2)+'\n');cases.append(case)
        print(name+': PASS',flush=True)
    report={'status':'PASS QEMU preflight only','image_sha256':m['image_sha256'],'kernel_sha256':m['kernel_sha256'],
        'fdt_sha256':sha(fdt),'case_selection':a.selected_cases,'available_cases':available_cases,'cases':cases,'segments_checked':len(segments),'linked_local_pointers':relocs,
        'verifier_sha256':sha(Path(__file__).read_bytes()),'xnu_hardware_boot':False,'ios_deployable':False,
        'limitations':'QEMU CPU cntfrq property configured13MHz; actual phone FDT is a fixture; no controller/page-table/phone XNU validation'}
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
