"""Explicit all-zero pmsg lifecycle, separate from the noninitializing codec."""
import ctypes as c
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]

class PstoreSeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();lib=Path(cls.tmp.name)/'seed.so'
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-shared','-fPIC',
            str(ROOT/'ace/pstore_ring.c'),str(ROOT/'ace/pstore_seed.c'),'-o',str(lib)],check=True)
        cls.lib=c.CDLL(str(lib));cls.lib.ace_pstore_seed_empty.argtypes=[c.c_void_p,c.c_size_t]
        cls.lib.ace_pstore_ring_validate.argtypes=[c.c_void_p,c.c_size_t,c.c_void_p]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_only_signature_written_and_second_call_preserves_existing_ring(self):
        b=c.create_string_buffer(bytes(65536)+b'guard')
        self.assertEqual(self.lib.ace_pstore_seed_empty(b,65536),1)
        self.assertEqual(b.raw,b'DBGC'+bytes(65532)+b'guard\0')
        self.assertEqual(self.lib.ace_pstore_ring_validate(b,65536,None),0)
        before=b.raw;self.assertEqual(self.lib.ace_pstore_seed_empty(b,65536),0)
        self.assertEqual(b.raw,before)
    def test_unknown_data_anywhere_and_corrupt_headers_never_overwritten(self):
        for pos in [0,1,4,8,11,12,128,32768,65535]:
            data=bytearray(65536);data[pos]=0x71;b=c.create_string_buffer(bytes(data))
            before=b.raw;self.assertEqual(self.lib.ace_pstore_seed_empty(b,65536),-3)
            self.assertEqual(b.raw,before)
        for start,size in [(7,3),(65525,65525),(1,65524)]:
            data=bytearray(65536);struct.pack_into('<III',data,0,0x43474244,start,size)
            data[300]=0xab;b=c.create_string_buffer(bytes(data));before=b.raw
            expected=0 if size<=65524 and start<=size else -3
            self.assertEqual(self.lib.ace_pstore_seed_empty(b,65536),expected)
            self.assertEqual(b.raw,before)
    def test_bad_spans_and_sizes_refuse_before_access(self):
        b=c.create_string_buffer(bytes(65536));before=b.raw
        for n in [0,12,65535,65537,1<<40]:
            self.assertEqual(self.lib.ace_pstore_seed_empty(b,n),-1)
            self.assertEqual(b.raw,before)
        self.assertEqual(self.lib.ace_pstore_seed_empty(None,65536),-1)
        self.assertEqual(self.lib.ace_pstore_seed_empty(c.c_void_p((1<<64)-4),65536),-2)

if __name__=='__main__':unittest.main()
