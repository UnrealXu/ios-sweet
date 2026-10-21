#!/usr/bin/env python3
"""Normal, pinned CPU loads of a QEMU-validated observation-only module."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('collect', ROOT/'tools/ace-collect.py')
collect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collect)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(text, key):
    values = re.findall('^'+re.escape(key)+'=(.*)$', text, re.M)
    assert len(values)==1, 'Missing/ambiguous '+key
    return values[0]


def observations(before, after):
    def records(s):
        s = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', s)
        return re.findall(r'ACE_IRQ_TIMER: ([^\r\n]*)', s)
    old, new = records(before), records(after)
    assert new[:len(old)]==old and len(new)==len(old)+8, 'Expected exactly eight new samples'
    result=[]
    decimal={'el','freq','first','last'}
    expected={'el','mpidr','daif','freq','first','last','ctl','sre','gctl','pmr','group','bpr'}
    for line in new[len(old):]:
        fields=line.split()
        assert len(fields)==len(expected), 'Malformed register record'
        pairs=[f.split('=') for f in fields]
        assert all(len(p)==2 for p in pairs)
        assert {p[0] for p in pairs}==expected
        r={k:int(v,10 if k in decimal else 16) for k,v in pairs}
        assert r['el']==1 and r['freq']==13000000 and r['last']>=r['first']
        assert r['sre']&1 and r['group']&1 and 0<r['pmr']<=255
        assert 0<=r['ctl']<=7 and r['bpr']<=7
        result.append(r)
    assert all(b['first']>a['last'] for a,b in zip(result,result[1:])), 'Counter did not progress between CPU samples'
    assert len({r['mpidr'] for r in result})==8, 'CPU affinity did not produce eight distinct CPUs'
    for marker in ['Kernel panic','BUG:','CFI failure','Unhandled fault','Unable to handle kernel']:
        assert after.count(marker)==before.count(marker), 'New kernel diagnostic: '+marker
    return result


def validate_recorded(out):
    before=(out/'before.txt').read_text()
    after=(out/'after.txt').read_text()
    assert (out/'load-unload.txt').read_text().splitlines()==[f'cpu{i}_load_unload=0' for i in range(8)]
    assert value(before,'boot_id')==value(after,'boot_id')
    assert value(before,'tainted')==value(after,'tainted')
    assert value(after,'boot_completed')=='1' and '\nEnforcing\n' in after
    assert not re.search(r'^ace_irq_timer ',after,re.M)
    samples=observations((out/'dmesg-before.txt').read_text(),(out/'dmesg-after.txt').read_text())
    def timer_counts(text):
        lines=[line for line in text.splitlines() if re.search(r'GICv3\s+27\s+Level\s+arch_timer',line)]
        assert len(lines)==1
        counts=[int(n) for n in lines[0].split(':',1)[1].split()[:8]]
        assert len(counts)==8
        return counts
    old,new=timer_counts(before),timer_counts(after)
    assert all(b>a for a,b in zip(old,new)), 'Android timer IRQ counts did not increase on all CPUs'
    return dict(passed=True,samples=samples,normal_load_unload_count=8,same_boot=True,taint_unchanged=True,
                android_timer_irq_deltas=[b-a for a,b in zip(old,new)],
                capture_sha256={n:sha(out/n) for n in ['before.txt','after.txt','load-unload.txt','remote-sha.txt','dmesg-before.txt','dmesg-after.txt']})


def main():
    if not __debug__:
        raise RuntimeError('Device verification requires Python without optimization')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--module',type=Path,required=True)
    p.add_argument('--qemu-result',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--load-readonly-module',action='store_true')
    p.add_argument('--verify-existing',action='store_true',help='Offline revalidation only')
    a=p.parse_args()
    assert not (a.verify_existing and a.load_readonly_module)
    module=a.module.resolve(); qemu=json.loads(a.qemu_result.read_text())
    build=json.loads((module.parent/'build-result.json').read_text())
    module_sha=sha(module)
    assert qemu['passed'] is True and qemu['exit_code']==0 and qemu['timed_out'] is False
    assert qemu['module_sha256']==module_sha==build['sha256']
    for report in (build,qemu):
        assert all(sha(HERE/n)==h for n,h in report['source_sha256'].items()), 'Changed validated source'
    out=a.output.resolve()
    assert out.is_relative_to(ROOT/'research/ace-irq-timer-live-20261019')
    if a.verify_existing:
        result=json.loads((out/'result.json').read_text())
        assert result['module_sha256']==module_sha and result['qemu_result_sha256']==sha(a.qemu_result)
        assert result['source_sha256']==sha(HERE/'ace_irq_timer.c')
        assert result['preflight_pass'] and result['execution_requested'] and result['cleanup_ok']
        assert (out/'remote-sha.txt').read_text().split()[0]==module_sha
        result.update(validate_recorded(out),revalidated_without_device_execution=True,parser_source_sha256=sha(HERE/'live.py'))
        destination=out/'result-verified.json'
        assert not destination.exists()
        destination.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2));return
    out.mkdir(parents=True,exist_ok=False)
    ids=[l.split()[0] for l in subprocess.check_output(['adb','devices'],text=True).splitlines()[1:] if l.endswith('\tdevice')]
    tls=[s for s in ids if s.endswith('_adb-tls-connect._tcp')]
    serial=tls[0] if len(tls)==1 else collect.select_device(None)
    adb=collect.Adb(serial,timeout=30)
    def read(command):
        b,e=adb.read(command,root=True)
        if e!='ok': raise RuntimeError('Device operation failed: '+e)
        return b
    def capture(name,command):
        b=read(command);(out/name).write_bytes(b);return b.decode(errors='replace')
    state='''printf 'model='; getprop ro.product.model
printf 'platform='; getprop ro.board.platform
printf 'kernel='; uname -r
printf 'slot='; getprop ro.boot.slot_suffix
printf 'boot_completed='; getprop sys.boot_completed
printf 'boot_id='; cat /proc/sys/kernel/random/boot_id
printf 'tainted='; cat /proc/sys/kernel/tainted
printf 'online='; cat /sys/devices/system/cpu/online
id
getenforce
cat /proc/modules
cat /proc/interrupts'''
    before=capture('before.txt',state)
    for k,v in [('model','PGKM10'),('platform','mt6895'),('kernel','5.10.236-android12-9-o-g6973d81cd2ac'),('slot','_b'),('boot_completed','1'),('online','0-7')]:
        assert value(before,k)==v, 'Wrong device state: '+k
    assert 'uid=0(root)' in before and '\nEnforcing\n' in before
    assert re.search(r'GICv3\s+27\s+Level\s+arch_timer',before)
    assert not re.search(r'^ace_irq_timer ',before,re.M)
    result=dict(passed=False,scope='Android EL1 observation only; NOT baremetal IRQ delivery or iOS',
                module_sha256=module_sha,qemu_result_sha256=sha(a.qemu_result),
                source_sha256=sha(HERE/'ace_irq_timer.c'),preflight_pass=True,
                execution_requested=a.load_readonly_module)
    def save(): (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    save()
    if not a.load_readonly_module:
        print('Preflight PASS; no module loaded');return
    remote='/data/local/tmp/ace_irq_timer-'+module_sha[:12]+'.ko'; quoted=shlex.quote(remote)
    assert read('[ ! -e '+quoted+' ]')==b'', 'Staging file exists'
    logs_before=capture('dmesg-before.txt','dmesg')
    attempted=False
    try:
        push=subprocess.run(['adb','-s',serial,'push',str(module),remote],capture_output=True,timeout=30)
        assert push.returncode==0, 'Staging failed'
        assert capture('remote-sha.txt','sha256sum '+quoted).split()[0]==module_sha
        commands=[]
        for cpu in range(8):
            commands.append(f'taskset {1<<cpu:x} insmod {quoted} || exit 1\nrmmod ace_irq_timer || exit 1\nprintf "cpu{cpu}_load_unload=0\\n"')
        attempted=True
        loaded=capture('load-unload.txt','\n'.join(commands))
        assert loaded.splitlines()==[f'cpu{i}_load_unload=0' for i in range(8)]
        after=capture('after.txt',state)
        logs_after=capture('dmesg-after.txt','dmesg')
        result.update(validate_recorded(out))
    finally:
        cleanup=('if grep -q "^ace_irq_timer " /proc/modules; then rmmod ace_irq_timer || exit 1; fi; ' if attempted else '')+'rm -f '+quoted+'; [ ! -e '+quoted+' ]'
        _,err=adb.read(cleanup,root=True)
        result['cleanup_ok']=err=='ok'
        if err!='ok': result['passed']=False
        save()
    print(json.dumps(result,indent=2))
    assert result['passed'] and result['cleanup_ok']


if __name__=='__main__': main()
