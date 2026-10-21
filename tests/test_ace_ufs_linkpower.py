"""Exercise the actual patched power-observation method against bounded MMIO.

This checks control effects and refusal paths, not hardware or UFS success.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LinkPowerEffectsTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang++'), 'clang++ required')
    def test_only_local_gets_and_no_transfer_writes_on_success_or_fault(self):
        patch = (ROOT / 'xnu/patches/0096-ace-read-link-power-before-first-transfer.patch').read_text()
        patched = '\n'.join(line[1:] for line in patch.splitlines()
                            if line.startswith((' ', '+')) and not line.startswith('+++'))
        start = patched.index('    bool inspect_link_power() {')
        method = patched[start:patched.index('\n    }', start) + len('\n    }')]
        harness = r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <utility>
#include <vector>
#define printf(...) ((void)0)
static uint64_t mach_absolute_time() { static uint64_t n; return ++n; }
struct Probe {
    std::map<unsigned,uint32_t> registers{{0x144,3},{0x20,0}};
    std::vector<std::pair<unsigned,uint32_t>> writes;
    std::vector<uint32_t> attributes;
    int fault_at=-1, mode=0, completed=0;
    bool ready=true;
    uint32_t rd(unsigned off) { return registers[off]; }
    void wr(unsigned off,uint32_t value) {
        writes.emplace_back(off,value);
        if(off==0x20) registers[off]&=~value;
        else registers[off]=value;
        if(off==0x90) {
            assert(value==1); // No SET, peer command, reset or startup.
            assert(registers[0x98]==0 && registers[0x9c]==0);
            attributes.push_back(registers[0x94]);
        }
    }
    bool inherited_ready() { return ready; }
    bool wait(unsigned off,uint32_t mask,uint32_t value) {
        assert(off==0x20 && mask==0x400 && value==0x400);
        bool fault=completed++==fault_at;
        if(fault && mode==1) return false;
        registers[0x20]=0x400 | (fault && mode==2 ? 0x800 : 0);
        registers[0x98]=fault && mode==3 ? 1 : 0;
        registers[0x9c]=0x11;
        if(fault && mode==4) ready=false;
        if(fault && mode==5) registers[0x144]=1;
        return true;
    }
    void snapshot(const char *,uint32_t words[5]) {
        for(unsigned i=0;i<5;i++) words[i]=0;
    }
METHOD
    void verify_effects() {
        for(auto write:writes) {
            unsigned off=write.first;
            assert(off==0x24 || off==0x94 || off==0x98 || off==0x9c || off==0x90 || off==0x20);
            if(off==0x24) assert(write.second==0);
            if(off==0x20) assert(write.second==0x400);
        }
        const uint32_t expected[3]={0x15710000,0x15680000,0x15830000};
        assert(attributes.size()<=3);
        for(unsigned i=0;i<attributes.size();i++) assert(attributes[i]==expected[i]);
    }
};
int main() {
    Probe good; assert(good.inspect_link_power()); good.verify_effects();
    assert(good.attributes.size()==3 && good.registers[0x20]==0);
    for(uint32_t clock:{0u,1u,2u}) {
        Probe p;p.registers[0x144]=clock;assert(!p.inspect_link_power());assert(p.writes.empty());
    }
    for(uint32_t status:{4u,0x400u,0x800u,0xffffffffu}) {
        Probe p;p.registers[0x20]=status;assert(!p.inspect_link_power());
        assert(p.attributes.empty());p.verify_effects();
    }
    Probe busy;busy.ready=false;assert(!busy.inspect_link_power());assert(busy.attributes.empty());busy.verify_effects();
    for(int fault=0;fault<3;fault++) for(int mode=1;mode<=5;mode++) {
        Probe p;p.fault_at=fault;p.mode=mode;assert(!p.inspect_link_power());
        assert(p.attributes.size()==unsigned(fault+1));p.verify_effects();
    }
}
'''.replace('METHOD', method)
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'probe.cpp'
            binary = Path(tmp) / 'probe'
            source.write_text(harness)
            subprocess.run(['clang++', '-std=c++17', '-O2', str(source), '-o', str(binary)], check=True)
            subprocess.run([str(binary)], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
