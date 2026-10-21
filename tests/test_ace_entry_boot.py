"""Pure host evidence/format mutation tests; no QEMU or phone is launched."""
import copy
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ace_entry_pack", ROOT / "tools/ace-entry-boot.py")
wrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wrap)


def image(payload=b""):
    blob = bytearray(64) + payload
    struct.pack_into("<QQ", blob, 8, 0x80000, len(blob))
    blob[56:60] = b"ARM\x64"
    return bytes(blob)


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_json(path, value):
    put(path, (json.dumps(value, indent=2) + "\n").encode())


def fixture(base):
    source = base / "source"
    for name in wrap.ENTRY_BUILD_SOURCES | {"verify.py", "verify_pmsg.py", "README.md"}:
        put(source / name, ("synthetic unit fixture " + name).encode())
    directory = base / "entry"
    probe_image = image(b"synthetic-probe-payload")
    entry_image = image(b"bridge" + probe_image + b"bridge-record")
    put(directory / "entry.Image", entry_image)
    put(directory / "probe.Image", probe_image)
    write_json(directory / "pmsg-config.json", {"enabled": False})
    hashes = wrap.source_hashes(source)
    build = {"image_sha256": wrap.pack.sha(entry_image),
             "probe_sha256": wrap.pack.sha(probe_image),
             "pmsg": {"enabled": False},
             "sources": {name: hashes[name] for name in wrap.ENTRY_BUILD_SOURCES}}
    write_json(directory / "build-manifest.json", build)
    report = {"status": "pass", "sources": hashes,
              "image_sha256": wrap.pack.sha(entry_image),
              "probe_sha256": wrap.pack.sha(probe_image),
              "build_manifest_sha256": wrap.pack.sha((directory / "build-manifest.json").read_bytes()),
              "cases": [], "artifacts_sha256": {}}
    for name in sorted(wrap.DEFAULT_CASES):
        mmu = name == "el2-mmu-rejected"
        bridge = [int.from_bytes(b"ACEENTRY", "little"), 1, 3 if mmu else 4,
                  0x44000000, 4 if name == "el1-pass" else 8,
                  0x30C50839 if mmu else 0x30C50838, 0 if mmu else 4,
                  0 if mmu else 0x30C50838]
        pv = [int.from_bytes(b"ACEPROBE", "little"), 2, 5, bridge[3], 4, 0x30C50838,
              0x80000000, 0x101122, 13000000, 0, 1, 0, 0, 0, 1]
        artifacts = {name + "-bridge.bin": struct.pack("<8Q", *bridge),
                     name + "-gdb.log": b"synthetic unit-test GDB result",
                     name + "-qemu.log": b"synthetic unit-test QEMU log"}
        if mmu:
            artifacts[name + "-table.bin"] = bytes(4096)
            artifacts[name + "-table-after.bin"] = bytes(4096)
        else:
            artifacts[name + "-probe.bin"] = struct.pack("<15Q", *pv)
        for filename, data in artifacts.items():
            put(directory / filename, data)
        digests = {filename: wrap.pack.sha(data) for filename, data in artifacts.items()}
        report["cases"].append({"case": name, "pass": True,
                                "bridge_record": [hex(v) for v in bridge],
                                "probe_record": None if mmu else [hex(v) for v in pv],
                                "artifact_paths": list(artifacts),
                                "artifacts_sha256": digests})
        report["artifacts_sha256"].update(digests)
    write_json(directory / "verification.json", report)
    return directory, source, probe_image, report


def rebind_artifact(directory, report, name, data):
    put(directory / name, data)
    report["artifacts_sha256"][name] = wrap.pack.sha(data)
    for case in report["cases"]:
        if name in case["artifacts_sha256"]:
            case["artifacts_sha256"][name] = wrap.pack.sha(data)
    write_json(directory / "verification.json", report)


def logger_fixture(base):
    directory, source, probe, _ = fixture(base)
    root = base / "logger"
    hashes = wrap.source_hashes(source)
    report = {"status": "pass", "sources": hashes,
              "fixture_configuration": {"address": "0x43000000", "bytes": 128, "qemu_mib": 128},
              "default_image_unchanged": True, "builds": {}, "cases": [],
              "artifacts_sha256": {}}
    images = {}
    for name in ("default", "enabled", "short", "image-alias"):
        configuration = ({"enabled": False} if name == "default" else
                         {"enabled": True, "address": "0x40080000" if name == "image-alias" else "0x43000000",
                          "bytes": 44 if name == "short" else 128})
        data = image(name.encode() + probe + bytes(128))
        images[name] = data
        manifest = {"image_sha256": wrap.pack.sha(data),
                    "probe_sha256": wrap.pack.sha(probe), "pmsg": configuration,
                    "sources": {n: hashes[n] for n in wrap.ENTRY_BUILD_SOURCES}}
        put(root / name / "entry.Image", data)
        put(root / name / "probe.Image", probe)
        write_json(root / name / "build-manifest.json", manifest)
        write_json(root / name / "pmsg-config.json", configuration)
        for file in ("entry.Image", "probe.Image", "build-manifest.json", "pmsg-config.json"):
            relative = name + "/" + file
            report["artifacts_sha256"][relative] = wrap.pack.sha((root / relative).read_bytes())
        report["builds"][name] = {
            "manifest": name + "/build-manifest.json",
            "manifest_sha256": report["artifacts_sha256"][name + "/build-manifest.json"],
            "image_sha256": wrap.pack.sha(data), "pmsg": configuration}
    report["default_image_sha256"] = wrap.pack.sha(images["default"])
    for name, (build, incoming, status, logged) in wrap.PMSG_MATRIX.items():
        prefix = build + "/" + name
        capacity = 32 if build == "short" else 116
        initial = bytes(range(32)) if build == "short" else b"old-log\n"
        start = 29 if build == "short" else len(initial)
        signature = 0 if name.startswith("bad-signature") else 0x43474244
        if name == "bad-cursor-el2":
            initial, start = b"12", 3
        elif name == "noncanonical-el2":
            initial, start = b"1234", 1
        before = struct.pack("<III", signature, start, len(initial)) + initial + bytes(capacity-len(initial))
        if name == "default-el2-untouched":
            before = b"\xa5" * 128
        if build == "image-alias":
            before = images[build][:128]
        after = bytearray(before)
        if logged:
            for message in (b"ACEENTRY accepted EL2\n" if incoming == 8 else b"ACEENTRY accepted EL1\n",
                            b"ACEENTRY payload EL1\n"):
                signature, start, used = struct.unpack_from("<III", after)
                tail = message[-capacity:]
                for i, value in enumerate(tail):
                    after[12 + (start+i) % capacity] = value
                struct.pack_into("<III", after, 0, signature, (start+len(tail)) % capacity,
                                 min(capacity, used+len(tail)))
        mmu = name.startswith("mmu-")
        bridge = [int.from_bytes(b"ACEENTRY", "little"), 1, 3 if mmu else 4,
                  0x44000000, incoming, 0x30C50839 if mmu else 0x30C50838,
                  0 if mmu else 4, 0 if mmu else 0x30C50838]
        pv = [int.from_bytes(b"ACEPROBE", "little"), 2, 5, bridge[3], 4, 0x30C50838,
              0x80000000, 0x101122, 13000000, 0, 1, 0, 0, 0, 1]
        artifacts = {prefix + "-bridge.bin": struct.pack("<8Q", *bridge),
                     prefix + "-ring-before.bin": before, prefix + "-ring-after.bin": bytes(after),
                     prefix + "-gdb.log": b"synthetic unit log", prefix + "-qemu.log": b""}
        if mmu:
            artifacts[prefix + "-table.bin"] = bytes(4096)
            artifacts[prefix + "-table-after.bin"] = bytes(4096)
        else:
            artifacts[prefix + "-probe.bin"] = struct.pack("<15Q", *pv)
        if status is not None:
            artifacts[prefix + "-pmsg-status.bin"] = struct.pack("<2i", *status)
        for relative, data in artifacts.items():
            put(root / relative, data)
        digests = {n: wrap.pack.sha(v) for n, v in artifacts.items()}
        report["artifacts_sha256"].update(digests)
        report["cases"].append({
            "case": name, "pass": True, "build": build, "image_sha256": wrap.pack.sha(images[build]),
            "expected_pmsg_status": status, "pmsg_status": status, "ring_matches_reference": True,
            "pmsg_fixture_bytes": len(before), "pmsg_fixture_address":
                "0x40080000" if build == "image-alias" else "0x43000000",
            "bridge_record": [hex(v) for v in bridge],
            "probe_record": None if mmu else [hex(v) for v in pv],
            "artifact_paths": list(artifacts), "artifacts_sha256": digests})
    write_json(root / "verification.json", report)
    return root, source, probe, report


class EntryBootTests(unittest.TestCase):
    def test_all_logger_cases_are_independently_validated(self):
        with tempfile.TemporaryDirectory() as temp:
            root, source, probe, report = logger_fixture(Path(temp))
            with mock.patch.object(wrap, "DEFAULT_IMAGE_SHA", report["default_image_sha256"]):
                checked = wrap.check_pmsg(root / "verification.json", source, probe)
            self.assertEqual(len(checked["cases"]), 14)

    def test_rehashed_wrong_logger_bytes_are_not_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            root, source, probe, report = logger_fixture(Path(temp))
            name = "short/wrap-el2-ring-after.bin"
            data = bytearray((root / name).read_bytes())
            data[-1] ^= 1
            rebind_artifact(root, report, name, bytes(data))
            with mock.patch.object(wrap, "DEFAULT_IMAGE_SHA", report["default_image_sha256"]):
                with self.assertRaises(ValueError):
                    wrap.check_pmsg(root / "verification.json", source, probe)

    def test_logger_missing_case_substitute_ram_and_false_status_are_rejected(self):
        for mutation in ("missing", "address", "status"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                root, source, probe, report = logger_fixture(Path(temp))
                if mutation == "missing":
                    report["cases"].pop()
                elif mutation == "address":
                    report["builds"]["enabled"]["pmsg"]["address"] = "0x48160000"
                else:
                    case = next(c for c in report["cases"] if c["case"] == "bad-signature-el2")
                    case["pmsg_status"] = case["expected_pmsg_status"] = [0, 0]
                write_json(root / "verification.json", report)
                with mock.patch.object(wrap, "DEFAULT_IMAGE_SHA", report["default_image_sha256"]):
                    with self.assertRaises(ValueError):
                        wrap.check_pmsg(root / "verification.json", source, probe)

    def test_complete_default_fixture_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            directory, source, probe, report = fixture(Path(temp))
            actual, checked = wrap.check_default(directory, source, probe)
            self.assertEqual(actual, (directory / "entry.Image").read_bytes())
            self.assertEqual(len(checked["cases"]), 4)

    def test_entry_image_source_and_embedded_probe_are_bound(self):
        for mutation in ("image", "source", "new-source", "probe-copy"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                directory, source, probe, report = fixture(Path(temp))
                if mutation == "image":
                    put(directory / "entry.Image", image(b"substituted payload"))
                elif mutation == "source":
                    put(source / "pmsg.S", b"changed")
                elif mutation == "new-source":
                    put(source / "new-assembly.S", b"unbound source")
                else:
                    put(directory / "probe.Image", image(b"another probe"))
                with self.assertRaises(ValueError):
                    wrap.check_default(directory, source, probe)

    def test_case_set_must_be_distinct_complete_and_passing(self):
        for mutation in ("missing", "duplicate", "false", "one", "incomplete", "no-sources"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                directory, source, probe, report = fixture(Path(temp))
                if mutation == "missing": report["cases"].pop()
                elif mutation == "duplicate": report["cases"][-1] = report["cases"][0]
                elif mutation == "false": report["cases"][0]["pass"] = False
                elif mutation == "one": report["cases"][0]["pass"] = 1
                elif mutation == "incomplete": report["status"] = "incomplete"
                else: report["sources"].pop("verify_pmsg.py")
                write_json(directory / "verification.json", report)
                with self.assertRaises(ValueError):
                    wrap.check_default(directory, source, probe)

    def test_artifact_corruption_missing_inventory_and_case_hash_are_rejected(self):
        for mutation in ("bytes", "inventory", "case-hash", "list", "missing-file"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                directory, source, probe, report = fixture(Path(temp))
                name = report["cases"][0]["artifact_paths"][0]
                if mutation == "bytes": put(directory / name, b"corrupted")
                elif mutation == "inventory": report["artifacts_sha256"].pop(name)
                elif mutation == "case-hash": report["cases"][0]["artifacts_sha256"][name] = "0" * 64
                elif mutation == "list": report["cases"][0]["artifact_paths"].append(name)
                else: (directory / name).unlink()
                write_json(directory / "verification.json", report)
                with self.assertRaises((ValueError, OSError)):
                    wrap.check_default(directory, source, probe)

    def test_even_rehashed_and_self_consistent_wrong_el_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory, source, probe, report = fixture(Path(temp))
            case = next(c for c in report["cases"] if c["case"] == "el2-to-el1")
            raw = bytearray((directory / "el2-to-el1-bridge.bin").read_bytes())
            struct.pack_into("<Q", raw, 6 * 8, 8)  # still at EL2 instead of EL1
            case["bridge_record"][6] = "0x8"
            rebind_artifact(directory, report, "el2-to-el1-bridge.bin", bytes(raw))
            with self.assertRaises(ValueError):
                wrap.check_default(directory, source, probe)

    def test_mmu_case_must_preserve_table_even_after_hashes_are_updated(self):
        with tempfile.TemporaryDirectory() as temp:
            directory, source, probe, report = fixture(Path(temp))
            name = "el2-mmu-rejected-table-after.bin"
            rebind_artifact(directory, report, name, b"changed" + bytes(4089))
            with self.assertRaises(ValueError):
                wrap.check_default(directory, source, probe)

    def test_build_and_configuration_cannot_enable_logger_in_default_package(self):
        with tempfile.TemporaryDirectory() as temp:
            directory, source, probe, report = fixture(Path(temp))
            build = wrap.load_json(directory / "build-manifest.json")
            build["pmsg"] = {"enabled": True, "address": "0x41000000", "bytes": 4096}
            write_json(directory / "build-manifest.json", build)
            report["build_manifest_sha256"] = wrap.pack.sha((directory / "build-manifest.json").read_bytes())
            write_json(directory / "verification.json", report)
            with self.assertRaises(ValueError):
                wrap.check_default(directory, source, probe)

    def test_paths_and_symlinks_cannot_replace_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            directory, source, probe, report = fixture(Path(temp))
            for name in ("../outside.bin", "/tmp/outside.bin", "nested/../inside"):
                with self.assertRaises(ValueError):
                    wrap.relative_file(directory, name)
            target = directory / "el1-pass-bridge.bin"
            original = target.read_bytes()
            target.unlink()
            put(Path(temp) / "outside.bin", original)
            target.symlink_to(Path(temp) / "outside.bin")
            with self.assertRaises(ValueError):
                wrap.check_default(directory, source, probe)

    def test_default_gzip_and_unsigned_v4_roundtrip_have_no_authentication(self):
        # Use the existing packaging format fixture, not a phone artifact.
        spec = importlib.util.spec_from_file_location("probe_boot_tests", ROOT / "tests/test_ace_probe_boot.py")
        fixtures = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixtures)
        stock = fixtures.fixture()
        layout = wrap.pack.boot_v4(stock)
        payload = image(b"synthetic-entry")
        compressed = wrap.pack.deterministic_gzip(payload)
        candidate, rebuilt = wrap.pack.unsigned_boot(stock, layout, compressed)
        self.assertEqual(wrap.pack.inflate(candidate[4096:4096+rebuilt["kernel_bytes"]]), payload)
        expected = bytearray(stock[:4096])
        struct.pack_into("<I", expected, 8, len(compressed))
        self.assertEqual(candidate[:4096], expected)
        self.assertIsNone(rebuilt["avb"])
        self.assertEqual(len(candidate), rebuilt["payload_end"])
        self.assertNotEqual(candidate[-64:-60], b"AVBf")

    def test_wrong_stock_identity_fails_before_creating_output(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "research") as temp:
            root = Path(temp)
            put(root / "stock.img", b"wrong")
            put(root / "vendor.img", b"wrong")
            with mock.patch("sys.stderr"), mock.patch.object(wrap, "check_probe", side_effect=AssertionError("must stop")):
                status = wrap.main(["--stock-boot", str(root / "stock.img"),
                                    "--stock-vendor-boot", str(root / "vendor.img"),
                                    "--output-dir", str(root / "output")])
            self.assertEqual(status, 1)
            self.assertFalse((root / "output").exists())

    def test_experimental_selection_is_explicit_and_fixed_to_ace_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            data = image(b"experimental synthetic fixture")
            put(root / 'enabled/entry.Image', data)
            report = {'builds': {'enabled': {'image_sha256': wrap.pack.sha(data),
                       'pmsg': {'enabled': True, 'address': '0x48160000', 'bytes': 65536}}}}
            path = root / 'verification.json'
            self.assertEqual(wrap.select_image(b'default', path, report, False), b'default')
            self.assertEqual(wrap.select_image(b'default', path, report, True), data)
            report['builds']['enabled']['pmsg']['address'] = '0x43000000'
            with self.assertRaises(ValueError):
                wrap.select_image(b'default', path, report, True)
            report['builds']['enabled']['pmsg']['address'] = '0x48160000'
            put(root / 'enabled/entry.Image', data + b'changed')
            with self.assertRaises(ValueError):
                wrap.select_image(b'default', path, report, True)


if __name__ == "__main__":
    unittest.main()
