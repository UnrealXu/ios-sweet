"""Bound the vendor-bit experiment's actual code effects; no hardware proof."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VendorControlEffectsTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang++'), 'clang++ required')
    def test_only_known_idle_state_can_change_one_vendor_bit(self):
        patch = (ROOT / 'xnu/patches/0097-ace-adopt-shipping-xoufs-control-bit.patch').read_text()
        patched = '\n'.join(line[1:] for line in patch.splitlines()
                            if line.startswith((' ', '+')) and not line.startswith('+++'))
        start = patched.index('    bool adopt_vendor_control() {')
        method = patched[start:patched.index('\n    }', start) + len('\n    }')]
        harness = r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <utility>
#include <vector>
#include "ace/ufs_cold_handoff.h"
#define printf(...) ((void)0)
static bool delayed;
static void IODelay(unsigned us) { assert(us==1000);delayed=true; }
struct Probe {
    std::map<unsigned,uint32_t> regs{{0x140,2},{0x144,3},{0x20,0}};
    std::vector<std::pair<unsigned,uint32_t>> writes;
    bool ready=true;
    int post_fault=0;
    uint32_t rd(unsigned off) {
        if(delayed && off==0x140 && post_fault==1) return 2;
        if(delayed && off==0x140 && post_fault==6) return 0x182;
        if(delayed && off==0x144 && post_fault==3) return 1;
        return regs[off];
    }
    void wr(unsigned off,uint32_t value) { writes.emplace_back(off,value);regs[off]=value; }
    bool inherited_ready() { return ready && !(delayed && post_fault==2); }
    uint32_t snapshot(const char *,uint32_t words[5]) {
        for(unsigned i=0;i<5;i++) words[i]=0;
        if(post_fault==5) words[0]=0x80000010;
        return post_fault==4?4:regs[0x20];
    }
METHOD
    void effects() {
        assert(writes.size()<=1);
        for(auto write:writes) assert(write.first==0x140 && write.second==0x82);
    }
    bool invoke() { delayed=false;return adopt_vendor_control(); }
};
int main() {
    Probe good;assert(good.invoke());good.effects();assert(good.writes.size()==1);
    Probe adopted;adopted.regs[0x140]=0x82;assert(adopted.invoke());assert(adopted.writes.empty());
    for(uint32_t value:{0u,1u,3u,0x80u,0x83u,0xffffffffu}) {
        Probe p;p.regs[0x140]=value;assert(!p.invoke());assert(p.writes.empty());
    }
    for(uint32_t clock:{0u,1u,2u}) {
        Probe p;p.regs[0x144]=clock;assert(!p.invoke());assert(p.writes.empty());
    }
    for(uint32_t status:{4u,0x400u,0x800u}) {
        Probe p;p.regs[0x20]=status;assert(!p.invoke());assert(p.writes.empty());
    }
    Probe busy;busy.ready=false;assert(!busy.invoke());assert(busy.writes.empty());
    for(int fault=1;fault<=6;fault++) {
        Probe p;p.post_fault=fault;assert(!p.invoke());p.effects();assert(p.writes.size()==1);
    }
}
'''.replace('METHOD', method)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'probe.cpp'
            binary = Path(tmp) / 'probe'
            source.write_text(harness)
            subprocess.run(['clang++', '-std=c++17', '-O2', '-I', str(ROOT), str(source), '-o', str(binary)], check=True)
            subprocess.run([str(binary)], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
