"""Host-only tests: no real adb process or connected phone is used."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shlex
import struct
import subprocess
import tempfile
import unittest
from unittest import mock
import zlib

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ace_collect", REPO / "tools/ace-collect.py")
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def result(data=b"", code=0):
    return subprocess.CompletedProcess([], code, stdout=data, stderr=b"PRIVATE_DEVICE error")


class MockAdb:
    """Simulate su access, binary FDT, timeout and hostile stderr."""
    def __init__(self, su=True, root=False, failure=None):
        self.calls = []
        self.su = su
        self.root = root
        self.failure = failure

    def __call__(self, args, **kwargs):
        self.calls.append((args, kwargs))
        if args == ["adb", "devices"]:
            return result(b"List of devices attached\nPRIVATE_DEVICE\tdevice\n")
        assert args[:4] == ["adb", "-s", "PRIVATE_DEVICE", "exec-out"]
        remote = args[4]
        is_su = remote.startswith("su -c ")
        command = shlex.split(remote)[2] if is_su else remote
        if command == "id -u":
            if is_su:
                return result(b"0\n") if self.su else result(code=1)
            return result(b"0\n" if self.root else b"2000\n")
        if command == self.failure:
            raise subprocess.TimeoutExpired(args, kwargs["timeout"], stderr=b"PRIVATE_DEVICE")
        if command.startswith("getprop "):
            return result(b"PGKM10 PRIVATE_DEVICE\n")
        if command == collector.ITEMS["live-fdt.dtb"]:
            return result(b"\xd0\x0d\xfe\xed\x00binary")
        if command == collector.ITEMS["boot-control.bin"]:
            return result(b"\0" * 32)
        return result(b"read evidence PRIVATE_DEVICE\n")


class CollectorTests(unittest.TestCase):
    def test_su_quotes_entire_multiline_command(self):
        run = MockAdb()
        adb = collector.Adb("PRIVATE_DEVICE", run=run)
        command = "printf '%s' \"a;b\"; cat '/path with spaces'\ntrue"
        adb.read(command, root=True)
        remote = run.calls[-1][0][-1]
        self.assertEqual(shlex.split(remote), ["su", "-c", command])
        self.assertNotIn("shell", run.calls[-1][0])
        self.assertEqual(run.calls[-1][1]["timeout"], 15)

    def test_device_selection_requires_unique_authorized_device(self):
        self.assertEqual(collector.select_device(run=MockAdb()), "PRIVATE_DEVICE")
        multiple = lambda *a, **k: result(b"List of devices attached\nA\tdevice\nB\tdevice\nC\tunauthorized\n")
        with self.assertRaises(collector.CollectionError):
            collector.select_device(run=multiple)
        self.assertEqual(collector.select_device("B", run=multiple), "B")
        with self.assertRaises(collector.CollectionError):
            collector.select_device("C", run=multiple)
        offline = lambda *a, **k: result(b"List of devices attached\nA\toffline\n")
        with self.assertRaises(collector.CollectionError):
            collector.select_device(run=offline)

    def test_collection_uses_only_allowlisted_reads_and_private_files(self):
        run = MockAdb()
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "capture"
            manifest = collector.collect(collector.Adb("PRIVATE_DEVICE", run=run), output)
            self.assertEqual(manifest["root"]["read_access"], "su")
            self.assertEqual((output.stat().st_mode & 0o777), 0o700)
            self.assertEqual((output / "live-fdt.dtb").read_bytes(), b"\xd0\x0d\xfe\xed\x00binary")
            for file in output.iterdir():
                self.assertEqual(file.stat().st_mode & 0o777, 0o600)
                self.assertNotIn(b"PRIVATE_DEVICE", file.read_bytes())
            self.assertEqual(set(manifest["identity"]), set(collector.PROPERTIES))
            allowed = set(collector.ITEMS.values()) | {
                "id -u", *("getprop " + p for p in collector.PROPERTIES.values())}
            for args, kwargs in run.calls:
                self.assertEqual(args[:4], ["adb", "-s", "PRIVATE_DEVICE", "exec-out"])
                remote = args[-1]
                command = shlex.split(remote)[2] if remote.startswith("su -c ") else remote
                self.assertIn(command, allowed)
                self.assertFalse(kwargs.get("shell", False))
            joined = "\n".join(allowed)
            for forbidden in ("adb root", "resetprop", "setenforce", "reboot",
                              "fastboot", "flash", "getprop\n", "android_id",
                              "serialno", " of=", " > "):
                self.assertNotIn(forbidden, joined)
            self.assertEqual(manifest["reads"]["boot-control.bin"], "ok")
            self.assertFalse(manifest["boot_control"]["valid"])

    def test_timeout_is_recorded_and_later_reads_continue(self):
        run = MockAdb(failure=collector.ITEMS["iomem.txt"])
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "capture"
            manifest = collector.collect(collector.Adb("PRIVATE_DEVICE", run=run), output)
            self.assertEqual(manifest["reads"]["iomem.txt"], "timeout")
            self.assertFalse((output / "iomem.txt").exists())
            self.assertEqual(manifest["reads"]["interrupts.txt"], "ok")
            self.assertNotIn("PRIVATE_DEVICE", json.dumps(manifest))

    def test_denied_su_falls_back_without_configuration_changes(self):
        run = MockAdb(su=False)
        with tempfile.TemporaryDirectory() as temp:
            manifest = collector.collect(collector.Adb("PRIVATE_DEVICE", run=run),
                                         Path(temp) / "capture")
        self.assertEqual(manifest["root"]["read_access"], "shell")
        su_commands = [args[-1] for args, _ in run.calls if args[-1].startswith("su -c ")]
        self.assertEqual(su_commands, ["su -c 'id -u'"])

    def test_existing_root_does_not_invoke_su(self):
        run = MockAdb(root=True)
        with tempfile.TemporaryDirectory() as temp:
            manifest = collector.collect(collector.Adb("PRIVATE_DEVICE", run=run),
                                         Path(temp) / "capture")
        self.assertEqual(manifest["root"]["read_access"], "shell-root")
        self.assertFalse(any(args[-1].startswith("su -c ") for args, _ in run.calls))

    def test_adb_errors_do_not_retain_stderr(self):
        adb = collector.Adb("PRIVATE_DEVICE", run=lambda *a, **k: result(code=1))
        self.assertEqual(adb.read("id -u"), (None, "exit-1"))
        with mock.patch.object(adb, "run", side_effect=OSError("PRIVATE_DEVICE")):
            self.assertEqual(adb.read("id -u"), (None, "adb-unavailable"))

    def test_ignored_new_path_is_checked_with_git(self):
        calls = []
        def run(args, **kwargs):
            calls.append(args)
            return result()
        output = REPO / "research/nonexistent-collector-unit-test"
        self.assertEqual(collector.validate_output(output, run=run), output)
        self.assertEqual(calls[0][3:], ["check-ignore", "--quiet", "--",
                                      "research/nonexistent-collector-unit-test"])

    def test_reject_existing_unignored_outside_and_symlink_output(self):
        with tempfile.TemporaryDirectory(dir=REPO / "research") as temp:
            with self.assertRaises(collector.CollectionError):
                collector.validate_output(temp)
            link = Path(temp) / "dangling"
            link.symlink_to(Path(temp) / "missing")
            with self.assertRaises(collector.CollectionError):
                collector.validate_output(link)
        with self.assertRaises(collector.CollectionError):
            collector.validate_output("/tmp/ace-collect-test-new")
        with self.assertRaises(collector.CollectionError):
            collector.validate_output(REPO / "docs/unignored-output",
                                      run=lambda *a, **k: result(code=1))

    def test_dry_run_does_not_invoke_adb_write_or_print_identifier(self):
        stdout = io.StringIO()
        with mock.patch.object(collector, "validate_output", return_value=REPO / "research/dry"), \
             mock.patch.object(collector, "select_device", side_effect=AssertionError("ADB called")), \
             mock.patch.object(collector, "collect", side_effect=AssertionError("write")), \
             contextlib.redirect_stdout(stdout):
            status = collector.main(["--serial", "PRIVATE_DEVICE",
                                     "--output", "research/dry", "--dry-run"])
        self.assertEqual(status, 0)
        self.assertNotIn("PRIVATE_DEVICE", stdout.getvalue())
        self.assertEqual(json.loads(stdout.getvalue())["items"], list(collector.ITEMS))

    def test_boot_metadata_crc_and_field_decode(self):
        record = bytearray(32)
        record[:4] = b"_b\0\0"
        struct.pack_into("<I", record, 4, 0x42414342)
        record[12], record[14] = 0x77, 0x8F
        struct.pack_into("<I", record, 28, zlib.crc32(record[:28]))
        decoded = collector.decode_boot_control(record)
        self.assertTrue(decoded["valid"])
        self.assertEqual(decoded["slots"][0]["tries_remaining"], 7)
        self.assertEqual(decoded["slots"][1]["priority"], 15)
        self.assertTrue(decoded["slots"][1]["successful"])
        record[12] ^= 1
        self.assertFalse(collector.decode_boot_control(record)["valid"])
        self.assertFalse(collector.decode_boot_control(b"short")["valid"])

    def test_remote_scripts_have_valid_shell_syntax(self):
        # Only parses scripts; never executes their commands.
        for name, command in collector.ITEMS.items():
            with self.subTest(name=name):
                p = subprocess.run(["sh", "-n", "-c", command], capture_output=True)
                self.assertEqual(p.returncode, 0, p.stderr.decode())


if __name__ == "__main__":
    unittest.main()

