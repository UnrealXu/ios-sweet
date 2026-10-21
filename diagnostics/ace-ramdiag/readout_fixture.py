"""Synthetic read-only USB disk for QEMU command compatibility, never phone IO."""
import hashlib
import importlib.util
from pathlib import Path
import struct
import uuid
import zlib

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('ace_ram_readout_fixture_api', ROOT/'tools/ace_ram_readout.py')
ram = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ram)


def disk(out):
    # Two complete 64MiB extents, deterministic GPT with backup table/header.
    sectors = 264192
    entries = bytearray(128*128)
    descriptors = {}
    for index, name in enumerate(ram.PARTITIONS):
        start = 2048 + index*131072
        identity = uuid.UUID(int=index+1).bytes_le
        kind = uuid.UUID('0fc63daf-8483-4772-8e79-3d69d8477de4').bytes_le
        label = name.encode('utf-16-le').ljust(72, b'\0')
        entries[index*128:(index+1)*128] = struct.pack('<16s16sQQQ72s',kind,identity,start,start+131071,0,label)
        descriptors[name] = dict(start_512=start,sectors_512=131072,number=index+1)
    def header(at, backup, table):
        value = bytearray(struct.pack('<8sIIIIQQQQ16sQIII', b'EFI PART',0x10000,92,0,0,at,backup,34,sectors-34,uuid.UUID(int=3).bytes_le,table,128,128,zlib.crc32(entries)))
        struct.pack_into('<I',value,16,zlib.crc32(value))
        return value.ljust(512,b'\0')
    path = out/'synthetic-readout-gpt.img'
    hashes = {}
    with path.open('xb') as stream:
        stream.truncate(sectors*512)
        mbr = bytearray(512)
        mbr[446:462] = struct.pack('<B3sB3sII',0,b'\0'*3,0xee,b'\xff'*3,1,sectors-1)
        mbr[510:] = b'\x55\xaa'
        stream.seek(0);stream.write(mbr+header(1,sectors-1,2)+entries)
        stream.seek((sectors-33)*512);stream.write(entries+header(sectors-1,1,sectors-33))
        for index,(name, part) in enumerate(descriptors.items()):
            # Distinct full-size deterministic data, no sparse-only hash shortcut.
            chunk = bytes([index+65])*(1024*1024)
            digest = hashlib.sha256()
            stream.seek(part['start_512']*512)
            for _ in range(64):stream.write(chunk);digest.update(chunk)
            hashes[name] = digest.hexdigest()
    return path, descriptors, hashes


def check(client, out, descriptors, hashes):
    setup = client.shell("mkdir -p /dev/block/by-name; ln -s /dev/block/sda1 /dev/block/by-name/boot_b; ln -s /dev/block/sda2 /dev/block/by-name/vendor_boot_b; echo ACE_FIXTURE_ALIASES_READY")
    ram.require(b'ACE_FIXTURE_ALIASES_READY' in setup, 'QEMU RAM aliases unavailable')
    observations = {}
    for name in ram.PARTITIONS:
        raw = client.shell(ram.partition_command(name))
        out.joinpath('command-partition-'+name+'.txt').write_bytes(raw)
        # shell service (unlike physical exec-out) may transform newline bytes.
        observation = ram.parse_partition(raw.replace(b'\r\n',b'\n'),name)
        ram.require(observation['SHA256'] == hashes[name], 'synthetic complete partition digest mismatch')
        part = descriptors[name]
        ram.require(observation['SECTORS_512'] == part['sectors_512'] and observation['START_512'] == part['start_512'] and observation['NUMBER'] == part['number'], 'synthetic GPT geometry mismatch')
        try:ram.validate_partition(observation,name,dict(partitions=descriptors,candidate_sha256=hashes['boot_b']))
        except ValueError as error:
            ram.require('expected UFS controller' in str(error), 'fixture rejected at unexpected gate: '+str(error))
        else:raise ValueError('synthetic USB disk incorrectly accepted as physical UFS')
        observations[name] = observation
    ram.require(observations['boot_b']['device_number'] != observations['vendor_boot_b']['device_number'], 'synthetic aliases collide')
    return dict(full_partition_command_verified=True, synthetic_usb_disk_refused_as_ufs=True, partition_observations=observations)
