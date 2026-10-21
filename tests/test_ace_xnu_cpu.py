"""CPU admission before real bounded materialization; no phone execution."""
import ctypes as c
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from test_ace_xnu_handoff import Range, Policy, Plan, bundle, BASE, SIZE

ROOT=Path(__file__).resolve().parents[1]

class State(c.Structure):
    _fields_=[(n,c.c_uint64) for n in ('el','sctlr','midr','mpidr','mmfr0','cntfrq','daif')]

def ready():
    # Explicit HOST fixture. These values combine cold-entry and Android
    # observations plus masked DAIF, NOT a complete captured native snapshot.
    return State(4,0x30d00800,0x412fd050,0x81000000,0x101122,13000000,0x3c0)

class AceXnuCpuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(); cls.d=Path(cls.tmp.name)
        lib=cls.d/'cpu.so'
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror',
            '-fno-builtin','-shared','-fPIC',str(ROOT/'ace/xnu_cpu.c'),
            str(ROOT/'ace/xnu_handoff.c'),'-o',str(lib)],check=True)
        cls.lib=c.CDLL(str(lib))
        cls.lib.ace_xnu_cpu_check.argtypes=[c.POINTER(State)]
        cls.lib.ace_xnu_prepare_cpu.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.POINTER(State),c.POINTER(Plan)]
        cls.lib.ace_xnu_materialize_cpu.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.POINTER(State),c.c_void_p,c.c_size_t,c.POINTER(Plan)]
    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()

    def test_runtime_admission_before_destination_store(self):
        bad=[('el',0,-17),('el',8,-17),('el',12,-17),
             ('sctlr',0x30d00801,-18),('sctlr',0x30d00804,-18),
             ('sctlr',0x30d01800,-18),('sctlr',0x32d00800,-18),
             ('midr',0x411fd411,-19),('midr',0x1412fd050,-19),
             ('mpidr',0x81000100,-20),('mpidr',0x81000001,-20),
             ('mpidr',0x10081000000,-20),('mmfr0',0x122,-21),
             ('mmfr0',0x101121,-21),('mmfr0',0x101127,-21),
             ('mmfr0',0x201122,-21),('cntfrq',24000000,-22),('daif',0,-23)]
        raw=bytes(bundle()); buf=c.create_string_buffer(raw)
        p=Policy(Range(BASE,SIZE),Range(0x90000000,len(raw)),None,0)
        for field,value,expected in bad:
            with self.subTest(field=field,value=hex(value)):
                state=ready();setattr(state,field,value)
                ram=(c.c_ubyte*SIZE)();c.memset(ram,0xa5,SIZE)
                out=Plan();c.memset(c.byref(out),0x5a,c.sizeof(out))
                rc=self.lib.ace_xnu_materialize_cpu(buf,len(raw),c.byref(p),c.byref(state),ram,SIZE,c.byref(out))
                self.assertEqual(rc,expected)
                self.assertEqual(bytes(ram),b'\xa5'*SIZE)
                self.assertEqual(bytes(out),b'\x5a'*c.sizeof(out))
                self.assertEqual(self.lib.ace_xnu_prepare_cpu(buf,len(raw),c.byref(p),c.byref(state),c.byref(out)),expected)
                self.assertEqual(bytes(out),b'\x5a'*c.sizeof(out))

    def test_ready_fixture_reaches_same_materializer_and_keeps_range_checks(self):
        raw=bytes(bundle());buf=c.create_string_buffer(raw);state=ready()
        p=Policy(Range(BASE,SIZE),Range(0x90000000,len(raw)),None,0)
        ram=(c.c_ubyte*SIZE)();out=Plan()
        self.assertEqual(self.lib.ace_xnu_materialize_cpu(buf,len(raw),c.byref(p),c.byref(state),ram,SIZE,c.byref(out)),0)
        self.assertEqual(bytes(ram[:32]),b'hello-kernel!'+bytes(19))
        self.assertEqual(out.entry,BASE)
        p.source=Range(BASE,len(raw))
        self.assertEqual(self.lib.ace_xnu_prepare_cpu(buf,len(raw),c.byref(p),c.byref(state),c.byref(out)),-4)
        p.ram=Range((1<<40)-0x4000,0x8000)
        self.assertEqual(self.lib.ace_xnu_prepare_cpu(buf,len(raw),c.byref(p),c.byref(state),c.byref(out)),-3)

    def test_arguments_revisions_and_full_affinity(self):
        self.assertEqual(self.lib.ace_xnu_cpu_check(None),-16)
        for revision in range(16):
            s=ready();s.midr=0x410fd050|revision
            self.assertEqual(self.lib.ace_xnu_cpu_check(c.byref(s)),0)
        for bit in (0,8,16,32):
            s=ready();s.mpidr|=1<<bit
            self.assertEqual(self.lib.ace_xnu_cpu_check(c.byref(s)),-20)

    def test_saved_real_observations_are_partial_and_android_is_not_cold_boot(self):
        irq=ROOT/'research/ace-irq-timer-live-20261019/phone-run1/result-verified.json'
        boot=ROOT/'research/ace-stock-chain-20261019/phone-test1/normal-reboot2/result-verified.json'
        if not irq.exists() or not boot.exists():self.skipTest('private phone captures absent')
        samples=json.loads(irq.read_text())['samples']
        prefix=json.loads(boot.read_text())['hardware_prefix_record']
        self.assertEqual(prefix['active_sctlr'],'0x30d00800')
        self.assertEqual(prefix['midr'],'0x412fd050')
        self.assertEqual(prefix['mmfr0'],'0x101122')
        for i,sample in enumerate(samples):
            self.assertEqual(sample['mpidr'] & 0xff00ffffff,i<<8)
            s=ready();s.el=sample['el']<<2;s.mpidr=sample['mpidr']
            s.daif=sample['daif'];s.cntfrq=sample['freq']
            self.assertEqual(self.lib.ace_xnu_cpu_check(c.byref(s)),-23 if i==0 else -20)

    @unittest.skipUnless(shutil.which('aarch64-linux-gnu-gcc'),'cross compiler absent')
    def test_freestanding_a55_objects_have_no_unexpected_runtime_or_state_write(self):
        objs=[]
        for name in ('xnu_cpu.c','xnu_cpu_capture.S','xnu_handoff.c'):
            out=self.d/(name+'.o');objs.append(str(out))
            subprocess.run(['aarch64-linux-gnu-gcc','-mcpu=cortex-a55','-ffreestanding',
                '-fno-builtin','-fno-stack-protector','-mgeneral-regs-only','-O2',
                '-Wall','-Wextra','-Werror','-c',str(ROOT/'ace'/name),'-o',str(out)],check=True)
        linked=self.d/'cpu-linked.o'
        subprocess.run(['aarch64-linux-gnu-ld','-r',*objs,'-o',str(linked)],check=True)
        self.assertEqual(subprocess.check_output(['aarch64-linux-gnu-nm','-u',str(linked)],text=True),'')
        asm=subprocess.check_output(['aarch64-linux-gnu-objdump','-d',str(self.d/'xnu_cpu_capture.S.o')],text=True)
        for forbidden in ('\tmsr\t','\tsmc\t','\thvc\t','\tbl\t'):
            self.assertNotIn(forbidden,asm)
        for reg in ('currentel','sctlr_el1','sctlr_el2','midr_el1','mpidr_el1','id_aa64mmfr0_el1','cntfrq_el0','daif'):
            self.assertIn(reg,asm.lower())

if __name__=='__main__':unittest.main()
