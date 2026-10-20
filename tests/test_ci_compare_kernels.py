from pathlib import Path
import importlib.util
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('compare', ROOT / 'tools/ci-compare-kernels.py')
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)


class KernelSectionAuditTests(unittest.TestCase):
    def fixture(self, code=b'code', metadata=b'type', address=0x1000):
        commands = bytearray()
        location = 32 + 2 * 152
        payload = bytearray()
        for segment, section, data in [('__TEXT_EXEC', '__text', code), ('__CTF', '__ctf', metadata)]:
            command = bytearray(152)
            struct.pack_into('<II', command, 0, 0x19, 152)
            command[8:8+len(segment)] = segment.encode()
            struct.pack_into('<I', command, 64, 1)
            command[72:72+len(section)] = section.encode()
            command[88:88+len(segment)] = segment.encode()
            struct.pack_into('<QQII', command, 104, address, len(data), location, 2)
            commands += command
            payload += data
            location += len(data)
        header = struct.pack('<8I', 0xfeedfacf, 0x100000c, 0, 2, 2, len(commands), 0, 0)
        return header + commands + payload

    def test_type_metadata_difference_is_explicit_not_file_equality(self):
        result = compare.compare(self.fixture(), self.fixture(metadata=b'other type'))
        self.assertFalse(result['byte_identical'])
        self.assertTrue(result['non_ctf_sections_identical'])
        self.assertIn('__CTF,__ctf', result['excluded_type_metadata'])

    def test_code_and_layout_differences_fail(self):
        for right in [self.fixture(code=b'evil'), self.fixture(address=0x2000)]:
            result = compare.compare(self.fixture(), right)
            self.assertFalse(result['non_ctf_sections_identical'])
            self.assertIn('__TEXT_EXEC,__text', result['mismatches'])

    def test_exact_file_is_identical(self):
        result = compare.compare(self.fixture(), self.fixture())
        self.assertTrue(result['byte_identical'])

    def test_truncated_image_and_out_of_bounds_section_refused(self):
        bad = bytearray(self.fixture())
        struct.pack_into('<I', bad, 32 + 120, len(bad) + 1)
        for data in [b'', self.fixture()[:40], bytes(bad)]:
            with self.assertRaises(ValueError):
                compare.sections(data)


if __name__ == '__main__':
    unittest.main()
