#!/usr/bin/env python3
"""Read-only Ace bring-up evidence collector. Output must be private/ignored.

Some reads require an already-authorized su. No adbd, SELinux, properties,
slots or partitions are changed. A lost connection leaves partial host evidence
and does not change the device. Raw FDT/proc evidence can contain private data.
"""
import argparse
import json
import os
from pathlib import Path
import shlex
import struct
import subprocess
import sys
import zlib

PROPERTIES = {
    "model": "ro.product.model", "soc": "ro.soc.model",
    "hardware": "ro.hardware", "firmware": "ro.build.display.id",
    "slot": "ro.boot.slot_suffix", "project": "ro.boot.prjname",
    "boot_completed": "sys.boot_completed",
}

# All remote programs only read. dd has NO output file and reads only the
# 32-byte boot-control record, never userdata content.
ITEMS = {
    "live-fdt.dtb": "cat /sys/firmware/fdt",
    "iomem.txt": "cat /proc/iomem",
    "interrupts.txt": "cat /proc/interrupts",
    "reserved-memory.txt": """for d in /proc/device-tree/reserved-memory/*; do
 [ -d "$d" ] || continue
 printf '\\nNODE %s\\n' "${d##*/}"
 for n in reg size alignment alloc-ranges no-map reusable; do
  [ -f "$d/$n" ] || continue
  printf '%s ' "$n"; od -An -tx1 -v "$d/$n"
 done
done""",
    "cpu.txt": """uname -r; getconf PAGESIZE
for d in /sys/devices/system/cpu/cpu[0-9]*; do
 [ -d "$d" ] || continue
 printf '\\nCPU %s\\n' "${d##*/}"
 for n in online regs/identification/midr_el1 regs/identification/revidr_el1; do
  [ -r "$d/$n" ] && { printf '%s ' "$n"; cat "$d/$n"; }
 done
done""",
    "display-input-bindings.txt": """for bus in platform spi i2c; do
 for d in /sys/bus/$bus/devices/*; do
  [ -d "$d" ] || continue
  # Avoid spawning readlink for hundreds of unrelated platform devices.
  if [ "$bus" = platform ]; then
   case "${d##*/}" in
    *drm*|*dsi*|*disp*|*panel*|*touch*|*synaptics*|*s3910*|*ufs*|*usb*|*mtu3*) ;;
    *) continue;;
   esac
  fi
  driver=$(readlink "$d/driver")
  case "$driver ${d##*/}" in
   *drm*|*dsi*|*disp*|*panel*|*touch*|*synaptics*|*s3910*|*ufshci*|*mtu3*)
    printf '%s %s %s\\n' "$bus" "${d##*/}" "$driver";;
  esac
 done
done
for d in /sys/class/drm/*; do
 [ -d "$d" ] || continue
 printf '\\nDRM %s\\n' "${d##*/}"
 for n in status enabled modes; do
  [ -r "$d/$n" ] && { printf '%s ' "$n"; cat "$d/$n"; }
 done
done
for d in /sys/class/input/input*; do
 [ -r "$d/name" ] || continue
 printf '\\nINPUT %s ' "${d##*/}"; cat "$d/name"
 readlink "$d/device/driver"
done""",
    "block-layout.txt": """for d in /sys/class/block/*; do
 [ -d "$d" ] || continue
 case "${d##*/}" in sd*|mmcblk*|dm-*) ;; *) continue;; esac
 printf '\\nBLOCK %s\\n' "${d##*/}"
 for n in dev size start partition queue/logical_block_size queue/physical_block_size; do
  if [ -r "$d/$n" ]; then
   IFS= read -r value < "$d/$n"
   printf '%s %s\\n' "$n" "$value"
  fi
 done
done
ls -l /dev/block/by-name
cat /proc/partitions""",
    "boot-control.bin": "dd if=/dev/block/by-name/misc bs=1 skip=2048 count=32 2>/dev/null",
}

# Missing optional sysfs attributes are normal. Keep the available inventory
# even when the final readlink/test in a loop fails; direct mandatory reads
# (FDT, proc, boot-control) retain their actual exit status.
for _inventory in ("reserved-memory.txt", "cpu.txt", "display-input-bindings.txt",
                   "block-layout.txt"):
    ITEMS[_inventory] += "\n:"


class CollectionError(Exception):
    pass


class Adb:
    def __init__(self, serial, timeout=15, run=None):
        self.serial = serial
        self.timeout = timeout
        self.run = run or subprocess.run

    def read(self, command, root=False):
        # One remote shell string; the whole su -c argument must be quoted.
        remote = "su -c " + shlex.quote(command) if root else command
        try:
            p = self.run(["adb", "-s", self.serial, "exec-out", remote],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         timeout=self.timeout, check=False)
        except subprocess.TimeoutExpired:
            return None, "timeout"
        except OSError:
            return None, "adb-unavailable"
        if p.returncode:
            # adb stderr can repeat transport identifiers. Never persist it.
            return None, "exit-" + str(p.returncode)
        return p.stdout, "ok"


def select_device(requested=None, run=None, timeout=15):
    run = run or subprocess.run
    try:
        p = run(["adb", "devices"], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CollectionError("Cannot list ADB devices.") from exc
    if p.returncode:
        raise CollectionError("Cannot list ADB devices.")
    devices = []
    for line in p.stdout.decode("utf-8", "replace").splitlines()[1:]:
        fields = line.split()
        if len(fields) == 2 and fields[1] == "device":
            devices.append(fields[0])
    if requested:
        if requested not in devices:
            raise CollectionError("Selected device is not connected and authorized.")
        return requested
    if len(devices) != 1:
        raise CollectionError("Connect exactly one authorized device or use --serial.")
    return devices[0]


def validate_output(path, run=None):
    run = run or subprocess.run
    original = Path(path).expanduser()
    if original.exists() or original.is_symlink():
        raise CollectionError("Output already exists; choose a new directory.")
    path = original.resolve()
    if path.exists() or path.is_symlink():
        raise CollectionError("Output already exists; choose a new directory.")
    repo = Path(__file__).resolve().parent.parent
    try:
        relative = path.relative_to(repo)
    except ValueError:
        raise CollectionError("Output must be inside the repository and ignored.") from None
    try:
        p = run(["git", "-C", str(repo), "check-ignore", "--quiet", "--",
                 str(relative)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CollectionError("Cannot verify ignored output.") from exc
    if p.returncode:
        raise CollectionError("Output must be git-ignored (normally research/).")
    return path


def clean(data, serial):
    return data.replace(serial.encode(), b"[redacted-device]") if serial else data


def decode_boot_control(data):
    if len(data) != 32:
        return {"valid": False, "reason": "expected-32-bytes"}
    magic, = struct.unpack_from("<I", data, 4)
    crc, = struct.unpack_from("<I", data, 28)
    if magic != 0x42414342 or zlib.crc32(data[:28]) != crc:
        return {"valid": False, "reason": "magic-or-crc"}
    slots = []
    for offset in (12, 14):
        bits = data[offset]
        slots.append({"priority": bits & 15, "tries_remaining": (bits >> 4) & 7,
                      "successful": bool(bits & 128),
                      "verity_corrupted": bool(data[offset + 1] & 1)})
    return {"valid": True, "slots": slots,
            "note": "Priority metadata does not prove the last executed slot."}


def collect(adb, output):
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    os.chmod(output, 0o700)
    manifest = {"identity": {}, "root": {}, "reads": {}}
    uid, status = adb.read("id -u")
    plain_root = status == "ok" and uid.strip() == b"0"
    manifest["root"]["shell_uid"] = (
        int(uid.strip()) if status == "ok" and uid.strip().isdigit() else None)
    manifest["root"]["shell_status"] = status
    use_su = False
    if not plain_root:
        uid, status = adb.read("id -u", root=True)
        use_su = status == "ok" and uid.strip() == b"0"
        manifest["root"]["su_status"] = status
    manifest["root"]["read_access"] = "shell-root" if plain_root else "su" if use_su else "shell"
    for label, prop in PROPERTIES.items():
        data, status = adb.read("getprop " + prop)
        if status == "ok":
            manifest["identity"][label] = clean(data, adb.serial).decode("utf-8", "replace").strip()[:256]
        else:
            manifest["reads"][label] = status
    for filename, command in ITEMS.items():
        data, status = adb.read(command, root=use_su)
        manifest["reads"][filename] = status
        if status != "ok":
            continue
        # Preserve binary evidence byte-for-byte in private ignored files.
        # FDT may itself contain serial properties; never publish it.
        saved = data if filename.endswith((".dtb", ".bin")) else clean(data, adb.serial)
        target = output / filename
        with target.open("xb") as f:
            os.chmod(target, 0o600)
            f.write(saved)
        if filename == "boot-control.bin":
            manifest["boot_control"] = decode_boot_control(data)
    target = output / "manifest.json"
    with target.open("x", encoding="utf-8") as f:
        os.chmod(target, 0o600)
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serial", help="Explicit ADB device (never saved)")
    parser.add_argument("--output", required=True, type=Path,
                        help="New git-ignored directory, normally research/<name>")
    parser.add_argument("--timeout", type=float, default=15,
                        help="Seconds per command (default 15)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List reads without contacting ADB or writing files")
    args = parser.parse_args(argv)
    if not 0 < args.timeout <= 120:
        parser.error("--timeout must be greater than zero and at most 120")
    try:
        output = validate_output(args.output)
        if args.dry_run:
            print(json.dumps({"mode": "read-only dry-run",
                              "properties": list(PROPERTIES.values()),
                              "items": list(ITEMS),
                              "root_probe": "id -u; su -c 'id -u' if needed",
                              "privacy": "No transport identifier saved; raw FDT/proc evidence is private."},
                             indent=2))
            return 0
        serial = select_device(args.serial, timeout=args.timeout)
        manifest = collect(Adb(serial, args.timeout), output)
        print("Read-only collection finished; inspect manifest.json for unavailable reads.")
        return 0 if all(s == "ok" for s in manifest["reads"].values()) else 2
    except (CollectionError, OSError):
        # Keep diagnostics bounded: exception paths may contain private IDs.
        print("Collection could not start or finish. Check authorization, a new git-ignored output path, and ADB availability.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

