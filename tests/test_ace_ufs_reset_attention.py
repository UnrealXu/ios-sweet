"""Actual SCSI transport and readiness path: one exact reset UA, then GOOD."""
from pathlib import Path
import ctypes as c
import shutil,subprocess,tempfile,unittest
from test_ace_ufs_sipreset import source_at,method
ROOT=Path(__file__).resolve().parents[1]
class ResetAttentionProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)
        (p/'wrap.c').write_text('#include "ufs_read_protocol.h"\n#include "ufs_reset_attention.h"\nint valid(const uint8_t *r,size_t n,unsigned lun){return ace_ufs_reset_attention_response(r,n,lun);}\n')
        subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I',str(ROOT/'ace'),str(p/'wrap.c'),'-o',str(p/'lib.so')],check=True)
        cls.lib=c.CDLL(str(p/'lib.so'));cls.lib.valid.argtypes=[c.c_void_p,c.c_size_t,c.c_uint]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_exact_fixed_reset_sense_and_every_guard(self):
        good=bytearray(512)
        for off,v in [(0,0x21),(2,2),(6,1),(7,2),(11,20),(33,18),(34,0x70),(36,6),(41,10),(46,0x29)]:good[off]=v
        self.assertEqual(self.lib.valid(c.create_string_buffer(bytes(good)),512,2),1)
        valid_info=good.copy();valid_info[34]=0xf0;valid_info[37:41]=bytes.fromhex('12345678')
        self.assertEqual(self.lib.valid(c.create_string_buffer(bytes(valid_info)),512,2),1)
        for off in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,36,41,46,47]:
            for bit in range(8):
                bad=good.copy();bad[off]^=1<<bit
                if off==34 and bad[off]==0xf0:continue # VALID flag is independent of fixed response code.
                if off==6 and bad[off]==0:continue # Valid response0 plus CHECK CONDITION is also classified narrowly.
                self.assertEqual(self.lib.valid(c.create_string_buffer(bytes(bad)),512,2),0,(off,bit))
        for n,lun in [(511,2),(513,2),(512,0),(512,1),(512,3)]:self.assertEqual(self.lib.valid(c.create_string_buffer(bytes(good)),n,lun),0)
        self.assertEqual(self.lib.valid(None,512,2),0)
    def test_final_kernel_header_exact_host_tested_bytes(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);source_at(p);self.assertEqual((p/'iokit/Kernel/arm/AceUFSResetAttention.h').read_bytes(),(ROOT/'ace/ufs_reset_attention.h').read_bytes())

@unittest.skipUnless(shutil.which('clang++'),'compiler required')
class ResetAttentionDriverTests(unittest.TestCase):
    def test_actual_command_and_lun_gate_refuse_errors_and_repeated_attention(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);source=source_at(p);start=source.index('    int command(');command=source[start:source.index('\n    }',start)+len('\n    }')]
            methods=command+'\n'+method(source,'device_init_ready')+'\n'+method(source,'lun2_ready_once')
            harness=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <map>
#include <array>
#include <vector>
#include "ace/ufs_read_protocol.h"
#include "ace/ufs_device_init.h"
#include "ace/ufs_reset_attention.h"
using vm_offset_t=uintptr_t;
#define printf(...) ((void)0)
#define __builtin_arm_dsb(n) assert((n)==15)
static uint64_t mach_absolute_time() {return 0;}
static void IODelay(unsigned us) {assert(us==1000);}
static void FlushPoC_DcacheRegion(uintptr_t,unsigned n) {assert(n==0x4000);}
struct Probe {
    std::array<uint8_t,0x4000> arena{};uint32_t ao=0;
    uintptr_t dma=reinterpret_cast<uintptr_t>(arena.data()),reset_ao=reinterpret_cast<uintptr_t>(&ao);
    uint64_t pa=0x142df4000ULL;
    bool nop_verified=true,reset_attempted=true,device_init_complete=true,lun2_readiness_attempted=false;
    bool device_init_attempted=true,init_set_issued=true,reset_ready=true;
    unsigned init_reads_issued=0,submits=0,fault=0;
    std::vector<unsigned> results{1,0}; // 1 exact reset UA;0 GOOD;2 unsupported LU;3 malformed UA.
    std::map<unsigned,uint32_t> regs{{0x34,1},{0x30,15},{0x50,0x42df4000},{0x54,1},{0x60,1},{0x2240,0x00360000},{0x144,3},{0x140,0x82}};
    uint32_t rd(unsigned off) {return regs[off];}
    bool inherited_ready() {return rd(0x34)==1 && rd(0x30)==15 && !rd(0x58) && !rd(0x78) && !rd(0x18);}
    bool reset_view_ready() {return reset_ready;}
    void wr(unsigned off,uint32_t value) {
        assert(off==0x58 || off==0x20);
        if(off==0x20) {regs[off]&=~value;return;}
        assert(value==1 && submits<results.size() && inherited_ready());
        assert(arena[ACE_UFS_UCD]==1 && arena[ACE_UFS_UCD+2]==2 && arena[ACE_UFS_UCD+16]==0 && !arena[ACE_UFS_UCD+1]);
        unsigned result=results[submits++];uint8_t *r=arena.data()+ACE_UFS_RESPONSE;memset(r,0,512);r[0]=0x21;r[2]=2;
        if(result) {
            r[6]=1;r[7]=2;r[11]=20;r[33]=18;r[34]=0xf0;r[36]=result==2?5:6;r[41]=10;r[46]=result==2?0x25:0x29;
            if(result==3)r[33]=0;
        }
        ace_ufs_le32(arena.data()+8,0);regs[0x20]=1;
        if(submits!=1)return;
        switch(fault) {
            case 1:regs[0x58]=1;break;
            case 2:ace_ufs_le32(arena.data()+8,1);break;
            case 3:regs[0x20]|=4;break;
            case 4:arena[ACE_UFS_GUARD]=0;break;
            case 5:arena[ACE_UFS_UCD+2]=3;break;
            case 6:reset_ready=false;break;
            case 7:r[3]=1;break;
            case 8:regs[0x140]=2;break;
            case 9:r[46]=0x28;break;
        }
    }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {assert(off==0x58);return (rd(off)&mask)==value;}
    uint32_t snapshot(const char *,uint32_t words[5]) {for(unsigned i=0;i<5;i++) words[i]=0;return rd(0x20);}
METHODS
};
int main() {
    Probe success;assert(success.lun2_ready_once() && success.submits==2);assert(!success.lun2_ready_once() && success.submits==2);
    Probe good;good.results={0};assert(good.lun2_ready_once() && good.submits==1);
    for(auto results:std::vector<std::vector<unsigned>>{{1,1},{1,2},{1,3},{2},{3}}) {
        Probe p;p.results=results;assert(!p.lun2_ready_once() && p.submits==results.size());unsigned saved=p.submits;assert(!p.lun2_ready_once() && p.submits==saved);
    }
    for(unsigned fault=1;fault<=9;fault++) {Probe p;p.fault=fault;assert(!p.lun2_ready_once() && p.submits==1);assert(!p.lun2_ready_once() && p.submits==1);}
    Probe notinit;notinit.device_init_complete=false;assert(!notinit.lun2_ready_once() && !notinit.submits);
    Probe busy;busy.regs[0x58]=1;assert(!busy.lun2_ready_once() && !busy.submits);
    Probe noack;noack.reset_ready=false;assert(!noack.lun2_ready_once() && !noack.submits);
}
'''.replace('METHODS',methods)
            (p/'driver.cpp').write_text(harness)
            subprocess.run(['clang++','-std=c++17','-O2','-I',str(ROOT),str(p/'driver.cpp'),'-o',str(p/'driver')],check=True)
            subprocess.run([str(p/'driver')],check=True,timeout=10)

if __name__=='__main__':unittest.main()
