"""Host-only tests for framing; no SPI, ADB or firmware commands are used."""
import random
import unittest

from ace.tcm_protocol import (decode_frame, extract_lsb_bits, reassemble_reads)


def frame(payload, code=0x11):
    return bytes((0xA5, code)) + len(payload).to_bytes(2, "little") + payload + b"\x5a"


class TcmProtocolTests(unittest.TestCase):
    def test_exact_frame_and_zero_payload(self):
        self.assertEqual(decode_frame(frame(b"abc")).payload, b"abc")
        self.assertEqual(decode_frame(frame(b"")).payload, b"")
        self.assertEqual(decode_frame(frame(b"abc", 0x10)).code, 0x10)

    def test_header_padding_length_and_payload_limit_rejections(self):
        cases = [b"", b"\xa5\x11\x00", b"\x00\x11\x00\x00\x5a",
                 b"\xa5\x03\x00\x00\x5a", frame(b"x")[:-1],
                 frame(b"x") + b"\x00", frame(b"x")[:-1] + b"\x00"]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ValueError):
                decode_frame(data)
        with self.assertRaises(ValueError):
            decode_frame(frame(b"abc"), max_payload=2)

    def test_little_endian_header_length(self):
        data = bytes(range(256)) + b"x"
        self.assertEqual(decode_frame(frame(data)).payload, data)

    def test_reassembly_strips_continuation_headers(self):
        data = frame(b"0123456789abcdef")
        result = reassemble_reads(data[:9], [b"\xa5\x03" + data[9:]])
        self.assertEqual(result.payload, b"0123456789abcdef")
        self.assertFalse(result.padding_synthesized)

    def test_multiple_chunks_and_predictive_overread(self):
        payload = bytes(range(256)) * 24
        data = frame(payload)
        initial = data[:9]
        chunks = [b"\xa5\x03" + data[i:i+2046]
                  for i in range(9, len(data), 2046)]
        result = reassemble_reads(initial, chunks)
        self.assertEqual(result.payload, payload)
        result = reassemble_reads(frame(b"x") + b"extra")
        self.assertEqual(result.predictive_bytes_discarded, 5)
        self.assertEqual(result.payload, b"x")

    def test_padding_only_tail_is_marked_synthesized(self):
        result = reassemble_reads(frame(b"abc")[:-1])
        self.assertTrue(result.padding_synthesized)
        self.assertEqual(result.payload, b"abc")

    def test_bad_missing_extra_and_wrong_size_continuations(self):
        data = frame(b"0123456789abcdef")
        for chunks in ([], [b"\xa5\x04" + data[9:]],
                       [b"\x00\x03" + data[9:]],
                       [b"\xa5\x03" + data[9:-1]],
                       [b"\xa5\x03" + data[9:], b"\xa5\x03"]):
            with self.subTest(chunks=chunks), self.assertRaises(ValueError):
                reassemble_reads(data[:9], chunks)
        with self.assertRaises(ValueError):
            reassemble_reads(data[:9], chunk_size=3)

    def test_transaction_and_payload_bounds(self):
        with self.assertRaises(ValueError):
            reassemble_reads(b"x" * 2049)
        for size in (0, 2, 2049):
            with self.assertRaises(ValueError):
                reassemble_reads(frame(b"x"), chunk_size=size)
        with self.assertRaises(ValueError):
            reassemble_reads(frame(b"x"), max_payload=0)

    def test_scalar_fields_cross_byte_boundaries(self):
        payload = bytes((0xAB, 0xCD, 0xEF, 0x12, 0x34))
        self.assertEqual(extract_lsb_bits(payload, 0, 4), 0xB)
        self.assertEqual(extract_lsb_bits(payload, 4, 12), 0xCDA)
        self.assertEqual(extract_lsb_bits(payload, 8, 16), 0xEFCD)
        self.assertEqual(extract_lsb_bits(payload, 8, 32), 0x3412EFCD)

    def test_fields_against_individual_bit_oracle(self):
        rng = random.Random(3910)
        for _ in range(5000):
            payload = rng.randbytes(rng.randrange(5, 64))
            width = rng.randrange(1, 33)
            offset = rng.randrange(len(payload) * 8 - width + 1)
            expected = sum(((payload[(offset+i)//8] >> ((offset+i) % 8)) & 1) << i
                           for i in range(width))
            self.assertEqual(extract_lsb_bits(payload, offset, width), expected)

    def test_reject_out_of_bounds_field_instead_of_vendor_zero_fill(self):
        for offset, width in ((-1, 4), (0, 0), (0, 33), (7, 2)):
            with self.subTest(offset=offset, width=width), self.assertRaises(ValueError):
                extract_lsb_bits(b"x", offset, width)


if __name__ == "__main__":
    unittest.main()

