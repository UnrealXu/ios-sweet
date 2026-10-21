#!/usr/bin/env python3
"""Offline package/prepare/validate an Ace RAM diagnostic trial. No phone calls."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ace_ram_readout as ram

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
chain=load('ace_ram_chain',ROOT/'tools/ace-stock-chain-boot.py')
cpio=load('ace_ram_cpio',ROOT/'tools/ace-recovery-diag.py')
need=ram.require
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def private(path):
    path=Path(path).resolve();need(path.is_relative_to(ROOT/'research'),'private research artifact required');return path

def ref(path):return str(private(path).relative_to(ROOT))
def get(name):return private(ROOT/name)
def source_pins(pins):
    for name,pin in pins.items():
        need(not Path(name).is_absolute() and '..' not in Path(name).parts and sha(ROOT/name)==pin,'source changed: '+name)

def validate_package(path,pin):
    path=private(path);need(ram.digest(pin) and sha(path)==pin,'candidate manifest pin mismatch')
    m=json.loads(path.read_text());need(m['format']=='ACE_RAM_CANDIDATE_V1' and m['ios_usable'] is False,'candidate format/scope')
    source_pins(m['source_sha256'])
    for name,pin in m['artifact_sha256'].items():need(sha(get(name))==pin,'candidate artifact changed: '+name)
    image=get(m['candidate_file']).read_bytes();need(len(image)==ram.PARTITION_BYTES and ram.sha(image)==m['candidate_sha256'],'candidate full extent/hash')
    layout=chain.boot.boot_v4(image)
    native=chain.boot.inflate(image[layout['kernel_offset']:layout['kernel_offset']+layout['kernel_bytes']],0x5000000)
    need(ram.sha(native)==m['native_image_sha256'],'candidate native extraction mismatch')
    generic=image[layout['ramdisk_offset']:layout['ramdisk_offset']+layout['ramdisk_bytes']]
    need(ram.sha(generic)==m['generic_sha256'],'candidate generic extraction mismatch')
    need(sha(chain.BACKUP)==chain.BACKUP_SHA and sha(ROOT/'research/ace-backup-20261019-wireless-v2/vendor_boot_b.img')==ram.VENDOR_SHA,'original backup mismatch')
    return m

def package(native_root,physical,ci_path,output):
    native_root,physical,ci_path,output=map(private,[native_root,physical,ci_path,output])
    need(not output.exists(),'new candidate output required')
    native=native_root/'native';m=json.loads((native/'build-manifest.json').read_text());profile=json.loads((physical/'manifest.json').read_text());ci=json.loads(ci_path.read_text())
    need(profile['format']=='ACE_PHYSICAL_RAMDISK_V1' and profile['kernel_sha256']==ram.KERNEL_SHA and profile['vendor_sha256']==ram.VENDOR_SHA,'physical kernel/vendor pins')
    need(m['run_token']==profile['run_token'] and m['auto_readout_after_reset'] and m['initialize_empty_pmsg'] and m['text_offset']==0,'native token/automatic profile mismatch')
    need(m['refusal_android']['sha256']==ram.KERNEL_SHA and m['refusal_android']['enabled'],'refusal kernel pin')
    need(ci['ci_conclusion']=='success' and ci['linked_observations_verified'] and ci['kernel_sha256']==m['kernel_sha256'],'CI linked kernel mismatch')
    need(ci['ci_run']==39429611804 and ci['ci_job']==118650915354,'reviewed actual0112 CI provenance required')
    sources={}
    for pins in [m['source_sha256'],profile['source_sha256'],profile['base_report']['source_sha256'],json.loads((physical/'bundle/report.json').read_text())['source_sha256']]:
        source_pins(pins);sources.update(pins)
    artifacts={}
    def retain(path):artifacts[ref(path)]=sha(path)
    for path in [ci_path,native/'build-manifest.json',physical/'manifest.json',physical/'bundle/report.json']:retain(path)
    image=(native/'native.Image').read_bytes();need(ram.sha(image)==m['image_sha256'] and len(image)<0x4e00000 and m['image_load_window']==[0x40000000,0x45000000],'native Image/layout guard')
    retain(native/'native.Image')
    symbols=json.loads((native/'symbols.json').read_text());retain(native/'symbols.json')
    need(ram.sha(image[symbols['android_payload']:symbols['android_payload_end']])==ram.KERNEL_SHA,'embedded refusal bytes')
    line=(native/'ace.payload').read_bytes()[72:680].split(b'\0',1)[0].decode();retain(native/'ace.payload')
    need(line==m['command_line'] and line.split().count('-noprogress')==1 and '-progress' not in line.split(),'headless native args')
    for folder,script,count in [('preflight','verify.py',9),('c-entry','verify_c_entry.py',None),('qemu-verified','verify_refusal.py',5)]:
        path=native_root/folder/'verification.json';r=json.loads(path.read_text());retain(path)
        need(r['status'].startswith('PASS QEMU') and r['image_sha256']==m['image_sha256'] and r['verifier_sha256']==sha(ROOT/'ace/native-loader'/script),'stale native verifier '+folder)
        source_pins(r.get('source_sha256',{}));sources.update(r.get('source_sha256',{}));sources['ace/native-loader/'+script]=r['verifier_sha256']
        if count:need(len(r['cases'])==count and all(c['passed'] for c in r['cases']),'native verifier cases missing')
        if folder=='qemu-verified':need(any(c.get('durable_handoff_record_verified') is True and c.get('pending_handoff_fixture_is_synthetic') is True for c in r['cases']),'durable Android handoff case missing')
        if folder=='preflight':need(sum(c['token_bound_kernel_marker_checked'] for c in r['cases'])==4 and any(c['case']=='auto-reset-refusal' and c['passed'] for c in r['cases']),'pending latch case missing')
        elif folder=='c-entry':need(r['first_c_instruction_executed'] and r['token_bound_kernel_marker_checked'],'C entry proof missing')
        else:need(sum(c['guest_record_readback_verified'] for c in r['cases'])==3 and sum(c['fallback_guard_error']!=0 for c in r['cases'])==2,'refusal checks missing')
        for case in r.get('cases',[]):
            for name,pin in case['dumps_sha256'].items():
                path=private(native_root/folder/case['case']/name);need(sha(path)==pin,'verifier dump changed');retain(path)
    generic=(physical/'physical-generic.lz4').read_bytes();need(ram.sha(generic)==profile['generic_sha256'],'physical ramdisk pin')
    raw=subprocess.run(['lz4','-dc'],input=generic,capture_output=True,check=True).stdout
    files={}
    for n,f,d in cpio.read_cpio(raw):
        if n=='TRAILER!!!':continue
        need(n not in files,'duplicate physical member');files[n]=(f,d)
    need(set(files)==set(profile['files']),'physical member set changed')
    for n,(f,d) in files.items():need(profile['files'][n]==dict(sha256=ram.sha(d),bytes=len(d),mode=oct(f[1])),'physical archive entry changed')
    guest=files['ace-ramdiag/profile.json'][1];need(ram.sha(guest)==profile['guest_profile_sha256'] and json.loads(guest)['run_token']==m['run_token'],'embedded guest profile mismatch')
    retain(physical/'physical-generic.lz4')
    compressed=chain.boot.deterministic_gzip(image);candidate,_,_,_=chain.package(chain.BACKUP.read_bytes(),compressed,diagnostic_ramdisk=generic,diagnostic_ramdisk_sha256=profile['generic_sha256'])
    output.mkdir(mode=0o700);candidate_path=output/'experimental-ramdiag-boot-b.img';candidate_path.write_bytes(candidate);retain(candidate_path)
    for name in ['tools/ace-ram-candidate.py','tools/ace-stock-chain-boot.py','tools/ace-probe-boot.py','tools/ace-recovery-diag.py','tools/ace-auto-trial.py','tools/ace_ram_readout.py','tools/ace_forensic_readout.py']:sources[name]=sha(ROOT/name)
    report=dict(format='ACE_RAM_CANDIDATE_V1',ios_usable=False,phone_io=False,candidate_file=ref(candidate_path),candidate_sha256=ram.sha(candidate),native_image_sha256=m['image_sha256'],generic_sha256=profile['generic_sha256'],
                run_token=m['run_token'],serial=profile['serial'],bundle_id=profile['bundle_id'],guest_profile_sha256=profile['guest_profile_sha256'],partitions=profile['partitions'],
                auto_readout_after_reset=True,source_sha256=sources,artifact_sha256=artifacts,original_boot_sha256=chain.BACKUP_SHA,
                limitations=['physical full RAM startup/return unproven','original AVB bytes relocated; no valid signature assertion','no iOS/display/touch/rootfs proof'])
    path=output/'manifest.json';path.write_text(json.dumps(report,indent=2)+'\n');validate_package(path,sha(path));return path

def failed_install_evidence(failed,verified,new_candidate):
    """Historical write acknowledgement only, never permission to replay it.

    Sources of the old image may now be obsolete. Check retained bytes and
    its consumed ledger; current source validation remains mandatory for the
    NEW candidate via validate_package. This is not a partition readback.
    """
    failed,verified=map(private,[failed,verified])
    old=json.loads((failed/'state.json').read_text())
    need(old['phase']=='no-adb-after-240s-no-retry','intervening trial is not the known terminal RAM timeout')
    need(old['candidate_flash_succeeded'] is True and type(old['candidate_flash_returncode']) is int and old['candidate_flash_returncode']==0,'intervening flash not acknowledged')
    writes=old['partition_writes_started']
    need(len(writes)==1 and writes[0]['partition']=='boot_b' and writes[0]['sha256']==old['candidate_sha256'],'intervening write ledger mismatch')
    need(get(old['previous_trial_file'])==verified/'state.json' and old['previous_trial_state_sha256']==sha(verified/'state.json'),'intervening trial ancestry mismatch')
    baseline=json.loads((verified/'state.json').read_text())
    need(old['previous_boot_b_sha256']==baseline['candidate_sha256'],'intervening previous hash mismatch')
    path=get(old['candidate_manifest_file']);need(sha(path)==old['candidate_manifest_sha256'],'historical package manifest changed')
    m=json.loads(path.read_text())
    need(m['format']=='ACE_RAM_CANDIDATE_V1' and m['serial']==new_candidate['serial'] and m['candidate_sha256']==old['candidate_sha256'] and m['run_token']==old['run_token'],'historical package identity mismatch')
    need(m['candidate_sha256']!=new_candidate['candidate_sha256'] and m['run_token']!=new_candidate['run_token'],'refuse replay of failed candidate/token')
    image=get(m['candidate_file']);need(image.stat().st_size==ram.PARTITION_BYTES and sha(image)==m['candidate_sha256'],'historical acknowledged image bytes changed')
    need(m['artifact_sha256'].get(m['candidate_file'])==m['candidate_sha256'],'historical image artifact pin missing')
    for name,pin in m['artifact_sha256'].items():need(sha(get(name))==pin,'historical artifact changed: '+name)
    log=(failed/'flash-candidate.log').read_text()
    need("Sending 'boot_b'" in log and "Writing 'boot_b'" in log and log.count('OKAY')>=2 and 'FAILED' not in log,'historical flash transcript incomplete')
    terminal=json.loads((failed/'controller-terminal-observation.json').read_text())
    need(terminal['returncode']==1 and terminal['phase']==old['phase'] and terminal['controller_restarted'] is False and terminal['writer_restarted'] is False,'historical controller termination missing')
    need(terminal.get('root_native_partition_readback_obtained') is False,'historical timeout/readback evidence conflicts')
    for file in failed.iterdir():
        if file.is_file():need(new_candidate['run_token'].encode() not in file.read_bytes(),'new token present in failed-trial evidence')
    pins={ref(file):sha(file) for file in failed.iterdir() if file.is_file()}
    pins[ref(path)]=sha(path)
    return dict(previous_boot_b_sha256=old['candidate_sha256'],previous_trial_file=ref(failed/'state.json'),previous_trial_state_sha256=sha(failed/'state.json'),
                previous_hash_basis='one acknowledged full64MiB boot_b write after last verified readback; subsequent RAM boot timed out; no current partition readback',
                previous_install_readback_verified=False,previous_evidence_sha256=pins)

def prepare(package_path,package_pin,prior,trial,*,failed_install=None):
    m=validate_package(package_path,package_pin);prior,trial=map(private,[prior,trial]);need(not trial.exists(),'fresh trial directory required')
    old=json.loads((prior/'state.json').read_text());result=json.loads((prior/'readout-result.json').read_text());stable=(prior/'android-stable.txt').read_bytes()
    need(old['phase']=='diagnostics-collected-fastboot-ready' and old.get('automatic_loop_verified') and result['boot_and_vendor_readback_verified'],'prior verified physical loop missing')
    need(old['candidate_sha256'].encode() in stable and ram.VENDOR_SHA.encode() in stable and stable.startswith(b'1\n_b\n'),'prior physical full readback missing')
    for name,pin in result['artifacts'].items():need(sha(prior/name)==pin,'prior evidence changed')
    for path in prior.iterdir():
        if path.is_file():need(m['run_token'].encode() not in path.read_bytes(),'new token present in pretrial evidence')
    intervening=failed_install_evidence(failed_install,prior,m) if failed_install is not None else {}
    trial.mkdir(mode=0o700)
    contract={k:m[k] for k in ['serial','run_token','candidate_sha256','bundle_id','guest_profile_sha256','partitions']}
    contract.update(format='ACE_RAMDIAG_HOST_V1',vendor_sha256=ram.VENDOR_SHA,kernel_sha256=ram.KERNEL_SHA,controller_sha256=sha(ROOT/'tools/ace-auto-trial.py'),validator_sha256=sha(ROOT/'tools/ace_ram_readout.py'))
    path=trial/'ram-host-contract.json';path.write_text(json.dumps(contract,indent=2)+'\n')
    state=dict(phase='write-authorized-awaiting-final-bootloader-checks',authorized=True,authorization_basis='Standing AGENTS user authorization for experimental boot_b and mandatory automatic trial',
               candidate_sha256=m['candidate_sha256'],run_token=m['run_token'],partition_writes_started=[],automatic_restore_after_trial=False,auto_readout_after_reset=True,ios_usable=False,
               readout_profile=ram.READY,ramdiag_contract_file=path.name,ramdiag_contract_sha256=sha(path),candidate_manifest_file=ref(package_path),candidate_manifest_sha256=package_pin,
               previous_boot_b_sha256=old['candidate_sha256'],previous_hash_basis='historical actual root/B/full boot+vendor readback and firmware Fastboot return; no subsequent partition writes',
               previous_trial_file=ref(prior/'state.json'),previous_trial_state_sha256=sha(prior/'state.json'),pretrial_token_absence_verified=True)
    state.update(last_verified_boot_b_sha256=old['candidate_sha256'],last_verified_trial_file=ref(prior/'state.json'),last_verified_trial_state_sha256=sha(prior/'state.json'))
    state.update(intervening)
    ram.load_contract(state,trial,m['serial'],sha(ROOT/'tools/ace-auto-trial.py'))
    (trial/'state.json').write_text(json.dumps(state,indent=2)+'\n');return state

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('native_root',type=Path);p.add_argument('physical',type=Path);p.add_argument('ci_json',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();path=package(a.native_root,a.physical,a.ci_json,a.output);print('Offline candidate verified SHA256',json.loads(path.read_text())['candidate_sha256'])
if __name__=='__main__':main()
