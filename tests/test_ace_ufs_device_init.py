"""Fixed init QUERY frames and actual bounded driver/transport failure paths."""
from pathlib import Path
import ctypes as c
import shutil,subprocess,tempfile,unittest,struct
from test_ace_ufs_sipreset import source_at,method
ROOT=Path(__file__).resolve().parents[1]

class DeviceInitProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)
        (p/'wrap.c').write_text('#include "ufs_read_protocol.h"\n#include "ufs_device_init.h"\nint build(uint8_t *a,size_t n,uint64_t pa,unsigned op){return ace_ufs_device_init_request(a,n,pa,op);}\nint response(const uint8_t *r,size_t n,unsigned op,uint32_t *v){return ace_ufs_device_init_response(r,n,op,v);}\n')
        subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I',str(ROOT/'ace'),str(p/'wrap.c'),'-o',str(p/'lib.so')],check=True)
        cls.lib=c.CDLL(str(p/'lib.so'));cls.lib.build.argtypes=[c.c_void_p,c.c_size_t,c.c_uint64,c.c_uint];cls.lib.response.argtypes=[c.c_void_p,c.c_size_t,c.c_uint,c.POINTER(c.c_uint32)]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_exact_zero_data_set_and_read_flag_frames(self):
        for op,func in [(5,1),(6,0x81)]:
            a=c.create_string_buffer(0x4000);self.assertEqual(self.lib.build(a,0x4000,0x142df8000,op),0)
            expected=bytearray(32);expected[0]=0x16;expected[5]=func;expected[12]=op;expected[13]=1
            self.assertEqual(a.raw[0x1000:0x1020],expected)
            self.assertEqual(struct.unpack_from('<8I',a.raw),(0x11000000,0,15,0,0x42df9000,1,0x800080,0))
            self.assertEqual(a.raw[0x1400:0x3c00],bytes(0x2800));self.assertEqual(a.raw[0x3c00:],b'\x5a'*1024)
        for op in [0,1,2,3,4,7,8,255]:
            a=c.create_string_buffer(b'\xaa'*0x4000,0x4000);self.assertEqual(self.lib.build(a,0x4000,0x142df8000,op),-1);self.assertEqual(a.raw,b'\xaa'*0x4000)
        for n,pa in [(0x3fff,0x142df8000),(0x4000,0),(0x4000,0x142df8001),(0x4000,1<<40)]:
            a=c.create_string_buffer(b'\xaa'*0x4000,0x4000);self.assertEqual(self.lib.build(a,n,pa,5),-1);self.assertEqual(a.raw,b'\xaa'*0x4000)
    def test_response_echo_and_flag_validation_before_output_store(self):
        for op in [5,6]:
            for value in [0,1]:
                good=bytearray(512);good[0]=0x36;good[12]=op;good[13]=1;struct.pack_into('>I',good,20,value)
                out=c.c_uint32(0xdeadbeef);self.assertEqual(self.lib.response(c.create_string_buffer(bytes(good)),512,op,c.byref(out)),0);self.assertEqual(out.value,value)
                for off in [0,1,2,3,6,7,10,11,12,13,14,15,18,19,20,21,22,23]:
                    bad=good.copy();bad[off]^=2;out.value=0xdeadbeef
                    self.assertEqual(self.lib.response(c.create_string_buffer(bytes(bad)),512,op,c.byref(out)),-1);self.assertEqual(out.value,0xdeadbeef)
        out=c.c_uint32(9);self.assertEqual(self.lib.response(None,512,5,c.byref(out)),-1)
        self.assertEqual(self.lib.response(c.create_string_buffer(512),511,5,c.byref(out)),-1)
        self.assertEqual(self.lib.response(c.create_string_buffer(512),512,5,None),-1)
    def test_final_kernel_header_matches_host_tested_bytes(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);source_at(p);self.assertEqual((p/'iokit/Kernel/arm/AceUFSDeviceInit.h').read_bytes(),(ROOT/'ace/ufs_device_init.h').read_bytes())

@unittest.skipUnless(shutil.which('clang++'),'compiler required')
class DeviceInitDriverTests(unittest.TestCase):
    def test_actual_transport_one_set_bounded_reads_and_fail_closed_paths(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);source=source_at(p)
            start=source.index('    int command(');command=source[start:source.index('\n    }',start)+len('\n    }')]
            methods=command+'\n'+method(source,'device_init_ready')+'\n'+method(source,'complete_device_init_once')
            harness=r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <map>
#include <array>
#include "ace/ufs_read_protocol.h"
#include "ace/ufs_device_init.h"
#include "ace/ufs_reset_attention.h"
using vm_offset_t=uintptr_t;
#include <cstdio>
#include <cstdarg>
static unsigned logbytes;
static int captured_printf(const char *fmt,...) {va_list ap;va_start(ap,fmt);int n=vsnprintf(nullptr,0,fmt,ap);va_end(ap);assert(n>=0);logbytes+=unsigned(n);return n;}
#define printf captured_printf
#define __builtin_arm_dsb(n) assert((n)==15)
static uint64_t ticks;
static uint64_t mach_absolute_time() {return ticks;}
static void nanoseconds_to_absolutetime(uint64_t ns,uint64_t *v) {*v=ns;}
static void IODelay(unsigned us) {assert(us==5000 || us==1000);ticks+=us*1000ULL;}
static void FlushPoC_DcacheRegion(uintptr_t,unsigned n) {assert(n==0x4000);}
struct Probe {
    std::array<uint8_t,0x4000> arena{};uint32_t ao=0;
    uintptr_t dma=reinterpret_cast<uintptr_t>(arena.data()),reset_ao=reinterpret_cast<uintptr_t>(&ao);
    uint64_t pa=0x142df8000ULL;
    bool nop_verified=true,reset_attempted=true,device_init_attempted=false,init_set_issued=false,reset_ready=true;
    unsigned submits=0,sets=0,reads=0,clear_after=1,fail_at=0,fault=0,init_reads_issued=0;
    bool device_init_complete=false;
    std::map<unsigned,uint32_t> regs{{0x34,1},{0x30,15},{0x50,0x42df8000},{0x54,1},{0x60,1},{0x2240,0x00360000},{0x144,3},{0x140,0x82}};
    uint32_t rd(unsigned off) {return regs[off];}
    bool inherited_ready() {return rd(0x34)==1 && rd(0x30)==15 && !rd(0x58) && !rd(0x78) && !rd(0x18);}
    bool reset_view_ready() {return reset_ready;}
    void wr(unsigned off,uint32_t value) {
        assert(off==0x58 || off==0x20);
        if(off==0x20) {regs[off]&=~value;return;}
        assert(value==1 && device_init_attempted && init_set_issued && rd(0x20)==0 && inherited_ready());
        unsigned opcode=arena[ACE_UFS_UCD+12];assert(opcode==5 || opcode==6);submits++;
        if(opcode==6) {assert(++sets==1);assert(arena[ACE_UFS_UCD+5]==0x81);}
        else {assert(sets==1);reads++;assert(arena[ACE_UFS_UCD+5]==1);}
        uint8_t *r=arena.data()+ACE_UFS_RESPONSE;memset(r,0,512);
        r[0]=0x36;r[12]=opcode;r[13]=1;r[23]=opcode==6 || reads<clear_after?1:0;
        ace_ufs_le32(arena.data()+8,0);regs[0x20]=1;
        if(submits!=fail_at)return;
        switch(fault) {
            case 1:regs[0x58]=1;break; // timeout, never reuse
            case 2:r[6]=0xf6;break;
            case 3:r[12]^=1;break;
            case 4:arena[ACE_UFS_GUARD]=0;break;
            case 5:arena[ACE_UFS_UCD+13]=2;break;
            case 6:regs[0x20]|=4;break;
            case 7:r[23]=2;break;
            case 8:reset_ready=false;break;
            case 9:ticks+=1500000000ULL;break;
            case 10:ace_ufs_le32(arena.data()+8,1);break;
            case 11:r[0]=0x21;break;
        }
    }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {assert(off==0x58);return (rd(off)&mask)==value;}
    uint32_t snapshot(const char *,uint32_t words[5]) {for(unsigned i=0;i<5;i++) words[i]=0;return rd(0x20);}
METHODS
};
int main() {
    for(unsigned delay:{1u,3u,299u}) {ticks=0;Probe p;p.clear_after=delay;assert(p.complete_device_init_once());assert(p.sets==1 && p.reads==delay);unsigned saved=p.submits;assert(!p.complete_device_init_once() && p.submits==saved);}
    ticks=0;logbytes=0;Probe stuck;stuck.clear_after=999;assert(!stuck.complete_device_init_once() && stuck.sets==1 && stuck.reads==300 && ticks==1500000000ULL);assert(logbytes>0 && logbytes<8192);
    for(unsigned at:{1u,2u}) for(unsigned fault=1;fault<=11;fault++) {
        if(at==1 && fault==9) continue; // Poll deadline begins after SET ack.
        ticks=0;Probe p;p.fail_at=at;p.fault=fault;assert(!p.complete_device_init_once());unsigned saved=p.submits;assert(saved==at);assert(!p.complete_device_init_once() && p.submits==saved);
    }
    for(unsigned off:{0x34u,0x30u,0x58u,0x78u,0x18u,0x2240u,0x144u,0x140u,0x24u,0x20u,0x60u,0x80u,0x50u,0x54u}) {
        ticks=0;Probe p;p.regs[off]^=2;assert(!p.complete_device_init_once() && !p.submits && !p.device_init_attempted);
    }
    for(unsigned mode=0;mode<5;mode++) {ticks=0;Probe p;
        if(mode==0)p.nop_verified=false;if(mode==1)p.reset_attempted=false;if(mode==2)p.reset_ready=false;if(mode==3)p.ao=1;if(mode==4)p.device_init_attempted=true;
        assert(!p.complete_device_init_once() && !p.submits);
    }
    ticks=0;Probe direct;assert(direct.command(ACE_UFS_INIT_SET)<0 && !direct.submits);
    direct.device_init_attempted=true;assert(direct.command(ACE_UFS_INIT_READ)<0 && !direct.submits);
    assert(direct.command(ACE_UFS_INIT_SET,1)<0 && !direct.submits && !direct.init_set_issued);
}
'''.replace('METHODS',methods)
            (p/'driver.cpp').write_text(harness)
            subprocess.run(['clang++','-std=c++17','-O2','-I',str(ROOT),str(p/'driver.cpp'),'-o',str(p/'driver')],check=True)
            subprocess.run([str(p/'driver')],check=True,timeout=10)

if __name__=='__main__':unittest.main()
