import ctypes as c
from pathlib import Path
import subprocess,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class ColdHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();p=Path(cls.temp.name)
        (p/'wrap.c').write_text('#include "ufs_cold_handoff.h"\nint quiet(const uint32_t *w){return ace_ufs_codes_quiet(w);}\nint ready(uint32_t s,const uint32_t *w){return ace_ufs_cold_final_ready(s,w);}\nint ack(uint32_t s,const uint32_t *w,uint32_t t,const uint32_t *v){return ace_ufs_cold_can_ack(s,w,t,v);}\n')
        subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I',str(ROOT/'ace'),str(p/'wrap.c'),'-o',str(p/'wrap.so')],check=True)
        cls.lib=c.CDLL(str(p/'wrap.so'));cls.lib.quiet.argtypes=[c.POINTER(c.c_uint32)];cls.lib.ready.argtypes=[c.c_uint32,c.POINTER(c.c_uint32)];cls.lib.ack.argtypes=[c.c_uint32,c.POINTER(c.c_uint32),c.c_uint32,c.POINTER(c.c_uint32)]
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def test_exact_observed_phy_dl_needs_quiet_followup_and_cleared_interrupt(self):
        old=(c.c_uint32*5)(0x80000011,0x80005a10,0,0,0);empty=(c.c_uint32*5)(0,0,0,0,0)
        self.assertEqual(self.lib.ack(4,old,4,empty),1);self.assertEqual(self.lib.ack(4,old,4,old),0)
        self.assertEqual(self.lib.ready(4,empty),0);self.assertEqual(self.lib.ready(0,empty),1)
    def test_invalid_retained_codes_are_not_active_but_valid_codes_are(self):
        invalid=(c.c_uint32*5)(0x10,0x5a10,7,0x7f,1);self.assertEqual(self.lib.quiet(invalid),1)
        masks=[0x1f,0xffff,7,0x7f,1]
        for layer,mask in enumerate(masks):
            for bit in range(16):
                if not mask&(1<<bit):continue
                words=(c.c_uint32*5)(0,0,0,0,0);words[layer]=0x80000000|(1<<bit)
                with self.subTest(layer=layer,bit=bit):self.assertEqual(self.lib.quiet(words),0)
    def test_unknown_bits_in_any_sample_and_fatal_status_never_admitted(self):
        initial=(c.c_uint32*5)(0x80000010,0,0,0,0);empty=(c.c_uint32*5)(0,0,0,0,0)
        for layer in range(5):
            bad=(c.c_uint32*5)(0,0,0,0,0);bad[layer]=1<<30
            self.assertEqual(self.lib.ack(0,bad,0,empty),0);self.assertEqual(self.lib.ack(0,initial,0,bad),0);self.assertEqual(self.lib.ready(0,bad),0)
        for status in [1,0x80,0x800,0x10000,0x20000,0x40000]:
            self.assertEqual(self.lib.ack(status,initial,0,empty),0);self.assertEqual(self.lib.ack(0,initial,status,empty),0)
    def test_fatal_dl_and_unsupported_layers_need_recovery_even_if_next_clears(self):
        empty=(c.c_uint32*5)(0,0,0,0,0)
        for value in [0x80002000,0x80000001,0x80000002]:
            bad=(c.c_uint32*5)(0,value,0,0,0);self.assertEqual(self.lib.ack(0,bad,0,empty),0)
        for layer in [2,3,4]:
            bad=(c.c_uint32*5)(0,0,0,0,0);bad[layer]=0x80000001;self.assertEqual(self.lib.ack(0,bad,0,empty),0)
        self.assertEqual(self.lib.quiet(None),0)
    def test_kernel_embeds_exact_policy(self):
        patch=(ROOT/'xnu/patches/0094-ace-sample-cold-uic-validity-before-probe.patch').read_text();part=patch.split('+++ b/iokit/Kernel/arm/AceUFSColdHandoff.h\n',1)[1]
        actual=''.join(x[1:]+'\n' for x in part.splitlines() if x.startswith('+'));self.assertEqual(actual,(ROOT/'ace/ufs_cold_handoff.h').read_text())
