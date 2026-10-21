#!/usr/bin/env python3
"""Host-only evidence-bound ACEENTRY gzip / optional unsigned boot-v4 wrapper.

No transport or partition operation is implemented. Default output is gzip plus
manifest. An explicit flag adds an UNTESTED bare v4 review candidate. This is an
entry bridge and register probe, not XNU or iOS. QEMU ordinary-RAM logging tests
do not validate physical pstore addresses, persistence or bootloader acceptance.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import struct
import sys
import zlib

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ace_probe_pack", REPO / "tools/ace-probe-boot.py")
pack = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pack)

DEFAULT_CASES = {"el1-pass", "el2-to-el1", "el2-relocated", "el2-mmu-rejected"}
DEFAULT_IMAGE_SHA = 'ff298998dfbc9b05a26904b095dabd90fb75f2293fa3abd31e6788d6ad965838'
# Fixed from the verifier's source matrix, never selected by an input report.
PMSG_MATRIX = {
    'default-el1-untouched': ('default', 4, None, False),
    'default-el2-untouched': ('default', 8, None, False),
    'log-el1': ('enabled', 4, [0, 0], True),
    'log-el2': ('enabled', 8, [0, 0], True),
    'log-el2-relocated': ('enabled', 8, [0, 0], True),
    'bad-signature-el1': ('enabled', 4, [-3, -3], False),
    'bad-signature-el2': ('enabled', 8, [-3, -3], False),
    'bad-cursor-el2': ('enabled', 8, [-3, -3], False),
    'noncanonical-el2': ('enabled', 8, [-4, -4], False),
    'mmu-el1-refused': ('enabled', 4, [0x7fffffff, 0x7fffffff], False),
    'mmu-el2-refused': ('enabled', 8, [0x7fffffff, 0x7fffffff], False),
    'wrap-el1': ('short', 4, [0, 0], True),
    'wrap-el2': ('short', 8, [0, 0], True),
    'image-alias-refused': ('image-alias', 8, [-2, -2], False),
}
PMSG_CASES = set(PMSG_MATRIX)
ENTRY_BUILD_SOURCES = {"start.S", "pmsg.S", "linker.ld", "build.sh"}
PROBE_FIELDS = ("magic version stage entry_x0 current_el sctlr mpidr mmfr0 cntfrq tcr "
                "tgran16 esr far elr supports_16k").split()


def require(ok, message):
    pack.require(ok, message)


def read(path, limit=16 * 1024 * 1024):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), "input must be an ordinary non-symlink file")
    return pack.bounded_read(path, limit)


def load_json(path):
    result = json.loads(read(path))
    require(isinstance(result, dict), "evidence must be a JSON object")
    return result


def number(value):
    require(type(value) is int or isinstance(value, str), "invalid numeric evidence")
    return int(value, 0) if isinstance(value, str) else value


def source_hashes(source_dir):
    result = {}
    for path in source_dir.rglob("*"):
        if "__pycache__" in path.parts:
            continue
        require(not path.is_symlink(), "entry source symlinks are not allowed")
        if path.is_file():
            result[path.relative_to(source_dir).as_posix()] = pack.sha(read(path, 1024 * 1024))
    require(ENTRY_BUILD_SOURCES | {"verify.py", "verify_pmsg.py", "README.md"} <= result.keys(),
            "complete entry source tree is required")
    return result


def relative_file(root, name):
    require(isinstance(name, str) and name and not Path(name).is_absolute(),
            "artifact name must be relative")
    path = Path(name)
    require(".." not in path.parts and path.as_posix() == name,
            "noncanonical artifact path")
    current = root
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), "artifact symlinks are not allowed")
    require(current.resolve().is_relative_to(root.resolve()), "artifact escapes evidence directory")
    return current


def check_bound_report(path, source_dir, expected_cases):
    require(expected_cases, "verifier case contract has not been configured")
    report = load_json(path)
    require(report.get("status") == "pass", "verification is incomplete or failed")
    require(report.get("sources") == source_hashes(source_dir),
            "entry source evidence is stale or incomplete")
    cases = report.get("cases")
    require(isinstance(cases, list) and all(isinstance(c, dict) for c in cases),
            "invalid case collection")
    require(len(cases) == len(expected_cases) and {c.get("case") for c in cases} == expected_cases,
            "all distinct current QEMU cases are required")
    require(all(c.get("pass") is True for c in cases), "a QEMU case did not pass")
    artifacts = report.get("artifacts_sha256")
    require(isinstance(artifacts, dict) and artifacts, "artifact hash inventory is required")
    root = path.parent
    for name, digest in artifacts.items():
        require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest),
                "invalid artifact digest")
        require(pack.sha(read(relative_file(root, name))) == digest,
                "artifact changed: " + name)
    for case in cases:
        names = case.get("artifact_paths")
        digests = case.get("artifacts_sha256")
        require(isinstance(names, list) and names and len(set(names)) == len(names),
                "case artifact list is missing or duplicated")
        require(isinstance(digests, dict) and set(digests) == set(names),
                "case artifact hash set mismatch")
        require(all(name in artifacts and digests[name] == artifacts[name] for name in names),
                "case artifacts differ from global inventory")
        require(any(name.endswith("-gdb.log") for name in names) and
                any(name.endswith("-qemu.log") for name in names),
                "case execution logs are required")
    return report


def check_probe(directory, source_dir):
    image = read(directory / "probe.Image", 1024 * 1024)
    report = load_json(directory / "verification.json")
    pack.validate_probe(image, report, source_dir)
    artifact_hashes = {}
    for case in report["cases"]:
        name = case["case"]
        record = read(directory / (name + "-record.bin"), 120)
        require(len(record) == 120, "invalid original probe record length")
        values = struct.unpack("<15Q", record)
        require(isinstance(case.get("record"), dict) and
                all(number(case["record"].get(field)) == value
                    for field, value in zip(PROBE_FIELDS, values)),
                "original probe record differs from evidence")
        require(record[:8] == b"ACEPROBE" and values[1] == 2, "invalid original probe record")
        expected_el = 8 if name.startswith("el2") else 4
        expected_stage = 3 if "mmu-on" in name else 6 if "brk" in name else 5
        require(values[2] == expected_stage and values[4] == expected_el,
                "original probe semantic result mismatch")
        for suffix in ("-record.bin", "-gdb.log", "-qemu.log"):
            file = directory / (name + suffix)
            artifact_hashes[file.name] = pack.sha(read(file))
    return image, report, artifact_hashes


def check_default(directory, source_dir, probe_image):
    image = read(directory / "entry.Image", 1024 * 1024)
    pack.image_check(image)
    report = check_bound_report(directory / "verification.json", source_dir, DEFAULT_CASES)
    require(report.get("image_sha256") == pack.sha(image), "entry Image/evidence mismatch")
    require(report.get("probe_sha256") == pack.sha(probe_image), "entry payload identity mismatch")
    require(read(directory / "probe.Image", 1024 * 1024) == probe_image,
            "entry copied probe differs")
    require(image.count(probe_image) == 1, "entry must contain exactly one verified probe payload")
    manifest = load_json(directory / "build-manifest.json")
    require(report.get("build_manifest_sha256") == pack.sha(read(directory / "build-manifest.json")),
            "build manifest differs from verification")
    require(manifest.get("image_sha256") == pack.sha(image) and
            manifest.get("probe_sha256") == pack.sha(probe_image),
            "build input/output identity mismatch")
    require(manifest.get("pmsg") == {"enabled": False},
            "only the default no-pmsg Image can be wrapped")
    require(manifest.get("sources") == {n: source_hashes(source_dir)[n] for n in ENTRY_BUILD_SOURCES},
            "build source hashes are stale")
    require(load_json(directory / "pmsg-config.json") == {"enabled": False},
            "default configuration must disable pmsg")
    for case in report["cases"]:
        name = case["case"]
        expected = {name + "-bridge.bin", name + "-gdb.log", name + "-qemu.log"}
        mmu = name == "el2-mmu-rejected"
        expected |= ({name + "-table.bin", name + "-table-after.bin"} if mmu
                     else {name + "-probe.bin"})
        require(expected <= set(case["artifact_paths"]), "required default artifacts missing")
        raw = read(directory / (name + "-bridge.bin"), 64)
        require(len(raw) == 64 and raw[:8] == b"ACEENTRY", "invalid bridge record")
        values = struct.unpack("<8Q", raw)
        require([number(v) for v in case.get("bridge_record", [])] == list(values),
                "bridge raw record differs from report")
        incoming = 4 if name == "el1-pass" else 8
        require(values[1] == 1 and values[4] == incoming, "bridge version/EL mismatch")
        if mmu:
            require(values[2] == 3 and values[5] & 1 and values[6] == 0,
                    "MMU-on case must refuse without entering probe")
            require(read(directory / (name + "-table.bin")) ==
                    read(directory / (name + "-table-after.bin")), "MMU refusal changed page tables")
        else:
            require(values[2] == 4 and values[6] == 4 and values[5] & 5 == 0 and
                    values[7] & 5 == 0, "bridge did not reach EL1 with M/C off")
            raw_probe = read(directory / (name + "-probe.bin"), 120)
            require(len(raw_probe) == 120 and raw_probe[:8] == b"ACEPROBE",
                    "entry probe record invalid")
            pv = struct.unpack("<15Q", raw_probe)
            require([number(v) for v in case.get("probe_record", [])] == list(pv),
                    "embedded probe record differs from report")
            require(pv[1:3] == (2, 5) and pv[3] == values[3] and pv[4] == 4 and pv[14] == 1,
                    "embedded probe semantic result mismatch")
    return image, report


def check_pmsg(path, source_dir, probe_image, *, fixture_address='0x43000000',
               fixture_bytes=128, qemu_mib=128):
    report = check_bound_report(path, source_dir, PMSG_CASES)
    require(report.get('fixture_configuration') ==
            {'address': fixture_address, 'bytes': fixture_bytes, 'qemu_mib': qemu_mib},
            'logger matrix configuration changed')
    require(report.get('default_image_sha256') == DEFAULT_IMAGE_SHA and
            report.get('default_image_unchanged') is True, 'default Image baseline changed')
    root = path.parent
    configurations = {
        'default': {'enabled': False},
        'enabled': {'enabled': True, 'address': fixture_address, 'bytes': fixture_bytes},
        'short': {'enabled': True, 'address': fixture_address, 'bytes': 44},
        'image-alias': {'enabled': True, 'address': '0x40080000', 'bytes': 128},
    }
    builds = report.get('builds')
    require(isinstance(builds, dict) and set(builds) == set(configurations),
            'all four bound logger configurations are required')
    images = {}
    for name, configuration in configurations.items():
        build = builds[name]
        manifest_name = name + '/build-manifest.json'
        require(build.get('manifest') == manifest_name and
                build.get('manifest_sha256') == report['artifacts_sha256'].get(manifest_name),
                'logger build manifest is not bound')
        manifest = load_json(root / manifest_name)
        image = read(root / name / 'entry.Image', 1024 * 1024)
        pack.image_check(image)
        require(build.get('pmsg') == configuration and manifest.get('pmsg') == configuration and
                load_json(root / name / 'pmsg-config.json') == configuration,
                'logger configuration is not an approved QEMU RAM fixture')
        require(build.get('image_sha256') == pack.sha(image) == manifest.get('image_sha256') and
                manifest.get('probe_sha256') == pack.sha(probe_image) and
                read(root / name / 'probe.Image', 1024 * 1024) == probe_image and
                image.count(probe_image) == 1, 'logger build/payload identity mismatch')
        require(manifest.get('sources') == {n: source_hashes(source_dir)[n] for n in ENTRY_BUILD_SOURCES},
                'logger build sources are stale')
        for file in ('entry.Image', 'probe.Image', 'pmsg-config.json', 'build-manifest.json'):
            require(name + '/' + file in report['artifacts_sha256'], 'logger build artifact missing')
        images[name] = image
    require(pack.sha(images['default']) == DEFAULT_IMAGE_SHA, 'default fixture Image changed')
    for case in report['cases']:
        name = case['case']
        build, incoming_el, status, logged = PMSG_MATRIX[name]
        stem = build + '/' + name
        require(case.get('build') == build and case.get('image_sha256') == pack.sha(images[build]),
                'case refers to a different logger build')
        require(case.get('expected_pmsg_status') == status and case.get('pmsg_status') == status and
                case.get('ring_matches_reference') is True, 'logger result does not match contract')
        before_name, after_name = stem + '-ring-before.bin', stem + '-ring-after.bin'
        required = {before_name, after_name, stem + '-bridge.bin', stem + '-gdb.log', stem + '-qemu.log'}
        mmu = name.startswith('mmu-')
        required |= ({stem + '-table.bin', stem + '-table-after.bin'} if mmu else {stem + '-probe.bin'})
        if status is not None:
            required.add(stem + '-pmsg-status.bin')
        require(required <= set(case['artifact_paths']), 'logger case artifacts missing')
        before, after = read(root / before_name), read(root / after_name)
        expected_size = 44 if build == 'short' else 128 if build == 'image-alias' else fixture_bytes
        expected_address = '0x40080000' if build == 'image-alias' else fixture_address
        require(len(before) == expected_size and len(after) == expected_size and
                case.get('pmsg_fixture_bytes') == expected_size and
                case.get('pmsg_fixture_address') == expected_address, 'logger fixture extent changed')
        expected = before
        if logged:
            signature, start, used = struct.unpack_from('<III', before)
            capacity = len(before) - 12
            require(signature == 0x43474244 and start < capacity and used <= capacity and
                    (used == capacity or start == used), 'invalid accepted logger fixture')
            for message in (b'ACEENTRY accepted EL2\n' if incoming_el == 8 else b'ACEENTRY accepted EL1\n',
                            b'ACEENTRY payload EL1\n'):
                expected = append_ring_reference(expected, message)
        require(after == expected, 'logger bytes differ from independent ring model')
        if status is not None:
            raw_status = read(root / (stem + '-pmsg-status.bin'), 8)
            require(len(raw_status) == 8 and list(struct.unpack('<2i', raw_status)) == status,
                    'logger raw status differs from report')
        bridge = read(root / (stem + '-bridge.bin'), 64)
        require(len(bridge) == 64 and bridge[:8] == b'ACEENTRY', 'logger bridge record invalid')
        values = struct.unpack('<8Q', bridge)
        require([number(v) for v in case.get('bridge_record', [])] == list(values) and
                values[1] == 1 and values[4] == incoming_el, 'logger bridge evidence mismatch')
        if mmu:
            require(values[2] == 3 and values[5] & 1 and values[6] == 0,
                    'logger MMU-on case did not refuse')
            require(read(root / (stem + '-table.bin')) == read(root / (stem + '-table-after.bin')),
                    'logger MMU refusal changed table')
        else:
            require(values[2] == 4 and values[6] == 4 and values[7] & 5 == 0,
                    'logger case did not reach EL1')
            probe = read(root / (stem + '-probe.bin'), 120)
            require(len(probe) == 120 and probe[:8] == b'ACEPROBE', 'logger probe record invalid')
            pv = struct.unpack('<15Q', probe)
            require([number(v) for v in case.get('probe_record', [])] == list(pv) and
                    pv[1:3] == (2, 5) and pv[3] == values[3] and pv[4] == 4 and pv[14] == 1,
                    'logger probe semantic mismatch')
    return report


def append_ring_reference(raw, message):
    signature, start, used = struct.unpack_from('<III', raw)
    capacity = len(raw) - 12
    tail = message[-capacity:]
    # Independent two-slice ring model, rather than the assembly's byte loop.
    first = min(len(tail), capacity - start)
    result = bytearray(raw)
    result[12 + start:12 + start + first] = tail[:first]
    result[12:12 + len(tail) - first] = tail[first:]
    struct.pack_into('<III', result, 0, signature, (start + len(tail)) % capacity,
                     min(capacity, used + len(tail)))
    return bytes(result)


def select_image(default_image, evidence_path, report, experimental):
    if not experimental:
        return default_image
    image = read(evidence_path.parent / 'enabled/entry.Image', 1024 * 1024)
    require(pack.sha(image) == report['builds']['enabled']['image_sha256'] and
            report['builds']['enabled']['pmsg'] ==
            {'enabled': True, 'address': '0x48160000', 'bytes': 65536},
            'experimental Image identity/configuration changed after validation')
    return image


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stock-boot", type=Path, default=REPO / "research/ace-20261019/images/boot.img")
    parser.add_argument("--stock-vendor-boot", type=Path, default=REPO / "research/ace-20261019/images/vendor_boot.img")
    parser.add_argument("--entry-dir", type=Path, default=REPO / "research/ace-entry-20261019")
    parser.add_argument("--pmsg-evidence", type=Path, default=REPO / "research/ace-entry-pmsg-20261019/verification.json")
    parser.add_argument("--ace-address-pmsg-evidence", type=Path,
                        default=REPO / "research/ace-entry-pmsg-ace-address-20261019/verification.json")
    parser.add_argument("--probe-dir", type=Path, default=REPO / "research/ace-offline/probe")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--emit-unsigned-boot", action="store_true",
                        help="Also emit an UNTESTED bare v4 review candidate; no AVB authentication")
    parser.add_argument("--experimental-ace-pmsg", action="store_true",
                        help="Select the verified experimental 0x48160000/65536 logger Image for review only")
    args = parser.parse_args(argv)
    try:
        output = pack.output_path(args.output_dir)
        stock = read(args.stock_boot, 64 * 1024 * 1024)
        vendor = read(args.stock_vendor_boot, 64 * 1024 * 1024)
        require(pack.sha(stock) == pack.STOCK_SHA and pack.sha(vendor) == pack.VENDOR_SHA,
                "stock boot/vendor_boot SHA pin mismatch")
        layout = pack.boot_v4(stock)
        source_dir = REPO / "ace/entry"
        probe_image, probe_report, probe_artifacts = check_probe(args.probe_dir, REPO / "probe")
        image, entry_report = check_default(args.entry_dir, source_dir, probe_image)
        require(pack.sha(image) == DEFAULT_IMAGE_SHA, 'default entry baseline bytes changed')
        pmsg_report = check_pmsg(args.pmsg_evidence, source_dir, probe_image)
        ace_pmsg_report = check_pmsg(args.ace_address_pmsg_evidence, source_dir, probe_image,
                                    fixture_address='0x48160000', fixture_bytes=65536, qemu_mib=256)
        image = select_image(image, args.ace_address_pmsg_evidence, ace_pmsg_report,
                             args.experimental_ace_pmsg)
        compressed = pack.deterministic_gzip(image)
        require(pack.inflate(compressed, 1024 * 1024) == image, "gzip roundtrip mismatch")
        report = {"schema_version": 1, "status": "UNTESTED entry diagnostic packaging only",
                  "ios_deployable": False, "hardware_execution_verified": False,
                  "hardware_test_recommended": False, "payload": "ACEENTRY -> ACEPROBE; not XNU or iOS",
                  "inputs": {"stock_boot_sha256": pack.sha(stock), "stock_vendor_boot_sha256": pack.sha(vendor),
                             "entry_image_sha256": pack.sha(image),
                             "entry_evidence_sha256": pack.sha(read(args.entry_dir / "verification.json")),
                             "pmsg_evidence_sha256": pack.sha(read(args.pmsg_evidence)),
                             "ace_address_pmsg_evidence_sha256": pack.sha(read(args.ace_address_pmsg_evidence)),
                             "probe_image_sha256": pack.sha(probe_image),
                             "probe_evidence_sha256": pack.sha(read(args.probe_dir / "verification.json")),
                             "all_entry_sources": source_hashes(source_dir),
                             "probe_sources": probe_report["input_sha256"],
                             "probe_record_log_sha256": probe_artifacts,
                             "packaging_tool_sha256": pack.sha(read(Path(__file__))),
                             "shared_packaging_helper_sha256": pack.sha(read(REPO / "tools/ace-probe-boot.py"))},
                  "qemu_cases": {"default": sorted(DEFAULT_CASES), "pmsg": sorted(PMSG_CASES),
                                 "ace_address_pmsg": sorted(PMSG_CASES),
                                 "original_probe": sorted(pack.CASES)},
                  "gzip": {"bytes": len(compressed), "sha256": pack.sha(compressed), "mtime": 0},
                  "stock_layout": layout,
                  "authentication": {"signed": False, "avb_authentication_verified": False,
                                     "candidate_avb_footer": False, "parent_vbmeta_authenticates_candidate": False},
                  "observability": {"pmsg_enabled_in_packaged_image": args.experimental_ace_pmsg,
                                    "pmsg_configuration": ({"enabled": True, "address": "0x48160000", "bytes": 65536}
                                                           if args.experimental_ace_pmsg else {"enabled": False}),
                                    "qemu_pmsg_test_scope": "explicit ordinary RAM fixtures only",
                                    "physical_log_retrieval_verified": False,
                                    "missing": ["Ace hardware entry/record retrieval", "safe physical memory ownership",
                                                "bootloader acceptance and restore-path execution"]}}
        files = {"entry.Image.gz": compressed}
        if args.emit_unsigned_boot:
            candidate, candidate_layout = pack.unsigned_boot(stock, layout, compressed)
            files["UNTESTED-unsigned-entry-boot.img"] = candidate
            report["candidate"] = {"bytes": len(candidate), "sha256": pack.sha(candidate),
                                   "layout": candidate_layout, "header_changed_fields": ["kernel_size"],
                                   "ramdisk_sha256": pack.sha(stock[layout["ramdisk_offset"]:
                                                                 layout["ramdisk_offset"] + layout["ramdisk_bytes"]]),
                                   "note": "Bare v4, no transferable stock AVB; physical acceptance untested"}
        output.mkdir(mode=0o700, parents=True, exist_ok=False)
        for name, data in files.items():
            path = output / name
            with path.open("xb") as file:
                path.chmod(0o600)
                file.write(data)
        path = output / "manifest.json"
        with path.open("x") as file:
            path.chmod(0o600)
            json.dump(report, file, indent=2)
            file.write("\n")
        print(json.dumps({"status": report["status"], "files": list(files),
                          "ios_deployable": False, "hardware_test_recommended": False}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error,
            zlib.error, pack.subprocess.SubprocessError) as exc:
        print("Entry diagnostic packaging failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
