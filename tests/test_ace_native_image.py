"""Native Image input refusal and actual built-artifact embedding checks."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('native_build',ROOT/'tools/ace-mknative.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class NativeImageTests(unittest.TestCase):
    def test_bsd_root_requires_explicit_name_and_automatic_recovery(self):
        for options in [dict(root_device='userdata'),dict(root_device='aceufsroot0'),
                        dict(root_device='aceufsroot0',pmsg=True)]:
            with self.assertRaises(ValueError):
                builder.build('absent','absent',ROOT/'research/root-no-output','0'*64,0x47c80000,**options)
        self.assertFalse((ROOT/'research/root-no-output').exists())
    def test_auto_reset_requires_logged_android_path(self):
        for opts in [dict(auto_readout_after_reset=True),dict(auto_readout_after_reset=1),
            dict(auto_readout_after_reset=True,pmsg=True),
            dict(auto_readout_after_reset=True,pmsg=True,refusal_android='absent',diagnostic_readout=True)]:
            with self.assertRaises(ValueError):
                builder.build('absent','absent',ROOT/'research/auto-no-output','0'*64,0x47c80000,**opts)
        self.assertFalse((ROOT/'research/auto-no-output').exists())
    def test_readout_requires_android_and_never_combines_with_seed(self):
        for options in [dict(diagnostic_readout=True),dict(diagnostic_readout=1),
            dict(diagnostic_readout=True,refusal_android='absent',init_empty_pmsg=True,pmsg=True)]:
            with self.assertRaises(ValueError):
                builder.build('absent','absent',ROOT/'research/readout-no-output','0'*64,0x47c80000,**options)
        self.assertFalse((ROOT/'research/readout-no-output').exists())
        for token in ['', 'A'*16, '0'*15, '0'*17, 'x;quit', True]:
            with self.assertRaises(ValueError):
                builder.build('absent','absent',ROOT/'research/readout-no-output','0'*64,0x47c80000,
                    text_offset=0,diagnostic_readout=True,refusal_android='absent',
                    expected_android=builder.REFUSAL_ANDROID_SHA,prior_run_token=token)
    def test_empty_ring_initialization_requires_explicit_logging_before_io(self):
        for flag,pmsg in [(True,False),(1,True),('yes',True)]:
            with self.assertRaises(ValueError):
                builder.build('absent','absent',ROOT/'research/seed-no-output','0'*64,0x47c80000,pmsg=pmsg,init_empty_pmsg=flag)
        self.assertFalse((ROOT/'research/seed-no-output').exists())
    def test_optional_android_requires_exact_known_image_pair_and_alignment_before_output(self):
        out=ROOT/'research/refusal-no-output'
        for options in [dict(refusal_android='absent'),dict(expected_android='0'*64),
            dict(refusal_android='absent',expected_android=builder.REFUSAL_ANDROID_SHA)]:
            with self.subTest(options=options),self.assertRaises(ValueError):
                builder.build('absent','absent',out,'0'*64,0x47c80000,**options)
        self.assertFalse(out.exists())
    def test_run_token_rejects_unbounded_or_nonhex_input_before_output(self):
        for token in ('', 'A'*16, '0'*15, '0'*17, 'x;quit', True):
            with self.subTest(token=token), self.assertRaises(ValueError):
                builder.build('absent','absent',ROOT/'research/token-no-output','0'*64,0x47c80000,True,run_token=token)
        self.assertFalse((ROOT/'research/token-no-output').exists())
    def test_debugger_numeric_operands_cannot_contain_commands_or_booleans(self):
        spec=importlib.util.spec_from_file_location('native_verify',ROOT/'ace/native-loader/verify.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        original=dict(fdt_pa=0x47c80000,text_offset=0x80000,entry_pa=0x140000000,
            args_pa=0x140008000,adt_pa=0x140004000,image_bytes=4096,ram={'base':0x140000000,'size':0x2000000})
        module.debugger_numbers(original,{'_start':0,'image_end':4096},4096)
        for value in ('0; shell false',True,-1,1<<64):
            m=dict(original,fdt_pa=value)
            with self.assertRaises(ValueError):module.debugger_numbers(m,{'_start':0},4096)
        with self.assertRaises(ValueError):module.debugger_numbers(original,{'native_halt':'shell false'},4096)

    def test_wrong_hash_and_unreviewed_address_refuse_before_output_creation(self):
        (ROOT/'research').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'research',prefix='native-input-test-') as d:
            d=Path(d);kernel=d/'kernel';kernel.write_bytes(b'input-not-a-kernel')
            for expected,address in [('0'*64,0x47c80000),(hashlib.sha256(kernel.read_bytes()).hexdigest(),0xc000000),('X'*64,0x47c80000)]:
                out=d/'output'
                with self.assertRaises(ValueError):builder.build(kernel,d,out,expected,address)
                self.assertFalse(out.exists())

    def test_existing_output_is_preserved_and_optimized_verifier_has_no_side_effect(self):
        (ROOT/'research').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'research',prefix='native-output-test-') as d:
            d=Path(d);out=d/'existing';out.mkdir();(out/'keep').write_bytes(b'keep')
            with self.assertRaises(ValueError):builder.build(d/'absent',d,out,'0'*64,0x47c80000)
            self.assertEqual((out/'keep').read_bytes(),b'keep')
            result=subprocess.run([sys.executable,'-O',str(ROOT/'ace/native-loader/verify.py')],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0);self.assertIn('optimized verification refused',result.stderr)
            self.assertEqual(list(out.iterdir()),[out/'keep'])

    def test_actual_image_header_bss_and_embedded_payload_are_bound(self):
        d=ROOT/'research/ace-native-entry-20261020/image-v2'
        if not (d/'build-manifest.json').exists():self.skipTest('private native build unavailable')
        m=json.loads((d/'build-manifest.json').read_text());s=json.loads((d/'symbols.json').read_text())
        image=(d/'native.Image').read_bytes();payload=(d/'ace.payload').read_bytes()
        self.assertEqual(hashlib.sha256(image).hexdigest(),m['image_sha256'])
        self.assertEqual(hashlib.sha256(payload).hexdigest(),m['payload_sha256'])
        self.assertEqual(image[s['bundle_start']:s['bundle_end']],payload)
        self.assertEqual(struct.unpack_from('<Q',image,8)[0],m['text_offset'])
        self.assertEqual(struct.unpack_from('<Q',image,16)[0],len(image))
        self.assertEqual(struct.unpack_from('<I',image,56)[0],0x644d5241)
        self.assertEqual(struct.unpack_from('<I',image)[0]>>26,5)
        self.assertEqual(image[s['__bss_start']:s['__bss_end']],bytes(s['__bss_end']-s['__bss_start']))
        self.assertGreaterEqual(s['stack_top']-s['stack_guard'],65536+64)
        self.assertEqual(s['native_vectors']%2048,0)
        self.assertFalse(m['ios_deployable']);self.assertFalse(m['xnu_hardware_boot'])

if __name__=='__main__':unittest.main()
