"""Host digest/bundle guards; actual module execution is tested only in QEMU."""
import ctypes
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'diagnostics/ace-ramdiag'
spec = importlib.util.spec_from_file_location('ace_bundle_tests', SOURCE / 'module_bundle.py')
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


class LoaderDigestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='ace-loader-sha-')
        p = Path(cls.temp.name)
        (p / 'wrapper.c').write_text('#include "sha256.h"\nvoid digest(const unsigned char *p,unsigned long n,unsigned long chunk,unsigned char *out){struct ace_sha256 s;ace_sha_init(&s);while(n){unsigned long take=n<chunk?n:chunk;ace_sha_update(&s,p,take);p+=take;n-=take;}ace_sha_final(&s,out);}\n')
        subprocess.run(['cc', '-shared', '-fPIC', '-O2', '-Wall', '-Wextra', '-Werror', '-I', str(SOURCE), str(p / 'wrapper.c'), '-o', str(p / 'sha.so')], check=True, capture_output=True)
        cls.library = ctypes.CDLL(str(p / 'sha.so'))
        cls.digest = cls.library.digest
        cls.digest.argtypes = [ctypes.c_char_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_void_p]
        cls.digest.restype = None

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def check_digest(self, data, chunk):
        output = ctypes.create_string_buffer(32)
        self.digest(data, len(data), chunk, output)
        self.assertEqual(output.raw, hashlib.sha256(data).digest())

    def test_empty_standard_and_padding_boundaries(self):
        for data in [b'', b'abc'] + [b'a' * n for n in [1, 55, 56, 63, 64, 65, 119, 120, 128]]:
            for chunk in [1, 7, 64, 4096]:
                with self.subTest(size=len(data), chunk=chunk):
                    self.check_digest(data, chunk)

    def test_large_binary_and_million_byte_vectors(self):
        self.check_digest(bytes(range(256)) * 513, 65536)
        self.check_digest(b'a' * 1000000, 8191)


class BundleInputGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ace-loader-unit-', dir=ROOT / 'research')
        self.out = Path(self.temp.name) / 'bundle'

    def tearDown(self):
        self.temp.cleanup()

    def build(self, items, serial='RAMDIAG_QEMU_FIXTURE', bindings=()):
        return bundle.compile_bundle(self.out, items, expected_release='5.10.test', expected_serial=serial, bindings=bindings)

    def test_empty_oversized_and_unsafe_identity_refused(self):
        with self.assertRaisesRegex(ValueError, 'count'):
            self.build([])
        with self.assertRaisesRegex(ValueError, 'count'):
            self.build([{}] * 271)
        with self.assertRaisesRegex(ValueError, 'serial'):
            self.build([{}], serial='bad/serial')
        self.assertFalse(self.out.exists())

    def test_unsafe_module_and_gate_paths_refused_before_compile(self):
        for item in [dict(module='../protected.ko', data=b'x'),
                     dict(module='valid.ko', data=b'x', gate='/data/ready'),
                     dict(module='valid.ko', data=b'x', gate='/sys/../data/ready'),
                     dict(module='valid.ko', data=b'x', gate='/sys/ready;reboot')]:
            with self.subTest(item=item), self.assertRaises(ValueError):
                self.build([item])
        self.assertFalse(self.out.exists())

    def test_empty_or_oversized_module_refused(self):
        for data in [b'', b'x' * (2 * 1024 * 1024 + 1)]:
            with self.assertRaisesRegex(ValueError, 'size'):
                self.build([dict(module='valid.ko', data=data)])
        self.assertFalse(self.out.exists())

    def test_non_aarch64_elf_refused(self):
        with self.assertRaisesRegex(ValueError, 'ELF64'):
            bundle.module_info(b'not an ELF')
        header = bytearray(64)
        header[:6] = b'\x7fELF\x02\x01'
        header[16:18] = (2).to_bytes(2, 'little')
        header[18:20] = (183).to_bytes(2, 'little')
        with self.assertRaisesRegex(ValueError, 'relocatable'):
            bundle.module_info(header)

    def test_binding_paths_and_property_bytes_refused_before_compile(self):
        good = dict(dt_path='/soc/usb@1', driver='mtu3', module='mtu3', class_path='/sys/class/udc/test', properties={'reg': '00000001'})
        for changes in [dict(dt_path='/soc/../protected'), dict(driver='bad;driver'), dict(module='../bad'),
                        dict(class_path='/data/ready'), dict(properties={'../reg': '00000001'}),
                        dict(properties={'reg': ''}), dict(properties={'reg': 'ff' * 65}), dict(properties={'reg': 'zz'})]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.build([dict(module='test.ko', data=b'x')], bindings=[{**good, **changes}])
        self.assertFalse(self.out.exists())

    def test_supervision_bounds_and_empty_return_proof_refused(self):
        for changes in [dict(return_prefix_count=2), dict(return_prefix_count=1),
                        dict(supervisor_timeout=0), dict(supervisor_timeout=181)]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                bundle.compile_bundle(self.out, [dict(module='test.ko', data=b'x')],
                                      expected_release='5.10.test', expected_serial='RAMDIAG_QEMU_FIXTURE', **changes)
        self.assertFalse(self.out.exists())


if __name__ == '__main__':
    unittest.main()
