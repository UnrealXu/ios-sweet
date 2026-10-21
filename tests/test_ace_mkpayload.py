import ctypes as c
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import test_ace_mkadt as trees
spec=importlib.util.spec_from_file_location('ace_mkpayload',ROOT/'tools/ace-mkpayload.py')
tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
VA=0xfffffe0007000000


def fixture():
    # Synthetic linked arm64 Mach-O, not XNU. Header, executable and BSS tails.
    text=struct.pack('<II16s4Q4I',0x19,72,b'__TEXT',VA,0x4000,0,0x400,5,5,0,0)
    data=struct.pack('<II16s4Q4I',0x19,72,b'__DATA',VA+0x4000,0x4000,0x400,13,3,3,0,0)
    thread=bytearray(288);struct.pack_into('<4I',thread,0,5,288,6,68)
    struct.pack_into('<Q',thread,16+32*8,VA+0x300)
    commands=text+data+thread
    b=bytearray(0x40d);struct.pack_into('<8I',b,0,0xfeedfacf,0x100000c,0,2,3,len(commands),1,0)
    b[32:32+len(commands)]=commands;b[0x300:0x304]=bytes.fromhex('1f2003d5');b[0x400:]=b'tail-13-bytes'
    return b


def make(kernel=None,tree=None,manifest=None,line='debug=0xc cpus=1'):
    blob,report=trees.build()
    return tool.build(bytes(fixture() if kernel is None else kernel),blob if tree is None else tree,
                      report if manifest is None else manifest,line)


def local_fixture():
    b=fixture();text=bytearray(b[32:104])
    struct.pack_into('<I',text,4,152);struct.pack_into('<I',text,64,1)
    section=struct.pack('<16s16sQQ8I',b'__text',b'__TEXT',VA+0x300,4,0x300,2,0,0,0,0,0,0)
    link=struct.pack('<II16s4Q4I',0x19,72,b'__LINKEDIT',VA+0x8000,0x4000,0x1000,8,1,1,0,0)
    fields=[0]*18;fields[16:]=[0x1000,1]
    dysym=struct.pack('<20I',0xb,80,*fields)
    commands=text+section+b[104:176]+link+b[176:464]+dysym
    b.extend(bytes(0x1008-len(b)));struct.pack_into('<II',b,16,5,len(commands));b[32:32+len(commands)]=commands
    struct.pack_into('<Q',b,0x400,VA+0x300);struct.pack_into('<iI',b,0x1000,0x4000,0x06000001)
    return b


class AcePayloadTests(unittest.TestCase):
    def test_root_discovery_policy_and_actual_tree_must_agree(self):
        tree,manifest=trees.build(trees.ufs_fixture(),ufs_read=True,ufs_root=True)
        tool.build(bytes(fixture()),tree,manifest,'debug=0xc')
        for key,value in [('ufs_root_discovery_probe',1),('ufs_command_read_probe',False),
                          ('required_xnu_patches',manifest['required_xnu_patches'][:-1])]:
            changed=dict(manifest);changed[key]=value
            with self.assertRaises(ValueError):tool.build(bytes(fixture()),tree,changed,'debug=0xc')
        changed=dict(manifest);changed['ufs_root_discovery_probe']=False
        changed['required_xnu_patches']=manifest['required_xnu_patches'][:-1]
        with self.assertRaises(ValueError):tool.build(bytes(fixture()),tree,changed,'debug=0xc')
        plain,_=trees.build(trees.ufs_fixture(),ufs_read=True)
        changed=dict(manifest);changed['adt_sha256']=tool.sha(plain)
        with self.assertRaises(ValueError):tool.build(bytes(fixture()),plain,changed,'debug=0xc')

    def test_zero_slide_local_relocations_preserve_resolved_bytes_and_reject_other_encodings(self):
        kernel=local_fixture();blob,report=make(kernel)
        data=next(s for s in report['segments'] if s['name']=='__DATA')
        _,_,off,size=struct.unpack_from('<4Q',blob,680+32)
        self.assertEqual(blob[off:off+size],kernel[data['fileoff']:data['fileoff']+size])
        for address,bits in [(0x4000,0x16000001),(0x4000,0x0e000001),(-1,0x06000001),
                             (0x4000,0x07000001),(0x4000,0x06000002),(0x4008,0x06000001)]:
            changed=bytearray(kernel);struct.pack_into('<iI',changed,0x1000,address,bits)
            with self.assertRaises(ValueError):make(changed)
        changed=bytearray(kernel);struct.pack_into('<Q',changed,0x400,0x1234)
        with self.assertRaises(ValueError):make(changed)
        changed=bytearray(kernel);changed[32+72:32+88]=b'__thread_starts'.ljust(16,b'\0')
        with self.assertRaises(ValueError):make(changed)  # nonempty __thread_starts

    def test_real_native_prepare_accepts_generated_bundle_and_64bit_addresses(self):
        if not shutil.which('clang'):self.skipTest('clang required')
        with tempfile.TemporaryDirectory() as d:
            lib=Path(d)/'loader.so'
            subprocess.run(['clang','-shared','-fPIC','-O2',str(ROOT/'ace/xnu_handoff.c'),'-o',str(lib)],check=True)
            native=c.CDLL(str(lib))
            class Range(c.Structure):_fields_=[('base',c.c_uint64),('size',c.c_uint64)]
            class Policy(c.Structure):_fields_=[('ram',Range),('source',Range),('reserved',c.POINTER(Range)),('count',c.c_size_t)]
            native.ace_xnu_prepare.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.c_void_p]
            blob,manifest=make();self.assertEqual(blob[:8],b'ACEXNU01');self.assertFalse(manifest['ios_deployable'])
            source=c.create_string_buffer(blob);out=c.create_string_buffer(4096)
            policy=Policy(Range(0x140000000,0x40000000),Range(0x42000000,len(blob)),None,0)
            self.assertEqual(native.ace_xnu_prepare(source,len(blob),c.byref(policy),out),0)
            args=struct.unpack_from('<4Q',out.raw,8)
            self.assertEqual(args,(VA&~0x1ffffff,0x140000000,0x40000000,manifest['top_of_kernel_data']))
            for index in range(2):
                va,n,off,size=struct.unpack_from('<4Q',blob,680+index*32)
                expected=fixture()[:0x400] if index==0 else b'tail-13-bytes'
                self.assertEqual(blob[off:off+size],expected)
            self.assertEqual(manifest['entry_pa'],0x141000300)

    def test_rejects_header_architecture_commands_and_truncations(self):
        for offset,value in [(0,0xfeedface),(4,0x1000007),(8,2),(12,12),(28,1),(16,4097),(20,8),(24,0),(32+4,7),(32+4,0xfffffff8)]:
            with self.subTest(offset=offset,value=value):
                b=fixture();struct.pack_into('<I',b,offset,value)
                with self.assertRaises(ValueError):make(b)
        for size in (0,31,39,100,0x400):
            with self.assertRaises(ValueError):make(fixture()[:size])
        for cmd in (0x80000034,0x22,0x80000022,0x80000028,0xc,0x21,0x2c):
            b=fixture();struct.pack_into('<I',b,32,cmd)
            with self.assertRaises(ValueError):make(b)

    def test_rejects_segment_alias_overflow_bad_entry_and_oversized_line(self):
        changes=[(32+24,VA+1),(32+32,2**64-1),(32+40,0x100000),(32+48,0x500),
                 (32+72+24,VA),(32+72+40,0x300),(32+72+4,80)]
        for offset,value in changes:
            b=fixture();struct.pack_into('<Q',b,offset,value)
            with self.assertRaises(ValueError):make(b)
        for entry in (VA+1,VA+0x4000,VA+0x400c,VA+0x8000):
            b=fixture();struct.pack_into('<Q',b,32+144+16+256,entry)
            with self.assertRaises(ValueError):make(b)
        for line in ('a'*608,'debug=0\0-v','中文'):
            with self.assertRaises((ValueError,UnicodeError)):make(line=line)

    def test_adt_manifest_tampering_malformed_tree_and_memory_exclusion_refuse(self):
        blob,manifest=trees.build()
        for key,value in [('target','SWEET'),('adt_sha256','0'*64),('cold_native_only',False),('required_xnu_patches',[])]:
            changed=dict(manifest);changed[key]=value
            with self.assertRaises(ValueError):make(manifest=changed)
        for bad in (blob[:-1],bytes([255])*len(blob),blob+b'\0'):
            changed=dict(manifest);changed['adt_sha256']=tool.sha(bad)
            with self.assertRaises((ValueError,UnicodeError)):make(tree=bad,manifest=changed)
        changed=dict(manifest);changed['requested_ram']={'base':0x140000000,'size':0x80000000}
        with self.assertRaises(ValueError):make(manifest=changed)
        changed=dict(manifest);changed['excluded_ranges']=[{'base':0x140000000,'size':0x1000}]
        with self.assertRaises(ValueError):make(manifest=changed)
        changed=dict(manifest);changed['excluded_ranges']=[]
        with self.assertRaises(ValueError):make(manifest=changed)

    def test_cli_exclusive_output_and_optimized_python_still_validate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'kernel').write_bytes(fixture());(root/'adt').mkdir()
            tree,manifest=trees.build();(root/'adt/ace.adt').write_bytes(tree)
            (root/'adt/manifest.json').write_text(json.dumps(manifest))
            cmd=[sys.executable,'-O',str(ROOT/'tools/ace-mkpayload.py'),str(root/'kernel'),str(root/'adt'),str(root/'out')]
            result=subprocess.run(cmd,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
            old=(root/'out/ace.payload').read_bytes()
            self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.assertEqual((root/'out/ace.payload').read_bytes(),old)
            (root/'kernel').write_bytes(b'BAD')
            cmd[-1]=str(root/'bad');self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0)
            self.assertFalse((root/'bad').exists())

    def test_actual_cached_linked_kernel_format_and_original_bytes(self):
        path=ROOT/'research/ci-0081/xnu-kernel-0081.zip'
        if not path.exists():self.skipTest('actual cached linked kernel unavailable')
        with zipfile.ZipFile(path) as archive:kernel=archive.read('kernel.development.sweet')
        blob,manifest=make(kernel)
        # A format regression using SWEET, explicitly not an ACE kernel/boot.
        self.assertFalse(manifest['kernel_ace_platform_verified'])
        self.assertFalse(manifest['ios_deployable'])
        for i,segment in enumerate(manifest['segments']):
            _,memory,off,size=struct.unpack_from('<4Q',blob,680+i*32)
            self.assertEqual((memory,size),(segment['memory'],segment['files']))
            self.assertEqual(blob[off:off+size],kernel[segment['fileoff']:segment['fileoff']+size])


if __name__=='__main__':unittest.main()
