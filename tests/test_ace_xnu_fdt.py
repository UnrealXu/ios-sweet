"""Exercise the native bounded FDT parser and actual exclusion policy."""
import ctypes as c
import copy
import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
from test_ace_mkadt import fixture,pack,node,u32,u64,tool
from test_ace_xnu_handoff import Range,Policy
ROOT=Path(__file__).resolve().parents[1]

class Node(c.Structure):_fields_=[(n,c.c_uint32) for n in ('name','parent','first','count','children')]
class Prop(c.Structure):_fields_=[(n,c.c_uint32) for n in ('name','value','bytes')]
class Fdt(c.Structure):
    _fields_=[('blob',c.c_void_p)]+[(n,c.c_uint32) for n in ('total','nodes','props','reserves','valid')]+[('node',Node*4096),('prop',Prop*16384),('reserve',Range*256)]
class Output(c.Structure):_fields_=[('policy',Policy),('reserved',Range*256),('deferred',c.c_uint32)]

class NativeFdtTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.d=Path(cls.tmp.name)
        wrapper=cls.d/'abi.c';wrapper.write_text('#include "xnu_fdt.h"\nsize_t fdt_size(void){return sizeof(struct ace_fdt);}\nsize_t output_size(void){return sizeof(struct ace_xnu_fdt_policy);}\n')
        lib=cls.d/'fdt.so'
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-shared','-fPIC','-I',str(ROOT/'ace'),str(ROOT/'ace/fdt.c'),str(ROOT/'ace/xnu_fdt.c'),str(wrapper),'-o',str(lib)],check=True)
        cls.lib=c.CDLL(str(lib));cls.lib.ace_fdt_open.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Fdt)]
        cls.lib.ace_fdt_find.argtypes=[c.POINTER(Fdt),c.c_char_p]
        cls.lib.ace_xnu_fdt_policy.argtypes=[c.POINTER(Fdt),c.c_uint64,c.POINTER(Policy),c.c_uint,c.POINTER(Output)]
        cls.lib.fdt_size.restype=c.c_size_t;cls.lib.output_size.restype=c.c_size_t
        assert cls.lib.fdt_size()==c.sizeof(Fdt) and cls.lib.output_size()==c.sizeof(Output)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def opened(self,blob):
        buf=c.create_string_buffer(blob);view=Fdt()
        rc=self.lib.ace_fdt_open(buf,len(blob),c.byref(view))
        self.assertEqual(rc,0)
        return buf,view
    def policy(self,blob=None,base=0x140000000,size=0x40000000,caller=None,native=1):
        buf,f=self.opened(pack(fixture()) if blob is None else blob)
        reserve=(Range*1)(Range(*(caller or (0x40000000,0x4000000))))
        p=Policy(Range(base,size),Range(0x42000000,0x1100000),reserve,1)
        out=Output();c.memset(c.byref(out),0xa5,c.sizeof(out))
        rc=self.lib.ace_xnu_fdt_policy(c.byref(f),0x47c80000,c.byref(p),native,c.byref(out))
        if rc:self.assertEqual(bytes(out),b'\xa5'*c.sizeof(out))
        return rc,out

    def test_actual_exclusions_match_host_builder_and_self_pointer(self):
        blob=pack(fixture());rc,out=self.policy(blob);self.assertEqual(rc,0)
        _,report=tool.build(blob,ram_base=0x140000000,ram_size=0x40000000,fdt_pa=0x47c80000,loader_ranges=[('loader',0x40000000,0x4000000)],boot_affinity=0,cold_native=True)
        expected={(x['base'],x['size']) for x in report['excluded_ranges']}|{(0x42000000,0x1100000)}
        got={(out.reserved[i].base,out.reserved[i].size) for i in range(out.policy.reserved_count)}
        self.assertEqual(got,expected);self.assertEqual(out.deferred,2)
        self.assertEqual(c.addressof(out.policy.reserved.contents),c.addressof(out.reserved))
        buf,f=self.opened(blob)
        self.assertEqual(self.lib.ace_fdt_find(c.byref(f),b'/'),0)
        self.assertGreater(self.lib.ace_fdt_find(c.byref(f),b'/cpus/cpu@000'),0)
        for path in (b'/not-present',b'/cpus/',b'cpus',b'//cpus'):
            self.assertEqual(self.lib.ace_fdt_find(c.byref(f),path),-1)

    def test_parser_truncation_duplicate_names_and_malformed_blocks(self):
        blob=pack(fixture())
        for n in (0,1,39,40,len(blob)-1):
            self.assertNotEqual(self.lib.ace_fdt_open(c.create_string_buffer(blob[:n]),n,c.byref(Fdt())),0)
        for offset,value in ((0,0),(4,0xffffffff),(8,41),(12,40),(16,41),(20,18),(24,18),(32,0xffffffff),(36,0xffffffff)):
            bad=bytearray(blob);struct.pack_into('>I',bad,offset,value)
            self.assertNotEqual(self.lib.ace_fdt_open(c.create_string_buffer(bytes(bad)),len(bad),c.byref(Fdt())),0)
        root=fixture();root.children.append(copy.deepcopy(root.children[0]))
        bad=pack(root);self.assertNotEqual(self.lib.ace_fdt_open(c.create_string_buffer(bad),len(bad),c.byref(Fdt())),0)
        bad=bytearray(blob);st=struct.unpack_from('>I',bad,8)[0]
        first=st+8;length,name=struct.unpack_from('>II',bad,first+4)
        second=(first+12+length+3)&~3
        struct.pack_into('>I',bad,second+8,name)
        self.assertNotEqual(self.lib.ace_fdt_open(c.create_string_buffer(bytes(bad)),len(bad),c.byref(Fdt())),0)

    def test_memreserve_dynamic_and_caller_changes_refuse_without_output_store(self):
        for changes in ({'base':0x50000000,'size':0x2000000}, {'caller':(0x140000000,1)},
                        {'native':0},{'base':0x140004000},{'base':0x240000000}):
            self.assertNotEqual(self.policy(**changes)[0],0)
        self.assertNotEqual(self.policy(pack(fixture(),[(0x140000000,1)]))[0],0)
        for key,value in [('size',u64(1)),('alignment',u64(4096)),('no-map',b''),('firmware-owned',b'')]:
            root=fixture();res=root.children[-1];res.children[-1].props[key]=value
            self.assertNotEqual(self.policy(pack(root))[0],0)
        root=fixture();root.children[-1].children.append(node('unknown',{'size':u64(4096)}))
        self.assertNotEqual(self.policy(pack(root))[0],0)
        root=fixture();root.children[-1].children[2].props['alloc-ranges']=u64(0x140000000,0x10000000)
        self.assertEqual(self.policy(pack(root))[0],-36)

    def test_workspace_and_output_aliases_are_rejected(self):
        blob=pack(fixture());storage=c.create_string_buffer(c.sizeof(Fdt()))
        c.memmove(storage,blob,len(blob));before=bytes(storage)
        self.assertNotEqual(self.lib.ace_fdt_open(storage,len(blob),c.cast(storage,c.POINTER(Fdt))),0)
        self.assertEqual(bytes(storage),before)
        buf,f=self.opened(blob);p=Policy(Range(0x140000000,0x40000000),Range(0x42000000,1),None,0)
        before=bytes(f)
        self.assertEqual(self.lib.ace_xnu_fdt_policy(c.byref(f),0x47c80000,c.byref(p),1,c.cast(c.byref(f),c.POINTER(Output))),-32)
        self.assertEqual(bytes(f),before)

    def test_private_real_fdt_matches_exact_existing_host_exclusions(self):
        path=ROOT/'research/ace-live-20261019-wireless/live-fdt.dtb'
        manifest=ROOT/'research/ace-adt-20261019/candidate-3g/manifest.json'
        if not path.exists() or not manifest.exists():self.skipTest('private phone FDT absent')
        blob=path.read_bytes();rc,out=self.policy(blob,size=0xc0000000);self.assertEqual(rc,0)
        _,f=self.opened(blob);self.assertEqual((f.nodes,f.props),(1830,9757))
        expected={(x['base'],x['size']) for x in json.loads(manifest.read_text())['excluded_ranges']}|{(0x42000000,0x1100000)}
        got={(out.reserved[i].base,out.reserved[i].size) for i in range(out.policy.reserved_count)}
        self.assertEqual(got,expected)

    @unittest.skipUnless(shutil.which('clang'),'sanitizer compiler absent')
    def test_sanitized_mutations_and_truncations_preserve_input_and_failed_output(self):
        blob=pack(fixture());data=','.join(map(str,blob))
        src=self.d/'fuzz.c';src.write_text('''#include "xnu_fdt.h"
#include <stdlib.h>
#include <string.h>
static const unsigned char original[]={'''+data+'''};
int main(void) {
 struct ace_fdt *f=malloc(sizeof(*f)); struct ace_xnu_fdt_policy *o=malloc(sizeof(*o));
 unsigned seed=31;
 for(unsigned k=0;k<3000;k++) {
  seed=seed*1664525u+1013904223u;
  size_t n=k%3?sizeof(original):(seed%sizeof(original));
  unsigned char *b=malloc(n?n:1),*saved=malloc(n?n:1);memcpy(b,original,n);
  if(n && k%3) b[seed%n]^=(unsigned char)(seed>>24);
  memcpy(saved,b,n);memset(o,0xa5,sizeof(*o));
  if(!ace_fdt_open(b,n,f)) {
   struct ace_xnu_range loader={0x40000000,0x4000000};
   struct ace_xnu_policy p={{0x140000000,0x40000000},{0x42000000,0x1100000},&loader,1};
   if(ace_xnu_fdt_policy(f,0x47c80000,&p,1,o))
    for(size_t i=0;i<sizeof(*o);i++) if(((unsigned char *)o)[i]!=0xa5) abort();
  }
  if(memcmp(b,saved,n)) abort();free(saved);free(b);
 }
 free(f);free(o);return 0;
}''')
        exe=self.d/'fuzz'
        subprocess.run(['clang','-std=c11','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-I',str(ROOT/'ace'),str(src),str(ROOT/'ace/fdt.c'),str(ROOT/'ace/xnu_fdt.c'),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,timeout=30)

    @unittest.skipUnless(shutil.which('aarch64-linux-gnu-gcc'),'cross compiler absent')
    def test_freestanding_native_policy_has_no_runtime_imports(self):
        objects=[]
        for name in ('fdt.c','xnu_fdt.c'):
            obj=self.d/(name+'.o');objects.append(str(obj))
            subprocess.run(['aarch64-linux-gnu-gcc','-mcpu=cortex-a55','-O2','-ffreestanding','-fno-builtin','-fno-stack-protector','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-c',str(ROOT/'ace'/name),'-o',str(obj)],check=True)
        linked=self.d/'fdt-linked.o';subprocess.run(['aarch64-linux-gnu-ld','-r',*objects,'-o',str(linked)],check=True)
        self.assertEqual(subprocess.check_output(['aarch64-linux-gnu-nm','-u',str(linked)],text=True),'')

    @unittest.skipUnless(shutil.which('aarch64-linux-gnu-gcc'),'cross compiler absent')
    def test_probe_elf_has_safe_bss_load_geometry_and_no_interpreter(self):
        output=self.d/'elf-output'
        subprocess.run(['bash',str(ROOT/'diagnostics/ace-fdt-policy/build.sh'),str(output)],check=True,stdout=subprocess.PIPE)
        data=(output/'ace-fdt-policy').read_bytes()
        self.assertEqual(data[:6],b'\x7fELF\x02\x01')
        self.assertEqual(struct.unpack_from('<HH',data,16),(2,183))
        phoff=struct.unpack_from('<Q',data,32)[0]
        entsize,count=struct.unpack_from('<HH',data,54)
        loads=[]
        for i in range(count):
            typ,flags,off,va,pa,files,memory,align=struct.unpack_from('<IIQQQQQQ',data,phoff+i*entsize)
            self.assertNotEqual(typ,3)  # no PT_INTERP / Android libc loader
            if typ!=1:continue
            self.assertNotEqual(flags&7,7)  # no writable executable segment
            self.assertLessEqual(off+files,len(data));self.assertLessEqual(files,memory)
            if not files:
                self.assertEqual(va%65536,0)
                self.assertEqual(off,0)
            loads.append((flags,files,memory))
        self.assertEqual(len(loads),2)
        self.assertEqual([x[0] for x in loads],[5,6])

if __name__=='__main__':unittest.main()
