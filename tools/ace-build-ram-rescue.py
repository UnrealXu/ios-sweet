#!/usr/bin/env python3
"""Build fresh Ace RAM+bounded Android-rescue candidate OFFLINE. No flash/reboot.

Uses accepted 0118 kernel, exact preserved stock artifacts and latest verified
normal-auto or approved forensic-return ancestry. Derived rescue generic preserves original Magiskinit blob. The
120s production native budget covers measured ~73s two-pass hash work. A completed package still needs the
parent's reviewed one-time writer and identity-bound automatic controller.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,re,secrets,struct,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(v,m):
 if not v:raise ValueError(m)
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
# One reviewed historical completion only. This allowlist binds the immutable
# receipt/helper/source/launch, rather than accepting arbitrary rc1 ancestors.
APPROVED_RETURN_COMPLETION_SHA='af920c8a51cdfa047f19e9ee6d3ba93eb25afcbfca14faa69a4af834bf358b5a'
APPROVED_RETURN_HELPER_SHA='645dd91c77f66ea1203dea407fd8aa6a53b79366bff58c2033ad1a046ba411bb'
APPROVED_RETURN_CONTROLLER_SHA='c915dcfc16d25f632d2f4c6ba86b5454904aef56ab142736702a57ede9920972'
APPROVED_RETURN_LOG_SHA='ad185890147adee59fc267d9d8cfda55cdae686f889a3f9a02b64942d3d514c3'
def verified_terminal_return_completion(prior,ps,pr,pm,launch):
 need(ps.get('diagnostic_readout_only') is True and ps.get('auto_readout_after_reset') is False and ps.get('automatic_loop_verified') is False,'completion is forensic-only, never normal auto success')
 need(ps.get('return_completion_verified') is True and ps.get('return_completion_file')=='return-completion.json','explicit terminal completion required')
 receipt=prior/'return-completion.json'
 need(sha(receipt)==ps.get('return_completion_sha256')==APPROVED_RETURN_COMPLETION_SHA,'unreviewed/changed return completion receipt')
 need(list(prior.glob('return-completion*.json'))==[receipt],'multiple completion receipts forbidden')
 c=json.loads(receipt.read_text())
 need(c.get('format')=='ACE_TERMINAL_READ_RETURN_COMPLETION_V1' and c.get('returncode')==0 and c.get('physical_fastboot_verified') is True,'terminal completion format/result mismatch')
 need(c.get('trial_restarted') is False and c.get('boot_restarted') is False and c.get('partition_writes')==[] and c.get('read_limit_total')==3,'completion restarted trial/boot/writes or changed read limit')
 need(launch.get('controller_returncode')==1 and launch.get('controller_restarted') is False and launch.get('writer_restarted') is False and 'controller_finished_utc' in launch,'original failed launch not immutable terminal')
 lp=prior/'controller-launch.json'
 need(c.get('original_controller_returncode')==1 and c.get('original_controller_launch_sha256')==sha(lp)==c.get('final_launch_sha256'),'original failed controller launch changed')
 need(launch.get('controller_sha256')==ps.get('controller_sha256')==pm.get('controller_sha256')==APPROVED_RETURN_CONTROLLER_SHA,'completion original controller source changed')
 need(sha(prior/'controller.log')==APPROVED_RETURN_LOG_SHA and (prior/'controller.log').read_text().endswith('Auto trial stopped: expected phone absent during return-token observation\n'),'different original controller failure')
 need(c.get('run_token')==ps['run_token']==pm['run_token'] and c.get('candidate_sha256')==ps['candidate_sha256']==pm['candidate_sha256'],'completion token/candidate mismatch')
 need(c.get('readout_result_sha256')==sha(prior/'readout-result.json') and c.get('forensic_manifest_sha256')==ps['forensic_manifest_sha256'] and c.get('fastboot_ready_sha256')==sha(prior/'fastboot-ready.json'),'completion readout/manifest/Fastboot evidence changed')
 need(pr.get('boot_and_vendor_readback_verified') is True and pr.get('log_collection_complete') is True and pr.get('log_collection_errors')==[] and pr.get('diagnostic_readout_only') is True and pr.get('automatic_pending_trial_return') is False,'completion requires full forensic readback/logs')
 obs=ps.get('return_record_observations',[]);attempts=ps.get('return_fastboot_attempts',[])
 need(c.get('initial_observation_count')==1 and 2<=len(obs)<=3 and c.get('observations_total')==len(obs),'completion global read bound/initial state mismatch')
 need(obs[0].get('bytes')==0 and obs[0].get('matches_expected') is False and (prior/obs[0]['file']).read_bytes()==b'','completion initial observation must be empty')
 need(c.get('return_reboot_attempts')==len(attempts) and 1<=len(attempts)<=2 and attempts[-1].get('returncode')==0,'completion one bounded return missing')
 # The surrounding verified_prior checks all individual observation hashes,
 # exact current288B record, pre-command-only retry, full boot/vendor and FB.
 helper=(ROOT/c['helper_file']).resolve()
 need(helper.is_relative_to(ROOT/'research') and sha(helper)==c.get('helper_sha256')==APPROVED_RETURN_HELPER_SHA,'completion helper changed/unreviewed')
 return {str(helper.relative_to(ROOT)):sha(helper)}
def verified_prior(path,serial,token):
 prior=path.resolve();need(prior.is_relative_to(ROOT/'research'),'private verified prior trial required')
 ps=json.loads((prior/'state.json').read_text());pr=json.loads((prior/'readout-result.json').read_text())
 need(ps['phase']=='diagnostics-collected-fastboot-ready' and ps.get('candidate_flash_succeeded') is True and ps.get('diagnostics_complete') is True and pr.get('boot_and_vendor_readback_verified') is True and pr.get('log_collection_complete') is True,'prior physical readback/collection incomplete')
 forensic=ps.get('diagnostic_readout_only') is True
 if forensic:
  need(ps.get('diagnostic_only_exception_authorized') is True and ps.get('authorized') is True and ps.get('diagnostic_only_return_verified') is True and ps.get('auto_readout_after_reset') is False,'approved forensic return required')
  mp=(prior/ps['forensic_manifest_file']).resolve();pin=ps['forensic_manifest_sha256']
  need(mp.is_relative_to(prior),'unsafe forensic prior manifest')
 else:
  need(ps.get('automatic_loop_verified') is True and ps.get('auto_readout_after_reset') is True and pr.get('automatic_pending_trial_return') is True,'normal automatic return required')
  mp=(ROOT/ps['candidate_manifest_file']).resolve();pin=ps['candidate_manifest_sha256']
 need(mp.is_relative_to(ROOT/'research') and sha(mp)==pin,'prior manifest hash mismatch');pm=json.loads(mp.read_text());installed=ps['candidate_sha256']
 need(pm['serial']==serial and pm['run_token']==ps['run_token'] and pm['candidate_sha256']==installed,'prior serial/token/candidate mismatch')
 cp=(ROOT/pm['candidate_file']).resolve();need(cp.is_relative_to(ROOT/'research') and cp.stat().st_size==67108864 and sha(cp)==installed,'prior full candidate mismatch')
 stable=(prior/'android-stable.txt').read_bytes();vendor='bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670'
 need(stable.startswith(b'1\n_b\n') and b'uid=0(root)' in stable and (installed+'  /dev/block/by-name/boot_b\n').encode() in stable and (vendor+'  /dev/block/by-name/vendor_boot_b\n').encode() in stable,'prior full readback/B/root mismatch')
 raw=(prior/'readout-record.bin').read_bytes();need(len(raw)==288 and raw[:8]==b'ACEFALL1' and raw[8:24]==ps['run_token'].encode() and raw[24:32]==bytes(8),'prior current native envelope/token')
 words=struct.unpack('<32Q',raw[32:]);need(words[0]==0x313054414e454341 and words[1]==1 and words[2]==(2 if forensic else 5) and words[3]==2**64-(66 if forensic else 67) and words[20]==0,'prior native return record mismatch')
 attempts=ps.get('return_fastboot_attempts',[]);need(1<=len(attempts)<=2 and attempts[-1]['returncode']==0,'prior automatic Fastboot return missing')
 if len(attempts)==2:need(attempts[0]['returncode'] and attempts[0]['output'].strip() in ('error: device not found',"error: device '%s' not found" % serial),'prior retry lacked exact pre-command missing-device error')
 observations=ps.get('return_record_observations',[]);need(1<=len(observations)<=3,'prior return read retry bound exceeded')
 observed=False
 for item in observations:
  f=(prior/item['file']).resolve();need(f.is_relative_to(prior) and sha(f)==item['sha256'] and f.stat().st_size==item['bytes'],'prior return observation changed')
  sample=f.read_bytes()
  if len(sample)==288 and sample[:8]==b'ACEFALL1' and struct.unpack_from('<Q',sample,32)[0]==0x313054414e454341:need(sample==raw,'prior complete different diagnostic record')
  if item.get('matches_expected') is True:need(sample==raw,'prior return token changed');observed=True
 need(observed,'prior exact return observation absent')
 fb=json.loads((prior/'fastboot-ready.json').read_text())
 for key,value in [('product','k6895v1_64'),('current-slot','b'),('unlocked','yes'),('is-userspace','no')]:need(re.search(re.escape(key)+r':\s*'+re.escape(value)+r'(?=\s|$)',fb[key]) is not None,'prior firmware Fastboot '+key+' mismatch')
 launch=json.loads((prior/'controller-launch.json').read_text());completion_evidence={}
 if launch.get('controller_returncode')==0:
  need('controller_finished_utc' in launch and launch.get('controller_restarted') is False and not ps.get('return_completion_verified'),'prior successful controller terminal/completion mismatch')
 else:
  completion_evidence=verified_terminal_return_completion(prior,ps,pr,pm,launch)
 need(pr.get('artifacts'),'prior evidence manifest missing')
 for name,pin in pr['artifacts'].items():
  f=(prior/name).resolve();need(f.is_relative_to(prior) and sha(f)==pin,'prior raw evidence hash changed')
 evidence={str(mp.relative_to(ROOT)):sha(mp),str(cp.relative_to(ROOT)):installed};evidence.update(completion_evidence)
 for f in prior.rglob('*'):
  if f.is_file():
   need(token.encode() not in f.read_bytes(),'token already in actual ancestor evidence');evidence[str(f.relative_to(ROOT))]=sha(f)
 return prior,ps,installed,evidence
p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);p.add_argument('--run-token');p.add_argument('--verified-prior-trial',type=Path,help='completed normal-auto or approved forensic-return trial for current installed boot_b');p.add_argument('--entry-case',action='append',help='pass selected native verifier case; repeat; default all cases');a=p.parse_args();out=a.output.resolve()
need(not out.exists() and out.is_relative_to(ROOT/'research'),'fresh private output required');out.mkdir(mode=0o700,parents=True)
def run(argv,name,timeout=180):
 r=subprocess.run(argv,capture_output=True,text=True,timeout=timeout);(out/(name+'.log')).write_text(r.stdout+r.stderr);need(r.returncode==0,name+' failed; retained log')
try:
 accepted=ROOT/'research/ace-pmsg-approved-reseed-20261021';linked=json.loads((accepted/'linked-kernel.json').read_text());kernel=accepted/'kernel.development.ace';adt=accepted/'adt'
 need(linked['ci_run']==39551656841 and linked['ci_conclusion']=='success' and linked['kernel_sha256']=='4f425b1716c6802b07fea6d373bac366126515f66735d69e55ce10038f5054c6' and sha(kernel)==linked['kernel_sha256'],'accepted0118 kernel provenance mismatch')
 am=json.loads((adt/'manifest.json').read_text());need(am['ufs_root_discovery_probe'] is True and sha(adt/'ace.adt')==am['adt_sha256'],'profile3/root discovery ADT mismatch')
 token=a.run_token or secrets.token_hex(8);need(len(token)==16 and all(c in '0123456789abcdef' for c in token),'fresh lowercase token')
 serial=json.loads((ROOT/'research/ace-stock-chain-20261019/phone-test1/transport.json').read_text())['usb_adb']
 prior,ps,installed,prior_evidence=verified_prior(a.verified_prior_trial or accepted/'phone-trial',serial,token)
 need(a.entry_case is None or len(set(a.entry_case))==len(a.entry_case),'duplicate entry-case selection')
 oldbase=ROOT/'research/ace-ramdiag-20261020';old=json.loads((oldbase/'physical-trace0/manifest.json').read_text());oldbundle=json.loads((oldbase/'physical-trace0/bundle/report.json').read_text());planpin=oldbundle['input_plan_sha256'];plans=[f for f in oldbase.glob('module-plan*/report.json') if sha(f)==planpin];need(len(plans)==1,'exact original48-module plan unavailable')
 transport=ROOT/'research/ace-stock-chain-20261019/phone-test1/transport.json';serial=json.loads(transport.read_text())['usb_adb'];need(serial==old['serial'],'prepared physical serial mismatch')
 key=oldbase/'physical-host-adb.pub';need(sha(key)==old['host_adb_public_key_sha256'],'physical trusted ADB key pin mismatch')
 physical=load('fresh_rescue_physical',ROOT/'diagnostics/ace-ramdiag/physical_assemble.py')
 rm=physical.assemble(out/'physical-ram',plans[0],planpin,serial,token,key.read_bytes(),old['host_adb_public_key_sha256'],old['partitions'])
 need(rm['run_token']==token and rm['files']['ace-ramdiag/trace-token']['sha256']==hashlib.sha256((token+'\n').encode()).hexdigest(),'fresh physical RAM token mismatch')
 run([sys.executable,str(ROOT/'diagnostics/ace-ramdiag/rescue_capsule.py'),str(out/'capsule'),'--token',token],'capsule')
 cr=json.loads((out/'capsule/report.json').read_text());need(cr['original_init_blob_unchanged'] and cr['derived_is_byte_identical_original'] is False,'derived capsule identity missing')
 cpio=load('rescue_cpio',ROOT/'tools/ace-recovery-diag.py');vendor_path=ROOT/'research/ace-backup-20261019-wireless-v2/vendor_boot_b.img';vendor_sha='bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670';need(sha(vendor_path)==vendor_sha,'preserved vendor backup changed');vendor=cpio.read_vendor(vendor_path.read_bytes())['ramdisk'];generic_path=out/'physical-ram/physical-generic.lz4';generic=generic_path.read_bytes();need(hashlib.sha256(generic).hexdigest()==rm['generic_sha256'],'fresh RAM generic changed')
 policy=dict(vendor_bytes=len(vendor),generic_offset=len(vendor),generic_bytes=len(generic),vendor_sha256=hashlib.sha256(vendor).hexdigest(),generic_sha256=rm['generic_sha256'],rescue_sha256=cr['derived_generic_sha256'],require_bootconfig=True);(out/'stream-policy.json').write_text(json.dumps(policy,indent=2)+'\n')
 # LK direct vendor+generic concatenation is established by targeted REA. Exact
 # current phone config bytes are NOT guessed: native validates checksum/footer,
 # geometry, all source pins and the current chosen bounds before any mutation.
 native_args=[sys.executable,str(ROOT/'tools/ace-mknative.py'),str(kernel),str(adt),str(out/'native'),'--expected-kernel-sha256',linked['kernel_sha256'],'--fdt-pa','0x47c80000','--text-offset','0','--pmsg','--init-empty-pmsg','--auto-readout-after-reset','--run-token',token,'--refusal-android-image',str(ROOT/'research/ace-stock-qemu-20261019/Image'),'--expected-android-sha256','8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0','--root-device','aceufsroot0','--ram-rescue-generic',str(out/'capsule/derived-rescue-generic.lz4'),'--ram-rescue-policy',str(out/'stream-policy.json')]
 need('now-begun<1560000000;' in (ROOT/'ace/native-loader/ram_rescue.c').read_text(),'production120s native budget changed')
 run(native_args,'native-build');nm=json.loads((out/'native/build-manifest.json').read_text());need(nm['run_token']==token and nm['ram_rescue']['enabled'],'native token/rescue missing')
 fdt=ROOT/'research/ace-xnu-entrylog-20261020/live-fdt.dtb';need(sha(fdt)==am['fdt_sha256'],'historical physical FDT pin mismatch')
 run([sys.executable,str(ROOT/'ace/native-loader/verify.py'),str(out/'native'),str(kernel),str(fdt),str(out/'native-entry')]+[v for name in (a.entry_case or []) for v in ['--case',name]],'native-entry',240)
 run([sys.executable,str(ROOT/'ace/native-loader/verify_c_entry.py'),str(out/'native'),str(kernel),str(fdt),str(out/'c-entry')],'c-entry',180)
 chain=load('rescue_full_boot_package',ROOT/'tools/ace-stock-chain-boot.py');image=(out/'native/native.Image').read_bytes();need(sha(out/'native/native.Image')==nm['image_sha256'],'native image changed');compressed=chain.boot.deterministic_gzip(image);candidate,_,layout,actualgeneric=chain.package(chain.BACKUP.read_bytes(),compressed,diagnostic_ramdisk=generic,diagnostic_ramdisk_sha256=rm['generic_sha256']);need(len(candidate)==67108864 and actualgeneric==generic,'full boot/generic extent mismatch');need(chain.boot.inflate(candidate[layout['kernel_offset']:layout['kernel_offset']+layout['kernel_bytes']],0x5000000)==image,'full package native extraction mismatch')
 candidate_path=out/'experimental-ram-rescue-boot-b.img';candidate_path.write_bytes(candidate)
 sources=dict(nm['source_sha256']);sources.update(rm['source_sha256']);sources.update(cr['source_sha256']);rescue=load('rescue_host_contract',ROOT/'tools/ace_ram_rescue_readout.py')
 for name in list(rescue.REQUIRED_SOURCES)+['tools/ace_ram_readout.py','tools/ace_forensic_readout.py','tools/ace-build-ram-rescue.py','diagnostics/ace-ramdiag/rescue_capsule.py']:sources[name]=sha(ROOT/name)
 for name,digest in sources.items():need(sha(ROOT/name)==digest,'package source pin mismatch '+name)
 retain=[candidate_path,out/'native/native.Image',out/'native/build-manifest.json',out/'native/native_config.h',out/'physical-ram/manifest.json',generic_path,out/'capsule/report.json',out/'capsule/rescue_init_config.h',out/'capsule/derived-rescue-generic.lz4',out/'capsule/original-init',out/'stream-policy.json',out/'native-entry/verification.json',out/'c-entry/verification.json',kernel,accepted/'linked-kernel.json',adt/'ace.adt',adt/'manifest.json']
 artifacts={str(f.relative_to(ROOT)):sha(f) for f in retain};artifacts.update(prior_evidence)
 manifest=dict(format='ACE_BOUNDED_RAM_RESCUE_CANDIDATE_V1',purpose='Physical RAM-stage diagnosis with dependent Android capsule rescue; usable iOS not achieved',serial=serial,run_token=token,candidate_sha256=sha(candidate_path),candidate_file=str(candidate_path.relative_to(ROOT)),kernel_sha256=linked['kernel_sha256'],android_sha256=physical.ram.KERNEL_SHA,diagnostic_readout_only=False,auto_readout_after_reset=True,initialize_empty_pmsg=True,readout_profile=physical.ram.READY,generic_sha256=rm['generic_sha256'],bundle_id=rm['bundle_id'],guest_profile_sha256=rm['guest_profile_sha256'],partitions=rm['partitions'],source_sha256=sources,artifact_sha256=artifacts,ios_usable=False,physical_RAM_recovery_verified=False,current_phone_footer_must_validate_at_runtime=True)
 mp=out/'manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n');trial=out/'phone-trial';trial.mkdir(mode=0o700)
 rc={k:manifest[k] for k in ['serial','run_token','candidate_sha256','bundle_id','guest_profile_sha256','partitions']};rc.update(format='ACE_RAMDIAG_HOST_V1',vendor_sha256=physical.ram.VENDOR_SHA,kernel_sha256=physical.ram.KERNEL_SHA,controller_sha256=sha(ROOT/'tools/ace-auto-trial.py'),validator_sha256=sha(ROOT/'tools/ace_ram_readout.py'));rp=trial/'ram-host-contract.json';rp.write_text(json.dumps(rc,indent=2)+'\n')
 ac=dict(format='ACE_RAMDIAG_ANDROID_RESCUE_V1',serial=serial,run_token=token,candidate_sha256=manifest['candidate_sha256'],first_ram_capability_hex=(b'ACERAMR1'+token.encode()).hex(),controller_sha256=sha(ROOT/'tools/ace-auto-trial.py'),validator_sha256=sha(ROOT/'tools/ace_ram_rescue_readout.py'),native_manifest_file=str(out/'native/build-manifest.json'),native_manifest_sha256=sha(out/'native/build-manifest.json'),capsule_manifest_file=str(out/'capsule/report.json'),capsule_manifest_sha256=sha(out/'capsule/report.json'));ap=trial/'rescue-contract.json';ap.write_text(json.dumps(ac,indent=2)+'\n')
 state=dict(phase='candidate-built-awaiting-guarded-writer',candidate_flash_succeeded=False,run_token=token,candidate_sha256=manifest['candidate_sha256'],candidate_manifest_file=str(mp),candidate_manifest_sha256=sha(mp),readout_profile=physical.ram.READY,ramdiag_contract_file=rp.name,ramdiag_contract_sha256=sha(rp),ramdiag_android_rescue_enabled=True,ramdiag_android_rescue_contract_file=ap.name,ramdiag_android_rescue_contract_sha256=sha(ap),auto_readout_after_reset=True,diagnostic_readout_only=False,previous_boot_b_sha256=installed,previous_install_readback_verified=True,previous_trial_file=str(prior/'state.json'),previous_trial_state_sha256=sha(prior/'state.json'),previous_evidence_sha256=prior_evidence,verified_prior_kind='approved-forensic-return' if ps.get('diagnostic_readout_only') else 'normal-auto',entry_case_selection=a.entry_case,pretrial_token_absence_verified=True,automatic_restore_after_trial=False,ios_usable=False)
 (trial/'state.json').write_text(json.dumps(state,indent=2)+'\n');physical.ram.load_contract(state,trial,serial,sha(ROOT/'tools/ace-auto-trial.py'));rescue.load_contract(state,trial,serial,sha(ROOT/'tools/ace-auto-trial.py'),rc)
 (out/'BUILD_COMPLETE.json').write_text(json.dumps(dict(status='full candidate and pinned host contracts built; no phone operation',candidate_sha256=manifest['candidate_sha256'],run_token=token,phone_io=False,writer_created=False,production_budget_seconds=120,physical_RAM_recovery_verified=False),indent=2)+'\n');print('Full RAM+dependent Android rescue candidate/contract ready for parent guarded writer:',manifest['candidate_sha256'])
except Exception as exc:
 (out/'FAILED.json').write_text(json.dumps(dict(error=str(exc),phone_io=False,do_not_use=True),indent=2)+'\n');raise
