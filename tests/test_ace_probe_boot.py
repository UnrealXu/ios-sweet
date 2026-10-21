"""Pure host format/evidence tests. No phone transport is invoked."""
import copy
import contextlib
import io
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ace_probe_boot', ROOT / 'tools/ace-probe-boot.py')
wrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wrap)


def image():
    data = bytearray(64)
    struct.pack_into('<QQ', data, 8, 0x80000, len(data))
    data[56:60] = b'ARM\x64'
    return bytes(data)


def fixture():
    kernel, ramdisk = wrap.deterministic_gzip(image()), b'stock-ramdisk-payload'
    h = bytearray(4096)
    h[:8] = b'ANDROID!'
    struct.pack_into('<4I', h, 8, len(kernel), len(ramdisk), 0x180001a4, 1584)
    struct.pack_into('<I', h, 40, 4)
    h[44:58] = b'preserve=yes\0\0'
    struct.pack_into('<I', h, 1580, 4096)
    data = bytes(h) + kernel + bytes(wrap.align(len(kernel)) - len(kernel))
    data += ramdisk + bytes(wrap.align(len(ramdisk)) - len(ramdisk)) + bytes(4096)
    end = len(data)
    data += b'AVB0' + bytes(252)
    data += struct.pack('>4sIIQQQ28s', b'AVBf', 1, 0, end, end, 256, bytes(28))
    return data


class ProbeBootTests(unittest.TestCase):
    def test_gzip_deterministic_exact_and_bounded(self):
        encoded = wrap.deterministic_gzip(image())
        self.assertEqual(encoded, wrap.deterministic_gzip(image()))
        self.assertEqual(encoded[3:10], b'\0\0\0\0\0\x02\xff')
        self.assertEqual(wrap.inflate(encoded), image())
        for bad in (encoded[:-1], encoded + b'bad', encoded + encoded):
            with self.subTest(bad=bad[-5:]), self.assertRaises((ValueError, zlib.error)):
                wrap.inflate(bad)
        corrupt = bytearray(encoded); corrupt[-8] ^= 1
        with self.assertRaises(zlib.error):
            wrap.inflate(corrupt)
        with self.assertRaises(ValueError):
            wrap.inflate(encoded, limit=32)

    def test_repack_changes_only_kernel_size_header_and_keeps_ramdisk(self):
        stock = fixture(); layout = wrap.boot_v4(stock)
        import random
        probe = bytearray(image() + random.Random(1).randbytes(8192))
        struct.pack_into('<Q', probe, 16, len(probe))
        probe = bytes(probe)
        candidate, new = wrap.unsigned_boot(stock, layout, wrap.deterministic_gzip(probe))
        expected_header = bytearray(stock[:4096])
        struct.pack_into('<I', expected_header, 8, new['kernel_bytes'])
        self.assertEqual(candidate[:4096], expected_header)
        before = stock[layout['ramdisk_offset']:layout['ramdisk_offset'] + layout['ramdisk_bytes']]
        after = candidate[new['ramdisk_offset']:new['ramdisk_offset'] + new['ramdisk_bytes']]
        self.assertEqual(before, after)
        self.assertEqual(wrap.inflate(candidate[4096:4096 + new['kernel_bytes']]), probe)
        self.assertEqual(len(candidate), new['payload_end'])
        self.assertIsNone(new['avb'])
        self.assertNotEqual(candidate[-64:-60], b'AVBf')
        with self.assertRaises(ValueError):
            wrap.boot_v4(candidate)  # no old authentication accidentally survives

    def test_bad_boot_headers_padding_and_payload_bounds(self):
        stock = fixture()
        for offset, value in ((0, 0), (20, 0), (24, 1), (40, 3), (1580, 1), (1600, 1)):
            data = bytearray(stock); data[offset] = value
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                wrap.boot_v4(data)
        for size in (0, 39, 4095, 8192):
            with self.subTest(size=size), self.assertRaises(ValueError):
                wrap.boot_v4(stock[:size])
        data = bytearray(stock); struct.pack_into('<I', data, 8, 0xffffffff)
        with self.assertRaises(ValueError):
            wrap.boot_v4(data)
        data = bytearray(stock); data[4096 + wrap.boot_v4(stock)['kernel_bytes']] = 1
        with self.assertRaises(ValueError):
            wrap.boot_v4(data)

    def test_bad_avb_and_nonzero_legacy_signature_are_rejected(self):
        stock = fixture(); layout = wrap.boot_v4(stock)
        for offset in (len(stock) - 64, len(stock) - 1, layout['signature_offset']):
            data = bytearray(stock); data[offset] ^= 1
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                wrap.boot_v4(data)
        data = bytearray(stock); struct.pack_into('>Q', data, len(data) - 64 + 20, 2**64 - 1)
        with self.assertRaises(ValueError):
            wrap.boot_v4(data)

    def test_probe_identity_sources_cases_and_version_are_bound(self):
        with tempfile.TemporaryDirectory() as t:
            source = Path(t)
            for name in wrap.SOURCE_NAMES:
                (source / name).write_bytes(name.encode())
            report = {'status': 'pass', 'record_version': 2, 'image_sha256': wrap.sha(image()),
                      'input_sha256': {n: wrap.sha(n.encode()) for n in wrap.SOURCE_NAMES},
                      'cases': [{'case': n, 'pass': True} for n in sorted(wrap.CASES)]}
            wrap.validate_probe(image(), report, source)
            for field, value in [('status', 'in-progress'), ('record_version', 1),
                                 ('image_sha256', '0' * 64), ('cases', []),
                                 ('cases', [1]),
                                 ('cases', report['cases'][:-1] + [report['cases'][0]]),
                                 ('cases', [dict(c, **{'pass': False}) for c in report['cases']]),
                                 ('input_sha256', [])]:
                bad = copy.deepcopy(report); bad[field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    wrap.validate_probe(image(), bad, source)
            (source / 'start.S').write_bytes(b'changed')
            with self.assertRaises(ValueError):
                wrap.validate_probe(image(), report, source)
        with self.assertRaises(ValueError):
            wrap.validate_probe(image(), [], Path('.'))
        bad = bytearray(image()); bad[56] = 0
        with self.assertRaises(ValueError):
            wrap.image_check(bad)

    def test_wrong_stock_pin_fails_before_any_output_is_created(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'research') as t:
            base = Path(t)
            (base / 'boot.img').write_bytes(fixture())
            (base / 'vendor.img').write_bytes(b'wrong vendor')
            output = base / 'output'
            with contextlib.redirect_stderr(io.StringIO()):
                status = wrap.main(['--stock-boot', str(base / 'boot.img'),
                                    '--stock-vendor-boot', str(base / 'vendor.img'),
                                    '--output-dir', str(output), '--emit-unsigned-boot'])
            self.assertEqual(status, 1)
            self.assertFalse(output.exists())
            with self.assertRaises(ValueError):
                wrap.bounded_read(base / 'boot.img', 8)

    def test_output_refuses_existing_outside_and_symlink(self):
        with self.assertRaises(ValueError):
            wrap.output_path(Path('/tmp/ace-probe-outside'))
        with tempfile.TemporaryDirectory(dir=ROOT / 'research') as t:
            with self.assertRaises(ValueError):
                wrap.output_path(Path(t))
            link = Path(t) / 'link'; link.symlink_to(Path(t) / 'absent')
            with self.assertRaises(ValueError):
                wrap.output_path(link)


if __name__ == '__main__':
    unittest.main()
