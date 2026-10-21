#!/usr/bin/env python3
"""Build an OFFLINE diagnostic vendor_boot for the exact PGKM10 H.20 OTA.

No adb, fastboot, device writes, partition mounts, or target execution. The
result is experimental, not an iOS image. It enables unauthenticated root ADB
in recovery and asks Android for permissive SELinux. Restore the original
vendor_boot before normal use. It must never be distributed as stock firmware.

Only the SHA256-verified original vendor_boot below is accepted. Supply an
explicit, inspected AOSP mkbootimg and avbtool checkouts and an absent output
directory. The self-contained AVB hash is unsigned; the original parent vbmeta
will still reject its changed content unless firmware permits that mismatch.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

STOCK_SHA256 = 'bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670'
INIT = 'system/etc/init/hw/init.rc'
PROPS = {'ro.secure': '0', 'ro.adb.secure': '0', 'ro.debuggable': '1'}
STOCK_AVB_SALT = '618a857ed39216335f988919ffef8507'
STOCK_AVB_FINGERPRINT = ('alps/hal_mgvi_64_armv82/mgvi_64_armv82:12/'
                         'SP1A.210812.016/1775212331257:user/release-keys')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def align(n, size=4096):
    return (n + size - 1) // size * size


def read_avb_footer(data):
    require(len(data) >= 64, 'AVB footer missing')
    magic, major, minor, size, offset, vbmeta_size, reserved = struct.unpack(
        '>4sIIQQQ28s', data[-64:])
    require(magic == b'AVBf' and (major, minor) == (1, 0), 'invalid AVB footer')
    require(not any(reserved), 'unexpected AVB footer reserved bytes')
    require(0 < size <= offset and offset + vbmeta_size <= len(data) - 64,
            'AVB footer bounds invalid')
    require(data[offset:offset + 4] == b'AVB0', 'AVB metadata header missing')
    return {'original_image_size': size, 'vbmeta_offset': offset,
            'vbmeta_size': vbmeta_size}


def read_vendor(data):
    require(data[:8] == b'VNDRBOOT', 'not a vendor_boot image')
    version, page, kernel, ramdisk_addr, ramdisk_size = struct.unpack_from('<5I', data, 8)
    require(version == 4 and page == 4096, 'expected vendor_boot v4, 4096-byte pages')
    header_size, dtb_size, dtb_addr = struct.unpack_from('<IIQ', data, 2096)
    table_size, count, entry_size, config_size = struct.unpack_from('<4I', data, 2112)
    require(header_size == 2128 and count == 1 and entry_size == 108, 'unexpected ramdisk layout')
    rd_offset = align(header_size, page)
    dt_offset = rd_offset + align(ramdisk_size, page)
    tab_offset = dt_offset + align(dtb_size, page)
    cfg_offset = tab_offset + align(table_size, page)
    require(cfg_offset + config_size <= len(data), 'truncated vendor_boot')
    table = data[tab_offset:tab_offset + table_size]
    size, offset, kind = struct.unpack_from('<3I', table)
    require(size == ramdisk_size and offset == 0 and kind == 1, 'unexpected fragment entry')
    require(not any(table[12:]), 'expected empty fragment name and zero board IDs')
    return {
        'kernel_address': kernel, 'ramdisk_address': ramdisk_addr,
        'tags_address': struct.unpack_from('<I', data, 2076)[0],
        'dtb_address': dtb_addr,
        'cmdline': data[28:2076].split(b'\0', 1)[0].decode('ascii'),
        'board': data[2080:2096].split(b'\0', 1)[0].decode('ascii'),
        'ramdisk': data[rd_offset:rd_offset + ramdisk_size],
        'dtb': data[dt_offset:dt_offset + dtb_size],
        'bootconfig': data[cfg_offset:cfg_offset + config_size],
    }


def read_cpio(raw):
    entries, offset = [], 0
    while offset + 110 <= len(raw):
        require(raw[offset:offset + 6] == b'070701', 'only newc CPIO without CRC is supported')
        fields = [int(raw[offset + 6 + j * 8:offset + 14 + j * 8], 16) for j in range(13)]
        name_end = offset + 110 + fields[11]
        require(fields[11] > 0 and name_end <= len(raw) and raw[name_end - 1] == 0, 'bad CPIO name')
        name = raw[offset + 110:name_end - 1].decode('utf-8')
        start = align(name_end, 4)
        end = start + fields[6]
        require(end <= len(raw), 'truncated CPIO data')
        entries.append((name, fields, raw[start:end]))
        offset = align(end, 4)
        if name == 'TRAILER!!!':
            require(not any(raw[offset:]), 'unexpected data after CPIO trailer')
            return entries
    raise ValueError('CPIO trailer missing')


def write_cpio(entries):
    raw = bytearray()
    for name, fields, data in entries:
        encoded = name.encode() + b'\0'
        fields = list(fields)
        fields[6], fields[11], fields[12] = len(data), len(encoded), 0
        raw.extend(b'070701' + ''.join(f'{v:08x}' for v in fields).encode())
        raw.extend(encoded)
        raw.extend(b'\0' * (align(len(raw), 4) - len(raw)))
        raw.extend(data)
        raw.extend(b'\0' * (align(len(raw), 4) - len(raw)))
    raw.extend(b'\0' * (align(len(raw), 512) - len(raw)))
    return bytes(raw)


def diagnostic_init(text):
    """Keep stock USB configuration; disable recovery UI and disk-side actions."""
    allowed_services = {'ueventd', 'adbd', 'console', 'logd'}
    blocked_services = set(re.findall(r'^service (\S+)', text, re.M)) - allowed_services
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == 'import /system/etc/init.aging.rc':
            continue
        if stripped in {'load_fastboot_adb_props', 'load_persist_props'}:
            continue
        if stripped.startswith(('exec ', 'exec_start ')):
            continue
        if stripped.startswith('copy ') and any(p in stripped for p in ('/cache/', '/data/', '/persist/', '/odm/')):
            continue
        if '/dev/block/' in stripped and stripped.startswith('mount '):
            continue
        if stripped.startswith('start ') and stripped.split()[1] not in allowed_services:
            continue
        lines.append(line)
        if line.startswith('service ') and line.split()[1] in blocked_services:
            lines.append('    disabled')
    result = '\n'.join(lines) + '''

# Diagnostic-only scratch paths: writes remain in RAM, not persistent FS.
on init
    mkdir /data 0755 root root
    mount tmpfs tmpfs /data mode=0755,uid=0,gid=0
    mkdir /cache 0755 root root
    mount tmpfs tmpfs /cache mode=0755,uid=0,gid=0
    mkdir /metadata 0755 root root
    mount tmpfs tmpfs /metadata mode=0755,uid=0,gid=0
    mkdir /mnt 0755 root root
    mkdir /mnt/vendor 0755 root root
    mkdir /mnt/vendor/persist 0755 root root
    mount tmpfs tmpfs /mnt/vendor/persist mode=0755,uid=0,gid=0
'''
    require('service adbd ' in result, 'ADB service missing')
    require('on fs && property:ro.debuggable=1' in result, 'stock ADB trigger missing')
    require('    mount ext4 /dev/block/' not in result, 'persistent block mount remains')
    require('    exec /sbin/e2fsck' not in result, 'filesystem repair remains')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stock-vendor-boot', type=Path, required=True)
    parser.add_argument('--mkbootimg', type=Path, required=True, help='inspected AOSP mkbootimg.py')
    parser.add_argument('--avbtool', type=Path, required=True, help='inspected AOSP avbtool.py')
    parser.add_argument('--output-dir', type=Path, required=True, help='must not exist')
    args = parser.parse_args()
    original = args.stock_vendor_boot.read_bytes()
    require(sha(original) == STOCK_SHA256, 'wrong stock image: SHA256 does not match PGKM10 H.20')
    require(args.mkbootimg.is_file(), 'mkbootimg.py missing')
    require(args.avbtool.is_file(), 'avbtool.py missing')
    require(not args.output_dir.exists(), 'output directory already exists')
    original_footer = read_avb_footer(original)
    stock = read_vendor(original)
    raw = subprocess.run(['lz4', '-dc'], input=stock['ramdisk'], capture_output=True, check=True).stdout
    entries = read_cpio(raw)
    require(len({n for n, _, _ in entries}) == len(entries), 'duplicate CPIO paths')
    changed, rebuilt = {}, []
    for name, fields, data in entries:
        updated = data
        if fields[1] & 0xf000 == 0x8000:
            if Path(name).name.startswith('fstab') or name.endswith('.fstab'):
                # First-stage init runs before the recovery init.rc. Do not
                # let it consume stock rw/check/formattable partition entries.
                updated = b'# Ace diagnostic: no persistent filesystem mounts.\n'
            elif name.endswith('.prop') or name == 'prop.default':
                text = data.decode('utf-8')
                for key, value in PROPS.items():
                    text = re.sub(r'^' + re.escape(key) + r'=[^\r\n]*', key + '=' + value, text, flags=re.M)
                updated = text.encode()
            elif name == INIT:
                updated = diagnostic_init(data.decode()).encode()
            elif name == 'init.recovery.mt6895.rc':
                # Keep the board's USB configfs/controller setup, not its
                # platform utility or any other executable boot action.
                lines = [line for line in data.decode().splitlines()
                         if not line.strip().startswith(('exec ', 'exec_start ', 'start '))]
                updated = ('\n'.join(lines) + '\n').encode()
        if updated != data:
            changed[name] = {'old_sha256': sha(data), 'new_sha256': sha(updated)}
        rebuilt.append((name, fields, updated))
    require(INIT in changed and 'prop.default' in changed, 'expected configuration changes missing')
    fstabs = [name for name, _, _ in rebuilt
              if Path(name).name.startswith('fstab') or name.endswith('.fstab')]
    require('first_stage_ramdisk/fstab.mt6895' in fstabs, 'first-stage fstab missing')
    for name, fields, data in rebuilt:
        if name in fstabs and fields[1] & 0xf000 == 0x8000:
            require(not any(line.strip() and not line.lstrip().startswith(b'#')
                            for line in data.splitlines()), 'active fstab entry remains: ' + name)
    raw_new = write_cpio(rebuilt)
    verified_entries = read_cpio(raw_new)
    require(len(verified_entries) == len(rebuilt), 'CPIO entry count changed')
    for before, after in zip(rebuilt, verified_entries):
        name, fields, data = before
        expected_fields = list(fields)
        expected_fields[6] = len(data)
        expected_fields[11] = len(name.encode()) + 1
        expected_fields[12] = 0
        require(after == (name, expected_fields, data), 'CPIO verification failed: ' + name)
    args.output_dir.mkdir(parents=True)
    compressed = args.output_dir / 'diagnostic-ramdisk.lz4'
    compressed.write_bytes(subprocess.run(['lz4', '-l', '-c', '-9'], input=raw_new, capture_output=True, check=True).stdout)
    dtb = args.output_dir / 'original-dtb-table.bin'
    dtb.write_bytes(stock['dtb'])
    config = args.output_dir / 'original-bootconfig.bin'
    config.write_bytes(stock['bootconfig'])
    output = args.output_dir / 'vendor_boot-ace-diag-UNTESTED.img'
    cmdline = stock['cmdline'] + ' androidboot.selinux=permissive'
    subprocess.run([
        sys.executable, str(args.mkbootimg.resolve()), '--header_version', '4',
        '--pagesize', '4096', '--base', '0',
        '--kernel_offset', hex(stock['kernel_address']),
        '--ramdisk_offset', hex(stock['ramdisk_address']),
        '--tags_offset', hex(stock['tags_address']), '--dtb_offset', hex(stock['dtb_address']),
        '--board', stock['board'], '--vendor_cmdline', cmdline,
        '--dtb', str(dtb), '--vendor_bootconfig', str(config),
        '--ramdisk_type', '1', '--ramdisk_name', '',
        '--vendor_ramdisk_fragment', str(compressed), '--vendor_boot', str(output),
    ], check=True)
    unsigned_size = output.stat().st_size
    subprocess.run([
        sys.executable, str(args.avbtool.resolve()), 'add_hash_footer',
        '--image', str(output), '--partition_size', str(len(original)),
        '--partition_name', 'vendor_boot', '--hash_algorithm', 'sha256',
        '--salt', STOCK_AVB_SALT, '--algorithm', 'NONE',
        '--prop', 'com.android.build.vendor_boot.fingerprint:' + STOCK_AVB_FINGERPRINT,
    ], check=True)
    result = output.read_bytes()
    footer = read_avb_footer(result)
    require(len(result) == len(original), 'AVB image must fill the original partition')
    require(footer['original_image_size'] == unsigned_size, 'AVB original size mismatch')
    # avbtool resolves hash descriptors by partition name beside the input.
    # Give it that name in an isolated host directory, never a device path.
    with tempfile.TemporaryDirectory(prefix='avb-check-', dir=args.output_dir) as tmp:
        verify_image = Path(tmp) / 'vendor_boot.img'
        verify_image.symlink_to(output.resolve())
        subprocess.run([sys.executable, str(args.avbtool.resolve()), 'verify_image',
                        '--image', str(verify_image)], check=True)
    checked = read_vendor(result)
    for key in ('kernel_address', 'ramdisk_address', 'tags_address', 'dtb_address', 'board', 'dtb', 'bootconfig'):
        require(checked[key] == stock[key], 'preserved field changed: ' + key)
    restored = subprocess.run(['lz4', '-dc'], input=checked['ramdisk'], capture_output=True, check=True).stdout
    require(restored == raw_new, 'repacked ramdisk mismatch')
    require(len(result) <= len(original), 'diagnostic image exceeds original partition image')
    report = {
        'status': 'offline-verified-device-UNTESTED', 'stock_sha256': sha(original),
        'output_sha256': sha(result), 'output_bytes': len(result),
        'stock_avb_footer': original_footer, 'output_avb_footer': footer,
        'self_avb_hash_verified': True, 'self_avb_algorithm': 'NONE',
        'tool_sha256': {'mkbootimg': sha(args.mkbootimg.read_bytes()),
                        'avbtool': sha(args.avbtool.read_bytes())},
        'changed_cpio_files': changed, 'original_dtb_sha256': sha(stock['dtb']),
        'cmdline': cmdline,
        'limitations': ['not iOS', 'not boot tested', 'no vendor AVB signature',
                        'original parent vbmeta vendor_boot hash still mismatches',
                        'self AVB footer does not establish firmware acceptance',
                        'recovery ADB intended to run unauthenticated as root',
                        'normal Android boot may fail until stock vendor_boot is restored',
                        'restore stock vendor_boot before normal use',
                        'external analysis cannot prove absence of runtime writes'],
    }
    (args.output_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
