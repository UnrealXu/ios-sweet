#!/usr/bin/env python3
"""Host-only preflight: verify assets and report unresolved Ace deployment facts.

This program never invokes ADB, fastboot, mount, or a phone-writing operation.
"""
import argparse
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import struct
import sys
import zlib

REPO = Path(__file__).resolve().parents[1]
REQUIRED = ['adb', 'fastboot', 'aarch64-linux-gnu-gcc', 'aarch64-linux-gnu-ld',
            'clang', 'ld.lld', 'llvm-nm', 'qemu-system-aarch64', 'gdb-multiarch',
            'dtc', 'mkbootimg', 'mkfs.hfsplus', 'fsck.hfsplus', 'img2simg',
            'simg2img', 'apfs-fuse', 'lzfse', 'gh', 'ninja', 'make']


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, REPO / 'tools' / filename)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as f:
        while data := f.read(8 * 1024 * 1024):
            digest.update(data)
    return digest.hexdigest()


def kernel_config(compressed):
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
        image = stream.read(256 * 1024 * 1024 + 1)
    if len(image) > 256 * 1024 * 1024:
        raise ValueError('kernel decompression exceeds limit')
    marker = image.find(b'IKCFG_ST')
    if marker < 0:
        raise ValueError('no embedded IKCONFIG')
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    config = decoder.decompress(image[marker + 8:], 4 * 1024 * 1024)
    if not decoder.eof or not decoder.unused_data.startswith(b'IKCFG_ED'):
        raise ValueError('invalid/incomplete embedded IKCONFIG')
    selected = [line for line in config.decode().splitlines() if any(
        option in line for option in ('CONFIG_KEXEC', 'CONFIG_IKCONFIG',
                                     'CONFIG_ARM64_4K_PAGES', 'CONFIG_ARM64_16K_PAGES',
                                     'CONFIG_DEVMEM', 'CONFIG_MODULES=', 'CONFIG_MODULE_SIG'))]
    return {'sha256': hashlib.sha256(config).hexdigest(), 'selected_options': selected,
            'meaning': 'build configuration only; not CPU granule or live execution evidence'}


def boot_v4(data):
    if len(data) < 4096 or data[:8] != b'ANDROID!':
        raise ValueError('not an Android boot image')
    kernel, ramdisk, _, header = struct.unpack_from('<4I', data, 8)
    version = struct.unpack_from('<I', data, 40)[0]
    if version != 4 or header != 1584 or any(data[24:40]):
        raise ValueError('expected standard boot v4 header')
    signature = struct.unpack_from('<I', data, 1580)[0]
    rd_off = 4096 + (kernel + 4095) // 4096 * 4096
    sig_off = rd_off + (ramdisk + 4095) // 4096 * 4096
    if not kernel or sig_off + signature > len(data):
        raise ValueError('boot payload outside image')
    return {'header_version': version, 'kernel_bytes': kernel,
            'ramdisk_bytes': ramdisk, 'signature_bytes': signature,
            'payload_end': sig_off + signature,
            'kernel_sha256': hashlib.sha256(data[4096:4096 + kernel]).hexdigest()}


def sparse_geometry(raw, sparse):
    with sparse.open('rb') as f:
        header = f.read(28)
    if len(header) != 28:
        raise ValueError('truncated sparse header')
    magic, major, minor, file_hdr, chunk_hdr, block, blocks, chunks, checksum = struct.unpack('<IHHHHIIII', header)
    if magic != 0xed26ff3a or major != 1 or file_hdr != 28 or chunk_hdr != 12 or not block or block % 4:
        raise ValueError('invalid sparse header')
    if block * blocks != raw.stat().st_size:
        raise ValueError('sparse logical size differs from raw image')
    return {'version': f'{major}.{minor}', 'logical_bytes': block * blocks,
            'sparse_bytes': sparse.stat().st_size, 'chunks': chunks}


def prepare(repo=REPO):
    profile = json.loads((repo / 'profiles/ace-mt6895.json').read_text())
    report = {'schema_version': 1, 'target': profile['target'],
              'scope': 'host preparation; no phone operation',
              'tools': {n: shutil.which(n) for n in REQUIRED},
              'host_errors': [], 'assets': {},
              'ios_deployable': False, 'deployment_blockers': profile['unresolved']}
    def check(name, function):
        try:
            report['assets'][name] = function()
        except (OSError, ValueError, KeyError, struct.error) as exc:
            report['host_errors'].append(f'{name}: {exc}')
    firmware = repo / 'research/ace-20261019/images'
    diag = module('ace_diag_preflight', 'ace-recovery-diag.py')
    audit = module('ace_dt_preflight', 'ace-dt-audit.py')
    def stock(name):
        data = (firmware / f'{name}.img').read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != profile['source'][name + '_sha256']:
            raise ValueError('original image SHA256 differs from pin')
        footer = diag.read_avb_footer(data)
        if name == 'boot':
            info = boot_v4(data)
            info['embedded_config'] = kernel_config(data[4096:4096 + info['kernel_bytes']])
        else:
            parsed = diag.read_vendor(data)
            info = {'header_version': 4, 'dtb_bytes': len(parsed['dtb']),
                    'ramdisk_bytes': len(parsed['ramdisk']),
                    'bootconfig_bytes': len(parsed['bootconfig'])}
        if name == 'boot' and info['payload_end'] > footer['original_image_size']:
            raise ValueError('boot payload overlaps AVB metadata')
        return dict(bytes=len(data), sha256=actual, footer=footer, **info)
    check('stock_boot', lambda: stock('boot'))
    check('stock_vendor_boot', lambda: stock('vendor_boot'))
    def dtb():
        data = (firmware / 'vendor-boot-dtb.bin').read_bytes()
        if hashlib.sha256(data).hexdigest() != profile['source']['dtb_sha256']:
            raise ValueError('firmware DTB SHA256 differs from pin')
        result = audit.audit(data)
        errors = audit.check_profile(result, profile)
        if errors:
            raise ValueError('; '.join(errors))
        return {'sha256': result['source_sha256'], 'profile_matches': True,
                'hardware_execution_verified': False}
    check('firmware_dtb', dtb)
    def root():
        base = repo / 'research/ipsw-x'
        info = sparse_geometry(base / 'ios16-root.img', base / 'ios16-root.simg')
        hashes = {}
        for line in (base / 'ROOT-SHA256SUMS').read_text().splitlines():
            digest, filename = line.split()
            if filename not in ('ios16-root.img', 'ios16-root.simg') or len(digest) != 64:
                raise ValueError('invalid root checksum manifest')
            int(digest, 16)
            hashes[filename] = digest
        if set(hashes) != {'ios16-root.img', 'ios16-root.simg'}:
            raise ValueError('incomplete root checksum manifest')
        contents = json.loads((base / 'root-content-verification.json').read_text())
        if contents['version']['ProductBuildVersion'] != '20H392':
            raise ValueError('unexpected iOS build')
        return dict(**info, recorded_sha256=hashes,
                    hash_check='previous verified preparation; not rehashed by this preflight',
                    configuration='SWEET reference userland; not Ace hardware validation')
    check('ios_root', root)
    def probe():
        base = repo / 'research/ace-offline/probe'
        result = json.loads((base / 'verification.json').read_text())
        if result['status'] != 'pass' or result['image_sha256'] != sha256(base / 'probe.Image'):
            raise ValueError('probe result/image mismatch')
        names = {'start.S', 'probe.c', 'linker.ld', 'build.sh', 'verify.py',
                 'qemu-mmu-on.S', 'qemu-el2-mmu-on.S'}
        inputs = result.get('input_sha256', {})
        if set(inputs) != names or any(sha256(repo / 'probe' / n) != inputs[n] for n in names):
            raise ValueError('probe sources changed or are not bound to verification')
        expected_cases = {'el1', 'el2', 'el1-relocated', 'el2-relocated',
                          'el1-brk-exception', 'el2-brk-exception',
                          'el1-mmu-on-rejected', 'el2-mmu-on-rejected'}
        cases = result.get('cases', [])
        if (result.get('record_version') != 2 or len(cases) != len(expected_cases)
                or {c['case'] for c in cases} != expected_cases
                or not all(c.get('pass') is True for c in cases)):
            raise ValueError('probe v2 EL1/EL2 execution evidence incomplete')
        return {'bytes': (base / 'probe.Image').stat().st_size,
                'sha256': result['image_sha256'], 'scope': result['scope'],
                'cases': [c['case'] for c in result['cases'] if c['pass']]}
    check('cpu_probe', probe)
    def baseline():
        result = json.loads((repo / 'research/ci-0081/qemu-baseline/verification.json').read_text())
        if sha256(repo / 'xnu/out-0081/kernel.development.sweet') != result['kernel_sha256']:
            raise ValueError('reference kernel/result mismatch')
        return {'ci_run': result['ci_run'], 'kernel_sha256': result['kernel_sha256'],
                'original_panic_observed': result['original_run']['panic_observed'],
                'trace_mode': result['trace_mode_run'], 'scope': result['scope']}
    check('qemu_reference', baseline)
    report['host_errors'] += [f'missing tool: {n}' for n, path in report['tools'].items() if path is None]
    report['host_preparation_passed'] = not report['host_errors']
    report['next_action'] = 'Connect Ace; run read-only collector; resolve live hardware/entry evidence before any image write'
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New private JSON file under ignored research/')
    parser.add_argument('--require-ios-deployable', action='store_true', help='Return 2 while Ace hardware/platform remains unresolved')
    args = parser.parse_args()
    if args.output:
        collect = module('ace_collect_preflight', 'ace-collect.py')
        try:
            args.output = collect.validate_output(args.output)
        except collect.CollectionError as exc:
            parser.error(str(exc))
    report = prepare()
    text = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f:
            args.output.chmod(0o600)
            f.write(text)
    print(json.dumps({k: report[k] for k in ('host_preparation_passed', 'host_errors', 'ios_deployable', 'deployment_blockers')}, indent=2))
    if not report['host_preparation_passed']:
        return 1
    return 2 if args.require_ios_deployable and not report['ios_deployable'] else 0


if __name__ == '__main__':
    sys.exit(main())
