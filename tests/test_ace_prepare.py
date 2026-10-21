import importlib.util
import gzip
from pathlib import Path
import struct
import sys
import tempfile
import types
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
spec = importlib.util.spec_from_file_location('ace_prepare_test', Path(__file__).resolve().parents[1] / 'tools/ace-prepare.py')
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)


def boot_fixture():
    data = bytearray(12288)
    data[:8] = b'ANDROID!'
    struct.pack_into('<4I', data, 8, 16, 16, 0, 1584)
    struct.pack_into('<I', data, 40, 4)
    struct.pack_into('<I', data, 1580, 4096)
    # kernel4K + ramdisk4K + signature4K needs 16K including header.
    return data + bytes(4096)


class ImageBoundsTests(unittest.TestCase):
    def test_cli_writes_to_validated_canonical_path(self):
        with tempfile.TemporaryDirectory() as d:
            validated = Path(d) / 'private/report.json'
            report = {'host_preparation_passed': True, 'host_errors': [],
                      'ios_deployable': False, 'deployment_blockers': ['hardware']}
            validator = types.SimpleNamespace(validate_output=lambda path: validated,
                                              CollectionError=RuntimeError)
            with mock.patch.object(sys, 'argv', ['ace-prepare.py', '--output', '~/research/report.json']), \
                 mock.patch.object(prep, 'module', return_value=validator), \
                 mock.patch.object(prep, 'prepare', return_value=report), \
                 mock.patch('builtins.print'):
                self.assertEqual(prep.main(), 0)
            self.assertTrue(validated.is_file())

    def test_config_is_bounded_and_has_complete_gzip_and_end_marker(self):
        config = b'CONFIG_IKCONFIG=y\n# CONFIG_KEXEC is not set\n'
        image = b'prefixIKCFG_ST' + gzip.compress(config) + b'IKCFG_EDsuffix'
        result = prep.kernel_config(gzip.compress(image))
        self.assertIn('# CONFIG_KEXEC is not set', result['selected_options'])
        with self.assertRaises(ValueError):
            prep.kernel_config(gzip.compress(image.replace(b'IKCFG_ED', b'bad-data')))
        with self.assertRaises(ValueError):
            prep.kernel_config(gzip.compress(b'no config here'))

    def test_boot_v4_and_truncated_signature(self):
        data = boot_fixture()
        self.assertEqual(prep.boot_v4(data)['payload_end'], 16384)
        for size in (39, 4095, 8192, 12288, 16383):
            with self.subTest(size=size), self.assertRaises(ValueError):
                prep.boot_v4(data[:size])

    def test_boot_wrong_version_and_reserved_bytes(self):
        data = boot_fixture(); data[24] = 1
        with self.assertRaises(ValueError):
            prep.boot_v4(data)
        data[24] = 0; struct.pack_into('<I', data, 40, 2)
        with self.assertRaises(ValueError):
            prep.boot_v4(data)

    def test_sparse_must_represent_exact_raw_length(self):
        with tempfile.TemporaryDirectory() as d:
            raw, sparse = Path(d) / 'raw', Path(d) / 'sparse'
            raw.write_bytes(bytes(8192))
            sparse.write_bytes(struct.pack('<IHHHHIIII', 0xed26ff3a, 1, 0, 28, 12, 4096, 2, 1, 0))
            self.assertEqual(prep.sparse_geometry(raw, sparse)['logical_bytes'], 8192)
            raw.write_bytes(bytes(4096))
            with self.assertRaises(ValueError):
                prep.sparse_geometry(raw, sparse)
            sparse.write_bytes(b'bad')
            with self.assertRaises(ValueError):
                prep.sparse_geometry(raw, sparse)


if __name__ == '__main__':
    unittest.main()
