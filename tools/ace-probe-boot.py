#!/usr/bin/env python3
"""Host-only Ace probe gzip/unsigned v4 diagnostic packaging. NEVER flashes.

Default: gzip + evidence manifest. --emit-unsigned-boot also emits a bare
v4 candidate, preserving the stock ramdisk and header except kernel_size,
but omitting the stock AVB footer/metadata. Neither output is authenticated,
hardware-tested, or recommended for a physical boot without record retrieval.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import zlib

REPO = Path(__file__).resolve().parents[1]
STOCK_SHA = '6ab84213977b384d058d3c48545d23654313f5639b7a28fabfb3712dd9c57969'
VENDOR_SHA = 'bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670'
SOURCE_NAMES = {'start.S', 'probe.c', 'linker.ld', 'build.sh', 'verify.py',
                'qemu-mmu-on.S', 'qemu-el2-mmu-on.S'}
CASES = {'el1', 'el2', 'el1-relocated', 'el2-relocated', 'el1-brk-exception',
         'el2-brk-exception', 'el1-mmu-on-rejected', 'el2-mmu-on-rejected'}
PAGE = 4096


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def align(n):
    return (n + PAGE - 1) // PAGE * PAGE


def bounded_read(path, limit):
    with Path(path).open('rb') as f:
        data = f.read(limit + 1)
    require(len(data) <= limit, 'input exceeds size bound')
    return data


def inflate(data, limit=256 * 1024 * 1024):
    require(data[:3] == b'\x1f\x8b\x08', 'kernel must be gzip/deflate')
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    result = d.decompress(data, limit + 1)
    require(len(result) <= limit and d.eof and not d.unused_data,
            'gzip exceeds bound, is truncated, or contains trailing/multiple members')
    return result


def deterministic_gzip(data):
    d = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    body = d.compress(data) + d.flush()
    return (b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff' + body +
            struct.pack('<II', zlib.crc32(data), len(data) & 0xffffffff))


def image_check(image):
    require(64 <= len(image) <= 1024 * 1024, 'unexpected probe Image size')
    require(image[56:60] == b'ARM\x64', 'probe ARM64 Image magic missing')
    offset, size = struct.unpack_from('<QQ', image, 8)
    require(offset == 0x80000 and size == len(image), 'probe Image header size/offset mismatch')


def boot_v4(data, avb_required=True):
    require(len(data) >= PAGE and data[:8] == b'ANDROID!', 'boot header missing')
    ksize, rsize, osversion, hsize = struct.unpack_from('<4I', data, 8)
    version = struct.unpack_from('<I', data, 40)[0]
    sigsize = struct.unpack_from('<I', data, 1580)[0]
    require(version == 4 and hsize == 1584 and not any(data[24:40]),
            'unsupported boot v4 header/reserved fields')
    require(not any(data[hsize:PAGE]) and b'\0' in data[44:1580], 'unexpected header padding/cmdline')
    require(ksize > 0 and rsize > 0 and sigsize == PAGE, 'unexpected kernel/ramdisk/signature geometry')
    roff = PAGE + align(ksize)
    soff = roff + align(rsize)
    end = soff + sigsize
    require(end <= len(data), 'truncated boot payload')
    require(not any(data[PAGE + ksize:roff]) and not any(data[roff + rsize:soff]),
            'unexpected payload padding')
    # This exact OEM boot has a zero legacy GKI signature area, not a certificate.
    require(not any(data[soff:end]), 'unsupported nonzero legacy boot signature')
    avb = None
    if avb_required:
        require(len(data) >= end + 64 and data[-64:-60] == b'AVBf', 'AVB footer missing')
        _, major, minor, original, meta, msize, reserved = struct.unpack('>4sIIQQQ28s', data[-64:])
        require((major, minor) == (1, 0) and not any(reserved), 'unsupported AVB footer')
        require(original == end and original <= meta and msize >= 256 and
                meta + msize <= len(data) - 64, 'AVB bounds/payload mismatch')
        require(data[meta:meta + 4] == b'AVB0' and not any(data[end:meta]), 'AVB metadata/padding invalid')
        avb = {'original_image_size': original, 'vbmeta_offset': meta, 'vbmeta_size': msize,
               'authentication_verified': False}
    else:
        require(len(data) == end, 'unsigned bare v4 image must end exactly at signature area')
    return {'header_version': version, 'header_size': hsize, 'os_version_raw': osversion,
            'kernel_offset': PAGE, 'kernel_bytes': ksize, 'ramdisk_offset': roff,
            'ramdisk_bytes': rsize, 'signature_offset': soff, 'signature_bytes': sigsize,
            'legacy_signature_all_zero': True, 'payload_end': end, 'avb': avb}


def validate_probe(image, report, source_dir):
    image_check(image)
    require(isinstance(report, dict), 'probe evidence must be an object')
    require(report.get('status') == 'pass' and report.get('record_version') == 2,
            'probe evidence must be passing record v2')
    require(report.get('image_sha256') == sha(image), 'probe image/evidence hash mismatch')
    cases = report.get('cases', [])
    require(isinstance(cases, list) and all(isinstance(c, dict) for c in cases), 'invalid probe cases')
    require(len(cases) == len(CASES) and {c.get('case') for c in cases} == CASES and
            all(c.get('pass') is True for c in cases), 'probe requires all eight distinct passing QEMU cases')
    inputs = report.get('input_sha256', {})
    require(isinstance(inputs, dict) and set(inputs) == SOURCE_NAMES, 'probe source evidence set mismatch')
    for name in SOURCE_NAMES:
        require(sha(bounded_read(source_dir / name, 1024 * 1024)) == inputs[name],
                'probe source changed: ' + name)


def unsigned_boot(stock, layout, compressed):
    decoded = inflate(compressed, 1024 * 1024)
    image_check(decoded)
    header = bytearray(stock[:PAGE])
    struct.pack_into('<I', header, 8, len(compressed))
    ramdisk = stock[layout['ramdisk_offset']:layout['ramdisk_offset'] + layout['ramdisk_bytes']]
    signature = stock[layout['signature_offset']:layout['payload_end']]
    result = bytes(header) + compressed + bytes(align(len(compressed)) - len(compressed))
    result += ramdisk + bytes(align(len(ramdisk)) - len(ramdisk)) + signature
    rebuilt = boot_v4(result, avb_required=False)
    require(inflate(result[PAGE:PAGE + rebuilt['kernel_bytes']], 1024 * 1024) == inflate(compressed, 1024 * 1024),
            'rebuilt kernel differs')
    require(result[rebuilt['ramdisk_offset']:rebuilt['ramdisk_offset'] + len(ramdisk)] == ramdisk,
            'rebuilt ramdisk differs')
    return result, rebuilt


def output_path(path):
    original = path.expanduser()
    require(not original.exists() and not original.is_symlink(), 'output already exists')
    resolved = original.resolve()
    require(resolved.is_relative_to(REPO / 'research'), 'output must be inside ignored research/')
    p = subprocess.run(['git', '-C', str(REPO), 'check-ignore', '--quiet', '--',
                        str(resolved.relative_to(REPO))], capture_output=True, timeout=10)
    require(p.returncode == 0, 'output is not git-ignored')
    return resolved


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--stock-boot', type=Path, default=REPO / 'research/ace-20261019/images/boot.img')
    ap.add_argument('--stock-vendor-boot', type=Path, default=REPO / 'research/ace-20261019/images/vendor_boot.img')
    ap.add_argument('--probe', type=Path, default=REPO / 'research/ace-offline/probe/probe.Image')
    ap.add_argument('--evidence', type=Path, default=REPO / 'research/ace-offline/probe/verification.json')
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--emit-unsigned-boot', action='store_true', help='Also emit UNTESTED bare v4 image without any AVB authentication')
    args = ap.parse_args(argv)
    try:
        out = output_path(args.output_dir)
        stock = bounded_read(args.stock_boot, 64 * 1024 * 1024)
        vendor = bounded_read(args.stock_vendor_boot, 64 * 1024 * 1024)
        require(sha(stock) == STOCK_SHA and sha(vendor) == VENDOR_SHA, 'stock boot/vendor_boot SHA pin mismatch')
        layout = boot_v4(stock)
        original = inflate(stock[PAGE:PAGE + layout['kernel_bytes']])
        require(original[56:60] == b'ARM\x64', 'stock gzip is not an ARM64 Image')
        image = bounded_read(args.probe, 1024 * 1024)
        evidence_bytes = bounded_read(args.evidence, 1024 * 1024)
        evidence = json.loads(evidence_bytes)
        validate_probe(image, evidence, REPO / 'probe')
        compressed = deterministic_gzip(image)
        require(inflate(compressed) == image, 'gzip roundtrip differs')
        report = {'schema_version': 1, 'status': 'UNTESTED diagnostic packaging only',
                  'ios_deployable': False, 'hardware_execution_verified': False,
                  'hardware_test_recommended': False,
                  'inputs': {'stock_boot_sha256': sha(stock), 'stock_vendor_boot_sha256': sha(vendor),
                             'probe_sha256': sha(image), 'probe_evidence_sha256': sha(evidence_bytes),
                             'probe_source_sha256': evidence['input_sha256']},
                  'stock_layout': layout, 'stock_raw_kernel_sha256': sha(original),
                  'gzip': {'bytes': len(compressed), 'sha256': sha(compressed), 'mtime': 0,
                           'os_byte': 255, 'zlib_version': zlib.ZLIB_VERSION},
                  'vendor_boot': 'Required original is hash-bound; never modified or copied to a candidate',
                  'authentication': {'candidate_signed': False, 'original_legacy_gki_area': '4096 zero bytes; not a valid signature',
                                     'original_avb': 'Stock AVB RSA authentication is not transferable to changed kernel',
                                     'candidate_avb': 'No AVB metadata/footer emitted; original parent vbmeta cannot authenticate candidate'},
                  'observability': {'record': 'v2 120B in image-local RAM; no persistence/cache flush guarantee',
                                    'missing': ['hardware load/record physical address evidence', 'UART/display/USB logging',
                                                'RAM record retrieval after halt/reset', 'safe memory window and bootloader acceptance'],
                                    'recommendation': 'Do not physically flash until a proven observation/retrieval path exists'},
                  'qemu_scope': 'Packaging does not emulate LK/ATF, bootloader authentication, or MT6895 hardware'}
        files = {'probe.Image.gz': compressed}
        if args.emit_unsigned_boot:
            candidate, candidate_layout = unsigned_boot(stock, layout, compressed)
            files['UNTESTED-unsigned-probe-boot.img'] = candidate
            report['candidate'] = {'bytes': len(candidate), 'sha256': sha(candidate), 'layout': candidate_layout,
                                   'header_changed_fields': ['kernel_size'], 'ramdisk_sha256': sha(stock[layout['ramdisk_offset']:layout['ramdisk_offset'] + layout['ramdisk_bytes']]),
                                   'note': 'Bare v4 file, not a signed/padded partition image; physical acceptance untested'}
        out.mkdir(mode=0o700, parents=True, exist_ok=False)
        for name, data in files.items():
            with (out / name).open('xb') as f:
                (out / name).chmod(0o600)
                f.write(data)
        with (out / 'manifest.json').open('x') as f:
            (out / 'manifest.json').chmod(0o600)
            json.dump(report, f, indent=2)
            f.write('\n')
        print(json.dumps({'status': report['status'], 'ios_deployable': False,
                          'hardware_test_recommended': False, 'files': list(files)}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error, zlib.error, subprocess.SubprocessError) as exc:
        print('Diagnostic packaging failed: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
