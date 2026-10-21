#!/usr/bin/env python3
"""Bounded QEMU ordinary-RAM fixtures for optional entry logging; no device use."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess

if not __debug__:
    raise RuntimeError('Verification requires Python assertions; optimized execution is refused')

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research/ace-entry-pmsg-20261019'
RAM = 0x43000000  # QEMU test RAM only; NEVER an Ace hardware default.
DEFAULT_SHA = 'ff298998dfbc9b05a26904b095dabd90fb75f2293fa3abd31e6788d6ad965838'
SENTINEL = 0x7fffffff


def fixture(length, initial=b'old-log\n', start=None, signature=0x43474244):
    capacity = length - 12
    assert len(initial) <= capacity
    return struct.pack('<III', signature, len(initial) if start is None else start,
                       len(initial)) + initial + bytes(capacity - len(initial))


def model_append(raw, text):
    data = bytearray(raw)
    signature, start, size = struct.unpack_from('<III', data)
    capacity = len(data) - 12
    tail = text[-capacity:]
    for i, byte in enumerate(tail):
        data[12 + (start + i) % capacity] = byte
    struct.pack_into('<III', data, 0, signature, (start + len(tail)) % capacity,
                     min(capacity, size + len(tail)))
    return bytes(data)


def main():
    global OUT, RAM
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=OUT)
    parser.add_argument('--ring-address', type=lambda x: int(x, 0), default=RAM)
    parser.add_argument('--ring-bytes', type=lambda x: int(x, 0), default=128)
    parser.add_argument('--qemu-mib', type=int, default=128)
    args = parser.parse_args()
    OUT = args.output_dir.resolve()
    RAM = args.ring_address
    try:
        OUT.relative_to(ROOT / 'research')
    except ValueError:
        parser.error('output must be inside ignored research/')
    ignored = subprocess.run(['git', 'check-ignore', '-q', str(OUT)], cwd=ROOT)
    if ignored.returncode:
        parser.error('output must be git-ignored')
    end = RAM + args.ring_bytes
    # Fixture must avoid the Image, trampoline/page table and QEMU generated DTB.
    dtb = 0x40000000 + min(args.qemu_mib * 1024 * 1024 // 2, 128 * 1024 * 1024)
    if (not 64 <= args.qemu_mib <= 1024 or RAM % 4 or RAM < 0x42000000
            or not 44 <= args.ring_bytes <= 0x7fffffff + 12
            or end > 0x40000000 + args.qemu_mib * 1024 * 1024
            or (RAM < dtb + 0x100000 and dtb < end)):
        parser.error('fixture must fit isolated aligned ordinary QEMU RAM, outside DTB')
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / 'verification.json'
    if report_path.exists():
        report_path.replace(OUT / 'verification.previous.json')
    report_path.write_text('{"status":"incomplete"}\n')
    spec = importlib.util.spec_from_file_location('entry_verify', ROOT / 'ace/entry/verify.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    verifier.REPORT_ROOT = OUT
    cases = []
    builds = {}
    artifacts = {}

    def build(name, size=None, address=RAM):
        verifier.OUT = OUT / name
        command = [str(ROOT / 'ace/entry/build.sh'), '--output-dir', str(verifier.OUT)]
        if size is not None:
            command += ['--pmsg-ram', hex(address), str(size)]
        subprocess.run(command, check=True)
        manifest = json.loads((verifier.OUT / 'build-manifest.json').read_text())
        builds[name] = {'manifest': str((verifier.OUT / 'build-manifest.json').relative_to(OUT)),
                        'manifest_sha256': verifier.sha(verifier.OUT / 'build-manifest.json'),
                        'image_sha256': manifest['image_sha256'], 'pmsg': manifest['pmsg'],
                        'build_argv': command}
        artifacts.update(verifier.build_artifacts())
        return verifier.OUT

    def run(name, virtualization, raw, expected_status, logged=False, mmu=False,
            base=0x40080000, address=RAM):
        item = verifier.case(name, virtualization, base=base, mmu=mmu,
                             memory_fixture=(address, raw), qemu_mib=args.qemu_mib)
        expected = raw
        if logged:
            accepted = b'ACEENTRY accepted EL2\n' if virtualization == 'on' else b'ACEENTRY accepted EL1\n'
            expected = model_append(model_append(raw, accepted), b'ACEENTRY payload EL1\n')
        after = (verifier.OUT / (name + '-ring-after.bin')).read_bytes()
        assert after == expected, name
        assert item['pmsg_status'] == expected_status, item
        item.update(pmsg_fixture_address=hex(address), pmsg_fixture_bytes=len(raw),
                    ring_matches_reference=True, expected_pmsg_status=expected_status,
                    image_sha256=verifier.sha(verifier.OUT / 'entry.Image'),
                    build=verifier.OUT.name)
        cases.append(item)
        artifacts.update(item['artifacts_sha256'])

    build('default')
    assert verifier.sha(verifier.OUT / 'entry.Image') == DEFAULT_SHA
    assert 'bridge_pmsg_results' not in verifier.symbols(verifier.OUT / 'entry.elf')
    run('default-el1-untouched', 'off', fixture(args.ring_bytes), None)
    run('default-el2-untouched', 'on', bytes([0xa5]) * args.ring_bytes, None)

    build('enabled', args.ring_bytes)
    run('log-el1', 'off', fixture(args.ring_bytes), [0, 0], logged=True)
    run('log-el2', 'on', fixture(args.ring_bytes), [0, 0], logged=True)
    run('log-el2-relocated', 'on', fixture(args.ring_bytes), [0, 0], logged=True, base=0x40200000)
    run('bad-signature-el1', 'off', fixture(args.ring_bytes, signature=0), [-3, -3])
    run('bad-signature-el2', 'on', fixture(args.ring_bytes, signature=0), [-3, -3])
    run('bad-cursor-el2', 'on', fixture(args.ring_bytes, initial=b'12', start=3), [-3, -3])
    run('noncanonical-el2', 'on', fixture(args.ring_bytes, initial=b'1234', start=1), [-4, -4])
    run('mmu-el1-refused', 'off', fixture(args.ring_bytes), [SENTINEL, SENTINEL], mmu=True)
    run('mmu-el2-refused', 'on', fixture(args.ring_bytes), [SENTINEL, SENTINEL], mmu=True)

    build('short', 44)
    run('wrap-el1', 'off', fixture(44, initial=bytes(range(32)), start=29), [0, 0], logged=True)
    run('wrap-el2', 'on', fixture(44, initial=bytes(range(32)), start=29), [0, 0], logged=True)

    build('image-alias', 128, address=0x40080000)
    run('image-alias-refused', 'on', (verifier.OUT / 'entry.Image').read_bytes()[:128],
        [-2, -2], address=0x40080000)

    report = {'status': 'pass', 'scope': 'QEMU caller-owned ordinary-RAM pmsg fixtures only; NOT physical Ace, LK/ATF, reset retention or iOS',
              'sources': verifier.source_hashes(), 'default_image_sha256': DEFAULT_SHA,
              'fixture_configuration': {'address': hex(RAM), 'bytes': args.ring_bytes, 'qemu_mib': args.qemu_mib},
              'default_image_unchanged': True, 'builds': builds, 'cases': cases,
              'artifacts_sha256': artifacts,
              'not_tested': ['Physical RAM ownership/access and ECC configuration',
                             'Real boot/reset/retrieval paths', 'Cache persistence',
                             'EL0/EL3 or D-cache-on refusal', 'XNU/iOS']}
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'cases': len(cases), 'default_image_unchanged': True}))


if __name__ == '__main__':
    main()
