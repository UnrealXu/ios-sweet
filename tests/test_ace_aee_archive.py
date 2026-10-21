"""Validate captured archives and bounded identity-bound read retries."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('auto_trial_aee',ROOT/'tools/ace-auto-trial.py')
trial=importlib.util.module_from_spec(spec);spec.loader.exec_module(trial)

def fixture():
    data=io.BytesIO()
    with tarfile.open(fileobj=data,mode='w') as archive:
        info=tarfile.TarInfo('data/vendor/aee_exp/current.HWT.dbg')
        payload=b'diagnostic bytes'*300
        info.size=len(payload);archive.addfile(info,io.BytesIO(payload))
    return data.getvalue()

class AeeArchiveTests(unittest.TestCase):
    def test_container_integrity_does_not_accept_truncated_member_or_footer(self):
        raw=fixture();self.assertTrue(trial.complete_tar(raw))
        for bad in [b'',raw[:4096],raw[:-1],raw[:512],raw[:-1024]+b'x'*1024]:
            self.assertFalse(trial.complete_tar(bad))
        corrupt=bytearray(raw);corrupt[100]^=1
        self.assertFalse(trial.complete_tar(bytes(corrupt)))
        # Header claims more content than the file carries, even with a footer.
        data=io.BytesIO()
        with tarfile.open(fileobj=data,mode='w') as archive:
            info=tarfile.TarInfo('large');info.size=65536
            archive.addfile(info,io.BytesIO(bytes(65536)))
        self.assertFalse(trial.complete_tar(data.getvalue()[:2048]+bytes(1024)))

    def test_each_bounded_read_refreshes_identity_and_retains_every_observation(self):
        good=fixture();bad=good[:4096]
        for replies,complete in [([bad,good],True),([bad,bad,bad],False),([good],True)]:
            with tempfile.TemporaryDirectory() as tmp:
                out=Path(tmp);events=[]
                def find():
                    events.append('identity');return 'verified-current-transport'
                def read(device):
                    self.assertEqual(device,'verified-current-transport')
                    self.assertEqual(events[-1],'identity')
                    events.append('read');return replies[events.count('read')-1]
                result=trial.collect_aee_archive(out,find,read)
                self.assertEqual(result['complete_tar'],complete)
                self.assertEqual(events,['identity','read']*len(replies))
                observations=json.loads((out/'aee-read-observations.json').read_text())
                self.assertEqual(observations,result['attempts'])
                for row,raw in zip(observations,replies):
                    self.assertEqual((out/row['file']).read_bytes(),raw)
                    self.assertEqual(row['sha256'],hashlib.sha256(raw).hexdigest())
                self.assertEqual((out/'aee-after.tar').read_bytes(),replies[-1])

    def test_missing_identity_waits_are_bounded_and_never_archive_or_reboot_retries(self):
        good=fixture();bad=good[:4096]
        for replies,archives,complete in [([None,'verified'],[good],True),
                (['verified',None,None,'verified'],[bad,good],True),
                ([None]*5,[],False),(['verified']+[None]*5,[bad],False)]:
            with tempfile.TemporaryDirectory() as tmp:
                out=Path(tmp);identities=iter(replies);reads=[];waits=[]
                def read(device):
                    self.assertEqual(device,'verified');raw=archives[len(reads)];reads.append(raw);return raw
                result=trial.collect_aee_archive(out,lambda:next(identities),read,waits.append)
                self.assertEqual(result['complete_tar'],complete)
                self.assertEqual(reads,archives)
                self.assertEqual(waits,[2]*sum(not v for v in replies[:-1]))
                lookups=json.loads((out/'aee-identity-observations.json').read_text())
                self.assertEqual([x['identity_verified'] for x in lookups],list(map(bool,replies)))
                self.assertEqual((out/'aee-after.tar').read_bytes(),archives[-1] if archives else b'')

if __name__=='__main__':unittest.main()
