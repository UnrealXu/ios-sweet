"""Controller accepts only the current phone diagnostic envelope."""
import importlib.util,struct,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'tools/ace-auto-trial.py'
s=importlib.util.spec_from_file_location('auto_trial',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class AutoTrialTests(unittest.TestCase):
    def fixture(self,error=-67):
        w=[0]*32;w[:4]=[0x313054414e454341,1,5,error%(1<<64)]
        return b'ACEFALL1'+b'0123456789abcdef'+bytes(8)+struct.pack('<32Q',*w)
    def test_reset_latch_and_other_failure_have_distinct_meaning(self):
        self.assertTrue(m.decode_record(self.fixture(),'0123456789abcdef')['automatic_pending_trial_return'])
        r=m.decode_record(self.fixture(-64),'0123456789abcdef');self.assertFalse(r['automatic_pending_trial_return']);self.assertFalse(r['ios_usable'])
    def test_other_trial_malformed_and_failed_android_handoff_rejected(self):
        good=self.fixture();bad=bytearray(good);struct.pack_into('<Q',bad,32+20*8,1)
        for data,token in [(good,'fedcba9876543210'),(good[:-1],'0123456789abcdef'),(bytes(bad),'0123456789abcdef'),(b'BADMAGIC'+good[8:],'0123456789abcdef')]:
            with self.assertRaises(ValueError):m.decode_record(data,token)

class ScreenEvidenceTests(unittest.TestCase):
    def test_real_saved_png_and_failed_capture_are_distinct(self):
        import subprocess,tempfile
        png=b'\x89PNG\r\n\x1a\n'+struct.pack('>I',13)+b'IHDR'+bytes(17)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);calls=[]
            def run(args):calls.append(args);return subprocess.CompletedProcess(args,0,png,b'')
            evidence=m.capture_screen('verified-phone',out,run)
            self.assertTrue(evidence['saved']);self.assertEqual((out/evidence['file']).read_bytes(),png)
            self.assertEqual(calls,[['adb','-s','verified-phone','exec-out','screencap','-p']])
        for raw,rc in [(b'',0),(b'not a PNG',0),(png,1)]:
            with tempfile.TemporaryDirectory() as tmp:
                out=Path(tmp)
                evidence=m.capture_screen('verified-phone',out,lambda args:subprocess.CompletedProcess(args,rc,raw,b''))
                self.assertFalse(evidence['saved']);self.assertFalse(list(out.iterdir()))
    def test_transport_exception_does_not_discard_other_logs(self):
        import tempfile
        def run(args):raise RuntimeError('transport gone')
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(m.capture_screen('verified-phone',Path(tmp),run)['saved'])

class ReturnRecordObservationTests(unittest.TestCase):
    def fixture(self):return AutoTrialTests().fixture()
    def test_exact_record_accepts_first_observation(self):
        expected=self.fixture();calls=[]
        m.verify_return_record(expected,lambda n:calls.append(n) or expected)
        self.assertEqual(calls,[0])
    def test_empty_or_partial_read_is_reobserved_without_mutation(self):
        expected=self.fixture();observations=iter([b'',expected[:40],expected]);calls=[]
        m.verify_return_record(expected,lambda n:calls.append(n) or next(observations))
        self.assertEqual(calls,[0,1,2])
    def test_complete_different_record_is_never_retried(self):
        expected=self.fixture();other=bytearray(expected);other[8]=ord('f');calls=[]
        def read(n):calls.append(n);return bytes(other)
        with self.assertRaisesRegex(RuntimeError,'different complete'):m.verify_return_record(expected,read)
        self.assertEqual(calls,[0])
    def test_repeated_malformed_observations_stop_after_three_reads(self):
        calls=[]
        with self.assertRaisesRegex(RuntimeError,'unreadable'):m.verify_return_record(self.fixture(),lambda n:calls.append(n) or b'bad')
        self.assertEqual(calls,[0,1,2])

class RebootTransportTests(unittest.TestCase):
    def setup_case(self,results,devices,fastboot):
        self.calls=[];self.checked=[];self.results=iter(results);self.devices=iter(devices);self.fastboot=iter(fastboot)
        def run(args):
            self.calls.append(args)
            return next(self.results)
        self.run=run
        self.find=lambda:next(self.devices)
        self.isfast=lambda:next(self.fastboot)
    def test_refreshes_before_reboot_and_validates_token(self):
        import subprocess
        self.setup_case([subprocess.CompletedProcess([],0,b'',b'')],['fresh'],[False])
        attempts=m.reboot_expected_phone('stale',self.find,self.isfast,self.checked.append,self.run)
        self.assertEqual(self.calls,[['adb','-s','fresh','reboot','bootloader']]);self.assertEqual(self.checked,['fresh']);self.assertEqual(len(attempts),1)
    def test_no_device_error_allows_one_fresh_identity_token_bound_attempt(self):
        import subprocess
        self.setup_case([subprocess.CompletedProcess([],1,b'',b"error: device 'old' not found"),subprocess.CompletedProcess([],0,b'',b'')],['old','new'],[False,False])
        attempts=m.reboot_expected_phone('old',self.find,self.isfast,self.checked.append,self.run)
        self.assertEqual([a[2] for a in self.calls],['old','new']);self.assertEqual(self.checked,['old','new']);self.assertEqual(len(attempts),2)
    def test_ambiguous_failure_never_reboots_again(self):
        import subprocess
        self.setup_case([subprocess.CompletedProcess([],1,b'',b'connection closed')],['fresh'],[False])
        self.assertEqual(len(m.reboot_expected_phone('stale',self.find,self.isfast,self.checked.append,self.run)),1);self.assertEqual(len(self.calls),1)
    def test_fastboot_observed_after_no_device_error_never_retries(self):
        import subprocess
        self.setup_case([subprocess.CompletedProcess([],1,b'',b'error: device not found')],['fresh'],[False,True])
        m.reboot_expected_phone('old',self.find,self.isfast,self.checked.append,self.run);self.assertEqual(len(self.calls),1)
    def test_token_mismatch_prevents_any_reboot(self):
        self.setup_case([],['fresh'],[False])
        def reject(_):raise RuntimeError('wrong current token')
        with self.assertRaises(RuntimeError):m.reboot_expected_phone('old',self.find,self.isfast,reject,self.run)
        self.assertEqual(self.calls,[])


    def test_remote_error_containing_not_found_is_not_a_no_device_retry(self):
        import subprocess
        self.setup_case([subprocess.CompletedProcess([],1,b'',b'remote: device handler not found')],['fresh'],[False])
        m.reboot_expected_phone('old',self.find,self.isfast,self.checked.append,self.run);self.assertEqual(len(self.calls),1)
    def test_second_missing_device_stops_after_two_attempts(self):
        import subprocess
        self.setup_case([subprocess.CompletedProcess([],1,b'',b'error: device not found'),subprocess.CompletedProcess([],1,b'',b'error: device not found')],['old','new'],[False,False])
        attempts=m.reboot_expected_phone('old',self.find,self.isfast,self.checked.append,self.run);self.assertEqual(len(attempts),2);self.assertEqual(len(self.calls),2)
    def test_timeout_is_ambiguous_and_must_be_observed_without_retry(self):
        self.setup_case([],['fresh'],[False])
        def timeout(args):self.calls.append(args);raise RuntimeError('bounded command timed out')
        attempts=m.reboot_expected_phone('old',self.find,self.isfast,self.checked.append,timeout)
        self.assertEqual(len(self.calls),1);self.assertIsNone(attempts[0]['returncode'])


class RootReadRecoveryTests(unittest.TestCase):
    def test_failures_retained_and_each_read_uses_fresh_identity(self):
        import tempfile,subprocess,json
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);devices=iter(['verified-old','verified-new']);calls=[];pauses=[]
            def run(args,timeout):
                calls.append(args);self.assertEqual(timeout,60)
                return subprocess.CompletedProcess(args,1,b'partial',b'connection closed') if len(calls)==1 else subprocess.CompletedProcess(args,0,b'complete',b'')
            result=m.read_root_evidence('dmesg',60,run,lambda:next(devices),out,pauses.append)
            self.assertEqual(result,b'complete');self.assertEqual([a[2] for a in calls],['verified-old','verified-new']);self.assertEqual(pauses,[2])
            observations=json.loads((out/'root-read-observations.json').read_text())
            self.assertEqual([x['returncode'] for x in observations],[1,0])
            self.assertEqual((out/observations[0]['stdout_file']).read_bytes(),b'partial')
            self.assertEqual((out/observations[0]['stderr_file']).read_bytes(),b'connection closed')
    def test_missing_identity_never_issues_read_and_exhaustion_preserved(self):
        import tempfile,json
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);calls=[]
            with self.assertRaises(m.RootEvidenceError):
                m.read_root_evidence('dmesg',60,lambda *a:calls.append(a),lambda:None,out,lambda _:None)
            self.assertEqual(calls,[])
            observations=json.loads((out/'root-read-observations.json').read_text())
            self.assertEqual(len(observations),4);self.assertTrue(all(not x['identity_verified'] for x in observations))
    def test_timeout_partial_output_is_retained(self):
        import tempfile,subprocess,json
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            def run(args,timeout):raise subprocess.TimeoutExpired(args,timeout,output=b'partial',stderr=b'late')
            with self.assertRaises(m.RootEvidenceError):m.read_root_evidence('dmesg',60,run,lambda:'verified',out,lambda _:None)
            observations=json.loads((out/'root-read-observations.json').read_text());self.assertEqual(len(observations),4)
            self.assertEqual((out/observations[3]['stdout_file']).read_bytes(),b'partial')
    def test_optional_log_failure_can_return_but_token_mismatch_still_stops(self):
        import tempfile,subprocess
        for mismatch in [False,True]:
            with tempfile.TemporaryDirectory() as tmp:
                out=Path(tmp);errors=[];calls=[]
                def missing():raise m.RootEvidenceError('all four attempts failed')
                self.assertEqual(m.optional_log_read('pstore-after.tar',missing,out,errors),b'')
                self.assertEqual(len(errors),1)
                def check(device):
                    self.assertEqual(device,'fresh-verified')
                    if mismatch:raise RuntimeError('different complete current record')
                def run(args):calls.append(args);return subprocess.CompletedProcess(args,0,b'',b'')
                if mismatch:
                    with self.assertRaises(RuntimeError):m.reboot_expected_phone('stale',lambda:'fresh-verified',lambda:False,check,run)
                    self.assertEqual(calls,[])
                else:
                    result=m.reboot_expected_phone('stale',lambda:'fresh-verified',lambda:False,check,run)
                    self.assertEqual(len(result),1);self.assertEqual(calls,[['adb','-s','fresh-verified','reboot','bootloader']])

class SeedSnapshotTests(unittest.TestCase):
    def fixture(self):
        raw=bytes(128)+b'\x71'+bytes(65536-129)
        b=bytearray(AutoTrialTests().fixture(-64));struct.pack_into('<Q',b,32+31*8,2**64-3);struct.pack_into('<Q',b,32+25*8,1)
        return bytes(b),raw
    def test_current_record_brackets_exact_complete_snapshot(self):
        import tempfile
        record,raw=self.fixture();calls=[]
        def read(cmd):calls.append(cmd);return raw if cmd.endswith('ace,pmsg-before-seed') else record
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);r=m.collect_seed_snapshot(record,'0123456789abcdef',read,out)
            self.assertTrue(r['verified']);self.assertEqual(r['nonzero_bytes'],1)
            self.assertEqual((out/r['file']).read_bytes(),raw);self.assertEqual(len(calls),3)
            self.assertEqual((out/'pmsg-snapshot-record-after.bin').read_bytes(),record)
    def test_short_or_changed_data_retained_and_different_token_stops(self):
        import tempfile
        record,raw=self.fixture()
        for bad in [raw[:-1],bytes(65536),raw[:129]+b'\x72'+raw[130:]]:
            with tempfile.TemporaryDirectory() as tmp:
                out=Path(tmp)
                def read(cmd):return bad if cmd.endswith('ace,pmsg-before-seed') else record
                with self.assertRaises(m.RootEvidenceError):m.collect_seed_snapshot(record,'0123456789abcdef',read,out)
                self.assertEqual((out/'pmsg-before-seed.bin').read_bytes(),bad)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);calls=[]
            def other(cmd):calls.append(cmd);return AutoTrialTests().fixture()
            with self.assertRaises(m.RootEvidenceError):m.collect_seed_snapshot(record,'0123456789abcdef',other,out)
            self.assertEqual(len(calls),1);self.assertFalse((out/'pmsg-before-seed.bin').exists())
    def test_pending_return_does_not_read_snapshot(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            calls=[];r=m.collect_seed_snapshot(AutoTrialTests().fixture(),'0123456789abcdef',lambda cmd:calls.append(cmd),Path(tmp))
            self.assertFalse(r['expected']);self.assertEqual(calls,[])

if __name__=='__main__':unittest.main()
