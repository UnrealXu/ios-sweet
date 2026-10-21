"""Keep an acknowledged failed install distinct from verified partition IO."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ram_candidate_ledger_test',ROOT/'tools/ace-ram-candidate.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class FailedInstallLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.addCleanup(patch.stopall);patch.object(m,'ROOT',self.root).start()
        self.verified=self.root/'research/verified';self.failed=self.root/'research/failed'
        self.verified.mkdir(parents=True);self.failed.mkdir()
        self.baseline=dict(candidate_sha256='a'*64,phase='diagnostics-collected-fastboot-ready')
        self.save(self.verified/'state.json',self.baseline)
        image=self.failed/'candidate.img'
        with image.open('wb') as stream:stream.truncate(m.ram.PARTITION_BYTES)
        self.image_sha=m.sha(image)
        self.package=dict(format='ACE_RAM_CANDIDATE_V1',serial='SYNTHETIC',candidate_sha256=self.image_sha,run_token='0123456789abcdef',candidate_file=m.ref(image),artifact_sha256={m.ref(image):self.image_sha},source_sha256={'old_source.c':'0'*64})
        self.save(self.failed/'manifest.json',self.package)
        self.state=dict(phase='no-adb-after-240s-no-retry',candidate_flash_succeeded=True,candidate_flash_returncode=0,
                        partition_writes_started=[dict(partition='boot_b',sha256=self.image_sha)],candidate_sha256=self.image_sha,run_token=self.package['run_token'],
                        previous_trial_file=m.ref(self.verified/'state.json'),previous_trial_state_sha256=m.sha(self.verified/'state.json'),previous_boot_b_sha256=self.baseline['candidate_sha256'],
                        candidate_manifest_file=m.ref(self.failed/'manifest.json'),candidate_manifest_sha256=m.sha(self.failed/'manifest.json'))
        self.save(self.failed/'state.json',self.state)
        self.terminal=dict(returncode=1,phase=self.state['phase'],controller_restarted=False,writer_restarted=False,root_native_partition_readback_obtained=False)
        self.save(self.failed/'controller-terminal-observation.json',self.terminal)
        (self.failed/'flash-candidate.log').write_text("Sending 'boot_b' OKAY\nWriting 'boot_b' OKAY\nFinished\n")
        self.new=dict(candidate_sha256='b'*64,run_token='f'*16,serial='SYNTHETIC')
    def save(self,path,value):path.write_text(json.dumps(value)+'\n')
    def check(self):return m.failed_install_evidence(self.failed,self.verified,self.new)
    def test_historical_sources_not_replayed_and_ack_is_explicitly_not_readback(self):
        with patch.object(m,'source_pins',side_effect=AssertionError('historical sources must not be executed/validated as current')):
            result=self.check()
        self.assertEqual(result['previous_boot_b_sha256'],self.image_sha)
        self.assertFalse(result['previous_install_readback_verified'])
        self.assertNotEqual(result['previous_boot_b_sha256'],self.baseline['candidate_sha256'])
        self.assertEqual(json.loads((self.failed/'state.json').read_text())['phase'],'no-adb-after-240s-no-retry')
        for name,pin in result['previous_evidence_sha256'].items():self.assertEqual(m.sha(m.get(name)),pin)
    def test_incomplete_write_active_controller_wrong_partition_or_broken_ancestry_stop(self):
        variants=[dict(phase='candidate-flashed-awaiting-reboot'),dict(candidate_flash_succeeded=False),dict(candidate_flash_returncode=1),
                  dict(partition_writes_started=[]),dict(partition_writes_started=[dict(partition='userdata',sha256=self.image_sha)]),
                  dict(previous_trial_state_sha256='0'*64),dict(previous_boot_b_sha256='c'*64),dict(candidate_manifest_sha256='d'*64)]
        for change in variants:
            with self.subTest(change=change):
                self.save(self.failed/'state.json',self.state|change)
                with self.assertRaises(ValueError):self.check()
        self.save(self.failed/'state.json',self.state)
    def test_replay_same_image_or_same_token_is_rejected(self):
        for change in [dict(candidate_sha256=self.image_sha),dict(run_token=self.package['run_token'])]:
            with self.subTest(change=change):
                original=self.new;self.new=self.new|change
                with self.assertRaises(ValueError):self.check()
                self.new=original
    def test_missing_flash_or_controller_evidence_is_never_success(self):
        for change in [dict(returncode=0),dict(controller_restarted=True),dict(writer_restarted=True),dict(root_native_partition_readback_obtained=True)]:
            self.save(self.failed/'controller-terminal-observation.json',self.terminal|change)
            with self.assertRaises(ValueError):self.check()
        self.save(self.failed/'controller-terminal-observation.json',self.terminal)
        (self.failed/'flash-candidate.log').write_text("Sending 'boot_b' OKAY\nWriting 'boot_b' FAILED\n")
        with self.assertRaises(ValueError):self.check()
    def test_new_token_in_evidence_stops_preparation(self):
        (self.failed/'evidence.bin').write_bytes(self.new['run_token'].encode())
        with self.assertRaisesRegex(ValueError,'token present'):self.check()

if __name__=='__main__':unittest.main()
