from pathlib import Path
import sys,importlib.util,tempfile,json,struct,hashlib,unittest,copy
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'tools/ace_ram_rescue_readout.py'
spec=importlib.util.spec_from_file_location('private_rescue_controller',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class ControllerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);mod.ROOT=self.root;self.trial=self.root/'research/trial';self.trial.mkdir(parents=True)
  self.token='0123456789abcdef';self.serial='QEMU_RESCUE_FIXTURE';self.sha=lambda b:hashlib.sha256(b).hexdigest()
  for name in mod.REQUIRED_SOURCES:
   dst=self.root/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((ROOT/name).read_bytes())
  candidate=self.root/'research/candidate.img';candidate.write_bytes(bytes(64*1024*1024));self.candidate_sha=self.sha(candidate.read_bytes())
  nm=dict(run_token=self.token,ram_rescue={'enabled':True,'independent_of_userdata':False,'policy':{'rescue_sha256':'d'*64}},auto_readout_after_reset=True,pmsg_enabled=True,diagnostic_readout_only=False,refusal_android={'sha256':'8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'},source_sha256={n:self.sha((self.root/n).read_bytes()) for n in mod.REQUIRED_SOURCES[:-1]})
  self.native=self.root/'research/native-manifest.json';self.native.write_text(json.dumps(nm));self.nsha=self.sha(self.native.read_bytes())
  cm=dict(serial=self.serial,run_token=self.token,candidate_sha256=self.candidate_sha,candidate_file='research/candidate.img',source_sha256={n:self.sha((self.root/n).read_bytes()) for n in mod.REQUIRED_SOURCES},artifact_sha256={'research/native-manifest.json':self.nsha})
  capsule=dict(run_token=self.token,original_init_blob_unchanged=True,derived_is_byte_identical_original=False,
   original_generic_sha256='54961de2dad343c35295905f1f1811b80d176e725b9fa93c48aada8e96fa90d2',original_init_sha256='383670a7ba3a6a4b79e5f3467e1da4b66a5df66a9b356ab9f70916854dd6b468',derived_generic_sha256='d'*64,source_sha256={'diagnostics/ace-ramdiag/rescue_init.c':cm['source_sha256']['diagnostics/ace-ramdiag/rescue_init.c']})
  self.capsule=self.root/'research/capsule.json';self.capsule.write_text(json.dumps(capsule));self.capsule_sha=self.sha(self.capsule.read_bytes());cm['artifact_sha256']['research/capsule.json']=self.capsule_sha
  self.cm=self.root/'research/candidate-manifest.json';self.cm.write_text(json.dumps(cm))
  contract=dict(format='ACE_RAMDIAG_ANDROID_RESCUE_V1',serial=self.serial,run_token=self.token,candidate_sha256=self.candidate_sha,first_ram_capability_hex=(b'ACERAMR1'+self.token.encode()).hex(),controller_sha256='c'*64,validator_sha256=self.sha(source.read_bytes()),native_manifest_file=str(self.native),native_manifest_sha256=self.nsha,capsule_manifest_file=str(self.capsule),capsule_manifest_sha256=self.capsule_sha)
  self.contract=contract;self.state=dict(run_token=self.token,candidate_sha256=self.candidate_sha,candidate_manifest_file=str(self.cm),candidate_manifest_sha256=self.sha(self.cm.read_bytes()),ramdiag_android_rescue_enabled=True,ramdiag_android_rescue_contract_file='rescue.json')
  self.write_contract()
 def tearDown(self):self.tmp.cleanup()
 def write_contract(self):
  p=self.trial/'rescue.json';p.write_text(json.dumps(self.contract));self.state['ramdiag_android_rescue_contract_sha256']=self.sha(p.read_bytes())
 def load(self):return mod.load_contract(self.state,self.trial,self.serial,'c'*64,{'verified':'RAM host contract'})
 def record(self,word=True):
  w=[0]*32;w[:4]=[0x313054414e454341,1,5,(-67)%(1<<64)];w[31]=mod.WORD if word else 0
  return b'ACEFALL1'+self.token.encode()+bytes(8)+struct.pack('<32Q',*w)
 def test_explicit_pinned_contract_and_selected_record_accepted_as_failed_RAM(self):
  contract=self.load();r=mod.classify(self.record(),self.token,contract)
  self.assertTrue(r['selected']);self.assertTrue(r['ram_diagnostic_failed']);self.assertFalse(r['independent_of_userdata']);self.assertFalse(r['ios_usable'])
  self.assertFalse(mod.classify(self.record(False),self.token,contract)['selected'])
 def test_wrong_token_source_candidate_and_native_pin_refuse(self):
  for field in ['run_token','serial','candidate_sha256','controller_sha256','validator_sha256','native_manifest_sha256','capsule_manifest_sha256','first_ram_capability_hex']:
   original=self.contract.copy();self.contract[field]='bad';self.write_contract()
   with self.assertRaises((ValueError,KeyError)):self.load()
   self.contract=original
  self.write_contract();(self.root/'ace/native-loader/ram_rescue.c').write_text('changed after review')
  with self.assertRaises(ValueError):self.load()
 def test_no_implicit_rescue_or_contract_escape(self):
  self.assertIsNone(mod.load_contract({},self.trial,self.serial,'c'*64,None))
  with self.assertRaises(ValueError):mod.classify(self.record(),self.token,None)
  self.state['ramdiag_android_rescue_contract_file']='../escape'
  with self.assertRaises(ValueError):self.load()
 def test_other_complete_record_and_selected_wrong_stage_or_guard_refuse(self):
  for pos in [0,8,24,32,40,48,56,192]:
   b=bytearray(self.record());b[pos]^=1
   with self.assertRaises(ValueError):mod.classify(bytes(b),self.token,self.contract)
  for size in [0,287,289]:
   with self.assertRaises(ValueError):mod.classify(self.record()[:size] if size<288 else self.record()+b'x',self.token,self.contract)
if __name__=='__main__':unittest.main()
