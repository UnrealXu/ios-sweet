"""Read-only direct-root RAM diagnostic contract. No transport or reboot calls."""
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess


class EvidenceReader:
    """One read, fresh serial-bound transport, every command result retained.

    No generic read retry. The caller may reobserve an incomplete native record
    through the existing three-observation return guard only.
    """
    def __init__(self, out, find_adb, run):
        self.out, self.find_adb, self.run = out, find_adb, run
        self.observations = []

    def read(self, command, timeout=120, allow_failure=False):
        device = self.find_adb()
        item = dict(command=command, identity_verified=bool(device))
        stem = 'ram-command-%03d' % len(self.observations)
        raw, stderr, rc = b'', b'', None
        try:
            if not device:
                raise RuntimeError('expected phone unavailable for RAM evidence read')
            result = self.run(['adb', '-s', device, 'exec-out', 'sh -c ' + shlex.quote(command)], timeout)
            raw, stderr, rc = result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired as error:
            raw, stderr = error.stdout or b'', error.stderr or b''
            item['exception'] = str(error)
            if not allow_failure:
                raise
        except (RuntimeError, OSError) as error:
            item['exception'] = str(error)
            raise
        finally:
            self.out.joinpath(stem + '.stdout').write_bytes(raw)
            self.out.joinpath(stem + '.stderr').write_bytes(stderr)
            item.update(returncode=rc, stdout=stem + '.stdout', stderr=stem + '.stderr',
                        bytes=len(raw), sha256=sha(raw))
            self.observations.append(item)
            self.out.joinpath('ram-command-observations.json').write_text(json.dumps(self.observations, indent=2) + '\n')
        if rc and not allow_failure:
            raise RuntimeError('RAM evidence command failed; observation retained')
        return raw

VENDOR_SHA = 'bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670'
KERNEL_SHA = '8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'
PARTITION_BYTES = 64 * 1024 * 1024
PARTITIONS = ('boot_b', 'vendor_boot_b')
UFS_COMPONENT = '112b0000.ufshci'
READY = 'ramdiag-v1'
RECORD_COMMAND = 'cat /sys/firmware/devicetree/base/chosen/ace,native-refusal'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def load_contract(state, trial, serial, controller_sha256):
    """Select RAM only through an explicitly pinned prepared-trial contract."""
    name = state.get('readout_profile', 'android-v1')
    if name == 'android-v1':
        return None
    require(name == READY, 'unknown readout profile')
    relative = Path(state['ramdiag_contract_file'])
    require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe RAM contract path')
    path = (trial / relative).resolve()
    require(path.is_relative_to(trial.resolve()), 'RAM contract escapes trial')
    raw = path.read_bytes()
    require(digest(state['ramdiag_contract_sha256']) and sha(raw) == state['ramdiag_contract_sha256'], 'RAM contract hash mismatch')
    contract = json.loads(raw)
    require(contract['format'] == 'ACE_RAMDIAG_HOST_V1', 'RAM host contract format')
    require(contract['serial'] == serial and contract['run_token'] == state['run_token'], 'RAM contract serial/token mismatch')
    require(re.fullmatch('[0-9a-f]{16}', contract['run_token']), 'invalid RAM token')
    require(contract['candidate_sha256'] == state['candidate_sha256'] and digest(contract['candidate_sha256']), 'RAM candidate pin mismatch')
    require(contract['vendor_sha256'] == VENDOR_SHA and contract['kernel_sha256'] == KERNEL_SHA, 'RAM vendor/kernel pin mismatch')
    require(contract['controller_sha256'] == controller_sha256 and contract['validator_sha256'] == sha(Path(__file__).read_bytes()), 'RAM controller source pin mismatch')
    require(digest(contract['bundle_id']) and digest(contract['guest_profile_sha256']), 'RAM profile identity pin missing')
    require(set(contract['partitions']) == set(PARTITIONS), 'RAM partition set mismatch')
    for part in contract['partitions'].values():
        for key in ['start_512', 'sectors_512', 'number']:
            require(type(part[key]) is int and part[key] > 0, 'invalid partition geometry')
        require(part['sectors_512'] * 512 == PARTITION_BYTES and part['start_512'] % 8 == 0, 'RAM partition full-size/alignment mismatch')
    first, second = sorted(contract['partitions'].values(), key=lambda p: p['start_512'])
    require(first['start_512'] + first['sectors_512'] <= second['start_512'] and first['number'] != second['number'], 'RAM partition contract overlaps or repeats a partition number')
    return contract


def snapshot_command(nonce):
    require(re.fullmatch('[0-9a-f]{32}', nonce), 'invalid snapshot nonce')
    return """set -e
echo ACE_RAM_STATE_V1:%s
echo SERIAL=$(getprop ro.serialno)
echo SLOT=$(getprop ro.boot.slot_suffix)
echo ROOT_UID=$(id -u)
echo SECURE=$(getprop ro.adb.secure)
echo READY=$(getprop sys.ace.ramdiag.ready)
if [ -e /data ]; then echo HAS_DATA=1; else echo HAS_DATA=0; fi
echo PROFILE_BEGIN
cat /ace-ramdiag/profile.json
printf '\\nPROFILE_END\\n'
echo COMPLETE_BEGIN
cat /tmp/ace-ramdiag-modules-complete
printf '\\nCOMPLETE_END\\n'
echo RETURN_BEGIN
cat /tmp/ace-ramdiag-return-checkpoint
printf '\\nRETURN_END\\n'
echo MOUNTS_BEGIN
cat /proc/1/mountinfo
printf '\\nMOUNTS_END\\n'
""" % nonce


def section(raw, name):
    begin, end = (name + '_BEGIN\n').encode(), ('\n' + name + '_END\n').encode()
    require(raw.count(begin) == 1 and raw.count(end) == 1, 'missing/duplicate section ' + name)
    after = raw.split(begin, 1)[1]
    require(end in after, 'misordered section ' + name)
    return after.split(end, 1)[0]


def validate_snapshot(raw, contract, nonce):
    # exec-out is binary-safe. CRLF normalization would weaken exact profile and
    # receipt checks; a PTY-transformed response is intentionally rejected.
    prefix = ('ACE_RAM_STATE_V1:' + nonce + '\n').encode()
    require(raw.startswith(prefix), 'fresh RAM snapshot nonce mismatch')
    header = raw[len(prefix):].split(b'PROFILE_BEGIN\n', 1)[0].decode('ascii')
    fields = {}
    for line in header.splitlines():
        key, sep, value = line.partition('=')
        require(sep and key not in fields, 'malformed/duplicate RAM state field')
        fields[key] = value
    require(fields == dict(SERIAL=contract['serial'], SLOT='_b', ROOT_UID='0', SECURE='1', READY=READY, HAS_DATA='0'), 'RAM root/serial/slot/auth/readiness/data mismatch')
    profile = section(raw, 'PROFILE')
    require(sha(profile) == contract['guest_profile_sha256'], 'guest profile hash mismatch')
    value = json.loads(profile)
    require(value == {k: contract[k] for k in ['serial', 'run_token', 'bundle_id', 'kernel_sha256']} | {'format': 'ACE_RAMDIAG_GUEST_V1'}, 'guest profile context mismatch')
    receipt = (contract['bundle_id'] + '\n').encode()
    require(section(raw, 'COMPLETE') == receipt and section(raw, 'RETURN') == receipt, 'RAM completion/return receipt mismatch')
    mounts = section(raw, 'MOUNTS').decode('ascii').splitlines()
    require(mounts, 'missing PID1 mounts')
    points = set()
    allowed = {'rootfs', 'tmpfs', 'proc', 'sysfs', 'devpts', 'selinuxfs', 'cgroup', 'cgroup2', 'configfs', 'functionfs', 'pstore'}
    for line in mounts:
        columns = line.split()
        require(len(columns) >= 10 and ' - ' in line, 'malformed PID1 mountinfo')
        point = columns[4]
        require('\\' not in point and point != '/data' and not point.startswith('/data/'), 'data/escaped mountpoint refused')
        require(line.split(' - ', 1)[1].split()[0] in allowed, 'persistent filesystem in RAM profile')
        points.add(point)
    require({'/', '/tmp', '/dev', '/proc', '/sys'} <= points, 'incomplete RAM virtual mounts')
    return dict(root_identity_verified=True, module_receipts_verified=True, no_data_verified=True,
                virtual_mounts_only=True, guest_profile_sha256=sha(profile), mountinfo=mounts)


def partition_command(name):
    require(name in PARTITIONS, 'unapproved partition query')
    return """set -e
dev=/dev/block/by-name/%s
[ -b "$dev" ]
node=$(readlink -f "$dev")
base=${node##*/}
case "$base" in ''|*[!A-Za-z0-9._-]*) exit 27;; esac
sys=/sys/class/block/$base
rdev=$(stat -Lc '%%t:%%T' "$dev")
sysdev=$(cat "$sys/dev")
sectors=$(cat "$sys/size")
start=$(cat "$sys/start")
number=$(cat "$sys/partition")
ancestry=$(readlink -f "$sys")
parent=${ancestry%%/*}
logical=$(cat "$parent/queue/logical_block_size")
echo ACE_RAM_PARTITION_V1
echo NODE=$node
echo RDEV=$rdev
echo SYSDEV=$sysdev
echo SECTORS_512=$sectors
echo START_512=$start
echo NUMBER=$number
echo ANCESTRY=$ancestry
echo LOGICAL_BLOCK_SIZE=$logical
echo UEVENT_BEGIN
cat "$sys/uevent"
printf '\\nUEVENT_END\\n'
hash=$(sha256sum "$dev")
echo "SHA256=$hash"
""" % name


def parse_partition(raw, name):
    require(name in PARTITIONS and raw.startswith(b'ACE_RAM_PARTITION_V1\n'), 'partition observation format')
    text = raw.decode('ascii')
    before, after = text.split('UEVENT_BEGIN\n', 1)
    event, after = after.split('\nUEVENT_END\n', 1)
    fields = {}
    for line in before.splitlines()[1:] + after.splitlines():
        key, sep, value = line.partition('=')
        require(sep and key not in fields, 'duplicate/malformed partition field')
        fields[key] = value
    expected_fields = {'NODE', 'RDEV', 'SYSDEV', 'SECTORS_512', 'START_512', 'NUMBER', 'ANCESTRY', 'LOGICAL_BLOCK_SIZE', 'SHA256'}
    require(set(fields) == expected_fields, 'partition fields incomplete')
    uevent = {}
    for line in event.splitlines():
        if not line:
            continue
        key, sep, value = line.partition('=')
        require(sep and key not in uevent, 'duplicate/malformed block uevent')
        uevent[key] = value
    require(uevent.get('PARTNAME') == name and uevent.get('DEVTYPE') == 'partition', 'partition label/type mismatch')
    node = fields['NODE']
    require(re.fullmatch(r'/dev/block/[A-Za-z0-9._-]+', node), 'unexpected resolved block path')
    require(uevent.get('DEVNAME') == node.rsplit('/', 1)[1], 'block node/sysfs name mismatch')
    require(re.fullmatch(r'[0-9a-fA-F]+:[0-9a-fA-F]+', fields['RDEV']), 'invalid block rdev')
    require(re.fullmatch(r'[0-9]+:[0-9]+', fields['SYSDEV']), 'invalid sysfs dev')
    rdev = tuple(int(v, 16) for v in fields['RDEV'].split(':'))
    sysdev = tuple(int(v) for v in fields['SYSDEV'].split(':'))
    require(rdev == sysdev == (int(uevent['MAJOR']), int(uevent['MINOR'])), 'block device number mismatch')
    for key in ['SECTORS_512', 'START_512', 'NUMBER', 'LOGICAL_BLOCK_SIZE']:
        require(re.fullmatch('[0-9]+', fields[key]) and int(fields[key]) > 0, 'invalid block geometry')
        fields[key] = int(fields[key])
    require(str(fields['NUMBER']) == uevent.get('PARTN'), 'partition number mismatch')
    checksum = re.fullmatch(r'([0-9a-f]{64})  /dev/block/by-name/' + name, fields['SHA256'])
    require(checksum is not None, 'full partition hash output mismatch')
    fields['SHA256'] = checksum[1]
    fields['device_number'] = sysdev
    return fields


def validate_partition(observation, name, contract):
    expected = contract['partitions'][name]
    require(observation['SECTORS_512'] * 512 == PARTITION_BYTES, 'partition is not the complete 64MiB extent')
    require(observation['START_512'] == expected['start_512'] and observation['SECTORS_512'] == expected['sectors_512'] and observation['NUMBER'] == expected['number'], 'partition GPT geometry mismatch')
    ancestry = observation['ANCESTRY']
    require(ancestry.startswith('/sys/devices/') and UFS_COMPONENT in ancestry.split('/'), 'partition is not under the expected UFS controller')
    require(ancestry.endswith('/' + observation['NODE'].rsplit('/', 1)[1]), 'partition ancestry leaf mismatch')
    require(observation['LOGICAL_BLOCK_SIZE'] == 4096 and observation['START_512'] % 8 == 0, 'UFS logical block geometry mismatch')
    expected_hash = contract['candidate_sha256'] if name == 'boot_b' else VENDOR_SHA
    require(observation['SHA256'] == expected_hash, 'full boot/vendor partition hash mismatch')
    return dict(partition=name, sha256=observation['SHA256'], bytes=PARTITION_BYTES, node=observation['NODE'],
                device_number=observation['device_number'], start_512=observation['START_512'], number=observation['NUMBER'])


def collect(read, contract, out, nonce):
    raw = read(snapshot_command(nonce))
    (out / 'ram-identity-snapshot.bin').write_bytes(raw)
    result = validate_snapshot(raw, contract, nonce)
    partitions = {}
    for name in PARTITIONS:
        raw = read(partition_command(name))
        (out / ('ram-partition-' + name + '.txt')).write_bytes(raw)
        partitions[name] = validate_partition(parse_partition(raw, name), name, contract)
    require(partitions['boot_b']['device_number'] != partitions['vendor_boot_b']['device_number'], 'boot/vendor alias the same block device')
    result.update(readout_profile=READY, partitions=partitions, boot_and_vendor_readback_verified=True,
                  aee_archive=dict(available=False, reason='RAM diagnostic profile has no Android userdata/AEE service'), ios_usable=False)
    return result
