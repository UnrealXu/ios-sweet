"""Exercise actual debug-mux method effects; this does not prove phone link state."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VendorStateEffectsTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang++'), 'clang++ required')
    def test_mux_selection_restoration_and_faults(self):
        patch = (ROOT / 'xnu/patches/0099-ace-observe-selected-vendor-link-state.patch').read_text()
        source = '\n'.join(line[1:] for line in patch.splitlines()
                           if line.startswith((' ', '+')) and not line.startswith('+++'))
        start = source.index('    void inspect_vendor_link(')
        method = source[start:source.index('\n    }', start) + len('\n    }')]
        harness = r'''
#include <cassert>
#include <cstdint>
#include <map>
#include <utility>
#include <vector>
#define printf(...) ((void)0)
static void IODelay(unsigned delay) { assert(delay==1); }
struct Probe {
    std::map<unsigned,uint32_t> regs{{0x2240,0x00360001},{0x144,3},
        {0x22c0,0x11},{0x22d0,0x22},{0x22d4,0x33},{0x22d8,0x44},{0x22dc,0x55}};
    std::vector<std::pair<unsigned,uint32_t>> writes;
    bool ready=true,broken_mux=false;
    unsigned probes=0;
    uint32_t rd(unsigned off) {
        if(off==0x22c8) { probes++;return 0x20000001; }
        return regs[off];
    }
    void wr(unsigned off,uint32_t value) {
        assert(off==0x22c0 || off==0x22d0 || off==0x22d4 || off==0x22d8 || off==0x22dc);
        writes.emplace_back(off,value);
        if(!broken_mux) regs[off]=value;
    }
    bool inherited_ready() { return ready; }
METHOD
};
int main() {
    for(uint32_t hw:{0u,0xffffffffu,0x00000001u,0x00ff0001u}) {
        Probe p;p.regs[0x2240]=hw;p.inspect_vendor_link("bad-version");
        assert(p.writes.empty() && p.probes==0);
    }
    for(unsigned major:{0x35u,0x36u,0x40u}) {
        Probe p;p.regs[0x2240]=(major<<16)|1;auto saved=p.regs;
        p.inspect_vendor_link("selected");assert(p.regs==saved && p.probes==2);
        assert(p.writes.size()==(major>=0x36?10u:2u));
        assert(p.writes.front().first==0x22c0);
        assert(p.writes.front().second==(major>=0x36?0x820820u:0x20u));
    }
    Probe bad;auto saved=bad.regs;bad.broken_mux=true;bad.inspect_vendor_link("bad-mux");
    assert(bad.probes==0 && bad.regs==saved && bad.writes.size()==10);
    Probe busy;busy.ready=false;busy.inspect_vendor_link("busy");assert(busy.writes.empty());
    Probe clock;clock.regs[0x144]=1;clock.inspect_vendor_link("clock");assert(clock.writes.empty());
}
'''.replace('METHOD', method)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / 'probe.cpp').write_text(harness)
            subprocess.run(['clang++', '-std=c++17', '-O2', str(path / 'probe.cpp'),
                            '-o', str(path / 'probe')], check=True)
            subprocess.run([str(path / 'probe')], check=True, timeout=10)


if __name__ == '__main__':
    unittest.main()
