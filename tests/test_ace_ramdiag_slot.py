"""Exercise the actual freestanding B-slot parser on host, with no device I/O."""
import ctypes
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

class RamDiagSlotGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='ace-slot-guard-')
        folder=Path(cls.temp.name);source=folder/'wrapper.c';library=folder/'guard.so'
        source.write_text('#include "slot_guard.h"\nint check(const unsigned char *a,unsigned long n,const unsigned char *b,unsigned long m){return ace_slot_states_valid(ace_slot_cmdline(a,n),ace_slot_bootconfig(b,m));}\n')
        subprocess.run(['cc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-I',str(ROOT/'diagnostics/ace-ramdiag'),str(source),'-o',str(library)],check=True,capture_output=True)
        cls.library=ctypes.CDLL(str(library));cls.check=cls.library.check
        cls.check.argtypes=[ctypes.c_char_p,ctypes.c_ulong,ctypes.c_char_p,ctypes.c_ulong];cls.check.restype=ctypes.c_int

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def valid(self,cmd=b'',boot=b''):
        return bool(self.check(cmd,len(cmd),boot,len(boot)))

    def test_cmdline_and_bootconfig_real_syntax(self):
        self.assertTrue(self.valid(b'console=ttyAMA0 androidboot.slot_suffix=_b loglevel=8\n'))
        self.assertTrue(self.valid(boot=b'androidboot.slot_suffix = "_b"\n'))
        self.assertTrue(self.valid(b'androidboot.slot_suffix="_b"',b' androidboot.slot_suffix=_b\r\n'))

    def test_absent_wrong_malformed_and_prefix_values_refused(self):
        for value in [b'',b'_a',b'b',b'_b_extra',b'_b\0',b'"_b',b'"_b", "_a"']:
            with self.subTest(value=value):
                self.assertFalse(self.valid(b'androidboot.slot_suffix='+value))
                self.assertFalse(self.valid(boot=b'androidboot.slot_suffix = '+value+b'\n'))
        self.assertFalse(self.valid())
        self.assertFalse(self.valid(b'prefix_androidboot.slot_suffix=_b'))

    def test_conflicts_in_either_authority_never_allow_b(self):
        self.assertFalse(self.valid(b'androidboot.slot_suffix=_b androidboot.slot_suffix=_a'))
        self.assertFalse(self.valid(b'androidboot.slot_suffix=_a androidboot.slot_suffix=_b'))
        self.assertFalse(self.valid(b'androidboot.slot_suffix=_b',b'androidboot.slot_suffix="_a"\n'))
        self.assertFalse(self.valid(boot=b'androidboot.slot_suffix="_b"\nandroidboot.slot_suffix="_a"\n'))
        self.assertFalse(self.valid(b'androidboot.slot_suffix=_b',b'androidboot.slot_suffix\n'))
        self.assertFalse(self.valid(b'androidboot.slot_suffix=_b',b'androidboot.slot_suffix \n'))

    def test_unrelated_properties_do_not_supply_identity(self):
        self.assertFalse(self.valid(boot=b'androidboot.slot_suffix_extra="_b"\n'))
        self.assertTrue(self.valid(b'androidboot.slot_suffix=_b',b'other="_a"\n'))

if __name__=='__main__':unittest.main()
