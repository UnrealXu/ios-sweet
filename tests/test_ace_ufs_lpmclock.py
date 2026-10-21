"""Actual read-only clock and bounded active-LPM methods, with injected faults."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from test_ace_ufs_activehandoff import patched_controller

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('clang++') and shutil.which('patch'), 'compiler and patch required')
class ActiveLpmClockTests(unittest.TestCase):
    def exercise(self, signature, harness):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            target = directory / 'iokit/Kernel/arm/AceUFSController.cpp'
            target.parent.mkdir(parents=True)
            patched_controller(directory)
            for number in ['0101', '0102', '0103', '0104']:
                patch, = (ROOT / 'xnu/patches').glob(number + '-*.patch')
                subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(patch)],
                               cwd=directory, capture_output=True, check=True)
            source = target.read_text()
            start = source.index('    bool ' + signature + '(')
            method = source[start:source.index('\n    }', start) + len('\n    }')]
            cpp = directory / 'probe.cpp'
            cpp.write_text(harness.replace('METHOD', method))
            subprocess.run(['clang++', '-std=c++17', '-O2', '-I', str(ROOT),
                            str(cpp), '-o', str(directory / 'probe')], check=True)
            subprocess.run([str(directory / 'probe')], check=True, timeout=10)

    def test_read_only_clock_mapping_and_gate_changes(self):
        self.exercise('inspect_platform_clocks', r'''
#include <cassert>
#include <cstdint>
#include <array>
#define printf(...) ((void)0)
#define __builtin_arm_dsb(x) do {assert((x)==15);} while(0)
using vm_offset_t=uintptr_t;
static constexpr unsigned VM_PROT_READ=1;
static std::array<uint32_t,1024> ao{},pdn{},top{};
static unsigned maps,fail_map,change;
static vm_offset_t ml_io_map_with_prot(uint64_t pa,uint64_t size,unsigned prot) {
    assert(size==4096 && prot==VM_PROT_READ);maps++;
    if(maps==fail_map) return 0;
    if(pa==0x112b8000) return reinterpret_cast<uintptr_t>(ao.data());
    if(pa==0x112bc000) return reinterpret_cast<uintptr_t>(pdn.data());
    assert(pa==0x10000000);return reinterpret_cast<uintptr_t>(top.data());
}
static void IODelay(unsigned us) {
    assert(us==1);
    if(change==1) top[0xf0/4]^=1;
    if(change==2) top[0x10/4]^=0x10000;
    if(change==3) ao[0]|=1;
    if(change==4) ao[0x90/4]=0;
}
struct Probe {
    uint32_t hw=0x00360000,refclk=3;
    bool ready=true;
    uint32_t rd(unsigned off) {assert(off==0x2240 || off==0x144);return off==0x2240?hw:refclk;}
    bool inherited_ready() {return ready;}
METHOD
};
static void reset() {ao.fill(0);ao[0x90/4]=1;pdn.fill(0);top.fill(0);maps=fail_map=change=0;}
int main() {
    reset();Probe good;auto a=ao,p=pdn,t=top;assert(good.inspect_platform_clocks());
    assert(maps==3 && ao==a && pdn==p && top==t);
    for(unsigned bit:{0u,1u,2u,3u,4u,8u}) {
        reset();ao[0]=1u<<bit;assert(!good.inspect_platform_clocks() && ao[0]==(1u<<bit));
    }
    reset();pdn[0]=1;assert(!good.inspect_platform_clocks());
    reset();pdn[0]=2;assert(good.inspect_platform_clocks()); // AES not required for plain reads.
    reset();top[0xf0/4]=0x80;assert(!good.inspect_platform_clocks());
    for(unsigned n:{1u,2u,3u}) {
        reset();fail_map=n;assert(!good.inspect_platform_clocks());
        reset();change=n;assert(!good.inspect_platform_clocks());
    }
    reset();ao[0x90/4]=0;assert(!good.inspect_platform_clocks());
    reset();change=4;assert(!good.inspect_platform_clocks());
    reset();Probe hw;hw.hw=0x00360001;assert(!hw.inspect_platform_clocks() && !maps);
    reset();Probe clock;clock.refclk=1;assert(!clock.inspect_platform_clocks() && !maps);
    reset();Probe busy;busy.ready=false;assert(!busy.inspect_platform_clocks() && !maps);
}
''')

    def test_lpm_conditional_changes_and_failure_stop(self):
        self.exercise('adopt_active_unipro', r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <tuple>
#include <vector>
#include "ace/ufs_cold_handoff.h"
#define printf(...) ((void)0)
struct Probe {
    bool peer_read_issued=false,ready=true,clocks=true,quiet=true,bad_readback=false;
    unsigned states=0,refclk=3,status=0;
    int fail_at=-1,bad_state=-1;
    std::map<unsigned,uint32_t> attrs{{0xd0a8,0},{0xd0a6,0x90}};
    std::vector<std::tuple<unsigned,unsigned,uint32_t>> commands;
    uint32_t rd(unsigned off) {assert(off==0x20 || off==0x144);return off==0x20?status:refclk;}
    bool inspect_platform_clocks() {return clocks;}
    bool inherited_ready() {return ready;}
    int inspect_vendor_link(const char *) {return int(states++)==bad_state?-1:2;}
    bool init_uic(unsigned op,uint32_t attr,uint32_t value,uint32_t &answer) {
        assert(attr==0xd0a8 || attr==0xd0a6);
        commands.emplace_back(op,attr,value);
        if(int(commands.size())-1==fail_at) return false;
        if(op==1) {assert(value==0);answer=attrs[attr];}
        else {
            assert(op==2 && (attr==0xd0a8?value==0:!(value&0x40)));
            if(!bad_readback) attrs[attr]=value;
        }
        return true;
    }
    uint32_t snapshot(const char *,uint32_t words[5]) {
        for(unsigned i=0;i<5;i++) words[i]=0;
        if(!quiet) words[0]=0x80000010;
        return 0;
    }
METHOD
};
int main() {
    for(unsigned lpm:{0u,1u}) for(unsigned stall:{0u,0x40u}) {
        Probe p;p.attrs[0xd0a8]=lpm;p.attrs[0xd0a6]=0x90|stall;
        assert(p.adopt_active_unipro());assert(p.attrs[0xd0a8]==0 && p.attrs[0xd0a6]==0x90);
        assert(p.commands.size()==4+lpm+(stall?1:0));
        for(int n=0;n<int(p.commands.size());n++) {
            Probe f;f.attrs[0xd0a8]=lpm;f.attrs[0xd0a6]=0x90|stall;f.fail_at=n;
            assert(!f.adopt_active_unipro() && f.commands.size()==unsigned(n+1));
        }
    }
    for(unsigned bad:{2u,0xffffffffu}) {
        Probe p;p.attrs[0xd0a8]=bad;assert(!p.adopt_active_unipro() && p.commands.size()==2);
    }
    Probe unknown;unknown.attrs[0xd0a6]=0xffffffff;assert(!unknown.adopt_active_unipro() && unknown.commands.size()==2);
    Probe clocks;clocks.clocks=false;assert(!clocks.adopt_active_unipro() && clocks.commands.empty());
    Probe issued;issued.peer_read_issued=true;assert(!issued.adopt_active_unipro() && issued.commands.empty());
    Probe busy;busy.ready=false;assert(!busy.adopt_active_unipro() && busy.commands.empty());
    Probe pending;pending.status=4;assert(!pending.adopt_active_unipro() && pending.commands.empty());
    Probe initial;initial.bad_state=0;assert(!initial.adopt_active_unipro() && initial.commands.empty());
    Probe after;after.bad_state=1;assert(!after.adopt_active_unipro() && after.commands.size()==4);
    Probe readback;readback.attrs[0xd0a8]=1;readback.bad_readback=true;
    assert(!readback.adopt_active_unipro() && readback.commands.size()==5);
    Probe errors;errors.quiet=false;assert(!errors.adopt_active_unipro() && errors.commands.empty());
}
''')


if __name__ == '__main__':
    unittest.main()
