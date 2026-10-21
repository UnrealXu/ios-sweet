"""One warm-reset attempt per token, without changing captured ring bytes."""
import ctypes as c
from pathlib import Path
import struct,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
TOKEN=b'0123456789abcdef'
MARKER=b'\nACETRIAL1:'+TOKEN+b': armed\n'
class TrialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)/'trial.so'
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-shared','-fPIC',str(ROOT/'ace/pstore_ring.c'),str(ROOT/'ace/pstore_trial.c'),'-o',str(p)],check=True)
        cls.lib=c.CDLL(str(p));cls.lib.ace_pstore_trial_pending.argtypes=[c.c_void_p,c.c_size_t,c.c_char_p]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def check(self,data,expected,token=TOKEN):
        b=c.create_string_buffer(data+b'GUARD');before=b.raw
        self.assertEqual(self.lib.ace_pstore_trial_pending(b,65536,token),expected)
        self.assertEqual(b.raw,before)
    def test_exact_token_and_complete_record_only(self):
        for body,expected in [(b'',0),(MARKER,1),(b'old log'+MARKER+b'kernel log',1),(MARKER[:-1],0),(MARKER.replace(TOKEN,b'fedcba9876543210'),0),(b'ACEXNU1:'+TOKEN+b': entry EL1\n',0)]:
            self.check(struct.pack('<III',0x43474244,len(body),len(body))+body+bytes(65524-len(body)),expected)
    def test_chronological_wrap_boundary_and_stale_unstored_bytes(self):
        capacity=65524
        for start in [1,5,capacity-len(MARKER)//2,capacity-1]:
            logical=MARKER+b'x'*(capacity-len(MARKER));physical=logical[-start:]+logical[:-start]
            self.check(struct.pack('<III',0x43474244,start,capacity)+physical,1)
        self.check(struct.pack('<III',0x43474244,0,0)+MARKER+bytes(capacity-len(MARKER)),0)
    def test_invalid_state_size_and_token_preserve_every_byte(self):
        self.check(bytes(65536),-3)
        self.check(struct.pack('<III',0x43474244,8,3)+bytes(65524),-3)
        data=struct.pack('<III',0x43474244,0,0)+bytes(65524)
        for token in [None,b'',b'A'*16,b'0'*15,b'0'*17]:self.check(data,-1,token)
        b=c.create_string_buffer(data);before=b.raw
        for n in [0,12,65535,65537,1<<40]:self.assertEqual(self.lib.ace_pstore_trial_pending(b,n,TOKEN),-1)
        self.assertEqual(self.lib.ace_pstore_trial_pending(None,65536,TOKEN),-1)
        self.assertEqual(b.raw,before)
if __name__=='__main__':unittest.main()
