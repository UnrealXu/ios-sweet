"""Actual firmware guards/register inputs, bounded recovery, and ARM64 SMC ABI."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from test_ace_ufs_activehandoff import patched_controller

ROOT=Path(__file__).resolve().parents[1]

def source_at(directory):
    (directory/'iokit/Kernel/arm').mkdir(parents=True)
    patched_controller(directory)
    for n in range(101,113):
        patch,=(ROOT/'xnu/patches').glob(f'{n:04d}-*.patch')
        subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(patch)],cwd=directory,check=True,capture_output=True)
    return (directory/'iokit/Kernel/arm/AceUFSController.cpp').read_text()

def method(source,name):
    start=source.index('    bool '+name+'(')
    return source[start:source.index('\n    }',start)+len('\n    }')]

@unittest.skipUnless(shutil.which('clang++') and shutil.which('patch'),'compiler and patch required')
class SipResetTests(unittest.TestCase):
    def test_stopped_xoufs_restore_refuses_faults_before_hce(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);source=source_at(d)
            methods='\n'.join(method(source,n) for n in ['reset_view_ready','stopped_vendor_ready','restore_stopped_vendor_control'])
            harness=r'''
#include <cassert>
#include <cstdint>
#include <array>
#include <map>
using vm_offset_t=uintptr_t;
#define printf(...) ((void)0)
static std::array<uint32_t,1024> ao{};
struct Probe {
    bool reset_attempted=true,reset_release_accepted=true,firmware_call_issued=true;
    bool peer_read_issued=false,cold_local_commands=false,drop_write=false,after_fault=false;
    uint32_t reset_view=1;unsigned writes=0;
    vm_offset_t reset_ao=reinterpret_cast<uintptr_t>(ao.data());
    std::map<unsigned,uint32_t> regs{{0x2240,0x00360000},{0x144,3},{0x140,2}};
    uint32_t rd(unsigned off) {return regs[off];}
    void wr(unsigned off,uint32_t value) {
        assert(off==0x140 && value==0x82 && writes++==0 && stopped_vendor_ready());
        if(!drop_write) regs[off]=value;
        if(after_fault) ao[0x90/4]=0;
    }
METHODS
};
static void reset() {ao.fill(0);ao[0x90/4]=1;}
int main() {
    reset();Probe p;assert(p.restore_stopped_vendor_control() && p.writes==1 && p.rd(0x140)==0x82);
    assert(p.restore_stopped_vendor_control() && p.writes==1);
    reset();Probe adopted;adopted.regs[0x140]=0x82;assert(adopted.restore_stopped_vendor_control() && !adopted.writes);
    for(unsigned value:{0u,1u,3u,0x80u,0xffffffffu}) {reset();Probe q;q.regs[0x140]=value;assert(!q.restore_stopped_vendor_control() && !q.writes);}
    for(unsigned off:{0x34u,0x30u,0x60u,0x80u,0x58u,0x78u,0x24u,0x20u,0x18u,0x2240u,0x144u}) {
        reset();Probe q;q.regs[off]=1;assert(!q.restore_stopped_vendor_control() && !q.writes);
    }
    for(unsigned bit=0;bit<5;bit++) {reset();Probe q;
        if(bit==0) q.reset_attempted=false;
        if(bit==1) q.reset_release_accepted=false;
        if(bit==2) q.firmware_call_issued=false;
        if(bit==3) q.peer_read_issued=true;
        if(bit==4) q.cold_local_commands=true;
        assert(!q.restore_stopped_vendor_control() && !q.writes);
    }
    for(unsigned value:{0u,2u,0xffffffffu}) {reset();Probe q;ao[0x90/4]=value;assert(!q.restore_stopped_vendor_control() && !q.writes);}
    reset();ao[0]=1;Probe gated;assert(!gated.restore_stopped_vendor_control() && !gated.writes);
    reset();Probe dropped;dropped.drop_write=true;assert(!dropped.restore_stopped_vendor_control() && dropped.writes==1);
    reset();Probe changed;changed.after_fault=true;assert(!changed.restore_stopped_vendor_control() && changed.writes==1);
    reset();Probe unmapped;unmapped.reset_ao=0;assert(!unmapped.restore_stopped_vendor_control() && !unmapped.writes);
}
'''.replace('METHODS',methods)
            cpp=d/'stopped.cpp';cpp.write_text(harness)
            subprocess.run(['clang++','-std=c++17','-O2',str(cpp),'-o',str(d/'stopped')],check=True)
            subprocess.run([str(d/'stopped')],check=True,timeout=10)

    def test_zero_ns_view_refused_after_physically_observed_firmware_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);source=source_at(d)
            harness=r'''
#include <cassert>
#include <cstdint>
#include <array>
using vm_offset_t=uintptr_t;
#define printf(...) ((void)0)
#define __builtin_arm_dsb(n) assert((n)==15)
static const unsigned VM_PROT_READ=1;
static std::array<uint32_t,1024> ao{},pdn{},top{};
static bool change_view;
static vm_offset_t ml_io_map_with_prot(uint64_t pa,uint64_t size,unsigned prot) {
    assert(size==4096 && prot==VM_PROT_READ);
    if(pa==0x112b8000)return reinterpret_cast<uintptr_t>(ao.data());
    if(pa==0x112bc000)return reinterpret_cast<uintptr_t>(pdn.data());
    assert(pa==0x10000000);return reinterpret_cast<uintptr_t>(top.data());
}
static void IODelay(unsigned us) {assert(us==1);if(change_view)ao[0x90/4]^=1;}
struct Probe {
    bool reset_release_accepted=false,firmware_call_issued=false;
    uint32_t reset_view=0;
    uint32_t rd(unsigned off) {assert(off==0x2240 || off==0x144);return off==0x2240?0x00360000:3;}
    bool inherited_ready() {return true;}
METHOD
};
int main() {
    Probe p;assert(!p.inspect_platform_clocks());assert(p.inspect_platform_clocks(true));
    p.reset_release_accepted=true;assert(!p.inspect_platform_clocks());
    p.firmware_call_issued=true;assert(!p.inspect_platform_clocks());
    p.reset_release_accepted=false;assert(!p.inspect_platform_clocks(true));
    p.reset_release_accepted=true;ao[0x90/4]=1;assert(!p.inspect_platform_clocks());
    p.reset_view=1;assert(p.inspect_platform_clocks());
    change_view=true;assert(!p.inspect_platform_clocks());change_view=false;
    p.reset_view=2;ao[0x90/4]=2;assert(!p.inspect_platform_clocks(true));
    p.reset_view=1;ao[0x90/4]=1;ao[0]=1;assert(!p.inspect_platform_clocks());
}
'''.replace('METHOD',method(source,'inspect_platform_clocks'))
            cpp=d/'clock.cpp';cpp.write_text(harness)
            subprocess.run(['clang++','-std=c++17','-O2',str(cpp),'-o',str(d/'clock')],check=True)
            subprocess.run([str(d/'clock')],check=True,timeout=10)

    def test_actual_methods_with_only_smc_instruction_and_register_bindings_mocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);source=source_at(d)
            methods='\n'.join(method(source,n) for n in ['firmware_release_device','reset_view_ready','stopped_vendor_ready','restore_stopped_vendor_control','local_init_ready','init_uic','recover_asserted_device_once'])
            # Preserve every guard, constant register input and return check.
            # Replace just the privileged transport instruction for host execution.
            methods=re.sub(r' __asm__\("x[0-7]"\)','',methods).replace('register uint64_t','uint64_t')
            methods=re.sub(r'        __asm__ volatile\("smc #0"[\s\S]*?"memory"\);','        smc_mock(x0,x1,x2,x3,x4,x5,x6,x7);',methods,count=1)
            self.assertNotIn('smc #0',methods)
            harness=r'''
#include <cassert>
#include <cstdint>
#include <array>
#include <map>
#include <vector>
#include "ace/ufs_cold_handoff.h"
using vm_offset_t=uintptr_t;
#define printf(...) ((void)0)
#define __builtin_arm_dsb(n) assert((n)==15)
static const unsigned VM_PROT_READ=1;
static std::array<uint32_t,1024> ao{};
static unsigned smcs,view,fail_map,delay_fault;
static uint64_t smc_rc;
static vm_offset_t ml_io_map_with_prot(uint64_t pa,uint64_t size,unsigned prot) {
    assert(pa==0x112b8000 && size==4096 && prot==VM_PROT_READ);
    return fail_map?0:reinterpret_cast<uintptr_t>(ao.data());
}
static void smc_mock(uint64_t &x0,uint64_t &x1,uint64_t &x2,uint64_t &x3,uint64_t &x4,uint64_t &x5,uint64_t &x6,uint64_t &x7) {
    assert(++smcs==1 && x0==0xc2000276ULL && x1==2 && x2==1 && !x3 && !x4 && !x5 && !x6 && !x7);
    x0=smc_rc;x1=x2=x3=x4=x5=x6=x7=0xdeadbeef;ao[0x90/4]=view;
}
static void IODelay(unsigned us) {
    assert(us==10 || us==600 || us==1000 || us==10000);
    if(us==delay_fault) ao[0x90/4]=2;
}
static uint64_t mach_absolute_time() {return 0;}
struct Probe {
    bool reset_attempted=false,peer_read_issued=false,cold_local_commands=false;
    bool firmware_call_issued=false,reset_release_accepted=false;
    uint32_t reset_view=0;vm_offset_t reset_ao=0;
    bool clocks=true,bad_hce=false,bad_local=false,bad_link=false;
    int fail_wait=-1,waits=0,bad_snapshot=-1,snapshots=0,fail_uic=-1,commands=0;
    uint32_t rc=0,error=0;
    std::map<unsigned,uint32_t> regs{{0x34,1},{0x30,15},{0x2240,0x00360000},{0x144,3},{0x140,0x82}};
    std::vector<std::pair<unsigned,uint32_t>> writes;
    uint32_t rd(unsigned off) {return regs[off];}
    bool inherited_ready() {return rd(0x34)==1 && (rd(0x30)&15)==15 && !rd(0x58) && !rd(0x78) && !rd(0x18);}
    bool inspect_platform_clocks(bool allow=false) {return clocks && (allow || (ao[0x90/4]&1) || reset_view_ready());}
    int inspect_vendor_link(const char *) {return bad_link?-1:2;}
    void wr(unsigned off,uint32_t value) {
        assert(off==0x140 || off==0x60 || off==0x80 || off==0x34 || off==0x94 || off==0x98 || off==0x9c || off==0x90 || off==0x20);
        writes.emplace_back(off,value);
        if(off==0x20) {regs[off]&=~value;return;}
        if(off==0x34) {
            if(bad_hce) return;
            if(!value) {assert(!smcs);regs[0x30]=0;regs[0x140]=2;}
            else {assert(smcs==1 && reset_release_accepted && reset_view_ready());regs[0x30]=bad_local?0:8;}
        }
        if(off==0x140) assert(value==0x82 && rd(off)==2 && stopped_vendor_ready());
        regs[off]=value;
        if(off==0x90) {
            assert(smcs==1 && reset_release_accepted && reset_view_ready() && cold_local_commands && (rd(0x30)&8));
            assert(!rd(0x60) && !rd(0x80) && !rd(0x24));
            bool fault=commands++==fail_uic;regs[0x20]=fault?error:0x400;regs[0x98]=fault?rc:0;
            if(value==1) regs[0x9c]=0x90;
            if(value==0x16 && !fault) regs[0x30]=15;
        }
    }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {return waits++==fail_wait?false:(rd(off)&mask)==value;}
    uint32_t snapshot(const char *,uint32_t words[5]) {for(unsigned i=0;i<5;i++) words[i]=0;return snapshots++==bad_snapshot?4:rd(0x20);}
METHODS
};
static void reset() {ao.fill(0);smcs=fail_map=delay_fault=0;view=1;smc_rc=0;}
int main() {
    for(unsigned ns:{1u}) {
        reset();view=ns;Probe p;assert(p.recover_asserted_device_once());
        assert(smcs==1 && p.commands==5 && p.waits==10 && p.reset_release_accepted && ao[0x90/4]==ns);
        auto saved=p.writes;assert(!p.recover_asserted_device_once() && p.writes==saved && smcs==1);
        assert(!p.firmware_release_device() && smcs==1);
    }
    for(uint64_t bad:{1ULL,0xffffffffULL,0xffffffffffffffffULL}) {
        reset();smc_rc=bad;Probe p;assert(!p.recover_asserted_device_once() && smcs==1 && !p.reset_release_accepted && p.commands==0 && p.rd(0x34)==0);
        assert(!p.firmware_release_device() && smcs==1);
    }
    for(unsigned ns:{0u,2u,0xffffffffu}) {reset();view=ns;Probe p;assert(!p.recover_asserted_device_once() && smcs==1 && p.commands==0 && !p.rd(0x34));}
    for(int n=0;n<10;n++) {reset();Probe p;p.fail_wait=n;assert(!p.recover_asserted_device_once() && p.waits==n+1);assert(smcs==(n<3?0u:1u));}
    for(unsigned us:{10u,10000u,600u}) {reset();delay_fault=us;Probe p;assert(!p.recover_asserted_device_once() && p.commands==0);assert(smcs==(us==10?0u:1u));}
    for(unsigned off:{0x24u,0x20u,0x58u,0x78u,0x18u}) {reset();Probe p;p.regs[off]=1;assert(!p.recover_asserted_device_once() && !smcs && p.writes.empty());}
    reset();fail_map=1;Probe map;assert(!map.recover_asserted_device_once() && !smcs && map.writes.empty());
    reset();Probe busy;busy.bad_hce=true;assert(!busy.recover_asserted_device_once() && !smcs);
    reset();Probe clocks;clocks.clocks=false;assert(!clocks.recover_asserted_device_once() && !smcs);
    reset();Probe link;link.bad_link=true;assert(!link.recover_asserted_device_once() && !smcs);
    reset();ao[0x90/4]=1;Probe already;assert(already.recover_asserted_device_once() && !smcs && already.writes.empty());
    for(int n=0;n<5;n++) for(unsigned rc:{0u,1u}) {reset();Probe p;p.fail_uic=n;p.rc=rc;p.error=rc?0x400:0x404;assert(!p.recover_asserted_device_once() && smcs==1 && p.commands==n+1);}
    reset();Probe q;q.reset_ao=reinterpret_cast<uintptr_t>(ao.data());q.reset_attempted=true;q.regs[0x34]=0;
    for(unsigned off:{0x34u,0x60u,0x80u,0x58u,0x78u,0x24u,0x20u}) {q.regs[off]=1;assert(!q.firmware_release_device() && !smcs);q.regs[off]=0;}
    q.regs[0x144]=1;assert(!q.firmware_release_device() && !smcs);q.regs[0x144]=3;
    ao[0]=1;assert(!q.firmware_release_device() && !smcs);ao[0]=0;
    q.reset_view=1;assert(q.firmware_release_device() && smcs==1 && q.reset_view_ready());
    q.reset_view=2;ao[0x90/4]=2;assert(!q.reset_view_ready());
}
'''.replace('METHODS',methods)
            cpp=d/'probe.cpp';cpp.write_text(harness)
            subprocess.run(['clang++','-std=c++17','-O2','-I',str(ROOT),str(cpp),'-o',str(d/'probe')],check=True)
            subprocess.run([str(d/'probe')],check=True,timeout=10)

    @unittest.skipUnless(shutil.which('llvm-objdump'),'objdump required')
    def test_actual_arm64_smc_register_abi(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);source=source_at(d);body=method(source,'firmware_release_device')
            cpp=d/'abi.cpp'
            cpp.write_text('''using uint64_t=unsigned long long;using uint32_t=unsigned;using vm_offset_t=unsigned long;
extern "C" int printf(const char *,...);
struct Probe {bool reset_attempted,firmware_call_issued,reset_release_accepted;vm_offset_t reset_ao;uint32_t rd(unsigned);
'''+body+'''\n};extern "C" bool invoke(Probe *p) {return p->firmware_release_device();}\n''')
            subprocess.run(['clang++','-target','arm64-apple-macos13.5','-std=c++17','-ffreestanding','-O2','-Wno-register','-c',str(cpp),'-o',str(d/'abi.o')],check=True)
            assembly=subprocess.check_output(['llvm-objdump','-d','--print-imm-hex',str(d/'abi.o')],text=True)
            self.assertEqual(len(re.findall(r'\bsmc\s+#(?:0x)?0\b',assembly)),1,assembly)
            for pattern in [r'mov\s+w0, #0x276',r'movk\s+w0, #0xc200, lsl #16',r'mov\s+w1, #0x2',r'mov\s+w2, #0x1']:
                self.assertRegex(assembly,pattern,assembly)
            for n in range(3,8):self.assertRegex(assembly,rf'mov\s+x{n}, (?:xzr|#0x0\b)')

if __name__=='__main__':unittest.main()
