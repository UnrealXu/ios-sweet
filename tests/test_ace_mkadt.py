import ctypes as c
import importlib.util
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import adt
import fdt
spec = importlib.util.spec_from_file_location('ace_mkadt',ROOT/'tools/ace-mkadt.py')
tool = importlib.util.module_from_spec(spec); spec.loader.exec_module(tool)
BASE = ROOT/'research/ace-xnu-pmsg-20261019/buildtree/xnu'
u32 = lambda *v: struct.pack('>%dI'%len(v),*v)
u64 = lambda *v: struct.pack('>%dQ'%len(v),*v)


def node(name,props=None,children=()):
    item=fdt.Node(name,props=props or {},children=list(children))
    for child in item.children:child.parent=item
    return item


def fixture():
    cpus=[node(f'cpu@{i:03x}',{'device_type':b'cpu\0','reg':u32(i<<8),
        'compatible':b'arm,cortex-a55\0' if i<4 else b'arm,cortex-a78\0',
        'enable-method':b'psci\0','phandle':u32(0x38+i),
        'clock-frequency':u32(1701000000 if i<4 else 2171000000)}) for i in range(8)]
    return node('',{'compatible':b'mediatek,MT6895\0','#address-cells':u32(2),'#size-cells':u32(2),
                    'interrupt-parent':u32(1)},[
        node('memory@40000000',{'device_type':b'memory\0','reg':u64(0x40000000,0x200000000)}),
        node('cpus',{'#address-cells':u32(1),'#size-cells':u32(0)},cpus),
        node('gic',{'compatible':b'arm,gic-v3\0','interrupt-controller':b'','phandle':u32(1),'#interrupt-cells':u32(4),
                    'reg':u64(0xc000000,0x40000,0xc040000,0x200000)}),
        node('timer',{'compatible':b'arm,armv8-timer\0','clock-frequency':u32(13000000),
                      'interrupts':u32(1,13,4,0,1,14,4,0,1,11,4,0,1,10,4,0)}),
        node('psci',{'compatible':b'arm,psci-1.0\0','method':b'smc\0'}),
        node('chosen',{'linux,initrd-start':u32(0x66f00000),'linux,initrd-end':u32(0x69509a70),
                        'serial-number':b'PRIVATE-SERIAL-MUST-NOT-COPY\0','bootargs':b'private-android-args\0'}),
        node('reserved-memory',{'#address-cells':u32(2),'#size-cells':u32(2),'ranges':b''},[
            node('pstore',{'compatible':b'mediatek,pstore\0','reg':u64(0x48090000,0xe0000),'no-map':b''}),
            node('firmware',{'reg':u64(0x138000000,0x8000000)}),
            node('reserve-memory-vcp_share',{'compatible':b'mediatek,reserve-memory-vcp_share\0',
                'no-map':b'','size':u64(0x201000),'alignment':u64(0x1000000),
                'alloc-ranges':u64(0x50000000,0x40000000)}),
            *[node(name.rsplit('/',1)[1],{'compatible':b'shared-dma-pool\0','reusable':b'',
                'size':u64(size),'alignment':u64(align)}) for name,(size,align) in tool.CMA.items()]])])


def ufs_fixture():
    root=fixture()
    soc=node('soc',{'#address-cells':u32(2),'#size-cells':u32(2),'ranges':b''},[
        node('ufshci@112b0000',{'compatible':b'mediatek,mt8183-ufshci\0',
            'reg':u64(0x112b0000,0x2300),'interrupts':u32(0,137,4,0)})])
    soc.parent=root;root.children.append(soc)
    return root


def pack(root,reservations=()):
    strings,body=bytearray(),bytearray(); offsets={}
    def visit(n):
        body.extend(u32(1)+n.name.encode()+b'\0');body.extend(b'\0'*(-len(body)%4))
        for name,value in n.props.items():
            if name not in offsets:offsets[name]=len(strings);strings.extend(name.encode()+b'\0')
            body.extend(u32(3,len(value),offsets[name])+value);body.extend(b'\0'*(-len(body)%4))
        for child in n.children:visit(child)
        body.extend(u32(2))
    visit(root);body.extend(u32(9));r=b''.join(u64(*x) for x in reservations)+u64(0,0)
    st=40+len(r);ss=st+len(body)
    return u32(0xd00dfeed,ss+len(strings),st,ss,40,17,16,0,len(strings),len(body))+r+body+strings


def build(root=None,**changes):
    policy=dict(ram_base=0x140000000,ram_size=0x40000000,fdt_pa=0x47c80000,
                loader_ranges=[('loader',0x40000000,0x4000000)],boot_affinity=0,cold_native=True,seed=bytes(range(64)))
    policy.update(changes)
    return tool.build(pack(root or fixture()),**policy)


class AceAdtTests(unittest.TestCase):
    def test_target_tree_matches_ace_registry_and_omits_unknown_or_private_data(self):
        blob,report=build();root,end=adt.parse(blob);self.assertEqual(end,len(blob))
        props={n.name:n for n in root.children};cpu=props['cpus'].children
        self.assertEqual(len(cpu),1);self.assertIn(b'ace,armv8-cpu\0',cpu[0].prop('compatible'))
        self.assertEqual(cpu[0].prop('reg'),struct.pack('<I',0))
        for key in ('bus-frequency','memory-frequency','peripheral-frequency'):self.assertIsNone(cpu[0].prop(key))
        self.assertEqual(cpu[0].prop('timebase-frequency'),struct.pack('<I',13000000))
        self.assertEqual(len(report['linux_cma_not_instantiated']),2)
        self.assertFalse(report['hardware_ram_ownership_verified']);self.assertFalse(report['ios_deployable'])
        for word in (b'PRIVATE-SERIAL',b'private-android-args',b'qcom,',b'sweet-fbcon',b'sweet-ufs',b'D22AP'):
            self.assertNotIn(word,blob)
        self.assertEqual(blob,build()[0])

    def test_root_discovery_is_explicit_and_requires_command_reads(self):
        for args in ({'ufs_root':True},{'ufs_root':True,'ufs_probe':True},{'ufs_root':1,'ufs_read':True}):
            with self.assertRaises(ValueError):build(ufs_fixture(),**args)
        blob,report=build(ufs_fixture(),ufs_read=True,ufs_root=True)
        root,_=adt.parse(blob)
        self.assertEqual(root.children[-1].prop('ace,root-read-probe'),struct.pack('<I',1))
        self.assertIn('0113',report['required_xnu_patches'])
        self.assertTrue(report['ufs_root_discovery_probe'])
        ordinary,report=build(ufs_fixture(),ufs_read=True)
        tree,_=adt.parse(ordinary)
        self.assertIsNone(tree.children[-1].prop('ace,root-read-probe'))
        self.assertFalse(report['ufs_root_discovery_probe'])

    def test_opt_in_ufs_probe_uses_absolute_root_resources(self):
        source=ufs_fixture();old=build(source)[0]
        self.assertEqual(old,build()[0])
        blob,manifest=build(source,ufs_probe=True);root,_=adt.parse(blob)
        probe=root.children[-1]
        self.assertEqual(probe.name,'ace-ufs')
        self.assertEqual(probe.prop('reg'),struct.pack('<QQ',0x112b0000,0x2300))
        self.assertEqual(probe.prop('interrupt-intid'),struct.pack('<I',169))
        self.assertTrue(manifest['ufs_read_only_probe'])
        self.assertIn('0090',manifest['required_xnu_patches'])
        with self.assertRaises(ValueError):build(ufs_probe=True)
        with self.assertRaises(ValueError):build(source,ufs_probe=1)

    def test_ufs_probe_refuses_changed_resources_and_duplicate_controller(self):
        for path,key,value in [('/soc','ranges',u64(0,0x10000000,0x10000000)),
            ('/soc','status',b'disabled\0'),('/soc','#address-cells',u32(1)),
            ('/soc/ufshci@112b0000','reg',u64(0x112b0000,0x2000)),
            ('/soc/ufshci@112b0000','interrupts',u32(0,138,4,0)),
            ('/soc/ufshci@112b0000','interrupt-parent',u32(999)),
            ('/soc/ufshci@112b0000','status',b'disabled\0'),
            ('/soc/ufshci@112b0000','interrupts-extended',u32(1,0,137,4,0))]:
            root=ufs_fixture();fdt.Tree(root,[],0).by_path(path).props[key]=value
            with self.subTest(path=path,key=key),self.assertRaises(ValueError):build(root,ufs_probe=True)
        root=ufs_fixture();root.children.append(node('duplicate',{'compatible':b'mediatek,mt8183-ufshci\0'}))
        with self.assertRaises(ValueError):build(root,ufs_probe=True)

    def test_explicit_stage_boot_cpu_ranges_alignment_and_entropy_are_required(self):
        for changes in ({'cold_native':False},{'boot_affinity':0x100},{'loader_ranges':[]},
                        {'ram_base':0x140004000},{'ram_size':0x40004000},
                        {'ram_base':0x240000000},{'ram_base':1<<40},
                        {'seed':b'x'*63},{'fdt_pa':0},{'loader_ranges':[('loader',0,0x1000)]}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):build(**changes)

    def test_fixed_loader_fdt_initrd_and_bounded_dynamic_exclusions_cover_whole_ram(self):
        for changes in ({'ram_base':0x50000000,'ram_size':0x2000000},
                        {'loader_ranges':[('loader',0x15fffffff,2)]},
                        {'fdt_pa':0x140000000}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):build(**changes)
        root=fixture();fdt.Tree(root,[],0).by_path('/chosen').props.update({
            'linux,initrd-start':u64(0x140000000),'linux,initrd-end':u64(0x140100000)})
        with self.assertRaises(ValueError):build(root)
        self.assertEqual(build()[1]['requested_ram']['base'],0x140000000)  # adjacent fixed range ends here

    def test_header_memreserve_and_new_unbounded_dynamic_node_are_not_ignored(self):
        root=fixture();policy=dict(ram_base=0x140000000,ram_size=0x40000000,fdt_pa=0x47c80000,
            loader_ranges=[('loader',0x40000000,0x4000000)],boot_affinity=0,cold_native=True)
        with self.assertRaises(ValueError):tool.build(pack(root,[(0x140000000,1)]),**policy)
        reserved=fdt.Tree(root,[],0).by_path('/reserved-memory')
        extra=node('unknown',{'size':u64(0x100000)});extra.parent=reserved;reserved.children.append(extra)
        with self.assertRaises(ValueError):build(root)

    def test_known_cma_cannot_bypass_changed_declarations(self):
        for key,value in [('size',u64(1)),('alignment',u64(4096)),('no-map',b''),('alloc-ranges',u64(0,1)),('firmware-owned',b'')]:
            root=fixture();fdt.Tree(root,[],0).by_path(next(iter(tool.CMA))).props[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):build(root)

    def test_hardware_mismatch_and_missing_pstore_are_rejected(self):
        for path,key,value in [('/gic','reg',u64(0x8000000,0x10000,0x80a0000,0x100000)),
            ('/timer','clock-frequency',u32(24000000)),('/psci','method',b'hvc\0'),
            ('/cpus/cpu@000','clock-frequency',u32(0)),('/cpus/cpu@000','reg',u32(1)),
            ('/reserved-memory/pstore','compatible',b'wrong\0'),('/reserved-memory/firmware','reg',b''),('/gic','status',b'disabled\0')]:
            root=fixture();fdt.Tree(root,[],0).by_path(path).props[key]=value
            with self.subTest(path=path,key=key),self.assertRaises(ValueError):build(root)

    def test_cli_candidate_is_exclusive_and_failure_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);source=base/'source.dtb';source.write_bytes(pack(fixture()));out=base/'output'
            args=[sys.executable,str(ROOT/'tools/ace-mkadt.py'),str(source),str(out),
                '--ram-base','0x140000000','--ram-size','0x40000000','--fdt-pa','0x47c80000',
                '--boot-affinity','0','--reserve','loader:0x40000000:0x4000000']
            failed=subprocess.run(args,capture_output=True,text=True);self.assertNotEqual(failed.returncode,0);self.assertFalse(out.exists())
            result=subprocess.run(args+['--cold-native'],capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
            old=(out/'ace.adt').read_bytes();again=subprocess.run(args+['--cold-native'],capture_output=True,text=True)
            self.assertNotEqual(again.returncode,0);self.assertEqual((out/'ace.adt').read_bytes(),old)
            self.assertFalse(json.loads((out/'manifest.json').read_text())['ios_deployable'])


@unittest.skipUnless(BASE.is_dir() and shutil.which('clang'),'actual cached XNU and compiler required')
class ActualXnuConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.base=Path(cls.tmp.name)
        path=cls.base/'pexpert/arm';path.mkdir(parents=True)
        shutil.copyfile(BASE/'pexpert/arm/pe_identify_machine.c',path/'pe_identify_machine.c')
        result=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(ROOT/'xnu/patches/0085-ace-clock-without-invented-bus.patch')],cwd=cls.base,capture_output=True,text=True)
        if result.returncode:raise AssertionError(result.stdout+result.stderr)
        header=(BASE/'pexpert/pexpert/device_tree.h').read_text();parser=(BASE/'pexpert/gen/device_tree.c').read_text()
        clock=(path/'pe_identify_machine.c').read_text();pe=(BASE/'pexpert/pexpert/pexpert.h').read_text()
        remove=lambda s:'\n'.join(l for l in s.splitlines() if not l.startswith('#include'))
        def function(name):
            match=re.search(r'(?:void|vm_offset_t)\n'+name+r'\(',clock);start=match.start()
            brace=clock.index('{',start);depth=1;i=brace+1
            while depth:depth+=(clock[i]=='{')-(clock[i]=='}');i+=1
            return clock[start:i]
        struct_text=re.search(r'struct clock_frequency_info_t \{.*?\n\};',pe,re.S).group()
        source=(ROOT/'tests/fixtures/ace_adt_xnu.c').read_text()
        source=source.replace('/* INSERT_DT_HEADER */','#define __APPLE_API_PRIVATE 1\n'+remove(header))
        source=source.replace('/* INSERT_DT_PARSER */',remove(parser))
        source=source.replace('/* INSERT_CLOCK_STRUCT */',struct_text+'\ntypedef struct clock_frequency_info_t clock_frequency_info_t;')
        source=source.replace('/* INSERT_CLOCK_FUNCTIONS */',function('pe_identify_machine')+'\n'+function('pe_arm_get_soc_base_phys'))
        cfile=cls.base/'consumer.c';cfile.write_text(source);lib=cls.base/'consumer.so'
        result=subprocess.run(['clang','-std=c11','-O2','-DARM64_BOARD_CONFIG_ACE','-shared','-fPIC',str(cfile),'-o',str(lib)],capture_output=True,text=True)
        if result.returncode:raise AssertionError(result.stderr)
        cls.lib=c.CDLL(str(lib));cls.lib.test_xnu_clocks.argtypes=[c.c_void_p,c.c_size_t,c.c_uint64,c.POINTER(c.c_uint64)]
        cls.lib.test_xnu_property.argtypes=[c.c_void_p,c.c_size_t,c.c_char_p,c.c_char_p,c.c_void_p,c.c_uint]
        wrapper=cls.base/'handoff.c'
        wrapper.write_text('''#include "xnu_handoff.h"
int test_plan(const void *b, size_t n, uint64_t base, uint64_t bytes,
              const struct ace_xnu_range *reserved, size_t count, uint64_t *out) {
    struct ace_xnu_policy policy={{base,bytes},{0x42000000,n},reserved,count};
    struct ace_xnu_plan plan;
    int rc=ace_xnu_prepare(b,n,&policy,&plan);
    if(rc) return rc;
    out[0]=plan.args.phys_base; out[1]=plan.args.mem_size;
    out[2]=plan.adt_pa; out[3]=plan.args.device_tree;
    out[4]=plan.args.device_tree_length; out[5]=plan.args.top_of_kernel_data;
    return 0;
}
''')
        library=cls.base/'handoff.so'
        result=subprocess.run(['clang','-std=c11','-O2','-shared','-fPIC','-I',str(ROOT/'ace'),
            str(ROOT/'ace/xnu_handoff.c'),str(wrapper),'-o',str(library)],capture_output=True,text=True)
        if result.returncode:raise AssertionError(result.stderr)
        cls.handoff=c.CDLL(str(library))
        cls.handoff.test_plan.argtypes=[c.c_void_p,c.c_size_t,c.c_uint64,c.c_uint64,c.c_void_p,c.c_size_t,c.POINTER(c.c_uint64)]

    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()

    def clocks(self,blob,counter=13000000):
        data=c.create_string_buffer(blob);out=(c.c_uint64*8)();rc=self.lib.test_xnu_clocks(data,len(blob),counter,out)
        return rc,list(out)

    def test_generated_tree_agrees_with_native_flat_loader_bootargs_and_exclusions(self):
        for memory_bytes in (0x40000000,0xc0000000):
            blob,report=build(ram_size=memory_bytes);va=0xfffffe0006000000
            payload=bytearray(728+len(blob));payload[728:]=blob
            struct.pack_into('<8sII7Q',payload,0,b'ACEXNU01',1,1,va,va+0x10000,
                             728,len(blob),va+0x14000,0x140000000,memory_bytes)
            struct.pack_into('<4Q',payload,680,va+0x10000,4,720,4)
            payload[720:724]=bytes.fromhex('1f2003d5')
            class Range(c.Structure):_fields_=[('base',c.c_uint64),('size',c.c_uint64)]
            reserved=(Range*len(report['excluded_ranges']))(*[Range(x['base'],x['size']) for x in report['excluded_ranges']])
            storage=c.create_string_buffer(bytes(payload));values=(c.c_uint64*6)()
            rc=self.handoff.test_plan(storage,len(payload),report['requested_ram']['base'],
                report['requested_ram']['size'],reserved,len(reserved),values)
            self.assertEqual(rc,0)
            self.assertEqual(list(values),[0x140000000,memory_bytes,0x140014000,va+0x14000,len(blob),0x14001c000])
            source=c.create_string_buffer(blob);buffer=c.create_string_buffer(8)
            for name,value in [(b'dram-base',values[0]),(b'dram-size',values[1])]:
                self.assertEqual(self.lib.test_xnu_property(source,len(blob),b'/chosen',name,buffer,8),8)
                self.assertEqual(struct.unpack('<Q',buffer.raw)[0],value)

    def test_actual_xnu_parser_and_clock_path_accept_generated_tree_without_bus_division(self):
        self.assertEqual(self.clocks(build()[0]),(0,[0xc000000,13000000,1701000000,0,0,1,0,1]))

    def test_actual_xnu_parser_finds_exact_gic_and_pmsg_bytes(self):
        blob=build()[0];storage=c.create_string_buffer(blob);buf=c.create_string_buffer(128)
        for path,key,expected in [(b'/arm-io/gic',b'reg',struct.pack('<4Q',0,0x40000,0x40000,0x200000)),
            (b'/chosen/ace-pmsg',b'reg',struct.pack('<2Q',0x48160000,0x10000))]:
            rc=self.lib.test_xnu_property(storage,len(blob),path,key,buf,len(buf))
            self.assertEqual(rc,len(expected));self.assertEqual(buf.raw[:rc],expected)

    def test_counter_mismatch_or_absent_timebase_is_refused_by_real_clock_code(self):
        blob=build()[0];self.assertEqual(self.clocks(blob,24000000)[0],-1)
        tree,_=adt.parse(blob);cpus=next(n for n in tree.children if n.name=='cpus')
        cpus.children[0].props=[p for p in cpus.children[0].props if p[0]!='timebase-frequency']
        self.assertEqual(self.clocks(adt.serialize(tree))[0],-1)

    def test_actual_clock_path_preserves_known_bus_ratio_when_present(self):
        tree,_=adt.parse(build()[0]);cpus=next(n for n in tree.children if n.name=='cpus')
        cpus.children[0].props.append(('bus-frequency',0,struct.pack('<I',100000000)))
        self.assertEqual(self.clocks(adt.serialize(tree)),(0,[0xc000000,13000000,1701000000,100000000,34,2,1,7]))


if __name__=='__main__':unittest.main()
