"""Recovery must require a specific exception and never imply XNU success."""
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('forensic_guards',ROOT/'tools/ace_forensic_readout.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ForensicGuards(unittest.TestCase):
    def record(self,valid=True):
        w=[0]*32;w[2]=2;w[3]=(-66)%(1<<64);w[23]=0 if valid else (-1)%(1<<64);w[24]=1
        marker=(b'ACEXNU1:'+b'0123456789abcdef'+b': entry EL1\n').ljust(40,b'\0');w[26:31]=struct.unpack('<5Q',marker)
        return bytes(32)+struct.pack('<32Q',*w)
    def test_valid_prior_entry_is_never_iOS_success(self):
        result=m.prior_observation(self.record(),'0123456789abcdef')
        self.assertTrue(result['prior_entry_marker_observed']);self.assertFalse(result['ios_usable'])
        self.assertFalse(m.prior_observation(self.record(False),'0123456789abcdef')['prior_entry_marker_observed'])
        self.assertFalse(m.prior_observation(self.record(),'f'*16)['prior_entry_marker_observed'])
    def test_only_intentional_stage_and_error_and_valid_prior_token(self):
        for off,value in [(48,5),(56,(-67)%(1<<64)),(56,0)]:
            record=bytearray(self.record());struct.pack_into('<Q',record,off,value)
            with self.assertRaises(ValueError):m.prior_observation(bytes(record),'0123456789abcdef')
        for token in ['short','g'*16]:
            with self.assertRaises(ValueError):m.prior_observation(self.record(),token)
    def test_ordinary_authorization_or_implicit_mode_is_insufficient(self):
        for state in [{},dict(authorized=True),dict(diagnostic_only_exception_authorized=False),dict(diagnostic_only_exception_authorized=True,auto_readout_after_reset=True)]:
            with self.assertRaises(ValueError):m.validate_request(state,Path('.'),'SYNTHETIC','x')
    def test_controller_refuses_exceptionless_or_implicit_mode_before_phone_commands(self):
        spec=importlib.util.spec_from_file_location('forensic_controller_denial',ROOT/'tools/ace-auto-trial.py')
        controller=importlib.util.module_from_spec(spec);spec.loader.exec_module(controller)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);trial=root/'research/trial';trial.mkdir(parents=True)
            state=dict(phase='candidate-flashed-awaiting-reboot',candidate_flash_succeeded=True,authorized=True,auto_readout_after_reset=False,
                diagnostic_readout_only=True,diagnostic_only_exception_authorized=False,run_token='f'*16,readout_profile='android-v1')
            (trial/'state.json').write_text(json.dumps(state));transport=root/'transport.json';transport.write_text(json.dumps(dict(usb_adb='SYNTHETIC')))
            for flag in [[],['--diagnostic-readout-only']]:
                with patch.object(controller,'ROOT',root),patch.object(controller.sys,'argv',['auto',str(transport),str(trial),*flag]),patch.object(controller.subprocess,'run') as run:
                    with self.assertRaises(ValueError):controller.main()
                    run.assert_not_called()

    def test_return_read_does_not_retry_or_discard_nonzero_and_timeout_output(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);calls=[]
            def run(args):calls.append(args);return subprocess.CompletedProcess(args,1,b'complete-other-record',b'late error')
            self.assertEqual(m.observe_return_record('verified',out,0,run),b'complete-other-record')
            self.assertEqual(len(calls),1);self.assertEqual((out/'android-return-command-000.stderr').read_bytes(),b'late error')
            def timeout(args):calls.append(args);raise subprocess.TimeoutExpired(args,20,output=b'partial',stderr=b'timeout')
            self.assertEqual(m.observe_return_record('verified',out,1,timeout),b'partial')
            self.assertEqual(len(calls),2);self.assertEqual((out/'android-return-command-001.stdout').read_bytes(),b'partial')

    def test_package_pins_scope_and_explicit_exception(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(m,'ROOT',Path(tmp)):
            root=Path(tmp);trial=root/'research/trial';trial.mkdir(parents=True)
            pins={}
            for name in ['tools/ace-auto-trial.py','tools/ace_forensic_readout.py','ace/native-loader/main.c']:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes());pins[name]=m.sha(p)
            image=trial/'candidate.img'
            with image.open('wb') as f:f.truncate(67108864)
            digest=m.sha(image);name=str(image.relative_to(root));manifest=dict(format='ACE_FORENSIC_CANDIDATE_V1',serial='SYNTHETIC',run_token='f'*16,candidate_sha256=digest,candidate_file=name,
                diagnostic_readout_only=True,auto_readout_after_reset=False,initialize_empty_pmsg=False,android_sha256=m.ANDROID_SHA,
                controller_sha256='c'*64,validator_sha256=m.sha(Path(m.__file__)),source_sha256=pins,artifact_sha256={name:digest})
            path=trial/'manifest.json';path.write_text(json.dumps(manifest))
            state=dict(diagnostic_only_exception_authorized=True,diagnostic_readout_only=True,auto_readout_after_reset=False,readout_profile='android-v1',
                forensic_manifest_file=path.name,forensic_manifest_sha256=m.sha(path),run_token='f'*16,candidate_sha256=digest)
            self.assertEqual(m.validate_request(state,trial,'SYNTHETIC','c'*64),manifest)
            for change in [dict(diagnostic_only_exception_authorized=False),dict(auto_readout_after_reset=True),dict(readout_profile='ramdiag-v1'),dict(candidate_sha256='0'*64),dict(forensic_manifest_file='../manifest.json')]:
                with self.subTest(change=change),self.assertRaises(ValueError):m.validate_request(state|change,trial,'SYNTHETIC','c'*64)
            (root/'ace/native-loader/main.c').write_text('changed')
            with self.assertRaisesRegex(ValueError,'source changed'):m.validate_request(state,trial,'SYNTHETIC','c'*64)

if __name__=='__main__':unittest.main()
