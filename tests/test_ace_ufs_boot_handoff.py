import ctypes as c
from pathlib import Path
import subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class BootHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();p=Path(cls.temp.name)
        (p/'wrap.c').write_text('#include "ufs_boot_handoff.h"\nint first(uint32_t s,const uint32_t *v){return ace_ufs_boot_linereset(s,v);}\nint cleared(uint32_t s,const uint32_t *v,uint32_t n,const uint32_t *w){return ace_ufs_boot_linereset_cleared(s,v,n,w);}\n')
        subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I',str(ROOT/'ace'),str(p/'wrap.c'),'-o',str(p/'wrap.so')],check=True)
        cls.lib=c.CDLL(str(p/'wrap.so'));cls.lib.first.argtypes=[c.c_uint32,c.POINTER(c.c_uint32)];cls.lib.cleared.argtypes=[c.c_uint32,c.POINTER(c.c_uint32),c.c_uint32,c.POINTER(c.c_uint32)]
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def test_exact_phone_snapshot_needs_empty_second_sample(self):
        first=(c.c_uint32*5)(0x80000010,0,0,0,0);empty=(c.c_uint32*5)(0,0,0,0,0)
        for status in [0,4]:
            self.assertEqual(self.lib.first(status,first),1)
            self.assertEqual(self.lib.cleared(status,first,status,empty),1)
            self.assertEqual(self.lib.cleared(status,first,status,first),0)
    def test_every_other_phy_bit_and_any_other_layer_code_refuses(self):
        for layer in range(5):
            for bit in range(31):
                value=[0x80000010,0,0,0,0];value[layer]|=1<<bit
                if layer==0 and bit==4:continue
                codes=(c.c_uint32*5)(*value)
                with self.subTest(layer=layer,bit=bit):self.assertEqual(self.lib.first(0,codes),0)
        for value in [0,0x10,0x80000000,0x80000001]:self.assertEqual(self.lib.first(0,(c.c_uint32*5)(value,0,0,0,0)),0)
    def test_second_error_or_fatal_either_sample_or_null_refuses(self):
        first=(c.c_uint32*5)(0x80000010,0,0,0,0);empty=(c.c_uint32*5)(0,0,0,0,0)
        for bit in [7,11,16,17,18]:
            self.assertEqual(self.lib.cleared(1<<bit,first,0,empty),0);self.assertEqual(self.lib.cleared(0,first,1<<bit,empty),0)
        for layer in range(5):
            bad=(c.c_uint32*5)(0,0,0,0,0);bad[layer]=0x80000001
            self.assertEqual(self.lib.cleared(0,first,0,bad),0)
        self.assertEqual(self.lib.first(0,None),0);self.assertEqual(self.lib.cleared(0,first,0,None),0)
    def test_patch_uses_exact_host_tested_policy(self):
        patch=(ROOT/'xnu/patches/0093-ace-verify-startup-linereset-cleared.patch').read_text();part=patch.split('+++ b/iokit/Kernel/arm/AceUFSBootHandoff.h\n',1)[1]
        content=''.join(line[1:]+'\n' for line in part.splitlines() if line.startswith('+'))
        self.assertEqual(content,(ROOT/'ace/ufs_boot_handoff.h').read_text())
