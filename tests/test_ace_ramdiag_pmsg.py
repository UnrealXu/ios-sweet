"""Exercise sysfs device-number parsing used by the freestanding PID1."""
import ctypes as c
from pathlib import Path
import subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class PmsgDeviceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)
        (p/'test.c').write_text('#include "pmsg_trace.h"\nint parse(const unsigned char*s,unsigned long n){return ace_pmsg_major(s,n);}\n')
        subprocess.run(['cc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-I',str(ROOT/'diagnostics/ace-ramdiag'),str(p/'test.c'),'-o',str(p/'test.so')],check=True,capture_output=True)
        cls.lib=c.CDLL(str(p/'test.so'));cls.parse=cls.lib.parse;cls.parse.argtypes=[c.c_char_p,c.c_ulong]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_dynamic_character_major_minor_zero(self):
        for n in [1,10,63,250,255,256,511,4095]:
            raw=f'{n}:0\n'.encode();self.assertEqual(self.parse(raw,len(raw)),n)
    def test_malformed_truncated_or_wrong_device_is_never_guessed(self):
        for raw in [b'',b'0:0\n',b'01:0\n',b'4096:0\n',b'250:1\n',b'250:00\n',b'250:0',b'250:0\nmore',b'250:0\0',b' 250:0\n',b'-1:0\n',b'99999999999999:0\n',b'250 0\n']:
            self.assertEqual(self.parse(raw,len(raw)),-1,raw)
        self.assertEqual(self.parse(None,0),-1)
if __name__=='__main__':unittest.main()
