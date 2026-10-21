"""Run the real reset-release path with hardware failures at each boundary."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from test_ace_ufs_activehandoff import patched_controller

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('clang++') and shutil.which('patch'), 'compiler and patch required')
class ResetInitTests(unittest.TestCase):
    def test_actual_reset_release_and_fault_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / 'iokit/Kernel/arm').mkdir(parents=True)
            patched_controller(d)
            for n in range(101, 106):
                p, = (ROOT / 'xnu/patches').glob(f'{n:04d}-*.patch')
                subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(p)],
                               cwd=d, check=True, capture_output=True)
            source = (d / 'iokit/Kernel/arm/AceUFSController.cpp').read_text()
            methods = []
            for name in ['local_init_ready', 'init_uic', 'recover_asserted_device_once']:
                start = source.index('    bool ' + name + '(')
                methods.append(source[start:source.index('\n    }', start) + len('\n    }')])
            harness = r'''
#include <cassert>
#include <cstdint>
#include <array>
#include <map>
#include <tuple>
#include <vector>
#include "ace/ufs_cold_handoff.h"
using vm_offset_t=uintptr_t;
#define printf(...) ((void)0)
#define __builtin_arm_dsb(x) dsb_mock(x)
static void dsb_mock(unsigned);
static const unsigned VM_PROT_READ=1,VM_PROT_WRITE=2;
static std::array<uint32_t,1024> ao{};
static unsigned maps,fail_map,delay_count,change_reset_at;
static bool drop_release;
static void dsb_mock(unsigned n) {assert(n==15);if(drop_release) ao[0x90/4]=0;}
static vm_offset_t ml_io_map_with_prot(uint64_t pa,uint64_t size,unsigned prot) {
    assert(pa==0x112b8000 && size==4096 && (prot==1 || prot==3));
    maps++;return maps==fail_map?0:reinterpret_cast<uintptr_t>(ao.data());
}
static void IODelay(unsigned us) {
    assert(us==10 || us==600 || us==1000 || us==10000);
    delay_count++;
    if(delay_count==change_reset_at) ao[0x90/4]=2;
}
static uint64_t mach_absolute_time() {return 0;}
struct Probe {
    bool peer_read_issued=false,reset_attempted=false,cold_local_commands=false;
    vm_offset_t reset_ao=0;
    bool clocks=true,bad_hce=false,bad_local=false,bad_link=false;
    int fail_wait=-1,waits=0,bad_snapshot=-1,snapshots=0,fail_uic=-1,commands=0;
    uint32_t uic_rc=0,uic_error=0;
    std::map<unsigned,uint32_t> regs{{0x34,1},{0x30,15},{0x2240,0x00360000},{0x144,3},{0x140,0x82}};
    std::vector<std::pair<unsigned,uint32_t>> writes;
    uint32_t rd(unsigned off) {return regs[off];}
    bool inherited_ready() {return rd(0x34)==1 && (rd(0x30)&15)==15 && !rd(0x58) && !rd(0x78) && !rd(0x18);}
    bool inspect_platform_clocks(bool allow=false) {return clocks && (allow || (ao[0x90/4]&1));}
    int inspect_vendor_link(const char *) {return bad_link?-1:2;}
    void wr(unsigned off,uint32_t value) {
        assert(off==0x60 || off==0x80 || off==0x34 || off==0x94 || off==0x98 || off==0x9c || off==0x90 || off==0x20);
        writes.emplace_back(off,value);
        if(off==0x20) {regs[off]&=~value;return;}
        if(off==0x34) {
            if(bad_hce) return;
            if(!value) {assert(ao[0x90/4]==0);regs[0x30]=0;}
            else {assert(ao[0x90/4]==1 && !rd(0x60) && !rd(0x80));regs[0x30]=bad_local?0:8;}
        }
        regs[off]=value;
        if(off==0x90) {
            assert(reset_attempted && cold_local_commands && ao[0x90/4]==1 && rd(0x34)==1 && (rd(0x30)&8));
            assert(!rd(0x60) && !rd(0x80) && !rd(0x24));
            bool fault=commands++==fail_uic;
            regs[0x20]=fault?uic_error:0x400;regs[0x98]=fault?uic_rc:0;
            if(value==1) regs[0x9c]=0x90;
            if(value==0x16 && !fault) regs[0x30]=15;
        }
    }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {
        if(waits++==fail_wait) return false;
        return (rd(off)&mask)==value;
    }
    uint32_t snapshot(const char *,uint32_t words[5]) {
        for(unsigned i=0;i<5;i++) words[i]=0;
        return snapshots++==bad_snapshot?4:rd(0x20);
    }
METHODS
};
static void reset() {ao.fill(0);maps=fail_map=delay_count=change_reset_at=0;drop_release=false;}
int main() {
    reset();Probe good;assert(good.recover_asserted_device_once());
    assert(good.commands==5 && good.waits==10 && ao[0x90/4]==1 && good.reset_attempted && !good.cold_local_commands);
    assert(good.writes[0]==std::make_pair(0x60u,0u) && good.writes[1]==std::make_pair(0x80u,0u) && good.writes[2]==std::make_pair(0x34u,0u));
    auto written=good.writes;assert(!good.recover_asserted_device_once() && good.writes==written);
    for(int n=0;n<10;n++) {
        reset();Probe p;p.fail_wait=n;assert(!p.recover_asserted_device_once());
        assert(p.waits==n+1);
        if(n<3) assert(ao[0x90/4]==0 && p.commands==0);
    }
    for(unsigned n:{1u,2u}) {reset();fail_map=n;Probe p;assert(!p.recover_asserted_device_once());assert(p.commands==0 && !ao[0x90/4]);}
    for(unsigned n:{1u,2u,3u}) {reset();change_reset_at=n;Probe p;assert(!p.recover_asserted_device_once() && p.commands==0);}
    for(unsigned value:{2u,0xffffffffu}) {reset();ao[0x90/4]=value;Probe p;assert(!p.recover_asserted_device_once() && p.writes.empty());}
    reset();ao[0x90/4]=1;Probe active;assert(active.recover_asserted_device_once() && active.writes.empty() && !active.reset_attempted);
    for(unsigned off:{0x24u,0x20u,0x58u,0x78u,0x18u}) {reset();Probe p;p.regs[off]=1;assert(!p.recover_asserted_device_once() && p.writes.empty());}
    for(unsigned off:{0x60u,0x80u}) {reset();Probe p;p.regs[off]=2;assert(!p.recover_asserted_device_once() && p.writes.empty());}
    reset();Probe clocks;clocks.clocks=false;assert(!clocks.recover_asserted_device_once() && clocks.writes.empty());
    reset();Probe link;link.bad_link=true;assert(!link.recover_asserted_device_once() && link.writes.empty());
    reset();Probe stop;stop.bad_hce=true;assert(!stop.recover_asserted_device_once() && !ao[0x90/4] && stop.commands==0);
    reset();drop_release=true;Probe release;assert(!release.recover_asserted_device_once() && release.commands==0 && release.rd(0x34)==0 && !ao[0x90/4]);
    reset();Probe local;local.bad_local=true;assert(!local.recover_asserted_device_once() && local.commands==0);
    for(int n=0;n<5;n++) for(unsigned rc:{0u,1u}) {
        reset();Probe p;p.fail_uic=n;p.uic_rc=rc;p.uic_error=rc?0x400:0x404;
        assert(!p.recover_asserted_device_once() && p.commands==n+1);
    }
    reset();Probe snap;snap.bad_snapshot=0;assert(!snap.recover_asserted_device_once() && snap.writes.empty());
    reset();Probe after;after.bad_snapshot=1;assert(!after.recover_asserted_device_once() && after.commands==0);
    reset();Probe p;p.cold_local_commands=true;assert(!p.local_init_ready());
    p.reset_attempted=true;p.reset_ao=reinterpret_cast<uintptr_t>(ao.data());ao[0x90/4]=1;assert(p.local_init_ready());
    for(unsigned off:{0x24u,0x58u,0x78u,0x18u,0x60u,0x80u}) {p.regs[off]=1;assert(!p.local_init_ready());p.regs[off]=0;}
    p.regs[0x30]=8;assert(p.local_init_ready() && !p.inherited_ready());
    ao[0]=1;assert(!p.local_init_ready());
}
'''.replace('METHODS', '\n'.join(methods))
            cpp=d/'probe.cpp';cpp.write_text(harness)
            subprocess.run(['clang++','-std=c++17','-O2','-I',str(ROOT),str(cpp),'-o',str(d/'probe')],check=True)
            subprocess.run([str(d/'probe')],check=True,timeout=10)


if __name__ == '__main__':
    unittest.main()
