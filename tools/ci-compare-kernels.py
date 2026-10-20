#!/usr/bin/env python3
"""Compare linked ARM64 Mach-O sections for same-source cache audits.

CTF type metadata may vary between independent builds. It is reported, never
silently treated as byte-identical. Every other section, including zerofill
layout, must match. This is not a hardware-boot or functional equivalence test.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct


def sections(raw):
    if len(raw) < 32 or struct.unpack_from('<II', raw) != (0xfeedfacf, 0x100000c):
        raise ValueError('expected little-endian ARM64 Mach-O')
    count, length = struct.unpack_from('<II', raw, 16)
    end = 32 + length
    if count > 1024 or end > len(raw):
        raise ValueError('load commands out of bounds')
    offset, result = 32, {}
    for _ in range(count):
        if offset + 8 > end:
            raise ValueError('truncated load command')
        command, size = struct.unpack_from('<II', raw, offset)
        if size < 8 or offset + size > end:
            raise ValueError('load command out of bounds')
        if command == 0x19:
            if size < 72:
                raise ValueError('truncated segment')
            nsects = struct.unpack_from('<I', raw, offset + 64)[0]
            if 72 + 80 * nsects > size:
                raise ValueError('section table out of bounds')
            for i in range(nsects):
                start = offset + 72 + 80 * i
                section = raw[start:start+16].split(b'\0')[0].decode('ascii')
                segment = raw[start+16:start+32].split(b'\0')[0].decode('ascii')
                address, length, location, alignment = struct.unpack_from('<QQII', raw, start + 32)
                flags = struct.unpack_from('<I', raw, start + 64)[0]
                zerofill = (flags & 255) in (1, 12, 18)
                if not zerofill and location + length > len(raw):
                    raise ValueError('section contents out of bounds')
                key = segment + ',' + section
                if key in result:
                    raise ValueError('duplicate section')
                result[key] = dict(address=address, bytes=length, alignment=alignment,
                    flags=flags, zerofill=zerofill,
                    sha256=None if zerofill else hashlib.sha256(raw[location:location+length]).hexdigest())
        offset += size
    if offset != end or not result:
        raise ValueError('incomplete load commands or missing sections')
    return result


def compare(left, right):
    a, b = sections(left), sections(right)
    metadata = {key for key in a.keys() | b.keys() if key.startswith('__CTF,')}
    runtime = (a.keys() | b.keys()) - metadata
    mismatches = [key for key in sorted(runtime) if a.get(key) != b.get(key)]
    return dict(byte_identical=left == right,
        left_sha256=hashlib.sha256(left).hexdigest(), right_sha256=hashlib.sha256(right).hexdigest(),
        non_ctf_sections_identical=not mismatches, checked_sections=len(runtime),
        mismatches=mismatches, excluded_type_metadata={key: dict(left=a.get(key), right=b.get(key))
                                                     for key in sorted(metadata)},
        limitation='same-source section audit only; no hardware/iOS success claim')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left', type=Path)
    parser.add_argument('right', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = compare(args.left.read_bytes(), args.right.read_bytes())
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    raise SystemExit(0 if result['non_ctf_sections_identical'] else 1)


if __name__ == '__main__':
    main()
