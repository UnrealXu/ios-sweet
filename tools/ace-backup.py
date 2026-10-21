#!/usr/bin/env python3
"""Prepare or perform read-only raw partition backups for OnePlus Ace.

Default mode is a host-only plan. Actual reads require --partitions and --output.
This tool does not represent an already completed phone backup, does not restore
backups, and never freezes, reboots, flashes or changes device configuration.
Calibration backups are private; keep the ignored output directory private.
Live Android may change calibration data: only identical before/after device
hashes and a matching host hash are marked verified.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import selectors
import shlex
import shutil
import subprocess
import sys
import time

_spec = importlib.util.spec_from_file_location(
    "ace_collect_for_backup", Path(__file__).with_name("ace-collect.py"))
collect = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(collect)

ALLOWED = tuple(
    name + "_" + slot
    for name in ("boot", "vendor_boot", "dtbo", "vbmeta", "vbmeta_system", "vbmeta_vendor")
    for slot in ("a", "b")
) + ("nvram", "nvdata", "nvcfg", "persist", "protect1", "protect2",
     "protect_f", "protect_s", "proinfo")
MAX_PARTITION = 1024 ** 3
MAX_TOTAL = 4 * 1024 ** 3
DISK_RESERVE = 256 * 1024 ** 2


def partitions(value):
    names = value.split(",")
    if not names or any(name not in ALLOWED for name in names):
        raise collect.CollectionError("Use only exact comma-separated allowed partition names.")
    if len(set(names)) != len(names):
        raise collect.CollectionError("Duplicate partitions are not allowed.")
    return names


def block_path(name):
    if name not in ALLOWED:
        raise collect.CollectionError("Partition is not allowed.")
    return "/dev/block/by-name/" + name


def source_hash(adb, name, use_su):
    data, status = adb.read("sha256sum " + block_path(name), root=use_su)
    if status != "ok":
        return None, status
    fields = data.split()
    if not fields or not re.fullmatch(b"[0-9a-fA-F]{64}", fields[0]):
        return None, "invalid-hash-response"
    return fields[0].decode("ascii").lower(), "ok"


def preflight(adb, names, use_su, output, disk_usage=None):
    disk_usage = disk_usage or shutil.disk_usage
    sizes = {}
    for name in names:
        data, status = adb.read("blockdev --getsize64 " + block_path(name), root=use_su)
        if status != "ok" or not re.fullmatch(b"[0-9]+\\s*", data):
            raise collect.CollectionError("Cannot read an allowed partition size.")
        size = int(data.strip())
        if not 0 < size <= MAX_PARTITION:
            raise collect.CollectionError("Partition exceeds the 1 GiB limit or is empty.")
        sizes[name] = size
    total = sum(sizes.values())
    if total > MAX_TOTAL:
        raise collect.CollectionError("Requested partitions exceed the 4 GiB total limit.")
    ancestor = output.parent
    while not ancestor.exists():
        ancestor = ancestor.parent
    if disk_usage(ancestor).free < total + DISK_RESERVE:
        raise collect.CollectionError("Insufficient host free space including 256 MiB reserve.")
    return sizes


def stream_copy(adb, name, target, timeout, popen=None):
    """Stream bounded chunks; kill/reap the child on timeout or host I/O error."""
    popen = popen or subprocess.Popen
    # exec-out uses a raw service: remote stderr may share the data channel.
    # Suppress dd's progress/statistics in the remote shell, not just on host.
    remote = "dd if=" + block_path(name) + " bs=4194304 2>/dev/null"
    if adb.use_su:
        remote = "su -c " + shlex.quote(remote)
    args = ["adb", "-s", adb.serial, "exec-out", remote]
    digest = hashlib.sha256()
    count = 0
    proc = None
    status = "host-error"
    selector = selectors.DefaultSelector()
    try:
        with target.open("xb") as file:
            os.chmod(target, 0o600)
            proc = popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL)
            selector.register(proc.stdout, selectors.EVENT_READ)
            deadline = time.monotonic() + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    status = "timeout"
                    break
                ready = selector.select(min(remaining, 1.0))
                if not ready:
                    continue
                chunk = os.read(proc.stdout.fileno(), 1024 * 1024)
                if not chunk:
                    try:
                        code = proc.wait(timeout=max(0.001, deadline - time.monotonic()))
                        status = "ok" if code == 0 else "exit-" + str(code)
                    except subprocess.TimeoutExpired:
                        status = "timeout"
                    break
                if count + len(chunk) > adb.expected_sizes.get(name, MAX_PARTITION):
                    status = "source-size-limit"
                    break
                file.write(chunk)
                digest.update(chunk)
                count += len(chunk)
            file.flush()
            os.fsync(file.fileno())
    except (OSError, ValueError):
        status = "host-error"
    finally:
        selector.close()
        if proc is not None:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
            if proc.stdout is not None:
                proc.stdout.close()
    return {"status": status, "bytes": count, "host_sha256": digest.hexdigest()}


def write_manifest(output, manifest):
    temporary = output / "manifest.json.partial"
    with temporary.open("w", encoding="utf-8") as file:
        os.chmod(temporary, 0o600)
        json.dump(manifest, file, indent=2)
        file.write("\n")
    temporary.replace(output / "manifest.json")


def verify_host_file(path):
    """Read the actual saved file independently, with bounded memory."""
    digest = hashlib.sha256()
    count = 0
    with path.open("rb") as file:
        while True:
            chunk = file.read(1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            digest.update(chunk)
    return count, digest.hexdigest()


def backup(adb, names, output, timeout=300, stream=None, disk_usage=None):
    stream = stream or stream_copy
    uid, status = adb.read("id -u")
    root = status == "ok" and uid.strip() == b"0"
    use_su = False
    if not root:
        uid, status = adb.read("id -u", root=True)
        use_su = status == "ok" and uid.strip() == b"0"
    if not root and not use_su:
        raise collect.CollectionError("An already-authorized root shell or su is required.")
    adb.use_su = use_su
    sizes = preflight(adb, names, use_su, output, disk_usage)
    adb.expected_sizes = sizes
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    os.chmod(output, 0o700)
    manifest = {"mode": "read-only live backup", "root": "su" if use_su else "shell-root",
                "warning": "No restore was performed; live data may change.",
                "partitions": {}}
    write_manifest(output, manifest)
    for name in names:
        record = {"expected_bytes": sizes[name], "verified": False}
        manifest["partitions"][name] = record
        before, status = source_hash(adb, name, use_su)
        record["before_status"] = status
        if before is None:
            write_manifest(output, manifest)
            continue
        record["device_sha256_before"] = before
        record["status"] = "streaming"
        write_manifest(output, manifest)
        partial = output / (name + ".partial")
        record.update(stream(adb, name, partial, timeout))
        if record["status"] == "ok":
            record["stream_sha256"] = record["host_sha256"]
            try:
                record["bytes"], record["host_sha256"] = verify_host_file(partial)
            except OSError:
                record["status"] = "host-verification-error"
                write_manifest(output, manifest)
                continue
            after, status = source_hash(adb, name, use_su)
            record["after_status"] = status
            record["device_sha256_after"] = after
            record["stable"] = after is not None and before == after
            record["verified"] = (record["stable"] and record["bytes"] == sizes[name]
                                  and record["host_sha256"] == before)
            if record["verified"]:
                partial.replace(output / (name + ".img"))
                record["status"] = "verified"
            elif not record["stable"]:
                record["status"] = "device-changed-or-after-hash-unavailable"
            else:
                record["status"] = "length-or-hash-mismatch"
        write_manifest(output, manifest)
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true", help="Host-only whitelist and limits; default")
    parser.add_argument("--partitions", help="Explicit comma-separated allowlisted names to actually read")
    parser.add_argument("--output", type=Path, help="New private git-ignored host directory")
    parser.add_argument("--serial", help="Explicit ADB selection; never saved")
    parser.add_argument("--timeout", type=float, default=300,
                        help="Seconds per metadata query and per streamed partition")
    args = parser.parse_args(argv)
    if not 0 < args.timeout <= 3600:
        parser.error("--timeout must be greater than zero and at most 3600")
    if args.plan and args.partitions:
        parser.error("--plan cannot be combined with --partitions")
    if args.plan or not args.partitions:
        print(json.dumps({"mode": "plan only; no phone accessed",
                          "recommended_allowlist": ALLOWED,
                          "max_partition_bytes": MAX_PARTITION,
                          "max_total_bytes": MAX_TOTAL,
                          "host_reserve_bytes": DISK_RESERVE,
                          "note": "Some allowed names may not exist on this phone. No completed backup or restore is claimed."},
                         indent=2))
        return 0
    try:
        names = partitions(args.partitions)
        if args.output is None:
            raise collect.CollectionError("--output is required for actual backups.")
        output = collect.validate_output(args.output)
        serial = collect.select_device(args.serial, timeout=args.timeout)
        adb = collect.Adb(serial, timeout=args.timeout)
        manifest = backup(adb, names, output, timeout=args.timeout)
        print("Read-only backup finished; inspect manifest.json. Unverified partial files are retained.")
        return 0 if all(r["verified"] for r in manifest["partitions"].values()) else 2
    except collect.CollectionError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except OSError:
        print("Host backup I/O failed; inspect private partial files and manifest.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

