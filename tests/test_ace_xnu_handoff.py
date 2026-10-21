"""Execute the freestanding loader on bounded host buffers, no device access."""
import ctypes as c
from pathlib import Path
import struct
import re
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]

class Range(c.Structure): _fields_=[('base',c.c_uint64),('size',c.c_uint64)]
class Policy(c.Structure): _fields_=[('ram',Range),('source',Range),('reserved',c.POINTER(Range)),('reserved_count',c.c_size_t)]
class Video(c.Structure): _fields_=[(n,c.c_uint64) for n in ['base','display','row_bytes','width','height','depth']]
class Args(c.Structure):
    _fields_=[('revision',c.c_uint16),('version',c.c_uint16)]+[(n,c.c_uint64) for n in ['virt_base','phys_base','mem_size','top']]+[('video',Video),('machine',c.c_uint32),('dt',c.c_uint64),('dt_len',c.c_uint32),('command',c.c_char*608),('flags',c.c_uint64),('actual',c.c_uint64)]
class Segment(c.Structure): _fields_=[(n,c.c_uint64) for n in ['dst','memory','offset','file']]
class Plan(c.Structure):
    _fields_=[('args',Args)]+[(n,c.c_uint64) for n in ['entry','adt','argpa','adtop','adtsz']]+[('count',c.c_uint32),('segments',Segment*32)]
VA=0xffffff0000000000
BASE=0x80000000
SIZE=0x40000

def bundle():
    b=bytearray(792)
    struct.pack_into('<8sII7Q',b,0,b'ACEXNU01',1,2,VA,VA,776,9,VA+0x8000,BASE,SIZE)
    b[72:77]=b'-v\0\0\0'
    struct.pack_into('<4Q',b,680,VA,32,744,13)
    struct.pack_into('<4Q',b,712,VA+0x4000,4097,760,8)
    b[744:757]=b'hello-kernel!';b[760:768]=b'segment2';b[776:785]=b'opaqueADT'
    return b

class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(); path=Path(cls.tmp.name)/'handoff.so'
        subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-O2','-fno-builtin','-shared','-fPIC',str(ROOT/'ace/xnu_handoff.c'),'-o',str(path)],check=True)
        cls.lib=c.CDLL(str(path))
        cls.lib.ace_xnu_prepare.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.POINTER(Plan)]
        cls.lib.ace_xnu_materialize.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.c_void_p,c.c_size_t,c.POINTER(Plan)]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def run_bundle(self,b=None,policy=None):
        b=bundle() if b is None else b
        source=(c.c_uint8*len(b)).from_buffer_copy(b)
        policy=policy or Policy(Range(BASE,SIZE),Range(0x90000000,len(b)),None,0)
        ram=(c.c_uint8*SIZE)(*([0xa5]*SIZE));out=Plan();c.memset(c.byref(out),0x5a,c.sizeof(out))
        rc=self.lib.ace_xnu_materialize(source,len(b),c.byref(policy),ram,SIZE,c.byref(out))
        if rc:
            self.assertEqual(bytes(ram),b'\xa5'*SIZE)
            self.assertEqual(bytes(out),b'\x5a'*c.sizeof(out))
        return rc,bytes(ram),out
    def test_real_byte_copies_bss_and_boot_args(self):
        rc,ram,o=self.run_bundle();self.assertEqual(rc,0)
        self.assertEqual(c.sizeof(Args),736);self.assertEqual(o.entry,BASE)
        self.assertEqual(ram[:32],b'hello-kernel!'+bytes(19))
        self.assertEqual(ram[32:64],b'\xa5'*32)
        self.assertEqual(ram[0x4000:0x5001],b'segment2'+bytes(4089))
        self.assertEqual(ram[0x5001],0xa5) # no rounded tail overrun
        self.assertEqual(ram[0x8000:0x8009],b'opaqueADT')
        self.assertEqual(o.argpa,BASE+0xc000)
        self.assertEqual(o.args.dt,VA+0x8000);self.assertEqual(o.args.top,BASE+0x10000)
        self.assertEqual(o.args.command,b'-v');self.assertEqual(o.args.actual,SIZE)
        self.assertEqual(bytes(o.args.video),bytes(48))
        self.assertEqual(ram[0xc000:0xc000+736],bytes(o.args))
        self.assertEqual(ram[0xc000+736:0x10000],bytes(0x4000-736))
    def test_header_and_table_mutations_refuse_before_any_store(self):
        mutations=[(0,b'SWEETXNU'),(8,struct.pack('<I',2)),(12,struct.pack('<I',33)),
                   (24,struct.pack('<Q',VA+16)), # entry in BSS
                   (24,struct.pack('<Q',VA+0x1000)), # entry in gap
                   (24,struct.pack('<Q',VA+1)),
                   (32,struct.pack('<Q',784)),(40,struct.pack('<Q',2**64-1)),
                   (48,struct.pack('<Q',VA+0x4000)),(56,struct.pack('<Q',BASE+0x4000)),
                   (64,struct.pack('<Q',SIZE+0x4000)),(72,b'x'*608),
                   (680+8,struct.pack('<Q',2**64-1)),(680+16,struct.pack('<Q',776)),
                   (680+24,struct.pack('<Q',33)),(712,struct.pack('<Q',VA+16))]
        for off,data in mutations:
            with self.subTest(offset=off,data=data):
                b=bundle();b[off:off+len(data)]=data
                self.assertNotEqual(self.run_bundle(b)[0],0)
    def test_truncation(self):
        for size in [0,1,679,680,743,780]:
            self.assertNotEqual(self.run_bundle(bundle()[:size])[0],0)
    def test_source_and_reserved_window_conflicts(self):
        p=Policy(Range(BASE,SIZE),Range(BASE+0x30000,792),None,0)
        self.assertNotEqual(self.run_bundle(policy=p)[0],0)
        ranges=(Range*1)(Range(BASE+0x30000,16))
        p=Policy(Range(BASE,SIZE),Range(0x90000000,792),ranges,1)
        self.assertNotEqual(self.run_bundle(policy=p)[0],0)
        ranges[0]=Range(2**64-8,16)
        self.assertNotEqual(self.run_bundle(policy=p)[0],0)
    def test_ram_exhaustion_and_overflow(self):
        for phys,mem in [(BASE,0xc000),(2**64-0x40000,0x80000)]:
            b=bundle();struct.pack_into('<2Q',b,56,phys,mem)
            p=Policy(Range(phys,mem),Range(0x90000000,len(b)),None,0)
            self.assertNotEqual(self.run_bundle(b,p)[0],0)
    def test_mapping_alias_refused(self):
        b=bundle();storage=(c.c_uint8*SIZE)();c.memmove(storage,bytes(b),len(b))
        p=Policy(Range(BASE,SIZE),Range(0x90000000,len(b)),None,0);o=Plan()
        before=bytes(storage)
        rc=self.lib.ace_xnu_materialize(storage,len(b),c.byref(p),storage,SIZE,c.byref(o))
        self.assertEqual(rc,-4);self.assertEqual(bytes(storage),before)
    def test_layout_matches_actual_cached_xnu_declarations(self):
        header=ROOT/'research/ci-0081/buildtree/xnu/pexpert/pexpert/arm64/boot.h'
        if not header.exists():self.skipTest('Local pinned XNU build artifact unavailable')
        text=header.read_text()
        video=re.search(r'struct Boot_Video \{.*?\n\};',text,re.S).group()
        args=re.search(r'typedef struct boot_args \{.*?\} boot_args;',text,re.S).group()
        fields={'Revision':'revision','Version':'version','virtBase':'virt_base','physBase':'phys_base','memSize':'mem_size','topOfKernelData':'top_of_kernel_data','Video':'video','machineType':'machine_type','deviceTreeP':'device_tree','deviceTreeLength':'device_tree_length','CommandLine':'command_line','bootFlags':'boot_flags','memSizeActual':'mem_size_actual'}
        source='#include <stdint.h>\n#include <stddef.h>\n#include "xnu_handoff.h"\n#define BOOT_LINE_LENGTH 608\n'+video+'\ntypedef struct Boot_Video Boot_Video;\n'+args+'\n'
        source+='_Static_assert(sizeof(boot_args)==sizeof(struct ace_xnu_boot_args),"size");\n'
        for old,new in fields.items():
            source+=f'_Static_assert(offsetof(boot_args,{old})==offsetof(struct ace_xnu_boot_args,{new}),"{old}");\n'
        file=Path(self.tmp.name)/'abi.c';file.write_text(source)
        subprocess.run(['cc','-std=c11','-Werror','-I',str(ROOT/'ace'),'-c',str(file),'-o',str(file.with_suffix('.o'))],check=True)

    def test_sanitized_mutated_payloads_do_not_modify_ram_on_refusal(self):
        # Real allocation bounds and ASan/UBSan protect both source and target.
        initial=','.join(str(n) for n in bundle())
        source='''#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "xnu_handoff.h"
static const unsigned char initial[]={INITIAL};
int main(void) {
 unsigned char *ram=malloc(0x40000),*old=malloc(0x40000);if(!ram||!old)return 2;
 uint32_t state=0x781239ab;
 for(unsigned i=0;i<5000;i++) {
   state=state*1664525+1013904223;
   size_t bytes=i%5?sizeof(initial):state%sizeof(initial);
   unsigned char *b=malloc(bytes?bytes:1);if(!b)return 3;
   memcpy(b,initial,bytes);
   for(unsigned j=0;j<8 && bytes;j++) {
     state=state*1664525+1013904223;b[state%bytes]^=(state>>24)|1;
   }
   struct ace_xnu_policy p={.ram={0x80000000,0x40000},.source={0x90000000,bytes}};
   struct ace_xnu_plan out;memset(&out,0x5a,sizeof(out));
   memset(ram,0xa5,0x40000);memcpy(old,ram,0x40000);
   int rc=ace_xnu_materialize(b,bytes,&p,ram,0x40000,&out);
   if(rc) {
     if(memcmp(ram,old,0x40000))return 4;
     for(size_t k=0;k<sizeof(out);k++)if(((unsigned char *)&out)[k]!=0x5a)return 5;
   }
   free(b);
 }
 free(ram);free(old);return 0;
}
'''.replace('INITIAL',initial)
        file=Path(self.tmp.name)/'fuzz.c';file.write_text(source);exe=file.with_suffix('')
        subprocess.run(['cc','-std=c11','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-no-pie','-I',str(ROOT/'ace'),str(file),str(ROOT/'ace/xnu_handoff.c'),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,timeout=45,capture_output=True)

    def test_optimized_qemu_verifier_refuses_before_mutating_evidence(self):
        report=ROOT/'research/ace-xnu-handoff-20261019/verification.json'
        before=report.read_bytes() if report.exists() else None
        run=subprocess.run(['python3','-O',str(ROOT/'ace/xnu-loader/verify.py')],capture_output=True,text=True,timeout=10)
        self.assertNotEqual(run.returncode,0)
        self.assertIn('Optimized verification is refused',run.stderr)
        self.assertEqual(report.read_bytes() if report.exists() else None,before)

    def test_freestanding_arm64_has_no_runtime_dependencies(self):
        o=Path(self.tmp.name)/'arm64.o'
        subprocess.run(['aarch64-linux-gnu-gcc','-O2','-ffreestanding','-fno-builtin','-mgeneral-regs-only','-mstrict-align','-fno-stack-protector','-Wall','-Wextra','-Werror','-c',str(ROOT/'ace/xnu_handoff.c'),'-o',str(o)],check=True)
        self.assertEqual(subprocess.check_output(['aarch64-linux-gnu-nm','-u',str(o)],text=True),'')

if __name__=='__main__':unittest.main()
