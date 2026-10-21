"""Actual link-init method effects against a mock UIC engine, not a device."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LinkStartupEffectsTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang++'), 'clang++ required')
    def test_single_startup_whitelist_and_stop_on_every_uic_fault(self):
        patch = (ROOT / 'xnu/patches/0098-ace-initialize-mtk-link-once-before-transfer.patch').read_text()
        patched = '\n'.join(line[1:] for line in patch.splitlines()
                            if line.startswith((' ', '+')) and not line.startswith('+++'))
        methods = []
        for name in ['init_uic(', 'initialize_link_once(']:
            start = patched.index('    bool ' + name)
            methods.append(patched[start:patched.index('\n    }', start) + len('\n    }')])
        harness = r'''
#include <cassert>
#include <cstdint>
#include <cstring>
#include <map>
#include <tuple>
#include <utility>
#include <vector>
#include "ace/ufs_cold_handoff.h"
#define printf(...) ((void)0)
static void IODelay(unsigned us) { assert(us==1000); }
static uint64_t mach_absolute_time() { static uint64_t ticks;return ++ticks; }
struct Probe {
    std::map<unsigned,uint32_t> regs{{0x20,0},{0x144,3}};
    std::map<unsigned,uint32_t> attrs{{0xd0a6,0xffff0040},{0xd0a1,0xffff0020}};
    std::vector<std::tuple<unsigned,unsigned,uint32_t>> commands;
    std::vector<std::pair<unsigned,uint32_t>> writes;
    bool ready=true,inspect_ok=true;
    unsigned inspected=0;
    int fail_at=-1,mode=0,snapshot_fault=0;
    uint32_t rd(unsigned off) { return regs[off]; }
    void wr(unsigned off,uint32_t value) {
        writes.emplace_back(off,value);
        if(off==0x20) regs[off]&=~value;
        else regs[off]=value;
        if(off==0x90) commands.emplace_back(value,regs[0x94]>>16,regs[0x9c]);
    }
    bool inherited_ready() { return ready; }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {
        assert(off==0x20 && mask==0x400 && value==0x400);
        auto [op,attr,sent]=commands.back();
        bool fail=int(commands.size())-1==fail_at;
        if(fail && mode==1) return false;
        regs[0x20]=op==0x16?0x504:0x400;
        regs[0x98]=fail && mode==2 ? 1 : 0;
        if(op==1) regs[0x9c]=attrs[attr];
        if(op==2) attrs[attr]=sent;
        if(fail && mode==3) regs[0x20]|=0x800;
        if(fail && mode==4) ready=false;
        if(fail && mode==5) regs[0x144]=1;
        return true;
    }
    uint32_t snapshot(const char *stage,uint32_t words[5]) {
        for(unsigned i=0;i<5;i++) words[i]=0;
        if(strstr(stage,"sample1")) words[0]=0x80000010;
        if(snapshot_fault==1 && strstr(stage,"sample1")) words[1]=0x80002000;
        if(snapshot_fault==2 && strstr(stage,"sample2")) words[0]=0x80000010;
        if(snapshot_fault==3 && strstr(stage,"sample3")) return 0x800;
        return regs[0x20];
    }
    bool inspect_link_power() { inspected++;return inspect_ok; }
METHODS
    void effects() {
        assert(commands.size()<=9);
        unsigned starts=0;
        for(auto [op,attr,value]:commands) {
            if(op==0x16) { starts++;assert(attr==0 && value==0); }
            else if(op==1) assert((attr==0xd0a6 || attr==0xd0a1) && value==0);
            else { assert(op==2);assert(attr==0xd0a6 || attr==0xd0a1 || ((attr==0xd0a8 || attr==0x155e) && value==0)); }
        }
        assert(starts<=1);
        for(auto [off,value]:writes) {
            assert(off==0x94 || off==0x98 || off==0x9c || off==0x90 || off==0x20);
            if(off==0x20) assert(value==0x400 || value==0x500 || value==4);
        }
    }
};
int main() {
    Probe good;assert(good.initialize_link_once());good.effects();assert(good.commands.size()==9 && good.inspected==1);
    assert(good.attrs[0xd0a6]==0xffff000d && good.attrs[0xd0a1]==0xffff0000);
    const unsigned ops[]={2,2,1,2,0x16,1,2,1,2};
    const unsigned attrs[]={0xd0a8,0x155e,0xd0a6,0xd0a6,0,0xd0a6,0xd0a6,0xd0a1,0xd0a1};
    for(unsigned i=0;i<9;i++) assert(std::get<0>(good.commands[i])==ops[i] && std::get<1>(good.commands[i])==attrs[i]);
    for(unsigned op:{0u,3u,4u,0x14u,0x18u}) {
        Probe p;uint32_t answer;assert(!p.init_uic(op,0xd0a6,0,answer));assert(p.writes.empty());
    }
    for(auto [op,attr,value]:std::vector<std::tuple<unsigned,unsigned,uint32_t>>{{2,0x1571,0x11},{2,0x155e,1},{2,0xd0a8,1},{1,0xd0a1,1},{0x16,1,0},{0x16,0,1}}) {
        Probe p;uint32_t answer;assert(!p.init_uic(op,attr,value,answer));assert(p.writes.empty());
    }
    for(int fault=0;fault<9;fault++) for(int mode=1;mode<=5;mode++) {
        Probe p;p.fail_at=fault;p.mode=mode;assert(!p.initialize_link_once());p.effects();
        assert(p.commands.size()==unsigned(fault+1) && p.inspected==0);
    }
    for(int fault=1;fault<=3;fault++) {
        Probe p;p.snapshot_fault=fault;assert(!p.initialize_link_once());p.effects();assert(p.commands.size()==5);
    }
    for(uint32_t status:{4u,0x400u,0x800u}) {
        Probe p;p.regs[0x20]=status;assert(!p.initialize_link_once());assert(p.writes.empty());
    }
    Probe absent;absent.regs[0x144]=1;assert(!absent.initialize_link_once());assert(absent.writes.empty());
    Probe busy;busy.ready=false;assert(!busy.initialize_link_once());assert(busy.writes.empty());
    Probe inspect;inspect.inspect_ok=false;assert(!inspect.initialize_link_once());assert(inspect.inspected==1);inspect.effects();
}
'''.replace('METHODS', '\n'.join(methods))
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'probe.cpp'
            binary = Path(tmp) / 'probe'
            source.write_text(harness)
            subprocess.run(['clang++', '-std=c++17', '-O2', '-I', str(ROOT), str(source), '-o', str(binary)], check=True)
            subprocess.run([str(binary)], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
