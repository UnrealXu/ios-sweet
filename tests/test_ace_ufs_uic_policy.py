import ctypes as c
from pathlib import Path
import subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class UicPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t=tempfile.TemporaryDirectory();p=Path(cls.t.name)
        (p/'wrap.c').write_text('#include "ufs_uic_policy.h"\nint test(uint32_t s,const uint32_t *v){return ace_ufs_uic_empty_event(s,v);}\n')
        subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I',str(ROOT/'ace'),str(p/'wrap.c'),'-o',str(p/'wrap.so')],check=True)
        cls.lib=c.CDLL(str(p/'wrap.so'));cls.lib.test.argtypes=[c.c_uint32,c.POINTER(c.c_uint32)]
    @classmethod
    def tearDownClass(cls):cls.t.cleanup()
    def test_empty_latched_event_only(self):
        for value in [0,0x80000000]:
            codes=(c.c_uint32*5)(*[value]*5);self.assertEqual(self.lib.test(4,codes),1)
            self.assertEqual(self.lib.test(0x404,codes),1)
        self.assertEqual(self.lib.test(4,None),0)
    def test_every_meaningful_or_reserved_bit_in_any_layer_refuses(self):
        for layer in range(5):
            for bit in range(31):
                codes=(c.c_uint32*5)(0,0,0,0,0);codes[layer]=0x80000000|(1<<bit);before=bytes(codes)
                with self.subTest(layer=layer,bit=bit):
                    self.assertEqual(self.lib.test(4,codes),0);self.assertEqual(bytes(codes),before)
    def test_fatal_or_link_lost_or_no_event_refuses(self):
        codes=(c.c_uint32*5)(0,0,0,0,0)
        for status in [0,1,0x400,0x84,0x804,0x10004,0x20004,0x40004]:self.assertEqual(self.lib.test(status,codes),0)
    def test_policy_is_exactly_the_kernel_patch_file(self):
        patch=(ROOT/'xnu/patches/0092-ace-uic-error-snapshot-and-lun2-read.patch').read_text()
        header=patch.split('+++ b/iokit/Kernel/arm/AceUFSUICPolicy.h\n',1)[1]
        actual=''.join(line[1:]+'\n' for line in header.splitlines() if line.startswith('+'))
        self.assertEqual(actual,(ROOT/'ace/ufs_uic_policy.h').read_text())
