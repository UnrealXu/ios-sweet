"""Exercise the actual patched active-link path against register/UIC mocks."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'iokit/Kernel/arm/AceUFSController.cpp'


def patched_controller(directory):
    # Reconstruct actual source from shipped patches, not a parallel model.
    for patch in sorted((ROOT / 'xnu/patches').glob('*.patch')):
        if not '0090' <= patch.name[:4] <= '0100':
            continue
        for section in re.split(r'(?=^--- )', patch.read_text(), flags=re.M):
            if '\n+++ b/' + TARGET + '\n' not in section:
                continue
            subprocess.run(['patch', '--batch', '--fuzz=0', '-p1'], input=section,
                           text=True, cwd=directory, capture_output=True, check=True)
    return (directory / TARGET).read_text()


class ActiveHandoffTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang++') and shutil.which('patch'), 'compiler and patch required')
    def test_active_down_and_fault_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / TARGET).parent.mkdir(parents=True)
            source = patched_controller(directory)
            methods = []
            for signature in ['int inspect_vendor_link(', 'bool finish_link_configuration(', 'bool initialize_link_once(']:
                start = source.index('    ' + signature)
                methods.append(source[start:source.index('\n    }', start) + len('\n    }')])
            harness = r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <tuple>
#include <vector>
#include "ace/ufs_cold_handoff.h"
#define printf(...) ((void)0)
static void IODelay(unsigned delay) { assert(delay==1 || delay==1000); }
struct Probe {
    std::map<unsigned,uint32_t> regs{{0x2240,0x00360000},{0x144,3},{0x34,1},
        {0x22c0,0x11},{0x22d0,0x22},{0x22d4,0x33},{0x22d8,0x44},{0x22dc,0x55}};
    std::map<unsigned,uint32_t> attrs{{0xd0a6,0x90},{0xd0a1,0x20}};
    std::vector<uint32_t> probes;
    std::vector<std::tuple<unsigned,unsigned,uint32_t>> commands;
    unsigned reads=0,link=2,snapshots=0,inspected=0;
    bool ready=true,broken_mux=false,broken_restore=false,power_ok=true;
    int fail_command=-1,bad_snapshot=-1;
    uint32_t rd(unsigned off) {
        if(off==0x22c8) { unsigned n=reads++;return n<probes.size()?probes[n]:(link<<28)|1; }
        return regs[off];
    }
    void wr(unsigned off,uint32_t value) {
        assert(off==0x22c0 || off==0x22d0 || off==0x22d4 || off==0x22d8 || off==0x22dc || off==0x20);
        if(off==0x20) { regs[off]&=~value;return; }
        if(broken_mux || (broken_restore && off==0x22c0 && value==0x11)) return;
        regs[off]=value;
    }
    bool inherited_ready() { return ready && regs[0x34]==1 && !regs[0x58] && !regs[0x78] && !regs[0x18]; }
    bool init_uic(unsigned op,uint32_t attr,uint32_t value,uint32_t &answer) {
        commands.emplace_back(op,attr,value);
        if(int(commands.size())-1==fail_command) return false;
        if(op==1) answer=attrs[attr];
        if(op==2) attrs[attr]=value;
        if(op==0x16) link=2;
        return true;
    }
    bool inspect_link_power() { inspected++;return power_ok; }
    uint32_t snapshot(const char *,uint32_t words[5]) {
        for(unsigned i=0;i<5;i++) words[i]=0;
        return int(snapshots++)==bad_snapshot?0x800:0;
    }
METHODS
};
int main() {
    Probe active;auto saved=active.regs;assert(active.initialize_link_once());
    assert(active.commands.size()==4 && active.inspected==1 && active.snapshots==3);
    for(auto [off,value]:saved) assert(active.regs[off]==value);
    assert(active.attrs[0xd0a6]==0x9d && active.attrs[0xd0a1]==0);
    for(auto [op,attr,value]:active.commands) assert((op==1 || op==2) && (attr==0xd0a6 || attr==0xd0a1));
    for(unsigned initial:{0u,1u}) {
        Probe p;p.link=initial;assert(p.initialize_link_once());assert(p.commands.size()==9);
        unsigned starts=0;for(auto [op,attr,value]:p.commands) if(op==0x16) starts++;
        assert(starts==1 && p.snapshots==6);
    }
    for(unsigned initial:{3u,4u,5u,15u}) {
        Probe p;p.link=initial;assert(!p.initialize_link_once() && p.commands.empty());
    }
    for(auto samples:std::vector<std::vector<uint32_t>>{{0x20000001,0x10000001},{0x20000008,0x20000008},
        {0xffffffff,0xffffffff},{0x20000001,0x20000002},{0x20000001,0x20000001,0x10000001,0x10000001}}) {
        Probe p;p.probes=samples;assert(!p.initialize_link_once());
        assert(p.commands.size()==(samples.size()>2?4u:0u));
    }
    for(uint32_t hw:{0u,0xffffffffu,0x00350000u,0x00360001u}) {
        Probe p;p.regs[0x2240]=hw;assert(!p.initialize_link_once() && p.commands.empty());
    }
    Probe mux;mux.broken_mux=true;assert(!mux.initialize_link_once() && mux.commands.empty());
    Probe restore;restore.broken_restore=true;assert(!restore.initialize_link_once() && restore.commands.empty());
    Probe busy;busy.ready=false;assert(!busy.initialize_link_once() && busy.commands.empty());
    Probe clock;clock.regs[0x144]=1;assert(!clock.initialize_link_once() && clock.commands.empty());
    for(unsigned off:{0x58u,0x78u,0x18u}) {
        Probe p;p.regs[off]=1;assert(!p.initialize_link_once() && p.commands.empty());
    }
    for(int n=0;n<4;n++) {
        Probe p;p.fail_command=n;assert(!p.initialize_link_once());assert(p.commands.size()==unsigned(n+1));
    }
    for(int n=0;n<3;n++) {
        Probe p;p.bad_snapshot=n;assert(!p.initialize_link_once());assert(p.snapshots==unsigned(n+1));
    }
    Probe power;power.power_ok=false;assert(!power.initialize_link_once());
    Probe fresh_fault;fresh_fault.link=1;fresh_fault.fail_command=4;
    assert(!fresh_fault.initialize_link_once() && fresh_fault.commands.size()==5);
}
'''.replace('METHODS', '\n'.join(methods))
            cpp = directory / 'probe.cpp'
            cpp.write_text(harness)
            subprocess.run(['clang++', '-std=c++17', '-O2', '-I', str(ROOT),
                            str(cpp), '-o', str(directory / 'probe')], check=True)
            subprocess.run([str(directory / 'probe')], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
