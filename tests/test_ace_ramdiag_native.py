"""Execute the actual native envelope predicate, without a phone or mock parser."""
import ctypes
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'diagnostics/ace-ramdiag'

class NativeGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)
        (p/'guard.c').write_text('#include "native_record_guard.h"\nint check(const unsigned char*p,unsigned long n,const char*t){return ace_native_refusal_record(p,n,t);}\n')
        subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC','-O2','-I',str(SOURCE),str(p/'guard.c'),'-o',str(p/'guard.so')],check=True,capture_output=True)
        cls.library=ctypes.CDLL(str(p/'guard.so'));cls.check=cls.library.check
        cls.check.argtypes=[ctypes.c_char_p,ctypes.c_ulong,ctypes.c_char_p];cls.check.restype=ctypes.c_int
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def fixture(self):
        w=[0]*32;w[:4]=[0x313054414e454341,1,5,(-67)%(1<<64)]
        return b'ACEFALL1'+b'0123456789abcdef'+bytes(8)+struct.pack('<32Q',*w)
    def test_only_exact_current_record(self):
        raw=self.fixture();token=b'0123456789abcdef'
        self.assertTrue(self.check(raw,len(raw),token))
        for changed in [b'',raw[:-1],raw+b'\0',b'BADMAGIC'+raw[8:],raw[:24]+b'\1'+raw[25:]]:
            self.assertFalse(self.check(changed,len(changed),token))
        for other in [b'f'*16,b'0123456789abcdeg',token+b'0']:
            self.assertFalse(self.check(raw,len(raw),other))
    def test_invalid_stage_error_handoff_or_header_never_unlocks_modules(self):
        for offset,value in [(32,0),(40,2),(48,0),(48,8),(56,(-128)%(1<<64)),(56,0),(192,1)]:
            raw=bytearray(self.fixture());struct.pack_into('<Q',raw,offset,value)
            self.assertFalse(self.check(bytes(raw),len(raw),b'0123456789abcdef'))

    def test_all_current_normal_refusal_stages_preserve_diagnostic_access(self):
        for stage in range(1,8):
            for error in [-127,-67,-66,-64,-1]:
                raw=bytearray(self.fixture());struct.pack_into('<QQ',raw,48,stage,error%(1<<64))
                self.assertTrue(self.check(bytes(raw),len(raw),b'0123456789abcdef'))

class PhysicalGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('physical_assembler_test',SOURCE/'physical_assemble.py')
        cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
    def test_unaligned_partial_overlapping_and_repeated_refused(self):
        good={name:dict(start_512=2048+i*131072,sectors_512=131072,number=i+1) for i,name in enumerate(['boot_b','vendor_boot_b'])}
        self.assertEqual(self.module.geometry(json.dumps(good)),good)
        for key,value in [('start_512',2049),('start_512',134000),('sectors_512',16),('number',2),('number',True)]:
            bad=json.loads(json.dumps(good));bad['boot_b'][key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):self.module.geometry(json.dumps(bad))

if __name__=='__main__':unittest.main()
