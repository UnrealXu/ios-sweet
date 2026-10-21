"""Native FDT/ADT consistency and refusal before actual C materialization."""
import ctypes as c
import mmap
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
from test_ace_mkadt import fixture,ufs_fixture,pack,node,u32,u64,tool,adt
from test_ace_xnu_fdt import Fdt
from test_ace_xnu_handoff import Range,Policy,Plan
from test_ace_xnu_cpu import State,ready
ROOT=Path(__file__).resolve().parents[1]
RAM=0x140000000;SIZE=0x2000000;VA=0xffffff0000000000
SOURCES=['fdt.c','xnu_fdt.c','xnu_platform.c','xnu_cpu.c','xnu_handoff.c']

def adt_for(root=None,ufs_probe=False,ufs_read=False,ufs_root=False):
    return tool.build(pack(root or fixture()),ram_base=RAM,ram_size=SIZE,fdt_pa=0x47c80000,
        loader_ranges=[('loader',0x40000000,0x4000000)],boot_affinity=0,cold_native=True,seed=bytes(range(64)),ufs_probe=ufs_probe,ufs_read=ufs_read,ufs_root=ufs_root)[0]

def bundle(tree):
    b=bytearray(720+len(tree))
    struct.pack_into('<8sII7Q',b,0,b'ACEXNU01',1,1,VA,VA,720,len(tree),VA+0x4000,RAM,SIZE)
    struct.pack_into('<4Q',b,680,VA,64,712,4);b[712:716]=bytes.fromhex('1f2003d5');b[720:]=tree
    return b

class PlatformHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.d=Path(cls.tmp.name);lib=cls.d/'platform.so'
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-ffreestanding','-fno-builtin','-shared','-fPIC',*[str(ROOT/'ace'/x) for x in SOURCES],'-o',str(lib)],check=True)
        cls.lib=c.CDLL(str(lib));cls.lib.ace_fdt_open.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Fdt)]
        cls.lib.ace_xnu_platform_check.argtypes=[c.POINTER(Fdt),c.c_void_p,c.c_size_t,Range]
        cls.lib.ace_xnu_prepare_platform.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.POINTER(State),c.POINTER(Fdt),c.POINTER(Plan)]
        cls.lib.ace_xnu_materialize_platform.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.POINTER(State),c.POINTER(Fdt),c.c_void_p,c.c_size_t,c.POINTER(Plan)]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def opened(self,blob):
        buf=c.create_string_buffer(blob);f=Fdt();self.assertEqual(self.lib.ace_fdt_open(buf,len(blob),c.byref(f)),0);return buf,f
    def check(self,root=None,tree=None):
        root=root or fixture();dtb,f=self.opened(pack(root));tree=adt_for() if tree is None else tree
        buf=c.create_string_buffer(tree)
        return self.lib.ace_xnu_platform_check(c.byref(f),buf,len(tree),Range(RAM,SIZE))

    def test_exact_host_adt_and_opaque_seed_match(self):
        self.assertEqual(self.check(),0)
        root,end=adt.parse(adt_for());self.assertEqual(end,len(adt_for()))
        chosen=root.children[0];chosen.props=[(k,flags,b'X'*64 if k=='random-seed' else v) for k,flags,v in chosen.props]
        self.assertEqual(self.check(tree=adt.serialize(root)),0)
        source=fixture();source.children[1].children[0].props['clock-frequency']=u32(1600000000)
        self.assertEqual(self.check(source),-45)
        self.assertEqual(self.check(source,adt_for(source)),0)

    def test_command_read_profile_is_separate_and_live_resources_required(self):
        source=ufs_fixture();tree=adt_for(source,ufs_read=True)
        self.assertEqual(self.check(source,tree),0)
        self.assertEqual(self.check(fixture(),tree),-46)
        parsed,_=adt.parse(tree)
        self.assertEqual(parsed.children[-1].prop('compatible'),b'ace,mt6895-ufs-read-v1\0')
        self.assertIsNone(parsed.children[-1].prop('ace,read-only-probe'))
        parsed.children[-1].props.append(('ace,read-only-probe',0,struct.pack('<I',1)))
        self.assertEqual(self.check(source,adt.serialize(parsed)),-45)
        with self.assertRaises(ValueError):adt_for(source,ufs_probe=True,ufs_read=True)

    def test_exact_root_discovery_profile_native_accepts_and_refuses_tampering(self):
        source=ufs_fixture();tree=adt_for(source,ufs_read=True,ufs_root=True)
        self.assertEqual(self.check(source,tree),0)
        parsed,_=adt.parse(tree)
        for name,value in [('ace,root-read-probe',struct.pack('<I',2)),('ace,command-read-probe',struct.pack('<I',0))]:
            changed,_=adt.parse(tree)
            changed.children[-1].props=[(k,flags,value if k==name else v) for k,flags,v in changed.children[-1].props]
            self.assertEqual(self.check(source,adt.serialize(changed)),-45)

    def test_ufs_opt_in_host_and_native_contract_agree(self):
        source=ufs_fixture();tree=adt_for(source,True)
        self.assertEqual(self.check(source,tree),0)
        self.assertEqual(self.check(source,adt_for()),0)
        self.assertEqual(self.check(fixture(),tree),-46)
        import fdt
        for path,key,value in [('/soc','ranges',u64(0,1,2)),
            ('/soc','status',b'disabled\0'),('/soc','#size-cells',u32(1)),
            ('/soc/ufshci@112b0000','reg',u64(0x112b0000,0x2000)),
            ('/soc/ufshci@112b0000','interrupts',u32(0,137,1,0)),
            ('/soc/ufshci@112b0000','interrupt-parent',u32(999)),
            ('/soc/ufshci@112b0000','status',b'disabled\0'),
            ('/soc/ufshci@112b0000','interrupts-extended',u32(1,0,137,4,0))]:
            source=ufs_fixture();fdt.Tree(source,[],0).by_path(path).props[key]=value
            with self.subTest(path=path,key=key):self.assertEqual(self.check(source,tree),-46)
        source=ufs_fixture();source.children.append(node('duplicate',{'compatible':b'mediatek,mt8183-ufshci\0'}))
        self.assertEqual(self.check(source,tree),-46)
        parsed,_=adt.parse(tree);probe=parsed.children[-1]
        probe.props=[(k,flags,u64(0x112b0000,0x2000) if k=='reg' else v) for k,flags,v in probe.props]
        self.assertEqual(self.check(ufs_fixture(),adt.serialize(parsed)),-45)

    def test_cpu_gic_timer_psci_and_provider_mismatches_refuse(self):
        changes=[('/cpus/cpu@000','reg',u32(0x100),-41),
            ('/cpus/cpu@004','compatible',b'arm,cortex-a55\0',-41),
            ('/cpus/cpu@007','enable-method',b'spin-table\0',-41),
            ('/gic','reg',u64(0x8000000,0x10000,0x80a0000,0x100000),-42),
            ('/gic','#interrupt-cells',u32(3),-42),
            ('/timer','interrupt-parent',u32(7),-43),
            ('/timer','interrupts',u32(1,13,4,0,1,14,4,0,1,11,1,0,1,10,4,0),-43),
            ('/timer','clock-frequency',u32(24000000),-43),
            ('/psci','method',b'hvc\0',-44)]
        import fdt
        for path,key,value,error in changes:
            root=fixture();fdt.Tree(root,[],0).by_path(path).props[key]=value
            with self.subTest(path=path,key=key):self.assertEqual(self.check(root),error)
        root=fixture();root.children.append(node('duplicate-provider',{'phandle':u32(1)}))
        self.assertEqual(self.check(root),-42)
        root=fixture();root.children[1].children.pop();self.assertEqual(self.check(root),-41)

    def test_noncanonical_adt_bytes_flags_properties_and_lengths_refuse(self):
        tree=adt_for()
        for off in (0,4,40,len(tree)-1):
            changed=bytearray(tree);changed[off]^=1;self.assertEqual(self.check(tree=bytes(changed)),-45)
        for n in (1,7,100,len(tree)-1):self.assertEqual(self.check(tree=tree[:n]),-45)
        root,_=adt.parse(tree);root.props.append(('serial-number',0,b'other-target\0'))
        self.assertEqual(self.check(tree=adt.serialize(root)),-45)
        self.assertEqual(self.check(tree=tree+b'\0'),-45)

    def test_ppi_partitions_match_cpu_handles_and_unknown_children_refuse(self):
        root=fixture();gic=root.children[2]
        parts=node('ppi-partitions',{},[node('interrupt-partition-0',{'affinity':u32(0x38,0x39,0x3a,0x3b),'phandle':u32(0x14d)}),
            node('interrupt-partition-1',{'affinity':u32(0x3c,0x3d,0x3e,0x3f),'phandle':u32(0x14e)})])
        parts.parent=gic;gic.children=[parts]
        self.assertEqual(self.check(root),0)
        parts.children[0].props['affinity']=u32(0x38,0x39,0x3a,0x3f)
        self.assertEqual(self.check(root),-42)
        gic.children=[node('unexpected-its',{'reg':u64(0x99900000,0x1000)})]
        self.assertEqual(self.check(root),-42)

    def test_platform_refusal_preserves_plan_and_entire_destination(self):
        _,f=self.opened(pack(fixture()));tree=adt_for();payload=bytes(bundle(tree));buf=c.create_string_buffer(payload)
        p=Policy(Range(RAM,SIZE),Range(0x42000000,len(payload)),None,0);cpu=ready();out=Plan()
        ram=mmap.mmap(-1,SIZE);anchor=c.c_char.from_buffer(ram)
        try:
            ram[:]=b'\xa5'*SIZE
            for off in (720, len(payload)-1):
                changed=bytearray(payload);changed[off]^=1;bad=c.create_string_buffer(bytes(changed))
                c.memset(c.byref(out),0x5a,c.sizeof(out))
                self.assertEqual(self.lib.ace_xnu_materialize_platform(bad,len(payload),c.byref(p),c.byref(cpu),c.byref(f),c.addressof(anchor),SIZE,c.byref(out)),-45)
                self.assertEqual(ram[:],b'\xa5'*SIZE);self.assertEqual(bytes(out),b'\x5a'*c.sizeof(out))
            self.assertEqual(self.lib.ace_xnu_materialize_platform(buf,len(payload),c.byref(p),c.byref(cpu),c.byref(f),c.addressof(anchor),SIZE,c.byref(out)),0)
            self.assertEqual(ram[:64],bytes.fromhex('1f2003d5')+bytes(60));self.assertEqual(out.entry,RAM)
            self.assertEqual(ram[0x4000:0x4000+len(tree)],tree)
        finally:del anchor;ram.close()

    def test_context_and_mapping_aliases_refuse(self):
        dtb,f=self.opened(pack(fixture()));payload=bytes(bundle(adt_for()));buf=c.create_string_buffer(payload)
        p=Policy(Range(RAM,SIZE),Range(0x42000000,len(payload)),None,0);cpu=ready();out=Plan();before=bytes(f)
        self.assertEqual(self.lib.ace_xnu_prepare_platform(buf,len(payload),c.byref(p),c.byref(cpu),c.byref(f),c.cast(c.byref(f),c.POINTER(Plan))),-40)
        self.assertEqual(self.lib.ace_xnu_materialize_platform(buf,len(payload),c.byref(p),c.byref(cpu),c.byref(f),c.byref(f),SIZE,c.byref(out)),-40)
        self.assertEqual(bytes(f),before)

    def test_actual_private_fdt_and_actual_candidate_adt(self):
        fpath=ROOT/'research/ace-native-fdt-20261020/live-fdt.dtb';apath=ROOT/'research/ace-adt-20261019/candidate-3g/ace.adt'
        if not fpath.exists() or not apath.exists():self.skipTest('private actual captures absent')
        dtb,f=self.opened(fpath.read_bytes());tree=apath.read_bytes();a=c.create_string_buffer(tree)
        self.assertEqual(self.lib.ace_xnu_platform_check(c.byref(f),a,len(tree),Range(RAM,0xc0000000)),0)

    @unittest.skipUnless(shutil.which('aarch64-linux-gnu-gcc'),'cross compiler absent')
    def test_actual_a55_freestanding_partial_link_has_no_runtime_imports(self):
        objects=[]
        for name in SOURCES:
            path=self.d/(name+'.o');objects.append(str(path))
            subprocess.run(['aarch64-linux-gnu-gcc','-O2','-mcpu=cortex-a55','-ffreestanding','-fno-builtin','-fno-stack-protector','-mgeneral-regs-only','-Wall','-Wextra','-Werror','-c',str(ROOT/'ace'/name),'-o',str(path)],check=True)
        target=self.d/'linked.o';subprocess.run(['aarch64-linux-gnu-ld','-r',*objects,'-o',str(target)],check=True)
        self.assertEqual(subprocess.check_output(['aarch64-linux-gnu-nm','-u',str(target)],text=True),'')
        relocations=subprocess.check_output(['aarch64-linux-gnu-readelf','-Wr',str(target)],text=True)
        for kind in ('R_AARCH64_ABS64','R_AARCH64_ABS32','R_AARCH64_ABS16','R_AARCH64_MOVW_UABS','R_AARCH64_MOVW_SABS'):
            self.assertNotIn(kind,relocations)

    @unittest.skipUnless(shutil.which('clang'),'sanitizer compiler absent')
    def test_sanitized_fdt_adt_mutations_and_truncations_preserve_inputs(self):
        dtb=pack(fixture());tree=adt_for();source=self.d/'fuzz-platform.c'
        source.write_text('''#include "xnu_platform.h"
#include <stdlib.h>
#include <string.h>
static const unsigned char original_fdt[]={'''+','.join(map(str,dtb))+'''};
static const unsigned char original_adt[]={'''+','.join(map(str,tree))+'''};
int main(void) {
 struct ace_fdt *f=malloc(sizeof(*f));unsigned seed=81;
 for(unsigned k=0;k<2000;k++) {
  seed=seed*1664525u+1013904223u;
  size_t n=k%3?sizeof(original_fdt):seed%sizeof(original_fdt);
  size_t m=k%4?sizeof(original_adt):seed%sizeof(original_adt);
  unsigned char *a=malloc(n?n:1),*b=malloc(m?m:1),*aa=malloc(n?n:1),*bb=malloc(m?m:1);
  memcpy(a,original_fdt,n);memcpy(b,original_adt,m);
  if(n && k%3) a[seed%n]^=(unsigned char)(seed>>24);
  if(m && k%4) b[(seed>>8)%m]^=(unsigned char)(seed>>16);
  memcpy(aa,a,n);memcpy(bb,b,m);
  if(!ace_fdt_open(a,n,f)) (void)ace_xnu_platform_check(f,b,m,(struct ace_xnu_range){0x140000000,0x2000000});
  if(memcmp(a,aa,n) || memcmp(b,bb,m)) abort();
  free(a);free(b);free(aa);free(bb);
 }
 free(f);return 0;
}''')
        exe=self.d/'fuzz-platform'
        subprocess.run(['clang','-std=c11','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-I',str(ROOT/'ace'),str(source),*[str(ROOT/'ace'/x) for x in SOURCES],'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True,timeout=30)

if __name__=='__main__':unittest.main()
