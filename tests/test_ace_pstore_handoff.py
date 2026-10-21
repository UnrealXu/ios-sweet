"""Run the actual durable boundary encoder on valid, stale and wrapped rings."""
import ctypes as c
from pathlib import Path
import struct,subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
TOKEN=b'0123456789abcdef'
ARM=b'\nACETRIAL1:'+TOKEN+b': armed\n'
class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)
        (p/'test.c').write_text('#include "pstore_handoff.h"\nint trace(void*z,unsigned long n,const char*t,const unsigned char*r,unsigned long l){return ace_pstore_android_handoff(z,n,t,r,l);}\n')
        subprocess.run(['cc','-O2','-Wall','-Wextra','-Werror','-shared','-fPIC','-I',str(ROOT/'ace'),str(p/'test.c'),str(ROOT/'ace/pstore_ring.c'),str(ROOT/'ace/pstore_trial.c'),'-o',str(p/'test.so')],check=True)
        cls.lib=c.CDLL(str(p/'test.so'));cls.trace=cls.lib.trace
        cls.trace.argtypes=[c.c_void_p,c.c_size_t,c.c_char_p,c.c_char_p,c.c_size_t]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def record(self):
        w=[0]*32;w[:4]=[0x313054414e454341,1,5,(-67)%(1<<64)]
        return b'ACEFALL1'+TOKEN+bytes(8)+struct.pack('<32Q',*w)
    def ring(self,body=ARM):return struct.pack('<III',0x43474244,len(body),len(body))+body+bytes(65524-len(body))
    def logical(self,b):
        _,start,size=struct.unpack_from('<III',b);data=b[12:65536]
        return data[start:size]+data[:start]
    def test_exact_record_appended_without_modifying_input_or_guards(self):
        record=self.record();zone=c.create_string_buffer(self.ring()+b'GUARD')
        self.assertEqual(self.trace(zone,65536,TOKEN,record,len(record)),0)
        self.assertEqual(self.logical(zone.raw),ARM+b'\nACEANDROID1:'+TOKEN+b': pending handoff\n'+record)
        self.assertEqual(zone.raw[65536:65541],b'GUARD')
    def test_stale_missing_corrupt_ring_and_record_are_read_only(self):
        for data in [bytes(65536),self.ring(b''),self.ring(ARM.replace(TOKEN,b'f'*16)),struct.pack('<III',0x43474244,8,3)+bytes(65524)]:
            zone=c.create_string_buffer(data);before=zone.raw
            self.assertLess(self.trace(zone,65536,TOKEN,self.record(),288),0);self.assertEqual(zone.raw,before)
        records=[b'',self.record()[:-1],b'BADMAGIC'+self.record()[8:]]
        for offset,value in [(32,0),(40,2),(48,2),(56,(-66)%(1<<64)),(192,1)]:
            b=bytearray(self.record());struct.pack_into('<Q',b,offset,value);records.append(bytes(b))
        for record in records:
            zone=c.create_string_buffer(self.ring());before=zone.raw
            self.assertLess(self.trace(zone,65536,TOKEN,record,len(record)),0);self.assertEqual(zone.raw,before)
    def test_full_ring_wrap_preserves_new_complete_boundary(self):
        capacity=65524;start=capacity-3;logical=ARM+b'x'*(capacity-len(ARM));physical=logical[-start:]+logical[:-start]
        zone=c.create_string_buffer(struct.pack('<III',0x43474244,start,capacity)+physical)
        record=self.record();self.assertEqual(self.trace(zone,65536,TOKEN,record,288),0)
        self.assertTrue(self.logical(zone.raw).endswith(b'\nACEANDROID1:'+TOKEN+b': pending handoff\n'+record))
if __name__=='__main__':unittest.main()
