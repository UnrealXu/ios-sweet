"""Test the actual bounded power-mode experiment, not physical link success."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from test_ace_ufs_activehandoff import patched_controller

ROOT = Path(__file__).resolve().parents[1]


class PeerAutoModeTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang++') and shutil.which('patch'), 'compiler and patch required')
    def test_power_completion_readback_and_single_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            target = directory / 'iokit/Kernel/arm/AceUFSController.cpp'
            target.parent.mkdir(parents=True)
            patched_controller(directory)
            for name in ['0101-ace-check-peer-before-dma-takeover.patch',
                         '0102-ace-probe-fastauto-peer-access.patch']:
                subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i',
                                str(ROOT / 'xnu/patches' / name)], cwd=directory,
                               capture_output=True, check=True)
            source = target.read_text()
            methods = []
            for signature in ['bool read_peer_mode_state(', 'bool prepare_peer_auto_mode_once(']:
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
static uint64_t mach_absolute_time() {static uint64_t t;return ++t;}
struct Probe {
    bool peer_mode_attempted=false,peer_read_issued=false,ready=true,quiet=true,disturb=false;
    int fail_at=-1,fault=0,bad_state=-1;
    unsigned states=0,snapshots=0;
    std::map<unsigned,uint32_t> regs{{0x2240,0x00360000},{0x144,3},{0x30,0x10f}};
    std::map<unsigned,uint32_t> attrs{{0x1571,0x11},{0x1568,4},{0x1583,4}};
    std::vector<std::tuple<unsigned,unsigned,uint32_t>> commands;
    uint32_t rd(unsigned off) {return regs[off];}
    void wr(unsigned off,uint32_t value) {
        assert(off==0x94 || off==0x98 || off==0x9c || off==0x90 || off==0x20);
        if(off==0x20) {assert(value==0x400 || value==0x410);regs[off]&=~value;return;}
        regs[off]=value;
        if(off==0x90) {
            unsigned attr=regs[0x94]>>16,sent=regs[0x9c];
            assert(regs[0x98]==0);
            commands.emplace_back(value,attr,sent);
            if(value==1) {
                assert((attr==0x1571 || attr==0x1568 || attr==0x1583) && sent==0);
                regs[0x9c]=attrs[attr];regs[0x20]=0x400;
            } else {
                assert(value==2 && attr==0x1571 && sent==0x44);
                attrs[attr]=sent;regs[0x20]=0x410;
                if(fault==8) attrs[attr]=0x11;
                if(fault==9) attrs[0x1568]=3;
            }
            if(int(commands.size())-1==fail_at) {
                if(fault==2) regs[0x98]=8;
                if(fault==3) regs[0x20]|=4;
                if(fault==4) ready=false;
                if(fault==5) regs[0x144]=1;
                if(fault==6) regs[0x20]=0x400;
                if(fault==7) regs[0x30]=0x50f;
            }
        }
    }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {
        assert(off==0x20 && mask==value && (mask==0x400 || mask==0x410));
        return !(int(commands.size())-1==fail_at && fault==1);
    }
    bool inherited_ready() {return ready;}
    int inspect_vendor_link(const char *) {
        if(disturb) regs[0x20]=4;
        return int(states++)==bad_state?-1:2;
    }
    uint32_t snapshot(const char *,uint32_t words[5]) {
        snapshots++;for(unsigned i=0;i<5;i++) words[i]=0;
        if(!quiet) words[0]=0x80000010;
        return regs[0x20];
    }
METHODS
};
int main() {
    Probe good;assert(good.prepare_peer_auto_mode_once());
    assert(good.commands.size()==7 && good.attrs[0x1571]==0x44 && good.attrs[0x1568]==4);
    auto saved=good.commands;assert(!good.prepare_peer_auto_mode_once() && good.commands==saved);
    for(int n=0;n<7;n++) for(int fault=1;fault<=5;fault++) {
        Probe p;p.fail_at=n;p.fault=fault;assert(!p.prepare_peer_auto_mode_once());
        assert(p.commands.size()==unsigned(n+1));
        assert(!p.prepare_peer_auto_mode_once() && p.commands.size()==unsigned(n+1));
    }
    for(int fault:{6,7}) {
        Probe p;p.fail_at=3;p.fault=fault;assert(!p.prepare_peer_auto_mode_once());
        assert(p.commands.size()==4 && p.regs[0x20]!=0);
    }
    for(int fault:{8,9}) {
        Probe p;p.fault=fault;assert(!p.prepare_peer_auto_mode_once() && p.commands.size()==7);
    }
    for(unsigned mode:{0u,0x44u,0x22u,0x55u,0xffffffffu}) {
        Probe p;p.attrs[0x1571]=mode;assert(!p.prepare_peer_auto_mode_once());
        assert(p.commands.size()==3);
    }
    Probe gear;gear.attrs[0x1583]=3;assert(!gear.prepare_peer_auto_mode_once() && gear.commands.size()==3);
    Probe issued;issued.peer_read_issued=true;assert(!issued.prepare_peer_auto_mode_once() && issued.commands.empty());
    Probe busy;busy.ready=false;assert(!busy.prepare_peer_auto_mode_once() && busy.commands.empty());
    Probe clock;clock.regs[0x144]=1;assert(!clock.prepare_peer_auto_mode_once() && clock.commands.empty());
    Probe hw;hw.regs[0x2240]=0x00350000;assert(!hw.prepare_peer_auto_mode_once() && hw.commands.empty());
    Probe status;status.regs[0x20]=4;assert(!status.prepare_peer_auto_mode_once() && status.commands.empty());
    Probe state;state.bad_state=0;assert(!state.prepare_peer_auto_mode_once() && state.commands.empty());
    Probe changed;changed.bad_state=1;assert(!changed.prepare_peer_auto_mode_once() && changed.commands.size()==7);
    Probe race;race.disturb=true;assert(!race.prepare_peer_auto_mode_once() && race.commands.empty());
    Probe errors;errors.quiet=false;assert(!errors.prepare_peer_auto_mode_once() && errors.commands.size()==7);
}
'''.replace('METHODS', '\n'.join(methods))
            cpp = directory / 'peer-auto.cpp'
            cpp.write_text(harness)
            subprocess.run(['clang++', '-std=c++17', '-O2', '-I', str(ROOT),
                            str(cpp), '-o', str(directory / 'peer-auto')], check=True)
            subprocess.run([str(directory / 'peer-auto')], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
