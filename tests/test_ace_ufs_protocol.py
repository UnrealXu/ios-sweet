"""Actual C codec tests: wire vectors, refusal boundaries and freestanding build."""
import ctypes as C
import pathlib
import shutil
import struct
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'ace/ufs_protocol.c'


class Command(C.Structure):
    _fields_ = [('cdb', C.c_uint8 * 16), ('transfer_bytes', C.c_uint32), ('cdb_len', C.c_uint8)]


class Utrd(C.Structure):
    _fields_ = [('bytes', C.c_uint8 * 32)]


class Ucd(C.Structure):
    _fields_ = [('bytes', C.c_uint8 * 1280)]


class Response(C.Structure):
    _fields_ = [('residual_bytes', C.c_uint32), ('sense_bytes', C.c_uint16),
                ('scsi_status', C.c_uint8), ('sense', C.POINTER(C.c_uint8))]


class UfsProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='ace-ufs-codec-')
        cls.directory = pathlib.Path(cls.temp.name)
        compiler = shutil.which('cc')
        if not compiler:
            raise unittest.SkipTest('host C compiler unavailable')
        subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-pedantic',
                        '-shared', '-fPIC', '-O2', str(SOURCE), '-o', str(cls.directory / 'codec.so')], check=True)
        cls.lib = C.CDLL(str(cls.directory / 'codec.so'))
        for name in ('ace_ufs_make_read10', 'ace_ufs_make_read16'):
            getattr(cls.lib, name).argtypes = [C.c_uint64, C.c_uint32, C.c_uint32, C.POINTER(Command)]
        cls.lib.ace_ufs_make_identify.argtypes = [C.c_int, C.c_uint32, C.POINTER(Command)]
        cls.lib.ace_ufs_encode.argtypes = [C.POINTER(Command), C.c_uint8, C.c_uint8,
                                        C.c_uint64, C.c_uint64, C.c_int, C.POINTER(Utrd), C.POINTER(Ucd)]
        for name in ('ace_ufs_parse_capacity10', 'ace_ufs_parse_capacity16'):
            getattr(cls.lib, name).argtypes = [C.POINTER(C.c_uint8), C.c_size_t,
                                              C.POINTER(C.c_uint64), C.POINTER(C.c_uint32)]
        cls.lib.ace_ufs_parse_luns.argtypes = [C.POINTER(C.c_uint8), C.c_size_t, C.POINTER(C.c_uint8)]
        cls.lib.ace_ufs_check_response.argtypes = [C.c_uint8, C.POINTER(C.c_uint8), C.c_size_t,
                                                 C.c_uint8, C.c_uint8, C.POINTER(Response)]

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def read(self, lba=0x12345678, blocks=2, block_bytes=4096, kind=10):
        command = Command()
        code = getattr(self.lib, f'ace_ufs_make_read{kind}')(lba, blocks, block_bytes, C.byref(command))
        self.assertEqual(code, 0)
        return command

    def encode(self, command, ucd_dma=0x40000000, data_dma=0x40100000, dma64=1, lun=3):
        request, descriptor = Utrd(), Ucd()
        C.memset(C.byref(request), 0xa5, C.sizeof(request))
        C.memset(C.byref(descriptor), 0xa5, C.sizeof(descriptor))
        code = self.lib.ace_ufs_encode(C.byref(command), lun, 7, ucd_dma, data_dma,
                                       dma64, C.byref(request), C.byref(descriptor))
        if code:
            self.assertEqual(bytes(request.bytes), b'\xa5' * 32)
            self.assertEqual(bytes(descriptor.bytes), b'\xa5' * 1280)
        return code, bytes(request.bytes), bytes(descriptor.bytes)

    def test_read10_wire_vector(self):
        command = self.read()
        self.assertEqual(bytes(command.cdb), bytes.fromhex('28 00 12 34 56 78 00 00 02 00') + bytes(6))
        code, request, descriptor = self.encode(command)
        self.assertEqual(code, 0)
        self.assertEqual(request, struct.pack('<8I', 0x15000000, 0, 0xf, 0, 0x40000000, 0,
                                             0x00800080, 0x01000001))
        self.assertEqual(descriptor[:32], bytes.fromhex('01 40 03 07') + bytes(8) +
                         bytes.fromhex('00 00 20 00') + bytes(command.cdb))
        self.assertEqual(descriptor[32:1024], bytes(992))
        self.assertEqual(descriptor[1024:1040], struct.pack('<4I', 0x40100000, 0, 0, 8191))
        self.assertEqual(descriptor[1040:], bytes(240))

    def test_read16_big_endian_lba_and_count(self):
        command = self.read(lba=0x123456789abcdef0, blocks=0x1234, block_bytes=512, kind=16)
        self.assertEqual(bytes(command.cdb), bytes.fromhex('88 00 12 34 56 78 9a bc de f0 00 00 12 34 00 00'))
        self.assertEqual(command.transfer_bytes, 0x1234 * 512)

    def test_command_range_boundaries(self):
        out = Command()
        for lba, count, size in [(0, 0, 4096), (0, 1, 0), (0, 1, 1000), (0, 1, 131072)]:
            self.assertLess(self.lib.ace_ufs_make_read16(lba, count, size, C.byref(out)), 0)
        for lba, count in [(0xffffffff, 2), (0x100000000, 1), (0, 65536)]:
            self.assertEqual(self.lib.ace_ufs_make_read10(lba, count, 4096, C.byref(out)), -2)
        self.assertEqual(self.lib.ace_ufs_make_read16(0xffffffffffffffff, 2, 512, C.byref(out)), -2)
        self.assertEqual(self.lib.ace_ufs_make_read16(0, 0x800000, 512, C.byref(out)), -2)
        self.assertEqual(self.lib.ace_ufs_make_read16(0xffffffffffffffff, 1, 512, C.byref(out)), 0)

    def test_identification_vectors(self):
        cases = [(0, 0, bytes(16), 6),
                 (1, 36, bytes.fromhex('12 00 00 00 24 00') + bytes(10), 6),
                 (2, 8, b'\x25' + bytes(15), 10),
                 (3, 32, bytes.fromhex('9e 10') + bytes(11) + b'\x20' + bytes(2), 16),
                 (4, 4096, bytes.fromhex('a0 00 00 00 00 00 00 00 10 00 00 00') + bytes(4), 12)]
        for kind, allocation, expected, length in cases:
            with self.subTest(kind=kind):
                command = Command()
                self.assertEqual(self.lib.ace_ufs_make_identify(kind, allocation, C.byref(command)), 0)
                self.assertEqual(bytes(command.cdb), expected)
                self.assertEqual(command.cdb_len, length)
                self.assertEqual(self.encode(command)[0], 0)
        command = Command()
        for kind, allocation in [(0, 4), (1, 0), (1, 255), (2, 16), (3, 16), (4, 12), (99, 0)]:
            self.assertLess(self.lib.ace_ufs_make_identify(kind, allocation, C.byref(command)), 0)

    def test_no_data_tur(self):
        command = Command()
        self.assertEqual(self.lib.ace_ufs_make_identify(0, 0, C.byref(command)), 0)
        code, request, descriptor = self.encode(command, data_dma=0xffffffffffffffff)
        self.assertEqual(code, 0)
        self.assertEqual(struct.unpack_from('<I', request)[0], 0x11000000)
        self.assertEqual(struct.unpack_from('<I', request, 28)[0], 0x01000000)
        self.assertEqual(descriptor[1], 0)
        self.assertEqual(descriptor[1024:], bytes(256))

    def test_prdt_split_and_limit(self):
        command = self.read(lba=0, blocks=65, block_bytes=4096)
        code, request, descriptor = self.encode(command, data_dma=0x100000000)
        self.assertEqual(code, 0)
        self.assertEqual(struct.unpack_from('<I', request, 28)[0], 0x01000002)
        self.assertEqual(struct.unpack_from('<4I', descriptor, 1024), (0, 1, 0, 262143))
        self.assertEqual(struct.unpack_from('<4I', descriptor, 1040), (262144, 1, 0, 4095))
        self.assertEqual(self.encode(self.read(lba=0, blocks=1024))[0], 0)
        self.assertEqual(self.encode(self.read(lba=0, blocks=1025))[0], -2)

    def test_dma_address_validation(self):
        command = self.read(lba=0, blocks=1)
        for settings in [dict(ucd_dma=0x40000001), dict(data_dma=0x40100001),
                         dict(ucd_dma=0xffffffffffffff80), dict(data_dma=0xfffffffffffffff0),
                         dict(ucd_dma=0x100000000, dma64=0), dict(data_dma=0x100000000, dma64=0),
                         dict(data_dma=0xfffff800, dma64=0), dict(data_dma=0x40000000),
                         dict(data_dma=0x3ffffffc)]:
            with self.subTest(settings=settings):
                self.assertEqual(self.encode(command, **settings)[0], -4)
        self.assertEqual(self.encode(command, data_dma=0xfffff000, dma64=0)[0], 0)
        self.assertEqual(self.encode(command, lun=8)[0], -1)

    def test_forged_write_and_noncanonical_commands_refused(self):
        for opcode in (0x2a, 0x8a, 0x42, 0x35, 0x04):
            command = self.read()
            command.cdb[0] = opcode
            self.assertEqual(self.encode(command)[0], -3)
        for mutate in ('cdb_length', 'flags', 'transfer', 'reserved'):
            command = self.read()
            if mutate == 'cdb_length': command.cdb_len = 16
            if mutate == 'flags': command.cdb[1] = 0x10
            if mutate == 'transfer': command.transfer_bytes = 8191
            if mutate == 'reserved': command.cdb[15] = 1
            self.assertEqual(self.encode(command)[0], -3)

    def response(self, raw=None, ocs=0, available=52):
        data = bytearray(52) if raw is None else raw
        if raw is None: data[:4] = bytes.fromhex('21 00 03 07')
        buffer = (C.c_uint8 * len(data)).from_buffer_copy(data)
        out = Response()
        code = self.lib.ace_ufs_check_response(ocs, buffer, available, 3, 7, C.byref(out))
        return code, out, buffer

    def test_good_and_check_condition_response(self):
        self.assertEqual(self.response()[0], 0)
        data = bytearray(52); data[:4] = bytes.fromhex('21 00 03 07'); data[7] = 2
        data[11] = 20; data[33] = 18; data[34:52] = bytes.fromhex('70 00 05 00 00 00 00 0a 00 00 00 00 20 00 00 00 00 00')
        code, out, buffer = self.response(data)
        self.assertEqual(code, -7); self.assertEqual(out.scsi_status, 2)
        self.assertEqual(out.sense_bytes, 18)
        self.assertEqual(C.string_at(out.sense, out.sense_bytes), bytes(data[34:52]))
        self.assertTrue(buffer)  # retain backing store for the borrowed view

    def test_malformed_completion_refused(self):
        self.assertEqual(self.response(ocs=0xf)[0], -5)
        self.assertEqual(self.response(available=31)[0], -1)
        for offset, value in [(0, 0x31), (2, 4), (3, 8), (6, 1), (8, 1),
                              (1, 0x20), (1, 0x40), (15, 1), (11, 21), (11, 1)]:
            data = bytearray(52); data[:4] = bytes.fromhex('21 00 03 07'); data[offset] = value
            self.assertEqual(self.response(data)[0], -6, (offset, value))
        data = bytearray(52); data[:4] = bytes.fromhex('21 00 03 07'); data[11] = 20; data[33] = 19
        self.assertEqual(self.response(data)[0], -6)

    def test_report_luns_well_known_lun_only(self):
        command = Command()
        self.assertEqual(self.lib.ace_ufs_make_identify(4, 4096, C.byref(command)), 0)
        self.assertEqual(self.encode(command, lun=0x81)[0], 0)
        self.assertEqual(self.encode(self.read(), lun=0x81)[0], -1)
        self.assertEqual(self.encode(command, lun=0xd0)[0], -1)

    def test_capacity_payloads(self):
        count, block_bytes = C.c_uint64(123), C.c_uint32(456)
        cases = [('10', struct.pack('>II', 0x12345678, 4096), 0, 0x12345679),
                 ('10', struct.pack('>II', 0xffffffff, 4096), -2, None),
                 ('16', struct.pack('>QI', 0x123456789abcdef0, 4096) + bytes(20), 0, 0x123456789abcdef1),
                 ('16', struct.pack('>QI', 0xffffffffffffffff, 4096) + bytes(20), -2, None),
                 ('10', struct.pack('>II', 10, 1000), -6, None),
                 ('16', bytes(31), -1, None)]
        for kind, data, expected, blocks in cases:
            with self.subTest(kind=kind, data=data):
                buffer = (C.c_uint8 * len(data)).from_buffer_copy(data)
                before = (count.value, block_bytes.value)
                code = getattr(self.lib, 'ace_ufs_parse_capacity' + kind)(buffer, len(data), C.byref(count), C.byref(block_bytes))
                self.assertEqual(code, expected)
                self.assertEqual((count.value, block_bytes.value), before if expected else (blocks, 4096))

    def test_report_luns_payload_and_refusals(self):
        def parse(data):
            buffer = (C.c_uint8 * len(data)).from_buffer_copy(data)
            mask = C.c_uint8(0xa5)
            code = self.lib.ace_ufs_parse_luns(buffer, len(data), C.byref(mask))
            return code, mask.value
        entries = bytes.fromhex('00 00 00 00 00 00 00 00 00 02 00 00 00 00 00 00')
        self.assertEqual(parse(struct.pack('>II', 16, 0) + entries), (0, 5))
        self.assertEqual(parse(bytes(8)), (0, 0))
        malformed = [bytes(7), struct.pack('>II', 0xfffffff8, 0), struct.pack('>II', 7, 0) + bytes(8),
                     struct.pack('>II', 16, 0) + bytes(16),  # duplicate LUN0
                     struct.pack('>II', 8, 0) + bytes.fromhex('40 01 00 00 00 00 00 00'),
                     struct.pack('>II', 8, 0) + bytes.fromhex('00 08 00 00 00 00 00 00')]
        for data in malformed:
            code, mask = parse(data)
            self.assertLess(code, 0)
            self.assertEqual(mask, 0xa5)

    def test_sanitized_bounded_response_fuzz(self):
        compiler = shutil.which('cc')
        harness = self.directory / 'bounds.c'
        harness.write_text(r"""
#include "ufs_protocol.h"
int main(void) {
    unsigned seed = 1;
    unsigned char response[512];
    struct ace_ufs_response parsed;
    unsigned char mask;
    unsigned long long count;
    uint64_t blocks;
    uint32_t size;
    for (count = 0; count < 12000; count++) {
        for (unsigned i = 0; i < sizeof(response); i++) {
            seed = seed * 1664525u + 1013904223u;
            response[i] = (unsigned char)(seed >> 24);
        }
        response[0] = 0x21; response[1] = 0;
        response[2] = 3; response[3] = 7; response[6] = 0; response[8] = 0;
        response[12] = response[13] = response[14] = response[15] = 0;
        size_t available = count % 513;
        (void)ace_ufs_check_response(0, response, available, 3, 7, &parsed);
        (void)ace_ufs_parse_luns(response, available, &mask);
        (void)ace_ufs_parse_capacity10(response, available, &blocks, &size);
        (void)ace_ufs_parse_capacity16(response, available, &blocks, &size);
    }
    return 0;
}
""")
        executable = self.directory / 'bounds'
        subprocess.run([compiler, '-std=c11', '-Wall', '-Wextra', '-Werror', '-O1', '-g',
                        '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
                        '-I', str(ROOT / 'ace'), str(SOURCE), str(harness), '-o', str(executable)], check=True)
        subprocess.run([str(executable)], check=True, timeout=15)

    def test_arm64_freestanding_cross_compile(self):
        compiler = shutil.which('aarch64-linux-gnu-gcc')
        if not compiler: self.skipTest('ARM64 cross compiler unavailable')
        output = self.directory / 'codec.o'
        subprocess.run([compiler, '-std=c11', '-O2', '-ffreestanding', '-fno-builtin', '-mgeneral-regs-only',
                        '-Wall', '-Wextra', '-Werror', '-c', str(SOURCE), '-o', str(output)], check=True)
        self.assertEqual(subprocess.check_output(['aarch64-linux-gnu-nm', '-u', str(output)], text=True).strip(), '')


if __name__ == '__main__':
    unittest.main()
