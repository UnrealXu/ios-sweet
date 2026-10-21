"""Explicit Android-rescue authorization and record classification. No transport.

A selected original-generic rescue is failed RAM diagnostics recovered through
Android; it is never a no-data diagnostic or iOS success receipt.
"""
from pathlib import Path
import hashlib,json,re,struct
ROOT=Path(__file__).resolve().parents[1]
WORD=0x3130455543534552
REQUIRED_SOURCES=('ace/native-loader/ram_rescue.c','ace/native-loader/ram_rescue.h',
    'ace/native-loader/refusal_android.c','ace/initrd_rescue.c','ace/initrd_rescue.h',
    'ace/fdt_refusal.c','ace/fdt_refusal.h','ace/pstore_rescue.c','ace/pstore_rescue.h',
    'diagnostics/ace-ramdiag/preinit.c','diagnostics/ace-ramdiag/rescue_init.c',
    'diagnostics/ace-ramdiag/pmsg_trace.h','diagnostics/ace-ramdiag/sha256.h','tools/ace-mknative.py','tools/ace-auto-trial.py',
    'tools/ace_ram_rescue_readout.py')
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pinned_file(path,digest):
    require(isinstance(digest,str) and re.fullmatch('[0-9a-f]{64}',digest),'rescue file digest format')
    require(path.is_file() and not path.is_symlink(),'rescue ordinary pinned file required')
    raw=path.read_bytes();require(sha(raw)==digest,'rescue file hash mismatch: '+path.name);return raw

def load_contract(state,trial,serial,controller_sha256,ram_contract):
    if not state.get('ramdiag_android_rescue_enabled',False):return None
    require(state['ramdiag_android_rescue_enabled'] is True and ram_contract is not None,'rescue requires explicit existing RAM trial contract')
    relative=Path(state['ramdiag_android_rescue_contract_file'])
    require(not relative.is_absolute() and '..' not in relative.parts,'unsafe rescue contract path')
    raw=pinned_file(trial/relative,state['ramdiag_android_rescue_contract_sha256']);contract=json.loads(raw)
    require(contract['format']=='ACE_RAMDIAG_ANDROID_RESCUE_V1','rescue contract format')
    require(contract['serial']==serial and contract['run_token']==state['run_token'] and re.fullmatch('[0-9a-f]{16}',contract['run_token']),'rescue serial/current token mismatch')
    require(contract['candidate_sha256']==state['candidate_sha256'],'rescue candidate contract mismatch')
    require(contract['first_ram_capability_hex']==(b'ACERAMR1'+state['run_token'].encode()).hex(),'rescue exact24B capability mismatch')
    require(contract['controller_sha256']==controller_sha256 and contract['validator_sha256']==sha(Path(__file__).read_bytes()),'rescue validator/controller source mismatch')
    cm=json.loads(pinned_file(Path(state['candidate_manifest_file']),state['candidate_manifest_sha256']))
    require(cm['serial']==serial and cm['run_token']==state['run_token'] and cm['candidate_sha256']==contract['candidate_sha256'],'rescue prepared candidate manifest mismatch')
    candidate=ROOT/cm['candidate_file'];require(candidate.resolve().is_relative_to(ROOT/'research'),'candidate outside private artifacts')
    require(len(pinned_file(candidate,cm['candidate_sha256']))==64*1024*1024,'rescue full partition candidate required')
    for name in REQUIRED_SOURCES:
        require(name in cm['source_sha256'],'missing rescue candidate source pin: '+name)
        pinned_file(ROOT/name,cm['source_sha256'][name])
    native=Path(contract['native_manifest_file'])
    require(native.resolve().is_relative_to(ROOT/'research'),'rescue native manifest outside private artifacts')
    key=str(native.relative_to(ROOT))
    require(cm['artifact_sha256'].get(key)==contract['native_manifest_sha256'],'native rescue artifact is not candidate-bound')
    nm=json.loads(pinned_file(native,contract['native_manifest_sha256']))
    require(nm['run_token']==state['run_token'] and nm['ram_rescue']['enabled'] is True and nm['ram_rescue']['independent_of_userdata'] is False,'native current rescue capability mismatch')
    require(nm['auto_readout_after_reset'] is True and nm['pmsg_enabled'] is True and nm['diagnostic_readout_only'] is False,'native rescue boot mode mismatch')
    require(nm['refusal_android']['sha256']=='8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0','rescue Android kernel pin mismatch')
    for name,digest in nm['source_sha256'].items():
        require(cm['source_sha256'].get(name)==digest,'native/candidate rescue source pin mismatch: '+name)
    capsule=Path(contract['capsule_manifest_file'])
    require(capsule.resolve().is_relative_to(ROOT/'research'),'rescue capsule manifest outside private artifacts')
    key=str(capsule.relative_to(ROOT))
    require(cm['artifact_sha256'].get(key)==contract['capsule_manifest_sha256'],'rescue capsule is not candidate-bound')
    cr=json.loads(pinned_file(capsule,contract['capsule_manifest_sha256']))
    require(cr['run_token']==state['run_token'] and cr['original_init_blob_unchanged'] is True and
            cr['derived_is_byte_identical_original'] is False,'derived rescue capsule/token mismatch')
    require(cr['original_generic_sha256']=='54961de2dad343c35295905f1f1811b80d176e725b9fa93c48aada8e96fa90d2' and
            cr['original_init_sha256']=='383670a7ba3a6a4b79e5f3467e1da4b66a5df66a9b356ab9f70916854dd6b468','original generic/Magiskinit blob pin mismatch')
    require(cr['derived_generic_sha256']==nm['ram_rescue']['policy']['rescue_sha256'],'native derived capsule digest mismatch')
    require(cr['source_sha256'].get('diagnostics/ace-ramdiag/rescue_init.c')==cm['source_sha256']['diagnostics/ace-ramdiag/rescue_init.c'],'capsule wrapper source missing/mismatch')
    for name,digest in cr['source_sha256'].items():
        require(cm['source_sha256'].get(name)==digest,'capsule/candidate source mismatch: '+name)
    return contract

def classify(record,token,contract):
    require(len(record)==288 and record[:8]==b'ACEFALL1' and record[8:24]==token.encode() and record[24:32]==bytes(8),'rescue current record mismatch')
    words=struct.unpack('<32Q',record[32:])
    if words[31]!=WORD:
        if contract:require(words[31]==0,'unexpected RAM rescue record flag')
        return {'selected':False}
    require(contract is not None,'unapproved Android rescue record')
    require(words[:4]==(0x313054414e454341,1,5,(-67)%(1<<64)) and words[20]==0,'rescue native stage/error/guard mismatch')
    return dict(selected=True,ram_diagnostic_failed=True,android_rescue_selected=True,
        independent_of_userdata=False,ram_diagnostic_usable=False,ios_usable=False)
