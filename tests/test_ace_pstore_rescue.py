"""Execute the one-RAM/one-rescue decision on chronological retained records."""
import ctypes as c
from pathlib import Path
import struct,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
TOKEN=b'0123456789abcdef';ARM=b'\nACETRIAL1:'+TOKEN+b': armed\n'
HAND=b'\nACEANDROID1:'+TOKEN+b': pending handoff\n';RESCUE=b'\nACERESCUE1:'+TOKEN+b': selected\n';MAGIC=0x3130455543534552
class RescueLatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)/'test.so'
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-shared','-fPIC',*[str(ROOT/'ace'/n) for n in ['pstore_ring.c','pstore_trial.c','pstore_rescue.c']],'-o',str(p)],check=True,capture_output=True)
        cls.lib=c.CDLL(str(p));cls.read=cls.lib.ace_pstore_ram_attempt;cls.read.argtypes=[c.c_void_p,c.c_size_t,c.c_char_p]
        cls.write=cls.lib.ace_pstore_rescue_selected;cls.write.argtypes=[c.c_void_p,c.c_size_t,c.c_char_p,c.c_char_p,c.c_size_t]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def record(self,rescue=False):
        w=[0]*32;w[:4]=[0x313054414e454341,1,5,(-67)%(1<<64)];w[31]=MAGIC if rescue else 0
        return b'ACEFALL1'+TOKEN+bytes(8)+struct.pack('<32Q',*w)
    def ring(self,body):return c.create_string_buffer(struct.pack('<III',0x43474244,len(body),len(body))+body+bytes(65524-len(body))+b'GUARD')
    def check(self,zone,expected):
        before=zone.raw;self.assertEqual(self.read(zone,65536,TOKEN),expected);self.assertEqual(zone.raw,before)
    def test_one_ram_then_one_rescue_then_stop(self):
        self.check(self.ring(ARM),0)
        zone=self.ring(ARM+HAND+self.record());self.check(zone,1)
        record=self.record(True);self.assertEqual(self.write(zone,65536,TOKEN,record,len(record)),0);self.check(zone,2)
        before=zone.raw;self.assertLess(self.write(zone,65536,TOKEN,record,len(record)),0);self.assertEqual(zone.raw,before);self.assertEqual(zone.raw[65536:65541],b'GUARD')
    def test_bad_order_duplicates_or_ascii_only_never_select_ram_again(self):
        normal=HAND+self.record();rescue=RESCUE+self.record(True)
        for body in [b'',ARM+normal+normal,ARM+rescue,normal+ARM,ARM+ARM,ARM+normal+rescue+rescue,ARM+HAND,ARM+HAND+b'x'*288,ARM+normal+RESCUE]:
            zone=self.ring(body);before=zone.raw;self.assertLess(self.read(zone,65536,TOKEN),0,body[:90]);self.assertEqual(zone.raw,before)
        for n in range(13,len(HAND)):
            self.assertLess(self.read(self.ring(ARM+HAND[:n]),65536,TOKEN),0)
    def test_wrong_token_corrupt_record_and_truncation_are_read_only(self):
        raw=self.record()
        for offset in [0,8,24,32,40,48,56,192,280]:
            changed=bytearray(raw);changed[offset]^=1
            zone=self.ring(ARM+HAND+changed);before=zone.raw;self.assertLess(self.read(zone,65536,TOKEN),0);self.assertEqual(zone.raw,before)
        for n in range(288):self.assertLess(self.read(self.ring(ARM+HAND+raw[:n]),65536,TOKEN),0)
        zone=self.ring(ARM+HAND+raw);before=zone.raw
        for token in [None,b'',b'f'*16,b'G'*16,b'0'*17]:
            self.assertLess(self.read(zone,65536,token),0);self.assertEqual(zone.raw,before)
        for n in [0,12,65535,65537]:self.assertLess(self.read(zone,n,TOKEN),0)
    def test_wrapped_complete_packets_and_opaque_record_bytes(self):
        logical=b'x'*(65524-len(ARM+HAND+self.record()))+ARM+HAND+self.record()
        for start in [1,17,65520]:
            physical=logical[-start:]+logical[:-start];zone=c.create_string_buffer(struct.pack('<III',0x43474244,start,65524)+physical);self.check(zone,1)
        # Stale markers from another token do not consume this token's attempt.
        self.check(self.ring((ARM+HAND+self.record()).replace(TOKEN,b'f'*16)+ARM),0)
    def test_selection_requires_valid_rescue_envelope_and_previous_handoff(self):
        for body in [ARM,ARM+HAND+self.record()]:
            for record in [b'',self.record(),self.record(True)[:-1]]:
                zone=self.ring(body);before=zone.raw;self.assertLess(self.write(zone,65536,TOKEN,record,len(record)),0);self.assertEqual(zone.raw,before)
        bad=c.create_string_buffer(bytes(65536));self.assertLess(self.read(bad,65536,TOKEN),0)
if __name__=='__main__':unittest.main()
