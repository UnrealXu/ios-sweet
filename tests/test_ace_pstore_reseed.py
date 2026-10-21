"""Explicit exact-archived reseed; all fixtures are synthetic ordinary RAM."""
import ctypes as c
import hashlib
import importlib.util
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
spec = importlib.util.spec_from_file_location('reseed_native', ROOT / 'tools/ace-mknative.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
ZONE_BYTES = 65536
# Invalid zero header with deterministic nonzero payload: no physical dump,
# device serial, Apple asset or real-device capture hash belongs in this test.
CAPTURE = bytes(12) + bytes((i * 17 + 9) % 251 for i in range(ZONE_BYTES - 12))
CAPTURE_SHA = hashlib.sha256(CAPTURE).hexdigest()


@unittest.skipUnless(shutil.which('cc'), 'C compiler required')
class PstoreReseedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.work = Path(cls.tmp.name)
        library = cls.work / 'seed.so'
        subprocess.run(['cc', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror',
                        '-shared', '-fPIC', str(ROOT / 'ace/pstore_ring.c'),
                        str(ROOT / 'ace/pstore_seed.c'), '-o', str(library)], check=True)
        cls.lib = c.CDLL(str(library))
        cls.lib.ace_pstore_seed_empty.argtypes = [c.c_void_p, c.c_size_t]
        cls.lib.ace_pstore_seed_from_snapshot.argtypes = [c.c_void_p, c.c_size_t,
                                                         c.c_void_p, c.c_size_t]
        cls.lib.ace_pstore_ring_validate.argtypes = [c.c_void_p, c.c_size_t, c.c_void_p]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def seed(self, data, expected=CAPTURE):
        zone = c.create_string_buffer(data + b'ZONE-GUARD')
        capture = c.create_string_buffer(expected + b'CAPTURE-GUARD')
        before = capture.raw
        result = self.lib.ace_pstore_seed_from_snapshot(zone, len(data), capture, len(expected))
        self.assertEqual(capture.raw, before)
        self.assertEqual(zone.raw[len(data):], b'ZONE-GUARD\0')
        return result, zone

    def test_complete_match_rebuilds_empty_and_second_call_preserves(self):
        result, zone = self.seed(CAPTURE)
        self.assertEqual(result, 2)
        self.assertEqual(zone.raw[:ZONE_BYTES], b'DBGC' + bytes(ZONE_BYTES - 4))
        self.assertEqual(self.lib.ace_pstore_ring_validate(zone, ZONE_BYTES, None), 0)
        capture = c.create_string_buffer(CAPTURE)
        before = zone.raw
        self.assertEqual(self.lib.ace_pstore_seed_from_snapshot(
            zone, ZONE_BYTES, capture, ZONE_BYTES), 0)
        self.assertEqual(zone.raw, before)

    def test_original_api_and_valid_or_zero_paths_unchanged(self):
        zone = c.create_string_buffer(CAPTURE)
        self.assertEqual(self.lib.ace_pstore_seed_empty(zone, ZONE_BYTES), -3)
        self.assertEqual(zone.raw[:ZONE_BYTES], CAPTURE)
        result, zone = self.seed(bytes(ZONE_BYTES))
        self.assertEqual(result, 1)
        self.assertEqual(zone.raw[:ZONE_BYTES], b'DBGC' + bytes(ZONE_BYTES - 4))
        valid = bytearray(CAPTURE)
        struct.pack_into('<III', valid, 0, 0x43474244, 7, 19)
        result, zone = self.seed(bytes(valid))
        self.assertEqual(result, 0)
        self.assertEqual(zone.raw[:ZONE_BYTES], valid)

    def test_unknown_header_payload_or_last_byte_never_overwritten(self):
        for offset in [0, 3, 4, 7, 8, 11, 12, 128, 32768, ZONE_BYTES - 1]:
            with self.subTest(offset=offset):
                changed = bytearray(CAPTURE)
                changed[offset] ^= 0x80
                result, zone = self.seed(bytes(changed))
                self.assertEqual(result, -3)
                self.assertEqual(zone.raw[:ZONE_BYTES], changed)
        expected = bytearray(CAPTURE)
        expected[-1] ^= 1
        result, zone = self.seed(CAPTURE, bytes(expected))
        self.assertEqual(result, -3)
        self.assertEqual(zone.raw[:ZONE_BYTES], CAPTURE)

    def test_bad_sizes_spans_and_aliases_refuse_before_stores(self):
        zone = c.create_string_buffer(bytes(ZONE_BYTES * 2))
        capture = c.create_string_buffer(CAPTURE)
        before = zone.raw
        cases = [(zone, ZONE_BYTES - 1, capture, ZONE_BYTES, -1),
                 (zone, ZONE_BYTES, capture, ZONE_BYTES - 1, -1),
                 (None, ZONE_BYTES, capture, ZONE_BYTES, -1),
                 (zone, ZONE_BYTES, None, ZONE_BYTES, -1),
                 (c.c_void_p((1 << 64) - 4), ZONE_BYTES, capture, ZONE_BYTES, -2),
                 (zone, ZONE_BYTES, c.c_void_p((1 << 64) - 4), ZONE_BYTES, -2),
                 (zone, ZONE_BYTES, zone, ZONE_BYTES, -4),
                 (zone, ZONE_BYTES, c.byref(zone, 1), ZONE_BYTES, -4),
                 (zone, ZONE_BYTES, c.byref(zone, ZONE_BYTES - 1), ZONE_BYTES, -4),
                 (c.byref(zone, 1), ZONE_BYTES, zone, ZONE_BYTES, -4)]
        for zone_arg, size, expected, expected_size, error in cases:
            with self.subTest(size=size, expected_size=expected_size, error=error):
                self.assertEqual(self.lib.ace_pstore_seed_from_snapshot(
                    zone_arg, size, expected, expected_size), error)
                self.assertEqual(zone.raw, before)

    def test_builder_requires_exact_hash_private_archive_and_all_gates(self):
        # This helper runs after build() has verified the pinned Android Image;
        # testing its None/non-None gate does not claim Android hash validation.
        gates = dict(pmsg=True, init_empty_pmsg=True, auto_readout_after_reset=True,
                     refusal_android=b'already-validated-by-build', diagnostic_readout=False)
        archive = self.work / 'research'
        archive.mkdir(exist_ok=True)
        path = archive / 'synthetic.snapshot'
        path.write_bytes(CAPTURE)
        with patch.object(native, 'ROOT', self.work):
            self.assertEqual(native.load_pmsg_reseed_snapshot(path, CAPTURE_SHA, **gates), CAPTURE)
            self.assertIsNone(native.load_pmsg_reseed_snapshot(None, None, **gates))
            cases = [(None, CAPTURE_SHA, gates), (path, None, gates),
                     (path, '0' * 64, gates), (self.work / 'outside-archive', CAPTURE_SHA, gates)]
            for key, value in [('pmsg', False), ('init_empty_pmsg', False),
                               ('auto_readout_after_reset', False), ('refusal_android', None),
                               ('diagnostic_readout', True), ('pmsg', 1),
                               ('init_empty_pmsg', 1), ('auto_readout_after_reset', 1),
                               ('diagnostic_readout', 0)]:
                cases.append((path, CAPTURE_SHA, dict(gates, **{key: value})))
            for source, expected, options in cases:
                with self.subTest(source=source, expected=expected), self.assertRaises(ValueError):
                    native.load_pmsg_reseed_snapshot(source, expected, **options)
            for name, data in [('short', CAPTURE[:-1]), ('zero', bytes(ZONE_BYTES)),
                               ('valid', b'DBGC' + bytes(ZONE_BYTES - 4))]:
                source = archive / (name + '.snapshot')
                source.write_bytes(data)
                with self.subTest(name=name), self.assertRaises(ValueError):
                    native.load_pmsg_reseed_snapshot(
                        source, hashlib.sha256(data).hexdigest(), **gates)


if __name__ == '__main__':
    unittest.main()
