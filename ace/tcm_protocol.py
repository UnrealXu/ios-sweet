"""Offline Synaptics TCM framing helpers, not a hardware touch driver.

Protocol references: OnePlusOSS android_vendor_mediatek_kernel_modules_mt6895,
commit 0c04020c19a68356afd49ce24f2ff95ee56c37e0,
vendor/oplus/kernel/touchpanel/oplus_touchscreen_v2/Synaptics/
Syna_tcm_S3910/synaptics_tcm_S3910.{c,h}:
syna_tcm_read_message, syna_tcm_continued_read, syna_get_report_data.

Only framing and bounded LSB-first fields are implemented. Touch reports use
dynamic report descriptors: no coordinate layout, firmware update, SPI, IRQ,
device access or driver registration is implemented here. Malformed/out-of-range
fields raise errors instead of the vendor helper's permissive zero-fill.
"""
from dataclasses import dataclass
from typing import Iterable

MESSAGE_MARKER = 0xA5
MESSAGE_PADDING = 0x5A
MESSAGE_HEADER_SIZE = 4
STATUS_CONTINUED_READ = 0x03
MAX_PAYLOAD = 0xFFFF
MTK_READ_CHUNK_SIZE = 2048


@dataclass(frozen=True)
class Message:
    code: int
    payload: bytes
    padding_synthesized: bool = False
    predictive_bytes_discarded: int = 0


def _payload_length(header: bytes, max_payload: int) -> int:
    if not isinstance(max_payload, int) or not 0 <= max_payload <= MAX_PAYLOAD:
        raise ValueError("max_payload must be in 0..65535")
    if len(header) < MESSAGE_HEADER_SIZE or header[0] != MESSAGE_MARKER:
        raise ValueError("invalid or truncated TCM header")
    if header[1] == STATUS_CONTINUED_READ:
        raise ValueError("a continuation is not an initial message header")
    size = int.from_bytes(header[2:4], "little")
    if size > max_payload:
        raise ValueError("payload exceeds configured limit")
    return size


def decode_frame(frame: bytes, *, max_payload: int = MAX_PAYLOAD) -> Message:
    """Validate one exact, already reassembled header+payload+padding frame."""
    size = _payload_length(frame, max_payload)
    if len(frame) != MESSAGE_HEADER_SIZE + size + 1:
        raise ValueError("frame size does not match header")
    if frame[-1] != MESSAGE_PADDING:
        raise ValueError("invalid TCM padding")
    return Message(frame[1], bytes(frame[MESSAGE_HEADER_SIZE:-1]))


def reassemble_reads(initial: bytes, continuations: Iterable[bytes] = (), *,
                     chunk_size: int = MTK_READ_CHUNK_SIZE,
                     max_payload: int = MAX_PAYLOAD) -> Message:
    """Reassemble saved SPI read transactions; performs no transport operation.

    Continuations carry A5/03 and at most chunk_size-2 data bytes. Predictive
    initial reads can contain bytes beyond this message; their number is
    reported, not interpreted as a following frame. The vendor read algorithm
    synthesizes padding when exactly one byte remains; this fact is explicit
    in the result and does not prove padding was received from the device.
    """
    if not isinstance(chunk_size, int) or not 3 <= chunk_size <= MTK_READ_CHUNK_SIZE:
        raise ValueError("chunk_size must be in 3..2048")
    if len(initial) > chunk_size:
        raise ValueError("initial transaction exceeds chunk size")
    size = _payload_length(initial, max_payload)
    total = MESSAGE_HEADER_SIZE + size + 1
    result = bytearray(initial[:total])
    extra = max(0, len(initial) - total)
    synthesized = False
    reads = iter(continuations)
    # This loop is bounded by the 16-bit payload length and positive chunk size.
    while len(result) < total:
        remaining = total - len(result)
        count = min(remaining, chunk_size - 2)
        if count == 1:
            # Matches the driver's one-byte-tail path. It is padding only when
            # the whole message has exactly one byte left; a tiny chunk size
            # that would synthesize payload is rejected.
            if remaining != 1:
                raise ValueError("chunk size would synthesize payload bytes")
            result.append(MESSAGE_PADDING)
            synthesized = True
            continue
        try:
            chunk = next(reads)
        except StopIteration:
            raise ValueError("missing continuation transaction") from None
        if len(chunk) != count + 2:
            raise ValueError("continuation size does not match expected transfer")
        if chunk[0:2] != bytes((MESSAGE_MARKER, STATUS_CONTINUED_READ)):
            raise ValueError("invalid continuation header")
        result.extend(chunk[2:])
    try:
        next(reads)
    except StopIteration:
        pass
    else:
        raise ValueError("unexpected continuation transaction")
    frame = decode_frame(result, max_payload=max_payload)
    return Message(frame.code, frame.payload, synthesized, extra)


def extract_lsb_bits(payload: bytes, offset: int, width: int) -> int:
    """Extract a scalar report field; dynamic descriptor decoding is separate."""
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("bit offset must be nonnegative")
    if not isinstance(width, int) or not 1 <= width <= 32:
        raise ValueError("field width must be in 1..32")
    if offset + width > len(payload) * 8:
        raise ValueError("field exceeds payload")
    start = offset // 8
    shift = offset % 8
    end = (offset + width + 7) // 8
    value = int.from_bytes(payload[start:end], "little")
    return (value >> shift) & ((1 << width) - 1)

