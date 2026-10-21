"""Offline backup safety/verification tests. No phone or real ADB is used."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import types
import unittest
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ace_backup", REPO / "tools/ace-backup.py")
backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backup)
PAYLOAD = b"private calibration fixture"
HASH = hashlib.sha256(PAYLOAD).hexdigest()


class FakeAdb:
    def __init__(self, size=len(PAYLOAD), hashes=None, root=True):
        self.serial = "PRIVATE_TRANSPORT"
        self.use_su = False
        self.expected_sizes = {"boot_a": len(PAYLOAD)}
        self.calls = []
        self.size = size
        self.hashes = list(hashes or [HASH, HASH])
        self.root = root

    def read(self, command, root=False):
        self.calls.append((command, root))
        if command == "id -u":
            return (b"0" if self.root else b"2000"), "ok"
        if command.startswith("blockdev --getsize64 "):
            return str(self.size).encode(), "ok"
        if command.startswith("sha256sum "):
            return (self.hashes.pop(0) + "  /dev/block/by-name/boot_a").encode(), "ok"
        raise AssertionError("Unexpected device command")


def ample_disk(_):
    return types.SimpleNamespace(free=20 * 1024 ** 3)


def fake_stream(adb, name, target, timeout):
    with target.open("xb") as file:
        os.chmod(target, 0o600)
        file.write(PAYLOAD)
    return {"status": "ok", "bytes": len(PAYLOAD), "host_sha256": HASH}


class PipeProcess:
    """Popen-shaped mock using an OS pipe so streaming/select logic is real."""
    def __init__(self, payload, keep_open=False, code=0):
        read_fd, write_fd = os.pipe()
        self.stdout = os.fdopen(read_fd, "rb", buffering=0)
        self.writer = write_fd
        os.write(write_fd, payload)
        if not keep_open:
            os.close(write_fd)
            self.writer = None
        self.running = keep_open
        self.code = code
        self.killed = False
        self.waited = False

    def poll(self):
        return None if self.running else self.code

    def kill(self):
        self.killed = True
        self.running = False
        if self.writer is not None:
            os.close(self.writer)
            self.writer = None

    def wait(self, timeout=None):
        self.waited = True
        return self.code


class BackupTests(unittest.TestCase):
    def test_whitelist_rejects_paths_userdata_bootloader_duplicates(self):
        self.assertEqual(backup.partitions("boot_a,persist"), ["boot_a", "persist"])
        for value in ("userdata", "super", "lk", "preloader", "/dev/block/boot_a",
                      "../boot_a", "boot_a;id", "boot_a,boot_a", "", "boot", "boot_a,"):
            with self.subTest(value=value), self.assertRaises(backup.collect.CollectionError):
                backup.partitions(value)
        with self.assertRaises(backup.collect.CollectionError):
            backup.block_path("userdata")

    def test_plan_has_no_device_access_and_no_serial_output(self):
        out = io.StringIO()
        with mock.patch.object(backup.collect, "select_device", side_effect=AssertionError("device")), \
             mock.patch.object(backup.collect, "validate_output", side_effect=AssertionError("filesystem")), \
             contextlib.redirect_stdout(out):
            self.assertEqual(backup.main(["--serial", "PRIVATE_TRANSPORT"]), 0)
        plan = json.loads(out.getvalue())
        self.assertEqual(plan["max_total_bytes"], 4 * 1024 ** 3)
        self.assertNotIn("PRIVATE_TRANSPORT", out.getvalue())

    def test_size_empty_partition_and_total_limits(self):
        for size in (0, backup.MAX_PARTITION + 1):
            with self.subTest(size=size), self.assertRaises(backup.collect.CollectionError):
                backup.preflight(FakeAdb(size=size), ["boot_a"], False, Path("/tmp/out"), ample_disk)
        with self.assertRaises(backup.collect.CollectionError):
            backup.preflight(FakeAdb(size=backup.MAX_PARTITION), list(backup.ALLOWED[:5]),
                             False, Path("/tmp/out"), ample_disk)

    def test_insufficient_disk_space(self):
        with self.assertRaises(backup.collect.CollectionError):
            backup.preflight(FakeAdb(), ["boot_a"], False, Path("/tmp/out"),
                             lambda p: types.SimpleNamespace(free=backup.DISK_RESERVE))
        sizes = backup.preflight(FakeAdb(), ["boot_a"], False, Path("/tmp/out"), ample_disk)
        self.assertEqual(sizes, {"boot_a": len(PAYLOAD)})

    def test_size_query_failure_and_non_numeric_response(self):
        for response in ((None, "timeout"), (b"PRIVATE_TRANSPORT", "ok"),
                         (b"4 PRIVATE_TRANSPORT", "ok")):
            adb = FakeAdb()
            adb.read = lambda *a, **k: response
            with self.subTest(response=response), self.assertRaises(backup.collect.CollectionError):
                backup.preflight(adb, ["boot_a"], False, Path("/tmp/out"), ample_disk)

    def test_verified_backup_rename_permissions_and_private_manifest(self):
        adb = FakeAdb()
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "backup"
            report = backup.backup(adb, ["boot_a"], output, stream=fake_stream, disk_usage=ample_disk)
            self.assertTrue(report["partitions"]["boot_a"]["verified"])
            self.assertEqual((output / "boot_a.img").read_bytes(), PAYLOAD)
            self.assertFalse((output / "boot_a.partial").exists())
            self.assertEqual(output.stat().st_mode & 0o777, 0o700)
            for file in output.iterdir():
                self.assertEqual(file.stat().st_mode & 0o777, 0o600)
            manifest = (output / "manifest.json").read_text()
            self.assertNotIn("PRIVATE_TRANSPORT", manifest)
            self.assertNotIn("stderr", manifest)
        self.assertEqual(adb.calls[0], ("id -u", False))
        self.assertTrue(all("of=" not in command and "userdata" not in command
                            for command, _ in adb.calls))

    def test_root_is_required_before_any_partition_read(self):
        adb = FakeAdb(root=False)
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(backup.collect.CollectionError):
                backup.backup(adb, ["boot_a"], Path(temp) / "backup", disk_usage=ample_disk)
        self.assertEqual(adb.calls, [("id -u", False), ("id -u", True)])

    def test_su_is_used_when_only_su_has_uid_zero(self):
        adb = FakeAdb()
        read = adb.read
        adb.read = lambda command, root=False: ((b"2000", "ok")
                    if command == "id -u" and not root else read(command, root))
        with tempfile.TemporaryDirectory() as temp:
            report = backup.backup(adb, ["boot_a"], Path(temp) / "backup",
                                   stream=fake_stream, disk_usage=ample_disk)
        self.assertEqual(report["root"], "su")
        self.assertTrue(adb.use_su)

    def test_device_changed_is_not_verified_and_partial_stays(self):
        adb = FakeAdb(hashes=[HASH, "0" * 64])
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "backup"
            report = backup.backup(adb, ["boot_a"], output,
                                   stream=fake_stream, disk_usage=ample_disk)
            row = report["partitions"]["boot_a"]
            self.assertFalse(row["verified"])
            self.assertFalse(row["stable"])
            self.assertTrue((output / "boot_a.partial").exists())
            self.assertFalse((output / "boot_a.img").exists())

    def test_host_hash_or_length_mismatch_keeps_partial(self):
        for payload in (b"x" * len(PAYLOAD), PAYLOAD[:-1]):
            def mismatch(*args):
                response = fake_stream(*args)
                # Deliberately claim the correct stream hash/length while the
                # actual saved file differs: the host must independently read it.
                args[2].write_bytes(payload)
                return response
            with tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / "backup"
                report = backup.backup(FakeAdb(), ["boot_a"], output,
                                       stream=mismatch, disk_usage=ample_disk)
                self.assertEqual(report["partitions"]["boot_a"]["status"], "length-or-hash-mismatch")
                self.assertTrue((output / "boot_a.partial").exists())

    def test_source_hash_failure_skips_stream(self):
        adb = FakeAdb(hashes=["PRIVATE_TRANSPORT"])
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "backup"
            report = backup.backup(adb, ["boot_a"], output,
                                   stream=mock.Mock(side_effect=AssertionError("stream")), disk_usage=ample_disk)
            self.assertFalse(report["partitions"]["boot_a"]["verified"])
            self.assertNotIn("PRIVATE_TRANSPORT", (output / "manifest.json").read_text())

    def test_stream_quotes_readonly_dd_and_reaps_child(self):
        adb = FakeAdb()
        adb.use_su = True
        proc = PipeProcess(PAYLOAD)
        popen = mock.Mock(return_value=proc)
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "boot_a.partial"
            response = backup.stream_copy(adb, "boot_a", target, 1, popen=popen)
            self.assertEqual(response, {"status": "ok", "bytes": len(PAYLOAD), "host_sha256": HASH})
            self.assertEqual(target.read_bytes(), PAYLOAD)
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
        args = popen.call_args.args[0]
        self.assertEqual(args[:4], ["adb", "-s", "PRIVATE_TRANSPORT", "exec-out"])
        remote = shlex.split(args[-1])
        self.assertEqual(remote, ["su", "-c", "dd if=/dev/block/by-name/boot_a bs=4194304 2>/dev/null"])
        self.assertNotIn("of=", args[-1])
        self.assertTrue(proc.waited)
        self.assertTrue(proc.stdout.closed)

    def test_raw_exec_stderr_merge_does_not_corrupt_backup(self):
        # Real local dd/shell model the raw service's shared stdout/stderr.
        # No adb or device access occurs in this regression.
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'source'; source.write_bytes(PAYLOAD)
            noisy = subprocess.run(['sh', '-c', 'dd if=' + shlex.quote(str(source))],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True).stdout
            self.assertTrue(noisy.startswith(PAYLOAD))
            self.assertGreater(len(noisy), len(PAYLOAD))
            def raw_service(args, **kwargs):
                remote = args[-1].replace('/dev/block/by-name/boot_a', shlex.quote(str(source)))
                kwargs['stderr'] = subprocess.STDOUT
                return subprocess.Popen(['sh', '-c', remote], **kwargs)
            target = Path(temp) / 'backup.partial'
            result = backup.stream_copy(FakeAdb(), 'boot_a', target, 2, popen=raw_service)
            self.assertEqual(result['status'], 'ok')
            self.assertEqual(target.read_bytes(), PAYLOAD)
            self.assertEqual(result['host_sha256'], HASH)

    def test_stream_timeout_kills_reaps_and_preserves_partial(self):
        proc = PipeProcess(PAYLOAD, keep_open=True)
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "boot_a.partial"
            response = backup.stream_copy(FakeAdb(), "boot_a", target, 0.01,
                                          popen=lambda *a, **k: proc)
            self.assertEqual(response["status"], "timeout")
            self.assertEqual(target.read_bytes(), PAYLOAD)
        self.assertTrue(proc.killed)
        self.assertTrue(proc.waited)
        self.assertTrue(proc.stdout.closed)

    def test_stream_failure_and_oversize_preserve_partial(self):
        for proc, status in ((PipeProcess(PAYLOAD, code=1), "exit-1"),
                             (PipeProcess(PAYLOAD + b"more"), "source-size-limit")):
            with tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / "boot_a.partial"
                response = backup.stream_copy(FakeAdb(), "boot_a", target, 1,
                                              popen=lambda *a, **k: proc)
                self.assertEqual(response["status"], status)
                self.assertTrue(target.exists())
                self.assertTrue(proc.waited)

    def test_failed_stream_records_manifest_and_partial(self):
        def failed(*args):
            response = fake_stream(*args)
            response["status"] = "timeout"
            return response
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "backup"
            report = backup.backup(FakeAdb(), ["boot_a"], output,
                                   stream=failed, disk_usage=ample_disk)
            self.assertEqual(report["partitions"]["boot_a"]["status"], "timeout")
            self.assertTrue((output / "boot_a.partial").exists())
            self.assertFalse((output / "boot_a.img").exists())

    def test_output_validation_is_reused_before_connecting(self):
        with mock.patch.object(backup.collect, "validate_output",
                               side_effect=backup.collect.CollectionError("existing or unignored")), \
             mock.patch.object(backup.collect, "select_device",
                               side_effect=AssertionError("must not connect")), \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(backup.main(["--partitions", "boot_a", "--output", "docs/out"]), 1)


if __name__ == "__main__":
    unittest.main()

