"""Execute actual root codec, patched singleton bridge and BSD strategy.

Mocked hardware proves bounds, serialization and failure behavior only.
"""
from pathlib import Path
import re,subprocess,tempfile,unittest
from test_ace_ufs_sipreset import source_at
ROOT=Path(__file__).resolve().parents[1]
PATCH=ROOT/'xnu/patches/0116-ace-serialized-readonly-bsd-userdata-root.patch'

def new_source(path):
    section=next(s for s in re.split(r'(?=^diff --git )',PATCH.read_text(),flags=re.M) if '\n+++ b/'+path+'\n' in s)
    return ''.join(line[1:]+'\n' for line in section.splitlines() if line.startswith('+') and not line.startswith('+++'))

def execute(code):
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);(p/'test.cpp').write_text(code)
        subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-pthread','-O2','-I',str(ROOT),str(p/'test.cpp'),'-o',str(p/'test')],check=True)
        subprocess.run([str(p/'test')],check=True,timeout=30)

PRELUDE=r'''
#include <cassert>
#include <initializer_list>
#include <cstdint>
#include <cstring>
#include <cerrno>
#include "ace/ufs_read_protocol.h"
#include "ace/ufs_root_gpt.h"
#include "ace/ufs_root_io.h"
'''

class BsdRootTests(unittest.TestCase):
    def test_codec_exact_cdb_boundaries_alias_and_random_slices(self):
        self.assertEqual(new_source('iokit/Kernel/arm/AceUFSRootIO.h'),(ROOT/'ace/ufs_root_io.h').read_text())
        execute(PRELUDE+r'''
int main() {
    ace_ufs_gpt_plan p={62480383,34,62480378,0};ace_ufs_root_bounds r={3514368,58961912};
    uint8_t a[ACE_UFS_ARENA];uint64_t pa=0x140000000;struct ace_ufs_root_slice s={};
    for(unsigned lba:{3514368u,62476279u}) {
        assert(ace_ufs_root_request(a,sizeof(a),pa,&p,&r,2,lba,4096)==4096);
        assert(a[ACE_UFS_UCD+16]==0x28 && a[ACE_UFS_UCD+24]==1);
        assert(ace_ufs_be32(a+ACE_UFS_UCD+18)==lba && a[ACE_UFS_UCD+1]==0x40);
    }
    for(unsigned lba:{0u,3514367u,62476280u,UINT32_MAX}) {
        memset(a,0x66,sizeof(a));assert(ace_ufs_root_request(a,sizeof(a),pa,&p,&r,2,lba,4096)<0);
        for(auto v:a) assert(v==0x66);
    }
    for(unsigned lun:{0u,1u,3u,7u}) assert(ace_ufs_root_request(a,sizeof(a),pa,&p,&r,lun,3514368,4096)<0);
    for(unsigned block:{0u,512u,8192u}) assert(ace_ufs_root_request(a,sizeof(a),pa,&p,&r,2,3514368,block)<0);
    assert(ace_ufs_root_request(a,sizeof(a),1,&p,&r,2,3514368,4096)<0);
    assert(ace_ufs_root_request(a,sizeof(a)-1,pa,&p,&r,2,3514368,4096)<0);
    assert(ace_ufs_root_request(a,sizeof(a),pa,(ace_ufs_gpt_plan *)a,&r,2,3514368,4096)<0);
    assert(ace_ufs_root_request(a,sizeof(a),pa,&p,(ace_ufs_root_bounds *)a,2,3514368,4096)<0);
    uint64_t capacity=r.blocks*4096;
    assert(!ace_ufs_root_slice(&p,&r,capacity,0,&s) && !s.bytes);
    for(uint64_t offset:{capacity+1,UINT64_MAX}) assert(ace_ufs_root_slice(&p,&r,offset,1,&s)<0);
    assert(ace_ufs_root_slice(&p,&r,capacity,1,&s)<0);
    assert(ace_ufs_root_slice(&p,&r,0,65537,&s)<0);
    assert(ace_ufs_root_slice(&p,&r,0,1,(struct ace_ufs_root_slice *)&r)<0);
    uint64_t state=123;
    for(unsigned i=0;i<10000;i++) {
        state=state*6364136223846793005ULL+1;uint64_t off=state%capacity;
        size_t n=(state>>32)%65536+1;if(n>capacity-off)n=capacity-off;
        assert(!ace_ufs_root_slice(&p,&r,off,n,&s));
        assert(s.lba==r.first_lba+off/4096 && s.skip==off%4096);
        assert(s.bytes==(n<4096-s.skip?n:4096-s.skip));
    }
    for(ace_ufs_root_bounds bad: {ace_ufs_root_bounds{0,1},{r.first_lba,0},{r.first_lba,UINT64_MAX},{p.last_usable,2}}) {
        assert(ace_ufs_root_slice(&p,&bad,0,1,&s)<0);
    }
}
'''.replace('#include <cassert>','#include <cassert>'))
#include <initializer_list>

    def test_actual_bridge_serializes_partial_failures_and_quarantines(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);source_at(d)
            for n in range(113,116):
                patch,=(ROOT/'xnu/patches').glob(f'{n:04d}-*.patch')
                subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(patch)],cwd=d,check=True,capture_output=True)
            for section in re.split(r'(?=^diff --git )',PATCH.read_text(),flags=re.M):
                if '\n+++ b/iokit/Kernel/arm/' in section:
                    subprocess.run(['patch','--batch','--fuzz=0','-p1'],input=section,text=True,cwd=d,check=True,capture_output=True)
            source=(d/'iokit/Kernel/arm/AceUFSController.cpp').read_text()
        start=source.index('extern "C" int ace_ufs_root_geometry(');end=source.index('\nbool AceUFSController::start(',start)
        execute(PRELUDE+r'''
#include <mutex>
#include <thread>
#include <vector>
#define bcopy(s,d,n) memcpy(d,s,n)
static std::mutex lock;
static std::mutex *ace_ufs_root_lock=&lock;
static thread_local bool locked;
static void IOLockLock(std::mutex *p) {assert(!locked);p->lock();locked=true;}
static void IOLockUnlock(std::mutex *p) {assert(locked);locked=false;p->unlock();}
static int ace_ufs_root_phase;
static uint8_t arena[ACE_UFS_ARENA],mmio[0x2300];
struct AceUFSReadProbe {
    ace_ufs_gpt_plan gpt_plan={62480383,34,62480378,0};
    ace_ufs_root_bounds root_bounds={3514368,58961912};
    uintptr_t dma=(uintptr_t)arena,mmio=(uintptr_t)::mmio;
    bool quarantined=false;unsigned calls=0;int fault=-1;
    int command(unsigned op,unsigned lun,unsigned lba,unsigned block) {
        assert(locked && !quarantined && op==7);
        assert(ace_ufs_root_request(arena,sizeof(arena),0x140000000,&gpt_plan,&root_bounds,lun,lba,block)==4096);
        if((int)calls++==fault) {quarantined=true;return -3;}
        for(unsigned i=0;i<4096;i++) arena[ACE_UFS_DATA+i]=(uint8_t)(lba+i);
        return 0;
    }
};
static AceUFSReadProbe ace_ufs_owner;
BRIDGE
int main() {
    uint64_t capacity=0;size_t done=999;uint8_t b[65536];
    assert(ace_ufs_root_geometry(&capacity)==EAGAIN);
    assert(ace_ufs_root_read(0,b,1,&done)==EAGAIN && done==999 && !ace_ufs_owner.calls);
    ace_ufs_root_phase=-2;assert(ace_ufs_root_geometry(&capacity)==ENXIO);
    ace_ufs_root_phase=-1;assert(ace_ufs_root_geometry(&capacity)==EIO);
    ace_ufs_root_phase=1;assert(!ace_ufs_root_geometry(&capacity) && capacity==241507991552ULL);
    assert(ace_ufs_root_read(0,arena,1,&done)==EINVAL);
    assert(ace_ufs_root_read(0,b,65537,&done)==EINVAL && !ace_ufs_owner.calls);
    assert(ace_ufs_root_read(capacity,b,1,&done)==EINVAL && !ace_ufs_owner.calls);
    assert(!ace_ufs_root_read(capacity,nullptr,0,&done) && !done && !ace_ufs_owner.calls);
    std::vector<std::thread> readers;
    for(unsigned t=0;t<8;t++) readers.emplace_back([t] {
        uint8_t result[65536];size_t read=0;uint64_t off=511+t;
        assert(!ace_ufs_root_read(off,result,sizeof(result),&read) && read==sizeof(result));
        for(unsigned i=0;i<sizeof(result);i++) assert(result[i]==(uint8_t)(3514368+(off+i)/4096+(off+i)%4096));
    });
    for(auto &t:readers)t.join();assert(ace_ufs_owner.calls==8*17);
    ace_ufs_owner.fault=ace_ufs_owner.calls+1;
    assert(ace_ufs_root_read(511,b,8192,&done)==EIO && done==3585 && ace_ufs_owner.quarantined);
    unsigned calls=ace_ufs_owner.calls;assert(ace_ufs_root_read(0,b,1,&done)==EIO && calls==ace_ufs_owner.calls);
    assert(ace_ufs_root_geometry(&capacity)==EIO);
}
'''.replace('BRIDGE',source[start:end]))

    def test_actual_bsd_strategy_write_eof_mapping_and_residual(self):
        source=new_source('bsd/dev/ace_ufs.c');start=source.index('static void\nace_strategy(');end=source.index('\nstatic int\nace_ioctl(',start)
        execute(r'''
#include <cstdint>
#include <cassert>
#include <initializer_list>
#include <cerrno>
#include <cstddef>
using caddr_t=char *;using daddr64_t=int64_t;
struct Buffer {uint32_t count,resid;int flags=1,dev=0,error=0,map_error=0,maps=0,unmaps=0,completed=0;int64_t sector=0;char bytes[65536];};
using buf_t=Buffer *;
#define B_READ 1
#define DEV_BSIZE 512
static int ace_bsd_ready=1;static uint64_t ace_bytes=8192;
static int read_error;static size_t read_done;static unsigned reads;static uint64_t read_offset;
static uint32_t buf_count(buf_t p){return p->count;}
static int64_t buf_blkno(buf_t p){return p->sector;}
static void buf_setresid(buf_t p,uint32_t n){p->resid=n;}
static int buf_flags(buf_t p){return p->flags;}
static int buf_device(buf_t p){return p->dev;}
static int minor(int dev){return dev;}
static int buf_map(buf_t p,caddr_t *a){p->maps++;*a=p->bytes;return p->map_error;}
static void buf_unmap(buf_t p){p->unmaps++;}
static void buf_seterror(buf_t p,int e){p->error=e;}
static void buf_biodone(buf_t p){p->completed++;}
static int ace_ufs_root_read(uint64_t off,void *,size_t n,size_t *done){reads++;read_offset=off;*done=read_error?read_done:n;return read_error;}
STRATEGY
int main() {
    Buffer b{};b.count=512;b.sector=1;ace_strategy(&b);assert(!b.error && !b.resid && b.completed==1 && b.maps==1 && b.unmaps==1 && reads==1 && read_offset==512);
    for(unsigned fault=0;fault<8;fault++) {
        Buffer q{};q.count=512;
        if(fault==0)q.flags=0;
        if(fault==1)q.sector=-1;
        if(fault==2)q.sector=INT64_MAX;
        if(fault==3)q.sector=16;
        if(fault==4)q.count=65537;
        if(fault==5)q.dev=1;
        if(fault==6)ace_bsd_ready=0;
        if(fault==7)q.map_error=1;
        unsigned before=reads;ace_strategy(&q);assert(q.error && q.resid==512+(fault==4?65025:0) && q.completed==1 && reads==before && !q.unmaps);
        if(fault==0)assert(q.error==EROFS);ace_bsd_ready=1;
    }
    Buffer empty{};empty.sector=16;ace_strategy(&empty);assert(!empty.error && !empty.maps && empty.completed==1);
    Buffer partial{};partial.count=8192;read_error=EIO;read_done=4096;ace_strategy(&partial);assert(partial.resid==4096 && partial.error==EIO && partial.unmaps==1);
}
'''.replace('STRATEGY',source[start:end]))
