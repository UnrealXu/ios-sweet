#!/usr/bin/env python3
"""Finish one reviewed Ace experiment: reboot, collect pinned Android or RAM diagnostics,
then return to Fastboot. Never flashes, restores backups or changes slots.

Requires a guarded writer's candidate-flashed-awaiting-reboot state.json.
The candidate must itself implement token-bound automatic reset readout.
All phone evidence and device identity stay in the ignored research directory.
"""
from pathlib import Path
import argparse,datetime,hashlib,io,json,re,secrets,shlex,struct,subprocess,sys,tarfile,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ace_ram_readout as ram
import ace_forensic_readout as forensic
import ace_ram_rescue_readout as rescue
ROOT=Path(__file__).resolve().parents[1]
VENDOR_SHA='bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670'
class RootEvidenceError(RuntimeError):
    pass
class DiagnosticIdentityError(RootEvidenceError):
    pass

def read_root_evidence(cmd,timeout,run,find_adb,out,pause=time.sleep):
    """Four bounded read attempts, each on a refreshed verified identity.
    Preserve failed output/status rather than losing the cause of a stopped
    read. This helper cannot reboot and never reuses an unverified transport.
    """
    path=out/'root-read-observations.json'
    observations=json.loads(path.read_text()) if path.exists() else []
    for attempt in range(4):
        device=None;raw=b'';err=b'';code=None;error=None
        try:device=find_adb()
        except (RuntimeError,OSError,subprocess.TimeoutExpired) as exc:error=str(exc)
        if device:
            try:
                r=run(['adb','-s',device,'exec-out','su -c '+shlex.quote(cmd)],timeout)
                raw=r.stdout;err=r.stderr;code=r.returncode
            except (RuntimeError,OSError,subprocess.TimeoutExpired) as exc:
                error=str(exc)
                if isinstance(exc,subprocess.TimeoutExpired):
                    raw=exc.stdout or b'';err=exc.stderr or b''
        entry=dict(command=cmd,attempt=attempt,identity_verified=bool(device),
            returncode=code,error=error,stdout_bytes=len(raw),stderr_bytes=len(err))
        if code!=0:
            prefix='root-read-failure-'+str(len(observations))
            for suffix,data in [('.stdout',raw),('.stderr',err)]:
                name=prefix+suffix;(out/name).write_bytes(data)
                entry['stdout_file' if suffix=='.stdout' else 'stderr_file']=name
        observations.append(entry);path.write_text(json.dumps(observations,indent=2)+'\n')
        if code==0:return raw
        if attempt<3:pause(2)
    raise RootEvidenceError('root evidence collection failed; all read observations retained')

def record_log_failure(name,exc,out,errors):
    errors.append(dict(file=name,error=str(exc)))
    (out/'log-collection-errors.json').write_text(json.dumps(errors,indent=2)+'\n')
    (out/name).write_bytes(b'')

def optional_log_read(name,read,out,errors):
    """A missing Android log is evidence loss, not permission to skip return.
    Identity, current-token and partition-readback checks remain mandatory in
    the caller, including another fresh token check before any reboot.
    """
    try:data=read()
    except (RuntimeError,OSError,subprocess.TimeoutExpired) as exc:
        record_log_failure(name,exc,out,errors)
        data=b''
    (out/name).write_bytes(data)
    return data

def collect_seed_snapshot(record,token,read,out):
    """Verify an immutable, full pre-seed snapshot against this exact record.
    Only a candidate advertising this capability calls this helper. It never
    grants permission to repair RAM and never writes to the phone.
    """
    decoded=decode_record(record,token);w=struct.unpack('<32Q',record[32:])
    if not (decoded['stage']==5 and decoded['error']==-64 and w[31]==2**64-3):
        return dict(expected=False,verified=False)
    count=w[25]&0xffffffff;size=w[25]>>32
    if not 1<=count<=65536:raise RootEvidenceError('missing pre-seed observation for snapshot-capable image')
    before=read(ram.RECORD_COMMAND);(out/'pmsg-snapshot-record-before.bin').write_bytes(before)
    if before!=record:raise DiagnosticIdentityError('different record before pre-seed snapshot')
    raw=read('cat /sys/firmware/devicetree/base/chosen/ace,pmsg-before-seed')
    name='pmsg-before-seed.bin';(out/name).write_bytes(raw)
    after=read(ram.RECORD_COMMAND);(out/'pmsg-snapshot-record-after.bin').write_bytes(after)
    if after!=record:raise DiagnosticIdentityError('different record after pre-seed snapshot')
    if len(raw)!=65536 or int.from_bytes(raw[:8],'little')!=w[23] or int.from_bytes(raw[8:12],'little')!=size or sum(b!=0 for b in raw)!=count:
        raise RootEvidenceError('pre-seed snapshot length/header/nonzero-count mismatch; bytes retained')
    return dict(expected=True,verified=True,file=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
        signature=int.from_bytes(raw[:4],'little'),start=int.from_bytes(raw[4:8],'little'),size=size,nonzero_bytes=count,
        scope='Opaque pre-seed RAM evidence only; no repair or XNU/iOS claim')

def complete_tar(raw):
    """Container integrity only; individual AEE ZIP/token checks stay separate."""
    if len(raw)<1024 or len(raw)%512 or raw[-1024:]!=bytes(1024):return False
    try:
        with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as archive:
            members=archive.getmembers()
            return bool(members) and all(
                member.offset_data+((member.size+511)//512)*512<=len(raw)-1024
                for member in members if member.isfile())
    except (tarfile.TarError,OSError,ValueError):return False

def collect_aee_archive(out,find_adb,read,pause=time.sleep):
    """At most three read attempts, each after a fresh identity-bound lookup.

    Keep every observation, including incomplete data. An exhausted read does
    not trigger a reboot retry or prevent the normal guarded Fastboot return.
    A complete tar does not establish that a current-token AEE record exists.
    """
    observations=[];lookups=[]
    for attempt in range(3):
        device=None
        for lookup in range(5):
            device=find_adb()
            lookups.append(dict(read_attempt=attempt,lookup=lookup,identity_verified=bool(device)))
            (out/'aee-identity-observations.json').write_text(json.dumps(lookups,indent=2)+'\n')
            if device:break
            if lookup<4:pause(2)
        if not device:
            # A USB/TLS transition can briefly hide both transports. These are
            # identity lookup waits only, never extra archive/reboot attempts.
            # Keep any partial archive and let the normal token-guarded return
            # handle its own fresh identity; absence never authorizes reboot.
            if not (out/'aee-after.tar').exists():(out/'aee-after.tar').write_bytes(b'')
            (out/'aee-read-observations.json').write_text(json.dumps(observations,indent=2)+'\n')
            return dict(complete_tar=False,attempts=observations,
                limitation='AEE transport absent after five identity lookups; no unverified read or reboot retry')
        raw=read(device)
        name='aee-after-attempt-'+str(attempt)+'.tar'
        (out/name).write_bytes(raw)
        valid=complete_tar(raw)
        observations.append(dict(file=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),complete_tar=valid))
        (out/'aee-read-observations.json').write_text(json.dumps(observations,indent=2)+'\n')
        (out/'aee-after.tar').write_bytes(raw)
        if valid:return dict(complete_tar=True,attempts=observations)
    return dict(complete_tar=False,attempts=observations,
        limitation='AEE tar incomplete after three identity-refreshed reads; retained partial data is not independently verified AEE')

def capture_screen(device,out,run,profile="android-v1"):
    """Best-effort screenshot through an already identity-verified transport."""
    try:
        result=run(['adb','-s',device,'exec-out','screencap','-p'])
        raw=result.stdout
        if result.returncode or len(raw)<33 or raw[:8]!=b'\x89PNG\r\n\x1a\n' or raw[12:16]!=b'IHDR':
            return dict(saved=False,reason='screencap failed or invalid PNG')
        path=out/('ram-screen.png' if profile==ram.READY else 'android-screen.png');path.write_bytes(raw)
        return dict(saved=True,file=path.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
            interpretation=('RAM Android diagnostic screen only; not XNU/iOS display proof' if profile==ram.READY else 'Android diagnostic screen only; not XNU/iOS display proof'))
    except (RuntimeError,OSError,subprocess.TimeoutExpired):
        return dict(saved=False,reason='screenshot transport unavailable; continue log collection')
def decode_record(b,token):
    if len(b)!=288 or b[:8]!=b'ACEFALL1' or b[8:24]!=token.encode() or b[24:32]!=bytes(8):
        raise ValueError('diagnostic property size/magic/token/padding mismatch')
    w=struct.unpack('<32Q',b[32:]);signed=lambda x:x if x<1<<63 else x-(1<<64)
    if w[:2]!=(0x313054414e454341,1) or not 1<=w[2]<=7 or not -127<=signed(w[3])<0 or w[20]!=0:
        raise ValueError('native diagnostic header/stage/error/handoff mismatch')
    return dict(stage=w[2],error=signed(w[3]),automatic_pending_trial_return=w[2]==5 and signed(w[3])==-67,
        record_sha256=hashlib.sha256(b).hexdigest(),ios_usable=False)
def verify_return_record(expected,read,max_attempts=3,pause=time.sleep):
    """Retry only incomplete read observations; a complete other record stops.
    read must refresh the expected phone identity and retain every observation.
    No reboot or other device mutation takes place here.
    """
    if not 1<=max_attempts<=3:raise RuntimeError('return record read budget exhausted')
    for attempt in range(max_attempts):
        current=read(attempt)
        if current==expected:return
        if len(current)==288 and current[:8]==b'ACEFALL1':
            raise RuntimeError('different complete diagnostic record before bootloader return')
        if attempt+1<max_attempts:pause(1)
    raise RuntimeError('diagnostic record unreadable before bootloader return; observations retained')

def retain_return_observation(out,state,expected,raw,transport_present):
    """Retain absent transport as an empty read, within one global3-read budget."""
    observations=state.setdefault('return_record_observations',[])
    if len(observations)>=3:raise RuntimeError('return record read budget exhausted')
    name='return-record-observation-'+str(len(observations))+'.bin'
    (out/name).write_bytes(raw)
    observations.append(dict(file=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
        matches_expected=raw==expected,identity_refreshed_transport_present=bool(transport_present)))
    return raw

def reboot_expected_phone(initial_device,find_adb,expected_fastboot,check_token,run):
    """Refresh identity-bound transport; retry only a proved no-device failure.
    find_adb must verify the expected serial. check_token must compare the
    current diagnostic record. Ambiguous errors are observed, never retried.
    Caller must still verify physical Fastboot and its product/slot identity.
    """
    attempts=[]
    if expected_fastboot():return attempts
    device=find_adb() or initial_device
    if not device:raise RuntimeError('expected ADB unavailable before bootloader return')
    check_token(device)
    try:result=run(['adb','-s',device,'reboot','bootloader'])
    except (RuntimeError,subprocess.TimeoutExpired) as error:
        attempts.append(dict(returncode=None,output='Ambiguous transport exception: '+str(error)+'\n'))
        return attempts
    attempts.append(dict(returncode=result.returncode,output=(result.stdout+result.stderr).decode(errors='replace')))
    missing=result.returncode and not result.stdout and result.stderr.strip() in (b'error: device not found', f"error: device '{device}' not found".encode())
    if missing and not expected_fastboot():
        device=find_adb()
        if device:
            check_token(device)
            try:result=run(['adb','-s',device,'reboot','bootloader'])
            except (RuntimeError,subprocess.TimeoutExpired) as error:
                attempts.append(dict(returncode=None,output='Ambiguous transport exception: '+str(error)+'\n'))
                return attempts
            attempts.append(dict(returncode=result.returncode,output=(result.stdout+result.stderr).decode(errors='replace')))
    return attempts

class EarlyFastbootFailureObserver:
    """Read-only explicit-rescue timeline; caller constructs only after reboot ACK."""
    def __init__(self,out,state,serial):
        self.out=out;self.state=state;self.serial=serial;self.departure=None
        self.started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def check(self,elapsed,find_adb,run):
        observations=self.state.setdefault('early_fastboot_observations',[])
        probe=dict(format='ACE_EARLY_FASTBOOT_PROBE_V1',elapsed_seconds=elapsed,
            utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),commands=[])
        def read(argv):
            utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
            try:
                r=run(argv);code=r.returncode;stdout=r.stdout;stderr=r.stderr;error=None
            except (OSError,subprocess.TimeoutExpired) as exc:
                code=None;stdout=getattr(exc,'stdout',None) or b'';stderr=getattr(exc,'stderr',None) or b'';error=str(exc)
            probe['commands'].append(dict(argv=argv,utc=utc,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),returncode=code,stdout_hex=stdout.hex(),stderr_hex=stderr.hex(),
                raw_sha256=hashlib.sha256(stdout+stderr).hexdigest(),error=error))
            return code,stdout,stderr
        def expected(code,stdout):
            return code==0 and any(row.split()==[self.serial.encode(),b'fastboot'] for row in stdout.splitlines())
        def retain(reason):
            probe['reason']=reason;name='early-fastboot-probe-'+str(len(observations))+'.json'
            path=self.out/name;path.write_text(json.dumps(probe,indent=2)+'\n')
            item=dict(file=name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),elapsed_seconds=elapsed,utc=probe['utc'],reason=reason)
            observations.append(item);return item
        code,stdout,stderr=read(['fastboot','devices'])
        present=expected(code,stdout)
        if code==0 and not present:
            item=retain('expected-fastboot-absent')
            if self.departure is None:self.departure=item
            return None,None
        if not present:
            retain('fastboot-observation-unavailable');return None,None
        if self.departure is None or elapsed<10:
            retain('no-proved-departure-or-too-early');return None,None
        values=[('product','k6895v1_64'),('current-slot','b'),('unlocked','yes'),('is-userspace','no')]
        for key,value in values:
            code,stdout,stderr=read(['fastboot','-s',self.serial,'getvar',key])
            if code!=0 or re.search(rb'(?m)^[ \t]*(?:\(bootloader\)[ \t]*)?'+re.escape(key.encode())+rb':[ \t]*'+re.escape(value.encode())+rb'(?=\s|$)',stdout+stderr) is None:
                retain('firmware-identity-not-verified');return None,None
        code,stdout,stderr=read(['fastboot','devices'])
        if not expected(code,stdout):retain('fastboot-left-during-identity-check');return None,None
        # Retain fresh ADB inventory too. Unavailable inventory or an online
        # expected candidate is insufficient evidence for an early failure.
        code,stdout,stderr=read(['adb','devices'])
        if code!=0:retain('adb-observation-unavailable');return None,None
        for row in stdout.splitlines():
            fields=row.split()
            if len(fields)>=2 and fields[1]==b'device' and (fields[0]==self.serial.encode() or fields[0].startswith(('adb-'+self.serial+'-').encode())):
                device=find_adb();retain('diagnostic-adb-candidate-now-available');return device,None
        # Recheck after all reads: newly available verified ADB always wins.
        device=find_adb()
        if device:retain('diagnostic-adb-now-available');return device,None
        final=retain('verified-physical-fastboot-without-adb')
        receipt=dict(format='ACE_EARLY_PHYSICAL_FASTBOOT_FAILURE_V1',run_token=self.state['run_token'],
            candidate_sha256=self.state['candidate_sha256'],explicit_rescue_profile=True,
            normal_reboot_acknowledged=True,normal_reboot_log_sha256=hashlib.sha256((self.out/'normal-reboot.log').read_bytes()).hexdigest(),
            observer_started_utc=self.started_utc,elapsed_seconds=elapsed,minimum_elapsed_seconds=10,
            departure=self.departure,physical_fastboot=final,adb_identity_available=False,
            trial_restarted=False,reboot_commands_after_ack=0,partition_writes_after_ack=[],ios_usable=False)
        path=self.out/'early-fastboot-failure.json';path.write_text(json.dumps(receipt,indent=2)+'\n')
        return None,dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('transport_json',type=Path);parser.add_argument('trial_directory',type=Path)
    parser.add_argument('--ufs-reference-snapshots',action='store_true',help='read at most8192bytes from each Android sda..sdd after diagnostics, before returning Fastboot')
    parser.add_argument('--diagnostic-readout-only',action='store_true',help='explicitly authorized recovery exception; no XNU attempt and no pmsg initialization')
    a=parser.parse_args();out=a.trial_directory.resolve()
    if not out.is_relative_to(ROOT/'research') or not (out/'state.json').is_file():raise ValueError('existing ignored trial state required')
    state=json.loads((out/'state.json').read_text());serial=json.loads(a.transport_json.read_text())['usb_adb'];token=state['run_token']
    if not __debug__ or state.get('phase')!='candidate-flashed-awaiting-reboot' or not state.get('candidate_flash_succeeded'):
        raise ValueError('fresh guarded auto-readout candidate flash required; never repeat a reboot/flash')
    state['controller_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    recovery=None
    if a.diagnostic_readout_only:
        recovery=forensic.validate_request(state,out,serial,state['controller_sha256'])
    elif not state.get('auto_readout_after_reset') or state.get('diagnostic_readout_only'):
        raise ValueError('normal trial requires automatic readout; diagnostic-only mode must be explicit')
    state['controller_version']='transport-refresh-v7-explicit-forensic-recovery'
    contract=ram.load_contract(state,out,serial,state['controller_sha256'])
    rescue_contract=rescue.load_contract(state,out,serial,state['controller_sha256'],contract)
    rescued=False
    if contract and a.ufs_reference_snapshots:raise ValueError('UFS reference snapshots are Android-profile only')
    def save(phase):
        state['phase']=phase;state['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();tmp=out/'state.json.tmp';tmp.write_text(json.dumps(state,indent=2)+'\n');tmp.replace(out/'state.json')
    def run(argv,timeout=15):
        # Preserve TimeoutExpired's partial stdout/stderr for read evidence.
        return subprocess.run(argv,capture_output=True,timeout=timeout)
    def root(device,cmd,timeout=60):
        if contract:return ram_reader.read(cmd,timeout)
        return read_root_evidence(cmd,timeout,run,find_adb,out)
    def find_adb():
        r=run(['adb','devices']);devices=[l.split()[0] for l in r.stdout.decode().splitlines() if len(l.split())==2 and l.split()[1]=='device']
        for device in sorted(devices,key=lambda x:x!=serial):
            # Never operate on an unrelated attached phone.
            if device!=serial and not device.startswith('adb-'+serial+'-'):continue
            r=run(['adb','-s',device,'shell','getprop ro.serialno'])
            if r.returncode==0 and r.stdout.decode().strip()==serial:return device
        return None
    def expected_fastboot():
        r=run(['fastboot','devices']);return any(l.split()==[serial.encode(),b'fastboot'] for l in r.stdout.splitlines())
    ram_reader=ram.EvidenceReader(out,find_adb,run) if contract else None
    if not expected_fastboot():raise RuntimeError('expected Fastboot device unavailable before normal reboot')
    save('automatic-trial-normal-reboot-started')
    r=run(['fastboot','-s',serial,'reboot']);(out/'normal-reboot.log').write_bytes(r.stdout+r.stderr)
    if r.returncode:save('normal-reboot-failed-no-retry');raise RuntimeError('normal reboot rejected; no automatic retry')
    # RAM startup includes a separately bounded 90s module supervisor. Keep
    # the original Android allowance and give that stage its complete budget.
    # Explicit rescue only:120s native prepare +150s RAM guard +120s rescue
    # validation +150s Android/module/readout margin. Other profiles unchanged.
    adb_deadline=540 if rescue_contract else 240 if contract else 150
    state['adb_return_deadline_seconds']=adb_deadline
    start=time.monotonic();device=None
    early_fastboot=EarlyFastbootFailureObserver(out,state,serial) if rescue_contract else None
    while time.monotonic()-start<adb_deadline:
        device=find_adb()
        if device:break
        if early_fastboot:
            device,failure=early_fastboot.check(time.monotonic()-start,find_adb,run)
            if device:break
            if failure:
                state['early_fastboot_failure']=failure
                state['adb_return_seconds']=round(time.monotonic()-start,1)
                save('early-fastboot-without-diagnostic-adb-no-retry')
                raise RuntimeError('expected physical firmware Fastboot returned before diagnostic ADB; no retry')
            save('automatic-trial-waiting-diagnostic-adb')
        time.sleep(2)
    state['adb_return_seconds']=round(time.monotonic()-start,1)
    if not device:
        save('no-adb-after-'+str(adb_deadline)+'s-no-retry')
        raise RuntimeError('automatic readout did not return within'+str(adb_deadline)+'s; retained state, no blind writes')
    save('automatic-diagnostic-adb-returned');print('Expected diagnostic ADB returned in',state['adb_return_seconds'],'seconds',flush=True)
    forensic_screen=capture_screen(device,out,run) if recovery else None
    if recovery:(out/'forensic-screen-capture.json').write_text(json.dumps(forensic_screen,indent=2)+'\n')
    ram_screen=capture_screen(device,out,run,ram.READY) if contract and not rescue_contract else None
    if contract:(out/'ram-screen-capture.json').write_text(json.dumps(ram_screen,indent=2)+'\n')
    record=root(device,ram.RECORD_COMMAND);(out/'readout-record.bin').write_bytes(record)
    result=decode_record(record,token)
    rescue_result=rescue.classify(record,token,rescue_contract)
    rescued=rescue_result['selected']
    if rescued:
        result.update(rescue_result)
        state['ramdiag_result']='failed-rescued-to-android'
        state['independent_of_userdata_verified']=False
        # Initial direct read is of the world-readable current sysfs property.
        # Only an explicitly pinned selected record switches to Android su.
        contract=None;ram_reader=None
    elif contract and rescue_contract:
        capability=root(device,'cat /sys/firmware/devicetree/base/chosen/ace,ram-rescue')
        (out/'ram-rescue-capability.bin').write_bytes(capability)
        if capability!=bytes.fromhex(rescue_contract['first_ram_capability_hex']):
            save('ram-rescue-capability-mismatch');raise RuntimeError('RAM exact current-token rescue capability mismatch')
        result['ram_rescue_capability_verified']=True
        ram_screen=capture_screen(device,out,run,ram.READY)
        (out/'ram-screen-capture.json').write_text(json.dumps(ram_screen,indent=2)+'\n')
    if recovery:result.update(forensic.prior_observation(record,recovery['prior_run_token']))
    (out/'readout-result.json').write_text(json.dumps(result,indent=2)+'\n')
    if contract:
        try:result.update(ram.collect(ram_reader.read,contract,out,secrets.token_hex(16)))
        except (ValueError,RuntimeError,KeyError):
            save('ram-diagnostic-contract-mismatch');raise
        result['screen_capture']=ram_screen
    else:
        stable=False
        for _ in range(45):
            device=find_adb()
            if device:
                r=run(['adb','-s',device,'shell','getprop sys.boot_completed'])
                if r.returncode==0 and r.stdout.strip()==b'1':stable=True;break
            time.sleep(2)
        if not stable:save('diagnostic-root-returned-android-not-complete');raise RuntimeError('Android diagnostic boot not complete; no forced reboot')
        text=root(device,'getprop sys.boot_completed; getprop ro.boot.slot_suffix; id; getenforce; sha256sum /dev/block/by-name/boot_b /dev/block/by-name/vendor_boot_b')
        (out/'android-stable.txt').write_bytes(text)
        if not text.startswith(b'1\n_b\n') or b'uid=0(root)' not in text or state['candidate_sha256'].encode() not in text or VENDOR_SHA.encode() not in text:
            save('diagnostic-identity-or-hash-mismatch');raise RuntimeError('boot/slot/root/vendor readback mismatch; stopped')
        result['screen_capture']=forensic_screen if recovery else capture_screen(device,out,run)
    log_errors=[]
    if not contract and state.get('pmsg_seed_snapshot_required'):
        try:result['seed_snapshot']=collect_seed_snapshot(record,token,lambda cmd:root(device,cmd,120),out)
        except DiagnosticIdentityError:raise
        except (RuntimeError,OSError,subprocess.TimeoutExpired) as exc:
            log_errors.append(dict(file='pmsg-before-seed.bin',error=str(exc)))
            (out/'log-collection-errors.json').write_text(json.dumps(log_errors,indent=2)+'\n')
            result['seed_snapshot']=dict(expected=True,verified=False,error=str(exc))
    for file,cmd in [('pstore-after.tar','tar -cf - /sys/fs/pstore 2>/dev/null'),('dmesg-after.txt','dmesg')]:
        if contract:(out/file).write_bytes(root(device,cmd,120))
        else:optional_log_read(file,lambda:root(device,cmd,120),out,log_errors)
    if not contract:
        try:
            result['aee_archive']=collect_aee_archive(out,find_adb,
                lambda current:root(current,'tar -cf - /data/vendor/aee_exp 2>/dev/null',120))
        except (RuntimeError,OSError,subprocess.TimeoutExpired) as exc:
            record_log_failure('aee-after.tar',exc,out,log_errors)
            result['aee_archive']=dict(complete_tar=False,limitation=str(exc))
        if not result['aee_archive']['complete_tar']:
            print(result['aee_archive']['limitation'],flush=True)
    if a.ufs_reference_snapshots:
        references={}
        for disk in ['sda','sdb','sdc','sdd']:
            data=root(device,'if [ -b /dev/block/'+disk+' ]; then dd if=/dev/block/'+disk+' bs=4096 count=2 2>/dev/null; fi')
            if len(data) not in (0,8192):raise RuntimeError('bounded UFS reference read length mismatch')
            if not data:continue
            metadata=root(device,'cat /sys/class/block/'+disk+'/queue/logical_block_size /sys/class/block/'+disk+'/size')
            name='ufs-reference-'+disk+'.bin';(out/name).write_bytes(data)
            references[disk]=dict(file=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),logical_block_size_and_512_sector_count=metadata.decode().splitlines())
        (out/'ufs-reference.json').write_text(json.dumps(references,indent=2)+'\n')
        result['ufs_references_manifest_sha256']=hashlib.sha256((out/'ufs-reference.json').read_bytes()).hexdigest()
    evidence=['readout-record.bin','pstore-after.tar','dmesg-after.txt']
    evidence += [name for name in ['pmsg-before-seed.bin','pmsg-snapshot-record-before.bin','pmsg-snapshot-record-after.bin'] if (out/name).exists()]
    evidence+=['ram-identity-snapshot.bin','ram-partition-boot_b.txt','ram-partition-vendor_boot_b.txt','ram-command-observations.json','ram-screen-capture.json'] if contract else ['android-stable.txt','aee-after.tar']
    result['artifacts']={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in evidence}
    result['log_collection_errors']=log_errors
    result['log_collection_complete']=not log_errors and (bool(contract) or result['aee_archive']['complete_tar'])
    result['boot_and_vendor_readback_verified']=True;(out/'readout-result.json').write_text(json.dumps(result,indent=2)+'\n');save('diagnostics-collected-returning-fastboot')
    def check_return_token(current):
        def read(attempt):
            if len(state.get('return_record_observations',[]))>=3:
                raise RuntimeError('return record read budget exhausted')
            refreshed=find_adb()
            raw=b'' if not refreshed else (ram_reader.read(ram.RECORD_COMMAND,allow_failure=True) if contract else forensic.observe_return_record(refreshed,out,len(state.get('return_record_observations',[])),lambda argv:subprocess.run(argv,capture_output=True,timeout=20)))
            retain_return_observation(out,state,record,raw,bool(refreshed))
            save('diagnostics-collected-returning-fastboot')
            return raw
        verify_return_record(record,read,3-len(state.get('return_record_observations',[])))
    attempts=reboot_expected_phone(device,find_adb,expected_fastboot,check_return_token,run)
    state['return_fastboot_attempts']=attempts
    state['return_transport_refresh_used']=len(attempts)>1 or any(x['returncode']!=0 for x in attempts)
    (out/'return-fastboot.log').write_text(''.join(x['output'] for x in attempts))
    save('diagnostics-collected-awaiting-fastboot-observation')
    start=time.monotonic()
    while time.monotonic()-start<45:
        if expected_fastboot():break
        time.sleep(2)
    else:save('diagnostics-collected-fastboot-not-found');raise RuntimeError('Fastboot unavailable after diagnostic reboot; evidence retained')
    checks={}
    for key,expected in [('product','k6895v1_64'),('current-slot','b'),('unlocked','yes'),('is-userspace','no')]:
        r=run(['fastboot','-s',serial,'getvar',key]);raw=r.stdout+r.stderr;checks[key]=raw.decode(errors='replace')
        if r.returncode or (key+': '+expected).encode() not in raw:
            save('diagnostics-collected-fastboot-identity-mismatch');raise RuntimeError('Fastboot identity mismatch')
    (out/'fastboot-ready.json').write_text(json.dumps(checks,indent=2)+'\n')
    # Return-token reads append command observations; finalize their hash only
    # after the last read rather than leaving a stale evidence-manifest digest.
    if contract:
        result['artifacts']={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in evidence}
        (out/'readout-result.json').write_text(json.dumps(result,indent=2)+'\n')
    if recovery:state['diagnostic_only_return_verified']=True
    state['diagnostics_complete']=result['log_collection_complete']
    state['automatic_loop_verified']=result['automatic_pending_trial_return'] and not rescued
    if rescued:state['android_rescue_return_verified']=True
    state['ios_usable']=False;save('diagnostics-collected-fastboot-ready')
    print(json.dumps(dict(automatic_pending_trial_return=result['automatic_pending_trial_return'],diagnostics_collected=result['log_collection_complete'],expected_fastboot_ready=True,ios_usable=False)),flush=True)
if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError,KeyError,subprocess.TimeoutExpired) as e:print('Auto trial stopped: '+str(e),file=sys.stderr);sys.exit(1)
