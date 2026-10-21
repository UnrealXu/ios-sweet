"""Exercise actual peer-read method; mock results are not phone evidence."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from test_ace_ufs_activehandoff import patched_controller

ROOT = Path(__file__).resolve().parents[1]


class PeerReadTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang++') and shutil.which('patch'), 'compiler and patch required')
    def test_single_read_and_fault_quarantine(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            target = directory / 'iokit/Kernel/arm/AceUFSController.cpp'
            target.parent.mkdir(parents=True)
            patched_controller(directory)
            patch = ROOT / 'xnu/patches/0101-ace-check-peer-before-dma-takeover.patch'
            subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(patch)],
                           cwd=directory, capture_output=True, check=True)
            source = target.read_text()
            start = source.index('    bool inspect_peer_transport_once(')
            method = source[start:source.index('\n    }', start) + len('\n    }')]
            harness = r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <utility>
#include <vector>
#include "ace/ufs_cold_handoff.h"
#define printf(...) ((void)0)
static uint64_t mach_absolute_time() { static uint64_t t;return ++t; }
struct Probe {
    bool peer_read_issued=false,ready=true,complete=true,quiet=true,disturb=false;
    unsigned commands=0,snapshots=0,states=0;
    int bad_state=-1;
    uint32_t response=1,result=0,status=0x400;
    std::map<unsigned,uint32_t> regs{{0x2240,0x00360000},{0x144,3}};
    std::vector<std::pair<unsigned,uint32_t>> writes;
    uint32_t rd(unsigned off) {return regs[off];}
    void wr(unsigned off,uint32_t value) {
        assert(off==0x94 || off==0x98 || off==0x9c || off==0x90 || off==0x20);
        writes.emplace_back(off,value);
        if(off==0x20) {assert(value==0x400);regs[off]&=~value;return;}
        regs[off]=value;
        if(off==0x90) {
            assert(value==3 && regs[0x94]==0x15610000 && !regs[0x98] && !regs[0x9c]);
            commands++;regs[0x98]=result;regs[0x9c]=response;regs[0x20]=status;
        }
    }
    bool inherited_ready() {return ready;}
    int inspect_vendor_link(const char *) {
        if(disturb) regs[0x20]=4;
        return int(states++)==bad_state?-1:2;
    }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {
        assert(off==0x20 && mask==0x400 && value==0x400);return complete;
    }
    uint32_t snapshot(const char *,uint32_t words[5]) {
        snapshots++;for(unsigned i=0;i<5;i++) words[i]=0;
        if(!quiet) words[0]=0x80000010;
        return regs[0x20];
    }
METHOD
};
int main() {
    for(unsigned lanes:{1u,2u}) {
        Probe p;p.response=lanes;assert(p.inspect_peer_transport_once());
        assert(p.commands==1 && p.peer_read_issued && p.snapshots==1 && p.regs[0x20]==0);
        auto writes=p.writes;assert(!p.inspect_peer_transport_once());
        assert(p.commands==1 && p.writes==writes);
    }
    for(unsigned bad:{0u,3u,0xffffffffu}) {
        Probe p;p.response=bad;assert(!p.inspect_peer_transport_once());
        assert(p.commands==1 && p.snapshots==1 && p.regs[0x20]==0x400);
    }
    for(unsigned status:{0u,4u,0x404u,0x815u}) {
        Probe p;p.status=status;assert(!p.inspect_peer_transport_once());assert(p.commands==1);
        for(auto [off,value]:p.writes) assert(off!=0x20);
    }
    for(unsigned rc:{1u,4u,0xffu}) {
        Probe p;p.result=rc;assert(!p.inspect_peer_transport_once());assert(p.commands==1);
        assert(p.regs[0x20]==0x400);
    }
    Probe timeout;timeout.complete=false;assert(!timeout.inspect_peer_transport_once());
    assert(timeout.commands==1 && timeout.regs[0x20]==0x400);
    assert(!timeout.inspect_peer_transport_once() && timeout.commands==1);
    for(unsigned hw:{0u,0x00350000u,0x00360001u,0xffffffffu}) {
        Probe p;p.regs[0x2240]=hw;assert(!p.inspect_peer_transport_once() && p.writes.empty());
    }
    Probe clock;clock.regs[0x144]=1;assert(!clock.inspect_peer_transport_once() && clock.writes.empty());
    Probe busy;busy.ready=false;assert(!busy.inspect_peer_transport_once() && busy.writes.empty());
    Probe pending;pending.regs[0x20]=0x400;assert(!pending.inspect_peer_transport_once() && pending.writes.empty());
    Probe state;state.bad_state=0;assert(!state.inspect_peer_transport_once() && state.writes.empty());
    Probe race;race.disturb=true;assert(!race.inspect_peer_transport_once() && race.writes.empty());
    Probe changed;changed.bad_state=1;assert(!changed.inspect_peer_transport_once() && changed.commands==1);
    Probe error;error.quiet=false;assert(!error.inspect_peer_transport_once() && error.commands==1);
}
'''.replace('METHOD', method)
            cpp = directory / 'peer.cpp'
            cpp.write_text(harness)
            subprocess.run(['clang++', '-std=c++17', '-O2', '-I', str(ROOT),
                            str(cpp), '-o', str(directory / 'peer')], check=True)
            subprocess.run([str(directory / 'peer')], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
