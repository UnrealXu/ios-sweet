"""Execute the same bounded GPT parser and request codec used by XNU."""
import ctypes as C
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import zlib

ROOT=Path(__file__).resolve().parents[1]
class Plan(C.Structure):
    _fields_=[('last',C.c_uint64),('first',C.c_uint64),('end',C.c_uint64),('crc',C.c_uint32)]
class Bounds(C.Structure):
    _fields_=[('first',C.c_uint64),('blocks',C.c_uint64)]

def entry(index,first,last,name):
    b=bytearray(128);b[:16]=bytes(range(1,17));b[16:32]=index.to_bytes(16,'little')
    struct.pack_into('<QQ',b,32,first,last);b[56:56+len(name.encode('utf-16le'))]=name.encode('utf-16le')
    return b

def fixture():
    a=bytearray(16384);a[:128]=entry(1,8,135,'misc');a[128:256]=entry(2,1000,62480375,'userdata')
    b=bytearray(4096);b[:8]=b'EFI PART'
    struct.pack_into('<IIIIQQQQ',b,8,0x10000,92,0,0,1,62480383,34,62480375)
    b[56:72]=bytes(range(1,17));struct.pack_into('<QIII',b,72,2,128,128,zlib.crc32(a))
    return header_crc(b),a

def header_crc(b):
    b=bytearray(b);b[16:20]=bytes(4);struct.pack_into('<I',b,16,zlib.crc32(b[:92]));return b

def buf(b):return (C.c_uint8*len(b)).from_buffer_copy(b)

class GptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('cc'):raise unittest.SkipTest('C compiler needed')
        cls.temp=tempfile.TemporaryDirectory();d=Path(cls.temp.name)
        (d/'codec.c').write_text('''#include "ace/ufs_read_protocol.h"
#include "ace/ufs_root_gpt.h"
int good(const uint8_t*r,size_t n,unsigned lun){return ace_ufs_gpt_good_response(r,n,lun);}
int header(const uint8_t*b,size_t n,uint64_t last,unsigned block,struct ace_ufs_gpt_plan*p){return ace_ufs_gpt_header(b,n,last,block,p);}
int entries(const uint8_t*b,size_t n,const struct ace_ufs_gpt_plan*p,struct ace_ufs_root_bounds*r){return ace_ufs_gpt_userdata(b,n,p,r);}
int request(uint8_t*a,size_t n,uint64_t pa,const struct ace_ufs_gpt_plan*p,unsigned lun,unsigned lba,unsigned block){return ace_ufs_gpt_request(a,n,pa,p,lun,lba,block);}
''')
        subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-pedantic','-O2','-shared','-fPIC','-I',str(ROOT),str(d/'codec.c'),'-o',str(d/'codec.so')],check=True)
        cls.lib=C.CDLL(str(d/'codec.so'));ptr=C.POINTER(C.c_uint8)
        cls.lib.good.argtypes=[ptr,C.c_size_t,C.c_uint]
        cls.lib.header.argtypes=[ptr,C.c_size_t,C.c_uint64,C.c_uint,C.POINTER(Plan)]
        cls.lib.entries.argtypes=[ptr,C.c_size_t,C.POINTER(Plan),C.POINTER(Bounds)]
        cls.lib.request.argtypes=[ptr,C.c_size_t,C.c_uint64,C.POINTER(Plan),C.c_uint,C.c_uint,C.c_uint]
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def plan(self,b=None):
        p=Plan();self.assertEqual(self.lib.header(buf(b or fixture()[0]),4096,62480383,4096,C.byref(p)),0);return p
    def parse(self,a,p,ok=False):
        r=Bounds(0xaaaa,0xbbbb);before=bytes(r)
        rc=self.lib.entries(buf(a),len(a),C.byref(p),C.byref(r))
        if ok:self.assertEqual(rc,0)
        else:self.assertLess(rc,0);self.assertEqual(bytes(r),before)
        return r
    def test_header_and_complete_userdata_bounds_input_unchanged(self):
        b,a=fixture();src=buf(b);p=Plan();self.assertEqual(self.lib.header(src,4096,62480383,4096,C.byref(p)),0)
        self.assertEqual(bytes(src),b);r=self.parse(a,p,True)
        zero_guid=bytearray(b);zero_guid[56:72]=bytes(16)
        self.assertEqual(self.lib.header(buf(header_crc(zero_guid)),4096,62480383,4096,C.byref(p)),0)
        self.assertEqual((r.first,r.blocks),(1000,62480375-1000+1))
    def test_header_refuses_crc_geometry_capacity_and_alias(self):
        b,_=fixture()
        changes=[(0,b'NO'),(8,struct.pack('<I',0x20000)),(12,struct.pack('<I',96)),(20,b'\1'),
                 (24,struct.pack('<Q',2)),(32,struct.pack('<Q',62480382)),(40,struct.pack('<Q',5)),
                 (48,struct.pack('<Q',62480379)),(72,struct.pack('<Q',3)),
                 (80,struct.pack('<I',129)),(84,struct.pack('<I',256))]
        for off,data in changes:
            bad=bytearray(b);bad[off:off+len(data)]=data;bad=header_crc(bad)
            p=Plan(1,2,3,4);old=bytes(p)
            self.assertLess(self.lib.header(buf(bad),4096,62480383,4096,C.byref(p)),0);self.assertEqual(bytes(p),old)
        for n,last,block in [(4095,62480383,4096),(4096,0xffffffffffffffff,4096),(4096,62480383,512)]:
            p=Plan(1,2,3,4);old=bytes(p)
            self.assertLess(self.lib.header(buf(b),n,last,block,C.byref(p)),0);self.assertEqual(bytes(p),old)
        bad=bytearray(b);bad[88]^=1;self.assertLess(self.lib.header(buf(bad),4096,62480383,4096,C.byref(Plan())),0)
        src=buf(b);self.assertLess(self.lib.header(src,4096,62480383,4096,C.cast(src,C.POINTER(Plan))),0);self.assertEqual(bytes(src),b)
    def test_full_array_crc_missing_name_duplicate_guid_overlap_and_ranges(self):
        _,a=fixture();p=self.plan();bad=bytearray(a);bad[-1]=1;self.parse(bad,p)
        cases=[]
        for first,last,name in [(7,135,'misc'),(8,136,'misc'),(8,135,'userdata'),(8,135,'miscX')]:
            bad=bytearray(a);bad[:128]=entry(1,first,last,name);cases.append(bad)
        bad=bytearray(a);bad[48]=1;cases.append(bad)
        bad=bytearray(a);bad[:128]=bytes(128);bad[256:384]=entry(3,8,135,'misc');cases.append(bad)
        for first,last,name in [(1000,62480376,'userdata'),(1000,999,'userdata'),(1000,2000,'Userdata'),(1000,2000,'userdataX')]:
            bad=bytearray(a);bad[128:256]=entry(2,first,last,name);cases.append(bad)
        for replacement in [entry(2,62480376,62480377,'extra'),entry(3,900,1100,'extra'),entry(3,2000,3000,'userdata')]:
            bad=bytearray(a);bad[256:384]=replacement;cases.append(bad)
        bad=bytearray(a);bad[144:160]=bytes(16);cases.append(bad)
        bad=bytearray(a);bad[16:32]=bad[144:160];cases.append(bad)
        bad=bytearray(a);bad[128:256]=entry(2,1000,1999,'userdata');bad[256:384]=entry(3,2000,3000,'userdata');cases.append(bad)
        for bad in cases:p.crc=zlib.crc32(bad);self.parse(bad,p)
        src=buf(a);p=self.plan();self.assertLess(self.lib.entries(src,len(a),C.byref(p),C.cast(src,C.POINTER(Bounds))),0);self.assertEqual(bytes(src),a)
    def test_actual_good_response_ignores_unused_tail_but_checks_all_header_bytes(self):
        raw=bytes.fromhex('21000200')+bytes(28)+b'\xa5'*480
        src=buf(raw);self.assertEqual(self.lib.good(src,512,2),1);self.assertEqual(bytes(src),raw)
        for value in [0,0x55,0xff]:
            self.assertEqual(self.lib.good(buf(raw[:32]+bytes([value])*480),512,2),1)
        for i in range(32):
            bad=bytearray(raw);bad[i]^=1;src=buf(bad)
            self.assertEqual(self.lib.good(src,512,2),0);self.assertEqual(bytes(src),bad)
        for n,lun in [(511,2),(0,2),(512,0),(512,3)]:self.assertEqual(self.lib.good(buf(raw),n,lun),0)
        self.assertEqual(self.lib.good(None,512,2),0)

    def test_only_four_primary_array_reads_and_refusal_no_stores(self):
        p=self.plan()
        for lba in range(2,6):
            a=buf(bytes(16384));self.assertEqual(self.lib.request(a,len(a),0x140000000,C.byref(p),2,lba,4096),4096)
            self.assertEqual(bytes(a)[0x1010:0x1020],bytes([0x28,0])+lba.to_bytes(4,'big')+bytes([0,0,1])+bytes(7))
            self.assertEqual(bytes(a)[0x140c:0x1410],struct.pack('<I',4095))
        for lun,lba,block,pa,n in [(2,0,4096,0x140000000,16384),(2,6,4096,0x140000000,16384),(0,2,4096,0x140000000,16384),(2,2,512,0x140000000,16384),(2,2,4096,1,16384),(2,2,4096,0x140000000,16383)]:
            a=buf(b'\x77'*16384);self.assertLess(self.lib.request(a,n,pa,C.byref(p),lun,lba,block),0);self.assertEqual(bytes(a),b'\x77'*16384)

class DriverIntegrationTests(unittest.TestCase):
    def test_patch_applies_header_matches_and_actual_discovery_stops_on_fault(self):
        import sys
        sys.path.insert(0,str(ROOT/'tests'))
        from test_ace_ufs_sipreset import source_at
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);source_at(d)
            patch=ROOT/'xnu/patches/0113-ace-ufs-retained-owner-primary-gpt-discovery.patch'
            subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(patch)],cwd=d,check=True,capture_output=True)
            subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(ROOT/'xnu/patches/0114-ace-accept-exact-observed-misc-gpt-extent.patch')],cwd=d,check=True,capture_output=True)
            subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(ROOT/'xnu/patches/0115-ace-check-good-response-header-without-unused-sense-tail.patch')],cwd=d,check=True,capture_output=True)
            self.assertEqual((d/'iokit/Kernel/arm/AceUFSRootGPT.h').read_bytes(),(ROOT/'ace/ufs_root_gpt.h').read_bytes())
            source=(d/'iokit/Kernel/arm/AceUFSController.cpp').read_text()
            self.assertNotIn('AceUFSReadProbe probe',source)
            self.assertIn('static AceUFSReadProbe ace_ufs_owner;',source)
            start=source.index('    void discover_root()');end=source.index('\n    void run(',start)
            wrapper=source[source.index('    int command('):source.index('    int command_inner(')]
            b,a=fixture();(d/'header.bin').write_bytes(b);(d/'array.bin').write_bytes(a)
            code=r'''
#include <cstdint>
#include <cstring>
#include <cassert>
#include <fstream>
#include "ace/ufs_read_protocol.h"
#include "ace/ufs_root_gpt.h"
#define printf(...) ((void)0)
#define bcopy(s,d,n) memcpy(d,s,n)
using vm_offset_t=uintptr_t;
static uint8_t arena[ACE_UFS_ARENA], entries[ACE_UFS_GPT_BYTES], header[4096];
struct Probe {
    bool gpt_header_valid=true,quarantined=false,root_ready=false;
    ace_ufs_gpt_plan gpt_plan={};ace_ufs_root_bounds root_bounds={};uint8_t gpt_entries[ACE_UFS_GPT_BYTES]={};
    vm_offset_t dma=(uintptr_t)arena;unsigned calls=0;int fault=-1;
    int command_inner(unsigned op,unsigned lun,unsigned lba,unsigned block) {
        assert(op==6 && lun==2 && lba==2+calls && block==4096);
        unsigned at=calls++;if((int)at==fault)return -3;
        memcpy(arena+ACE_UFS_DATA,entries+at*4096,4096);return 0;
    }
WRAPPER
DISCOVERY
};
int main(int argc,char**argv) {
    assert(argc==3);std::ifstream(argv[1],std::ios::binary).read((char*)header,sizeof(header));
    std::ifstream(argv[2],std::ios::binary).read((char*)entries,sizeof(entries));
    ace_ufs_gpt_plan plan={};assert(!ace_ufs_gpt_header(header,4096,62480383,4096,&plan));
    Probe good;good.gpt_plan=plan;good.discover_root();assert(good.calls==4 && good.root_ready && !good.quarantined);
    assert(good.root_bounds.first_lba==1000 && good.root_bounds.blocks==62479376);
    for(int i=0;i<4;i++) {Probe p;p.gpt_plan=plan;p.fault=i;p.discover_root();
        assert(p.calls==(unsigned)i+1 && p.quarantined && !p.root_ready);
        assert(p.command(6,2,2,4096)==-7 && p.calls==(unsigned)i+1);
    }
    Probe noheader;noheader.gpt_header_valid=false;noheader.discover_root();assert(!noheader.calls);
    entries[100]^=1;Probe corrupt;corrupt.gpt_plan=plan;corrupt.discover_root();assert(corrupt.calls==4 && !corrupt.root_ready);
}
'''.replace('WRAPPER',wrapper).replace('DISCOVERY',source[start:end])
            (d/'driver.cpp').write_text(code)
            subprocess.run(['clang++','-std=c++17','-O2','-I',str(ROOT),str(d/'driver.cpp'),'-o',str(d/'driver')],check=True)
            subprocess.run([str(d/'driver'),str(d/'header.bin'),str(d/'array.bin')],check=True)
