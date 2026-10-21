"""Exercise actual bounded dummy-USB descriptor parser; no USB devices opened."""
import ctypes
from pathlib import Path
import random
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'diagnostics/ace-ramdiag'


def descriptor(packet=512):
    device = bytes.fromhex('1201000200000040d11801d0000101020301')
    config = bytes.fromhex('090223000101008002')
    otg = bytes([3, 9, 3])
    interface = bytes([9, 4, 0, 0, 2, 255, 66, 1, 0])
    out = bytes([7, 5, 2, 2, packet & 255, packet >> 8, 0])
    incoming = bytes([7, 5, 129, 2, packet & 255, packet >> 8, 0])
    return device + config + otg + interface + out + incoming


class USBDescriptorGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='ace-usb-descriptor-')
        p = Path(cls.temp.name)
        (p / 'wrapper.c').write_text('#include "usb_descriptors.h"\nint parse(const unsigned char *p,unsigned long n,struct ace_usb_endpoints *out){return ace_usb_descriptors(p,n,out);}\n')
        subprocess.run(['cc', '-shared', '-fPIC', '-O2', '-Wall', '-Wextra', '-Werror', '-I', str(SOURCE), str(p / 'wrapper.c'), '-o', str(p / 'usb.so')], check=True, capture_output=True)
        cls.library = ctypes.CDLL(str(p / 'usb.so'))
        cls.parser = cls.library.parse
        cls.parser.argtypes = [ctypes.c_char_p, ctypes.c_ulong, ctypes.c_void_p]
        cls.parser.restype = ctypes.c_int

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def parse(self, data):
        output = (ctypes.c_uint * 3)()
        accepted = bool(self.parser(bytes(data), len(data), output))
        return accepted, tuple(output)

    def test_exact_single_adb_interface_and_two_speeds(self):
        for packet in [64, 512]:
            self.assertEqual(self.parse(descriptor(packet)), (True, (129, 2, packet)))

    def test_every_truncated_prefix_and_zero_or_oversized_length_refused(self):
        data = descriptor()
        for size in range(len(data)):
            with self.subTest(size=size):
                self.assertFalse(self.parse(data[:size])[0])
        for size in [0, 1, 255]:
            data = bytearray(descriptor())
            data[18] = size
            self.assertFalse(self.parse(data)[0])

    def test_vendor_product_interface_and_configuration_disagreements_refused(self):
        for offset in [8, 10, 17, 20, 22, 23, 32, 33, 34, 35, 36, 37]:
            data = bytearray(descriptor())
            data[offset] ^= 1
            with self.subTest(offset=offset):
                self.assertFalse(self.parse(data)[0])

    def test_duplicate_direction_nonbulk_and_mismatched_packet_sizes_refused(self):
        for offset, value in [(41, 130), (42, 3), (43, 64), (44, 0)]:
            data = bytearray(descriptor())
            data[offset] = value
            with self.subTest(offset=offset):
                self.assertFalse(self.parse(data)[0])

    def test_random_bounded_inputs_never_accept_a_foreign_descriptor(self):
        rng = random.Random(6895)
        for _ in range(500):
            data = rng.randbytes(rng.randrange(256))
            self.assertFalse(self.parse(data)[0])


if __name__ == '__main__':
    unittest.main()
