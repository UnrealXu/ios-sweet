"""Host-owned RAM only; differential reference is persistent_ram write/save_old.

Reference: official OnePlus fs/pstore/ram_core.c at 8baa5a377e2776402de745579cc3835d08ee1cca.
The model independently expresses completed-call cursor/size/data equations.
No device, raw-memory mapping, driver, reset or storage operation is performed.
"""
import ctypes as C
from pathlib import Path
import random
import shutil
import struct
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SIG = 0x43474244
OK, ARG, RANGE, HEADER, ALIAS, STATE, SPACE = 0, -1, -2, -3, -4, -5, -6


class Info(C.Structure):
    _fields_ = [('capacity', C.c_size_t), ('start', C.c_uint32), ('size', C.c_uint32)]


def zone(capacity, data=b'', cursor=None):
    assert len(data) <= capacity
    raw = struct.pack('<III', SIG, len(data) if cursor is None else cursor, len(data))
    raw += data + bytes(capacity - len(data))
    return (C.c_ubyte * len(raw)).from_buffer_copy(raw)


def reference_append(raw, payload):
    """Official truncate, saturate size, advance cursor, two-part write."""
    raw = bytearray(raw)
    sig, start, size = struct.unpack_from('<III', raw)
    cap = len(raw) - 12
    if not payload:
        return bytes(raw)
    keep = payload[-cap:]
    size = min(cap, size + len(keep))
    cursor = (start + len(keep)) % cap
    remaining = min(cap - start, len(keep))
    raw[12 + start:12 + start + remaining] = keep[:remaining]
    raw[12:12 + len(keep) - remaining] = keep[remaining:]
    struct.pack_into('<III', raw, 0, sig, cursor, size)
    return bytes(raw)


def reference_save_old(raw):
    _, start, size = struct.unpack_from('<III', raw)
    return raw[12 + start:12 + size] + raw[12:12 + start]


class PstoreRingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.path = Path(cls.tmp.name)
        subprocess.run(['cc', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror',
                        '-ffreestanding', '-fno-builtin', '-shared', '-fPIC',
                        str(ROOT / 'ace/pstore_ring.c'), '-o', str(cls.path / 'ring.so')], check=True)
        cls.lib = C.CDLL(str(cls.path / 'ring.so'))
        cls.lib.ace_pstore_ring_validate.argtypes = [C.c_void_p, C.c_size_t, C.c_void_p]
        cls.lib.ace_pstore_ring_append.argtypes = [C.c_void_p, C.c_size_t, C.c_void_p, C.c_size_t]
        cls.lib.ace_pstore_ring_read.argtypes = [C.c_void_p, C.c_size_t, C.c_void_p, C.c_size_t, C.c_void_p]
        for n in ('validate', 'append', 'read'):
            getattr(cls.lib, 'ace_pstore_ring_' + n).restype = C.c_int

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def append(self, buf, payload):
        source = C.create_string_buffer(payload) if payload else None
        return self.lib.ace_pstore_ring_append(buf, len(buf), source, len(payload))

    def read(self, buf):
        out = C.create_string_buffer(len(buf))
        written = C.c_size_t(999)
        self.assertEqual(self.lib.ace_pstore_ring_read(buf, len(buf), out, len(out), C.byref(written)), OK)
        return out.raw[:written.value]

    def test_known_append_wrap_full_and_oversized_vectors(self):
        b = zone(5)
        for payload, expected in [(b'ab', b'ab'), (b'cde', b'abcde'),
                                  (b'XY', b'cdeXY'), (b'01234567', b'34567')]:
            self.assertEqual(self.append(b, payload), OK)
            self.assertEqual(self.read(b), expected)
        self.assertEqual(struct.unpack_from('<I', bytes(b))[0], SIG)
        one = zone(1)
        self.assertEqual(self.append(one, b'abc'), OK)
        self.assertEqual(self.read(one), b'c')

    def test_differential_against_official_completed_call_model(self):
        rng = random.Random(0xace)
        for cap in (1, 2, 3, 4, 5, 7, 8, 17, 64, 257):
            buf = zone(cap)
            model = bytes(buf)
            history = b''
            for _ in range(160):
                payload = rng.randbytes(rng.randrange(0, cap * 3 + 2))
                before = bytes(buf)
                self.assertEqual(self.append(buf, payload), OK)
                model = reference_append(model, payload)
                history = (history + payload)[-cap:]
                self.assertEqual(bytes(buf), model)
                self.assertEqual(self.read(buf), reference_save_old(model))
                self.assertEqual(self.read(buf), history)
                if not payload:
                    self.assertEqual(bytes(buf), before)

    def test_unknown_signature_bad_size_cursor_and_truncated_zone_unchanged(self):
        for sig, start, size in [(0, 0, 0), (SIG ^ 1, 0, 0),
                                 (SIG, 0, 9), (SIG, 3, 2), (SIG, 0xffffffff, 0)]:
            buf = zone(8)
            struct.pack_into('<III', buf, 0, sig, start, size)
            old = bytes(buf)
            info = Info(77, 88, 99)
            self.assertEqual(self.lib.ace_pstore_ring_validate(buf, len(buf), C.byref(info)), HEADER)
            self.assertEqual((info.capacity, info.start, info.size), (77, 88, 99))
            self.assertEqual(self.append(buf, b'x'), HEADER)
            self.assertEqual(bytes(buf), old)
        b = zone(8, b'abc')
        for n in range(13):
            self.assertEqual(self.lib.ace_pstore_ring_validate(b, n, None), ARG)
        self.assertEqual(self.lib.ace_pstore_ring_validate(b, 14, None), HEADER)
        self.assertEqual(self.lib.ace_pstore_ring_append(None, 0, None, 0), ARG)
        self.assertEqual(self.lib.ace_pstore_ring_read(None, 0, None, 0, None), ARG)

    def test_read_accepts_official_bounds_append_refuses_noncanonical_state(self):
        b = zone(8, b'abcd', cursor=1)
        self.assertEqual(self.lib.ace_pstore_ring_validate(b, len(b), None), OK)
        self.assertEqual(self.read(b), b'bcda')
        old = bytes(b)
        self.assertEqual(self.append(b, b'e'), STATE)
        self.assertEqual(bytes(b), old)
        self.assertEqual(self.append(b, b''), OK)
        b = zone(4, b'abcd', cursor=4)
        self.assertEqual(self.read(b), b'abcd')
        self.assertEqual(self.append(b, b'e'), STATE)

    def test_alias_input_metadata_output_and_written_are_rejected(self):
        b = zone(64, b'abcd')
        addr = C.addressof(b)
        before = bytes(b)
        self.assertEqual(self.lib.ace_pstore_ring_append(b, len(b), addr + 12, 2), ALIAS)
        self.assertEqual(self.lib.ace_pstore_ring_append(b, len(b), addr - 1, 2), ALIAS)
        self.assertEqual(self.lib.ace_pstore_ring_validate(b, len(b), addr + 16), ALIAS)
        written = C.c_size_t(99)
        self.assertEqual(self.lib.ace_pstore_ring_read(b, len(b), addr + 12, 4, C.byref(written)), ALIAS)
        out = C.create_string_buffer(32)
        self.assertEqual(self.lib.ace_pstore_ring_read(b, len(b), out, 32, addr + 16), ALIAS)
        self.assertEqual(self.lib.ace_pstore_ring_read(b, len(b), out, 32, C.addressof(out)), ALIAS)
        self.assertEqual(written.value, 99)
        self.assertEqual(bytes(b), before)

    def test_small_output_and_empty_read_contract(self):
        b = zone(8, b'abcd')
        out = C.create_string_buffer(b'ZZ', 2)
        written = C.c_size_t(99)
        self.assertEqual(self.lib.ace_pstore_ring_read(b, len(b), out, 2, C.byref(written)), SPACE)
        self.assertEqual(out.raw, b'ZZ')
        self.assertEqual(written.value, 99)
        empty = zone(1)
        self.assertEqual(self.lib.ace_pstore_ring_read(empty, len(empty), None, 0, C.byref(written)), OK)
        self.assertEqual(written.value, 0)
        self.assertEqual(self.lib.ace_pstore_ring_read(empty, len(empty), None, 0, None), ARG)
        self.assertEqual(self.lib.ace_pstore_ring_append(b, len(b), None, 1), ARG)

    def test_range_overflow_and_misaligned_typed_outputs_fail_without_access(self):
        b = zone(8)
        high = (1 << (8 * C.sizeof(C.c_void_p))) - 1
        self.assertEqual(self.lib.ace_pstore_ring_validate(b, (1 << 31) + 12, None), RANGE)
        self.assertEqual(self.lib.ace_pstore_ring_validate(high - 7, 20, None), RANGE)
        self.assertEqual(self.lib.ace_pstore_ring_append(b, len(b), high - 3, 8), RANGE)
        self.assertEqual(self.lib.ace_pstore_ring_read(b, len(b), None, 0, high - 7), RANGE)
        out = C.create_string_buffer(64)
        self.assertEqual(self.lib.ace_pstore_ring_validate(b, len(b), C.addressof(out) + 1), ARG)
        self.assertEqual(self.lib.ace_pstore_ring_read(b, len(b), out, 32, C.addressof(out) + 33), ARG)

    def test_byte_unaligned_zone_is_supported(self):
        raw = bytes(zone(7))
        backing = C.create_string_buffer(b'!' + raw + b'?')
        ptr = C.addressof(backing) + 1
        data = C.create_string_buffer(b'hello')
        self.assertEqual(self.lib.ace_pstore_ring_append(ptr, len(raw), data, 5), OK)
        self.assertEqual(backing.raw[0:1], b'!')
        self.assertEqual(backing.raw[1 + len(raw):2 + len(raw)], b'?')
        out = C.create_string_buffer(7); written = C.c_size_t()
        self.assertEqual(self.lib.ace_pstore_ring_read(ptr, len(raw), out, 7, C.byref(written)), OK)
        self.assertEqual(out.raw[:written.value], b'hello')

    def test_invalid_pointers_are_rejected_before_arithmetic_under_ubsan(self):
        harness = self.path / 'ubsan.c'
        harness.write_text("""#include "pstore_ring.h"
int main(void) {
 if (ace_pstore_ring_append(0, 0, 0, 0) != ACE_PSTORE_RING_E_ARGUMENT) return 1;
 if (ace_pstore_ring_read(0, 0, 0, 0, 0) != ACE_PSTORE_RING_E_ARGUMENT) return 2;
 if (ace_pstore_ring_validate((void *)(UINTPTR_MAX - 7), 20, 0) != ACE_PSTORE_RING_E_RANGE) return 3;
 return 0;
}
""")
        executable = self.path / 'ubsan'
        subprocess.run(['cc', '-std=c11', '-O1', '-Wall', '-Wextra', '-Werror',
                        '-ffreestanding', '-fno-builtin', '-fsanitize=undefined',
                        '-fno-sanitize-recover=all', '-I', str(ROOT / 'ace'),
                        str(ROOT / 'ace/pstore_ring.c'), str(harness),
                        '-o', str(executable)], check=True)
        completed = subprocess.run([str(executable)], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, '')

    @unittest.skipUnless(shutil.which('aarch64-linux-gnu-gcc'), 'ARM64 cross compiler unavailable')
    def test_arm64_freestanding_emits_no_undefined_symbols(self):
        obj = self.path / 'ring-arm64.o'
        subprocess.run(['aarch64-linux-gnu-gcc', '-std=c11', '-march=armv8-a',
                        '-O2', '-Wall', '-Wextra', '-Werror', '-ffreestanding',
                        '-fno-builtin', '-fno-stack-protector', '-c',
                        str(ROOT / 'ace/pstore_ring.c'), '-o', str(obj)], check=True)
        undefined = subprocess.check_output(['aarch64-linux-gnu-nm', '-u', str(obj)], text=True)
        self.assertEqual(undefined.strip(), '')


if __name__ == '__main__':
    unittest.main()
