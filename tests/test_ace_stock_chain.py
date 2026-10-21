"""Packaging/evidence guards only. Never runs ADB, fastboot or QEMU."""
import copy
import hashlib
import importlib.util
import json
import random
from pathlib import Path
import subprocess
import unittest
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
wrap=load('stock_chain_wrap','tools/ace-stock-chain-boot.py')
fixture=load('probe_fixture_for_chain','tests/test_ace_probe_boot.py')

class StockChainTests(unittest.TestCase):
    def test_current_ramdisk_header_and_metadata_preserved_with_valid_full_partition_footer(self):
        before=fixture.fixture();compressed=wrap.boot.deterministic_gzip(b'new diagnostic chain test'*800)
        with mock.patch.object(wrap,'BACKUP_SHA',hashlib.sha256(before).hexdigest()):
            after,old,new,ramdisk=wrap.package(before,compressed)
        self.assertEqual(wrap.boot.inflate(after[4096:4096+new['kernel_bytes']]),b'new diagnostic chain test'*800)
        self.assertEqual(after[new['ramdisk_offset']:new['ramdisk_offset']+new['ramdisk_bytes']],ramdisk)
        self.assertEqual(ramdisk,b'stock-ramdisk-payload')
        header=bytearray(after[:4096]);header[8:12]=before[8:12]
        self.assertEqual(bytes(header),before[:4096])
        self.assertEqual(len(after),len(before));self.assertEqual(after[-64:-60],b'AVBf')
        a,b=old['avb'],new['avb']
        self.assertEqual(before[a['vbmeta_offset']:a['vbmeta_offset']+a['vbmeta_size']],after[b['vbmeta_offset']:b['vbmeta_offset']+b['vbmeta_size']])
        self.assertEqual(b['original_image_size'],new['payload_end'])
        self.assertEqual(b['vbmeta_offset'],new['payload_end'])
        self.assertFalse(b['authentication_verified'])
    def test_wrong_backup_pin_refused(self):
        with self.assertRaisesRegex(ValueError,'backup changed'):wrap.package(fixture.fixture(),b'x')
    def test_explicit_diagnostic_ramdisk_preserves_other_header_fields_and_avb(self):
        small=fixture.fixture();before=small[:-64]+bytes(32768)+small[-64:]
        compressed=wrap.boot.deterministic_gzip(random.Random(1).randbytes(8192))
        # Cross page boundaries in both payloads to detect stale offsets/sizes.
        ramdisk=b'diagnostic ramdisk fixture'*500
        pin=hashlib.sha256(ramdisk).hexdigest()
        with mock.patch.object(wrap,'BACKUP_SHA',hashlib.sha256(before).hexdigest()):
            after,old,new,selected=wrap.package(before,compressed,diagnostic_ramdisk=ramdisk,diagnostic_ramdisk_sha256=pin)
        self.assertEqual(selected,ramdisk)
        self.assertEqual(after[new['ramdisk_offset']:new['ramdisk_offset']+new['ramdisk_bytes']],ramdisk)
        self.assertEqual(after[4096:4096+new['kernel_bytes']],compressed)
        header=bytearray(after[:4096]);header[8:16]=before[8:16]
        self.assertEqual(bytes(header),before[:4096]);self.assertEqual(len(after),len(before))
        a,b=old['avb'],new['avb']
        self.assertEqual(before[a['vbmeta_offset']:a['vbmeta_offset']+a['vbmeta_size']],after[b['vbmeta_offset']:b['vbmeta_offset']+b['vbmeta_size']])
        self.assertEqual(b['original_image_size'],new['payload_end'])
        self.assertFalse(b['authentication_verified'])
    def test_diagnostic_ramdisk_missing_or_wrong_pin_empty_and_overflow_refused(self):
        before=fixture.fixture();pin=hashlib.sha256(b'ramdisk').hexdigest()
        cases=[({'diagnostic_ramdisk':b'ramdisk'},'together'),
               ({'diagnostic_ramdisk_sha256':pin},'together'),
               ({'diagnostic_ramdisk':b'ramdisk','diagnostic_ramdisk_sha256':'0'*64},'hash mismatch'),
               ({'diagnostic_ramdisk':b'ramdisk','diagnostic_ramdisk_sha256':'G'*64},'Invalid diagnostic ramdisk SHA256'),
               ({'diagnostic_ramdisk':b'','diagnostic_ramdisk_sha256':hashlib.sha256(b'').hexdigest()},'size/type'),
               ({'diagnostic_ramdisk':b'x'*len(before),'diagnostic_ramdisk_sha256':'0'*64},'size/type')]
        with mock.patch.object(wrap,'BACKUP_SHA',hashlib.sha256(before).hexdigest()):
            for kwargs,message in cases:
                with self.subTest(kwargs=list(kwargs),message=message),self.assertRaisesRegex(ValueError,message):
                    wrap.package(before,b'kernel',**kwargs)
            large=b'x'*(len(before)-1)
            with self.assertRaisesRegex(ValueError,'exceeds partition'):
                wrap.package(before,b'kernel',diagnostic_ramdisk=large,diagnostic_ramdisk_sha256=hashlib.sha256(large).hexdigest())
    def test_evidence_path_escape_refused(self):
        for path in ['../foo','/etc/passwd','research/ace-stock-chain-20261019/../../../etc/passwd','research/ipsw-x/a']:
            with self.subTest(path=path),self.assertRaises(ValueError):wrap.private_file(path)
    def test_missing_evidence_and_false_scope_refused(self):
        base={'status':'pass','hardware_tested':False,'ios_deployable':False}
        for r in [{},base,dict(base,hardware_tested=True),dict(base,ios_deployable=True)]:
            with self.subTest(r=r),self.assertRaises(ValueError):wrap.validate(r)
    def test_optimized_tools_refuse_before_output_change(self):
        report=ROOT/'research/ace-stock-chain-20261019/verification.json'
        before=report.read_bytes() if report.exists() else None
        for script in ['ace/stock-chain/build.py','ace/stock-chain/verify.py','tools/ace-stock-chain-boot.py']:
            p=subprocess.run(['python3','-O',str(ROOT/script)],capture_output=True,text=True,timeout=10)
            self.assertNotEqual(p.returncode,0);self.assertIn('Optimized',p.stderr)
            self.assertEqual(report.read_bytes() if report.exists() else None,before)
    def test_current_saved_evidence_and_source_mutation(self):
        report=ROOT/'research/ace-stock-chain-20261019/verification.json'
        if not report.exists():self.skipTest('Local private execution evidence absent')
        r=json.loads(report.read_text())
        image,build=wrap.validate(r)
        self.assertEqual(len(image),build['images']['pmsg']['bytes'])
        bad=copy.deepcopy(r);bad['sources']['ace/stock-chain/start.S']='0'*64
        with self.assertRaisesRegex(ValueError,'Changed source'):wrap.validate(bad)
        bad=copy.deepcopy(r);bad['cases'][1]=copy.deepcopy(bad['cases'][0])
        with self.assertRaisesRegex(ValueError,'duplicate'):wrap.validate(bad)

if __name__=='__main__':unittest.main()
