"""Explicitly authorized diagnostic-only recovery gates; no phone commands."""
import hashlib
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]
ANDROID_SHA='8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def need(ok,message):
    if not ok:raise ValueError(message)

def validate_request(state,trial,serial,controller_sha):
    need(state.get('diagnostic_only_exception_authorized') is True,'diagnostic-only workflow exception requires explicit user authorization')
    need(state.get('diagnostic_readout_only') is True and state.get('auto_readout_after_reset') is False and state.get('readout_profile')=='android-v1','diagnostic-only mode/profile mismatch')
    name=Path(state['forensic_manifest_file']);need(not name.is_absolute() and '..' not in name.parts,'unsafe forensic manifest path')
    path=(trial/name).resolve();need(path.is_relative_to(trial.resolve()) and sha(path)==state['forensic_manifest_sha256'],'forensic manifest pin mismatch')
    m=json.loads(path.read_text())
    need(m['format']=='ACE_FORENSIC_CANDIDATE_V1' and m['serial']==serial and m['run_token']==state['run_token'] and m['candidate_sha256']==state['candidate_sha256'],'forensic candidate context mismatch')
    need(m['diagnostic_readout_only'] is True and m['auto_readout_after_reset'] is False and m['initialize_empty_pmsg'] is False,'forensic pmsg/no-XNU mode mismatch')
    need(m['controller_sha256']==controller_sha and m['validator_sha256']==sha(Path(__file__)),'forensic controller source mismatch')
    need(m['android_sha256']==ANDROID_SHA,'forensic Android pin mismatch')
    required={'tools/ace-auto-trial.py','tools/ace_forensic_readout.py','ace/native-loader/main.c'}
    need(required<=set(m['source_sha256']),'incomplete forensic source pins')
    need(m['artifact_sha256'].get(m['candidate_file'])==m['candidate_sha256'],'forensic candidate artifact pin missing')
    image=(ROOT/m['candidate_file']).resolve()
    need(image.is_relative_to(ROOT/'research') and image.stat().st_size==67108864,'forensic full boot extent mismatch')
    for name,pin in m['source_sha256'].items():
        need(not Path(name).is_absolute() and '..' not in Path(name).parts and sha(ROOT/name)==pin,'forensic source changed: '+name)
    for name,pin in m['artifact_sha256'].items():
        p=(ROOT/name).resolve();need(p.is_relative_to(ROOT/'research') and sha(p)==pin,'forensic artifact changed: '+name)
    return m

def prior_observation(record,prior_token):
    need(len(record)==288 and len(prior_token)==16 and all(c in '0123456789abcdef' for c in prior_token),'invalid forensic record/prior token')
    w=struct.unpack('<32Q',record[32:]);signed=lambda n:n if n<1<<63 else n-(1<<64)
    need(w[2]==2 and signed(w[3])==-66,'expected intentional diagnostic-only stage2/error-66')
    marker=('ACEXNU1:'+prior_token+': entry EL1\n').encode();copied=struct.pack('<5Q',*w[26:31])
    observed=signed(w[23])==0 and w[24]>0 and copied.startswith(marker)
    return dict(diagnostic_readout_only=True,prior_run_token=prior_token,prior_ring_validation=signed(w[23]),prior_marker_count=w[24],
                prior_marker_offset=w[25],prior_marker_bytes_hex=copied.hex(),prior_zone_nonzero_bytes=w[31],prior_entry_marker_observed=observed,
                interpretation='retained prior entry marker only; never iOS/kernel/driver success',ios_usable=False)


def observe_return_record(device,out,index,run):
    """One Android SU read; preserve rc/partial output for the three-read guard."""
    import shlex
    import subprocess
    stem='android-return-command-%03d'%index
    raw,stderr,rc=b'',b'',None
    meta=dict(identity_verified_by_caller=True)
    try:
        r=run(['adb','-s',device,'exec-out','su -c '+shlex.quote('cat /sys/firmware/devicetree/base/chosen/ace,native-refusal')])
        raw,stderr,rc=r.stdout,r.stderr,r.returncode
    except subprocess.TimeoutExpired as error:
        raw,stderr=error.stdout or b'',error.stderr or b'';meta['exception']=str(error)
    except OSError as error:
        meta['exception']=str(error);raise
    finally:
        (out/(stem+'.stdout')).write_bytes(raw);(out/(stem+'.stderr')).write_bytes(stderr)
        meta.update(returncode=rc,stdout=stem+'.stdout',stderr=stem+'.stderr',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        (out/(stem+'.json')).write_text(json.dumps(meta,indent=2)+'\n')
    return raw
