#!/usr/bin/env python3
"""Ace-only preflight; explicit normal load/unload of a QEMU-validated read-only probe."""
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
spec = importlib.util.spec_from_file_location('ace_collect', ROOT/'tools/ace-collect.py')
collect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collect)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(text, key):
    matches = re.findall('^'+re.escape(key)+'=(.*)$', text, re.M)
    assert len(matches)==1, 'Missing/ambiguous '+key
    return matches[0]


def header_observation(before, after):
    # Android dmesg inserts SGR controls between the tag and its colon.
    def plain(text): return re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text)
    before, after = plain(before), plain(after)
    old = re.findall(r'ACE_PMSG_HEADER: ([^\r\n]*)', before)
    new = re.findall(r'ACE_PMSG_HEADER: ([^\r\n]*)', after)
    assert len(new)==len(old)+1, 'Expected one new header observation'
    match = re.fullmatch(r'sig=([0-9a-f]+) start=(\d+) size=(\d+) capacity=(\d+) stable=(\d+) valid=(\d+) attempts=(\d+)',new[-1])
    assert match, 'Unexpected header result'
    sig, start, size, capacity, stable, valid, attempts = match.groups()
    assert sig=='43474244' and capacity=='65524' and stable=='1' and valid=='1'
    assert 0<=int(start)<=int(size)<=65524 and 1<=int(attempts)<=8
    for pattern in ['Kernel panic','BUG:','CFI failure']:
        assert after.count(pattern)==before.count(pattern), 'New kernel diagnostic: '+pattern
    return dict(sig=sig,start=int(start),size=int(size),capacity=int(capacity),stable=True,valid=True,attempts=int(attempts))


def validate_recorded(out):
    before, after = [(out/name).read_text() for name in ['before.txt','after.txt']]
    load = (out/'load-unload.txt').read_text()
    assert 'insmod_rc=0\n' in load and 'rmmod_rc=0\n' in load
    assert value(after,'boot_id')==value(before,'boot_id')
    assert value(after,'tainted')==value(before,'tainted')
    assert value(after,'boot_completed')=='1' and 'uid=0(root)' in after and '\nEnforcing\n' in after
    assert not re.search(r'^ace_pmsg_header ',after,re.M)
    h = header_observation((out/'dmesg-before.txt').read_text(errors='replace'),
                           (out/'dmesg-after.txt').read_text(errors='replace'))
    files = ['before.txt','after.txt','load-unload.txt','remote-sha.txt',
             'dmesg-before.txt','dmesg-after.txt','pstore-old-console.bin','pstore-old-pmsg.bin']
    return dict(passed=True,normal_load_unload=True,header=h,same_boot=True,
                taint_unchanged=True,no_residual_module=True,
                capture_sha256={name:sha(out/name) for name in files})


def main():
    if not __debug__:
        raise RuntimeError('Device checks require Python without optimization')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--module', type=Path, required=True)
    p.add_argument('--qemu-result', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--serial')
    p.add_argument('--load-readonly-module', action='store_true', help='Without this, only read preflight metadata')
    p.add_argument('--verify-existing', action='store_true', help='Validate saved evidence only; no device operation')
    a = p.parse_args()
    assert not (a.verify_existing and a.load_readonly_module)
    module = a.module.resolve()
    module_sha = sha(module)
    qemu = json.loads(a.qemu_result.read_text())
    build = json.loads((module.parent/'build-result.json').read_text())
    assert qemu['passed'] is True and qemu['module_sha256']==module_sha
    assert qemu['exit_code']==0 and qemu['timed_out'] is False
    assert build['sha256']==module_sha
    assert all(sha(HERE/name)==value for name,value in qemu['source_sha256'].items()), 'QEMU source changed'
    assert all(sha(HERE/name)==value for name,value in build['source_sha256'].items()), 'Build source changed'
    out = a.output.resolve()
    assert out.is_relative_to(ROOT/'research/ace-pmsg-header-20261019'), 'Output must be private'
    if a.verify_existing:
        result = json.loads((out/'result.json').read_text())
        assert result['module_sha256']==module_sha and result['qemu_result_sha256']==sha(a.qemu_result)
        assert result['source_sha256']==sha(HERE/'ace_pmsg_header.c')
        assert result['preflight_pass'] and result['execution_requested'] and result['cleanup_ok']
        assert (out/'remote-sha.txt').read_text().split()[0]==module_sha
        result.update(validate_recorded(out))
        result['revalidated_without_device_execution'] = True
        result['parser_source_sha256'] = sha(HERE/'live.py')
        destination = out/'result-verified.json'
        assert not destination.exists(), 'Do not overwrite an existing verification'
        destination.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2));return
    out.mkdir(parents=True, exist_ok=False)
    serial = collect.select_device(a.serial)
    adb = collect.Adb(serial, timeout=30)
    def read(command):
        data, error = adb.read(command,root=True)
        if error!='ok': raise RuntimeError('Device operation failed: '+error)
        return data
    def capture(name, command):
        data=read(command);(out/name).write_bytes(data);return data
    state_command = '''printf 'model='; getprop ro.product.model
printf 'platform='; getprop ro.board.platform
printf 'kernel='; uname -r
printf 'boot_completed='; getprop sys.boot_completed
printf 'boot_id='; cat /proc/sys/kernel/random/boot_id
printf 'tainted='; cat /proc/sys/kernel/tainted
printf 'slot='; getprop ro.boot.slot_suffix
id
getenforce
cat /proc/iomem
printf '\\nRAMOOPS\\n'
for path in /sys/module/ramoops/parameters/*; do printf '%s=' "${path##*/}"; cat "$path"; done
printf '\\nMODULES\\n'
cat /proc/modules'''
    before=capture('before.txt',state_command).decode()
    assert value(before,'model')=='PGKM10' and value(before,'platform')=='mt6895'
    assert value(before,'kernel')=='5.10.236-android12-9-o-g6973d81cd2ac'
    assert value(before,'boot_completed')=='1' and value(before,'slot')=='_b'
    assert 'uid=0(root)' in before and '\nEnforcing\n' in before
    assert re.search(r'^\s*48160000-4816ffff : ramoops:pmsg\s*$',before,re.M)
    for key, expected in [('mem_address','1208549376'),('mem_size','917504'),('pmsg_size','65536'),('mem_type','0'),('ecc','0')]:
        assert value(before,key)==expected,'Unexpected ramoops geometry/type'
    assert not re.search(r'^ace_pmsg_header ',before,re.M), 'Module already loaded'
    result=dict(scope='Fixed pmsg header observation in running Android; no pmsg writes, reset or flash',
                module_sha256=module_sha, qemu_result_sha256=sha(a.qemu_result),
                source_sha256=sha(HERE/'ace_pmsg_header.c'), preflight_pass=True,
                execution_requested=a.load_readonly_module, passed=False)
    def save(): (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    save()
    if not a.load_readonly_module:
        print('Ace preflight PASS; no module loaded.');return
    remote='/data/local/tmp/ace_pmsg_header-'+module_sha[:12]+'.ko'
    quoted=shlex.quote(remote)
    assert read('[ ! -e '+quoted+' ]')==b'', 'Temporary file already exists'
    capture('pstore-old-console.bin','cat /sys/fs/pstore/console-ramoops-0')
    capture('pstore-old-pmsg.bin','cat /sys/fs/pstore/pmsg-ramoops-0')
    dmesg_before=capture('dmesg-before.txt','dmesg').decode(errors='replace')
    attempted_load=False
    try:
        pushed=subprocess.run(['adb','-s',serial,'push',str(module),remote],capture_output=True,timeout=30)
        assert pushed.returncode==0, 'Module staging failed'
        remote_sha=capture('remote-sha.txt','sha256sum '+quoted).decode().split()[0]
        assert remote_sha==module_sha, 'Remote module hash mismatch'
        attempted_load=True
        load=capture('load-unload.txt', 'insmod '+quoted+'''
rc=$?
printf 'insmod_rc=%s\\n' "$rc"
if [ "$rc" -eq 0 ]; then
    rmmod ace_pmsg_header
    printf 'rmmod_rc=%s\\n' "$?"
fi
:''').decode()
        assert 'insmod_rc=0\n' in load and 'rmmod_rc=0\n' in load, 'Normal load/unload failed'
        after=capture('after.txt',state_command).decode()
        dmesg_after=capture('dmesg-after.txt','dmesg').decode(errors='replace')
        result.update(validate_recorded(out))
    finally:
        # Only our fixed module and newly staged file are eligible for cleanup.
        cleanup=('if grep -q "^ace_pmsg_header " /proc/modules; then rmmod ace_pmsg_header || exit 1; fi; '
                 if attempted_load else '')+'rm -f '+quoted+'; [ ! -e '+quoted+' ]'
        data,error=adb.read(cleanup,root=True)
        result['cleanup_ok']=error=='ok'
        if error!='ok': result['passed']=False
        save()
    print(json.dumps(result,indent=2))
    assert result['passed'] and result['cleanup_ok'], 'Device check or cleanup incomplete'


if __name__=='__main__': main()
