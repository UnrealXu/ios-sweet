"""Fail closed on stale identities, persistent mounts and wrong block evidence."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ram_readout_test',ROOT/'tools/ace_ram_readout.py')
m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class ContractTests(unittest.TestCase):
    def contract(self):
        profile = json.dumps(dict(format='ACE_RAMDIAG_GUEST_V1',serial='SYNTHETIC',run_token='0123456789abcdef',bundle_id='a'*64,kernel_sha256=m.KERNEL_SHA)).encode()
        contract = json.loads(profile)
        contract.update(format='ACE_RAMDIAG_HOST_V1',candidate_sha256='b'*64,vendor_sha256=m.VENDOR_SHA,guest_profile_sha256=m.sha(profile),
                        controller_sha256='c'*64,validator_sha256=m.sha((ROOT/'tools/ace_ram_readout.py').read_bytes()),
                        partitions={name:dict(start_512=2048+i*131072,sectors_512=131072,number=i+1) for i,name in enumerate(m.PARTITIONS)})
        return contract,profile

    def test_default_android_and_unknown_profile(self):
        self.assertIsNone(m.load_contract({},Path('.'),'s','c'*64))
        with self.assertRaisesRegex(ValueError,'unknown'):m.load_contract(dict(readout_profile='typo'),Path('.'),'s','c'*64)

    def test_pinned_contract_context_sources_and_safe_path(self):
        contract,_=self.contract()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);path=out/'host.json';raw=json.dumps(contract).encode();path.write_bytes(raw)
            state=dict(readout_profile=m.READY,ramdiag_contract_file='host.json',ramdiag_contract_sha256=m.sha(raw),run_token=contract['run_token'],candidate_sha256=contract['candidate_sha256'])
            self.assertEqual(m.load_contract(state,out,'SYNTHETIC','c'*64),contract)
            for changes in [dict(run_token='f'*16),dict(candidate_sha256='e'*64),dict(ramdiag_contract_sha256='d'*64),dict(ramdiag_contract_file='../host.json')]:
                with self.assertRaises(ValueError):m.load_contract(state|changes,out,'SYNTHETIC','c'*64)
            with self.assertRaises(ValueError):m.load_contract(state,out,'OTHER','c'*64)
            with self.assertRaises(ValueError):m.load_contract(state,out,'SYNTHETIC','d'*64)

    def snapshot(self):
        contract,profile=self.contract();nonce='d'*32
        raw=('ACE_RAM_STATE_V1:'+nonce+'\nSERIAL=SYNTHETIC\nSLOT=_b\nROOT_UID=0\nSECURE=1\nREADY=ramdiag-v1\nHAS_DATA=0\nPROFILE_BEGIN\n').encode()+profile+b'\nPROFILE_END\n'
        for name in ['COMPLETE','RETURN']:raw+=name.encode()+b'_BEGIN\n'+('a'*64+'\n').encode()+b'\n'+name.encode()+b'_END\n'
        mounts=''.join(f'{i+1} 0 0:{i} / {point} rw - {kind} {kind} rw\n' for i,(point,kind) in enumerate([('/','rootfs'),('/tmp','tmpfs'),('/dev','tmpfs'),('/proc','proc'),('/sys','sysfs')]))
        raw+=b'MOUNTS_BEGIN\n'+mounts.encode()+b'\nMOUNTS_END\n'
        return raw,contract,nonce

    def test_snapshot_exact_identity_and_virtual_mounts(self):
        raw,contract,nonce=self.snapshot()
        self.assertTrue(m.validate_snapshot(raw,contract,nonce)['no_data_verified'])
        mutations=[raw.replace(b'SLOT=_b',b'SLOT=_a'),raw.replace(b'ROOT_UID=0',b'ROOT_UID=2000'),raw.replace(b'SECURE=1',b'SECURE=0'),raw.replace(b'HAS_DATA=0',b'HAS_DATA=1'),raw.replace(b'/tmp rw - tmpfs',b'/data rw - ext4'),raw.replace(b'/tmp rw',b'/tmp\\040bad rw'),raw.replace(b'RETURN_BEGIN\n'+b'a'*64,b'RETURN_BEGIN\n'+b'b'*64),raw.replace(b'PROFILE_BEGIN\n',b'PROFILE_BEGIN\n '),raw.replace(b'\n',b'\r\n')]
        for bad in mutations:
            with self.subTest(bad=bad[:50]):
                with self.assertRaises(ValueError):m.validate_snapshot(bad,contract,nonce)
        with self.assertRaises(ValueError):m.validate_snapshot(raw,contract,'e'*32)

    def observation(self,name='boot_b'):
        contract,_=self.contract();part=contract['partitions'][name];index=part['number']
        checksum=contract['candidate_sha256'] if name=='boot_b' else m.VENDOR_SHA
        raw=f'''ACE_RAM_PARTITION_V1
NODE=/dev/block/sdc{index}
RDEV=103:{index:x}
SYSDEV=259:{index}
SECTORS_512=131072
START_512={part['start_512']}
NUMBER={index}
ANCESTRY=/sys/devices/platform/112b0000.ufshci/host0/target0/block/sdc/sdc{index}
LOGICAL_BLOCK_SIZE=4096
UEVENT_BEGIN
MAJOR=259
MINOR={index}
DEVNAME=sdc{index}
DEVTYPE=partition
PARTN={index}
PARTNAME={name}

UEVENT_END
SHA256={checksum}  /dev/block/by-name/{name}
'''.encode()
        return raw,contract

    def test_full_extent_identity_geometry_and_digest(self):
        for name in m.PARTITIONS:
            raw,contract=self.observation(name)
            self.assertEqual(m.validate_partition(m.parse_partition(raw,name),name,contract)['bytes'],64*1024*1024)
        raw,contract=self.observation()
        mutations=[(b'SYSDEV=259:1',b'SYSDEV=259:2'),(b'PARTNAME=boot_b',b'PARTNAME=boot_a'),(b'PARTN=1',b'PARTN=2'),(b'SECTORS_512=131072',b'SECTORS_512=16'),(b'START_512=2048',b'START_512=4096'),(b'112b0000.ufshci',b'USB_FIXTURE'),(b'LOGICAL_BLOCK_SIZE=4096',b'LOGICAL_BLOCK_SIZE=512'),(b'SHA256='+b'b'*64,b'SHA256='+b'e'*64),(b'NODE=/dev/block/sdc1',b'NODE=/dev/block/sdc2'),(b'NUMBER=1',b'NUMBER=1\nNUMBER=1')]
        for before,after in mutations:
            with self.subTest(mutation=after):
                with self.assertRaises(ValueError):m.validate_partition(m.parse_partition(raw.replace(before,after),'boot_b'),'boot_b',contract)

    def test_failed_single_read_retains_output_and_never_retries(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls=[];identities=[]
            def find():identities.append(1);return 'verified'
            def run(args,timeout):calls.append(args);return subprocess.CompletedProcess(args,1,b'partial',b'failed')
            reader=m.EvidenceReader(Path(tmp),find,run)
            with self.assertRaises(RuntimeError):reader.read('cat fixed')
            self.assertEqual(len(calls),1);self.assertEqual(len(identities),1)
            self.assertEqual(Path(tmp,'ram-command-000.stdout').read_bytes(),b'partial')
            self.assertEqual(Path(tmp,'ram-command-000.stderr').read_bytes(),b'failed')
            self.assertEqual(reader.read(m.RECORD_COMMAND,allow_failure=True),b'partial')
            self.assertEqual(len(calls),2)
            self.assertNotIn('su -c',str(calls))

    def test_timeout_partial_record_can_only_be_reobserved_by_caller(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls=[]
            def run(args,timeout):
                calls.append(args)
                raise subprocess.TimeoutExpired(args,timeout,output=b'partial-record',stderr=b'late')
            reader=m.EvidenceReader(Path(tmp),lambda:'verified',run)
            self.assertEqual(reader.read(m.RECORD_COMMAND,allow_failure=True),b'partial-record')
            self.assertEqual(len(calls),1)
            self.assertEqual(Path(tmp,'ram-command-000.stderr').read_bytes(),b'late')
            with self.assertRaises(subprocess.TimeoutExpired):reader.read('cat fixed')
            self.assertEqual(len(calls),2)

    def test_absent_identity_or_timeout_is_retained_without_command_retry(self):
        for missing in (True,False):
            with tempfile.TemporaryDirectory() as tmp:
                calls=[]
                def run(args,timeout):calls.append(args);raise RuntimeError('timed out')
                reader=m.EvidenceReader(Path(tmp),lambda:None if missing else 'verified',run)
                with self.assertRaises(RuntimeError):reader.read('cat fixed')
                self.assertEqual(len(calls),0 if missing else 1)
                self.assertIn('exception',json.loads(Path(tmp,'ram-command-observations.json').read_text())[0])


class ControllerRAMTests(unittest.TestCase):
    contract=ContractTests.contract
    snapshot=ContractTests.snapshot
    observation=ContractTests.observation
    def test_main_ram_loop_and_preboot_contract_refusal(self):
        from unittest.mock import patch
        import shlex
        import struct
        auto_spec=importlib.util.spec_from_file_location('ace_controller_ram_integration',ROOT/'tools/ace-auto-trial.py')
        auto=importlib.util.module_from_spec(auto_spec);auto_spec.loader.exec_module(auto)
        for malformed in (False,True):
            with self.subTest(malformed=malformed),tempfile.TemporaryDirectory() as tmp:
                base=Path(tmp);out=base/'research'/'trial';out.mkdir(parents=True)
                contract,_=self.contract();contract['controller_sha256']=m.sha((ROOT/'tools/ace-auto-trial.py').read_bytes())
                raw=json.dumps(contract).encode();(out/'host.json').write_bytes(raw)
                state=dict(phase='candidate-flashed-awaiting-reboot',candidate_flash_succeeded=True,auto_readout_after_reset=True,
                           run_token=contract['run_token'],candidate_sha256=contract['candidate_sha256'],readout_profile=m.READY,
                           ramdiag_contract_file='host.json',ramdiag_contract_sha256='0'*64 if malformed else m.sha(raw))
                (out/'state.json').write_text(json.dumps(state));transport=base/'transport.json';transport.write_text(json.dumps(dict(usb_adb='SYNTHETIC')))
                calls=[];fastboot=True
                words=[0]*32;words[:4]=[0x313054414e454341,1,5,(-67)%(1<<64)]
                record=b'ACEFALL1'+contract['run_token'].encode()+bytes(8)+struct.pack('<32Q',*words)
                def run(args,**kwargs):
                    nonlocal fastboot
                    calls.append(args);rc=0;stdout=b''
                    if args==['fastboot','devices']:stdout=b'SYNTHETIC fastboot\n' if fastboot else b''
                    elif args==['fastboot','-s','SYNTHETIC','reboot']:fastboot=False
                    elif args==['adb','devices']:stdout=b'List of devices attached\nSYNTHETIC device\n'
                    elif args[-2:]==['shell','getprop ro.serialno']:stdout=b'SYNTHETIC\n'
                    elif args[-2:]==['screencap','-p']:rc=1
                    elif args[-2:]==['reboot','bootloader']:fastboot=True
                    elif len(args)>=5 and args[-2]=='getvar':
                        stdout=(args[-1]+': '+dict(product='k6895v1_64',**{'current-slot':'b','unlocked':'yes','is-userspace':'no'})[args[-1]]).encode()
                    elif 'exec-out' in args:
                        command=shlex.split(args[-1])[2]
                        if command==m.RECORD_COMMAND:stdout=record
                        elif command.startswith('set -e\necho ACE_RAM_STATE_V1:'):
                            nonce=command.split('ACE_RAM_STATE_V1:',1)[1].splitlines()[0]
                            snapshot,_,old=self.snapshot();stdout=snapshot.replace(old.encode(),nonce.encode())
                        elif 'dev=/dev/block/by-name/' in command:
                            name=command.split('dev=/dev/block/by-name/',1)[1].splitlines()[0];stdout=self.observation(name)[0]
                        elif command=='dmesg' or command.startswith('tar -cf - /sys/fs/pstore'):stdout=b'fixture evidence'
                        else:raise AssertionError(command)
                    else:raise AssertionError(args)
                    return subprocess.CompletedProcess(args,rc,stdout,b'')
                with patch.object(auto,'ROOT',base),patch.object(auto.sys,'argv',['ace-auto-trial',str(transport),str(out)]),patch.object(auto.subprocess,'run',side_effect=run):
                    if malformed:
                        with self.assertRaises(ValueError):auto.main()
                        self.assertEqual(calls,[])
                    else:
                        auto.main()
                        saved=json.loads((out/'state.json').read_text());self.assertEqual(saved['phase'],'diagnostics-collected-fastboot-ready')
                        self.assertTrue(saved['automatic_loop_verified']);self.assertFalse(saved['ios_usable'])
                        result=json.loads((out/'readout-result.json').read_text());self.assertTrue(result['boot_and_vendor_readback_verified']);self.assertFalse(result['aee_archive']['available'])
                        self.assertEqual(sum(c[-2:]==['reboot','bootloader'] for c in calls),1)
                        self.assertNotIn('su -c',str(calls));self.assertNotIn('sys.boot_completed',str(calls));self.assertNotIn('/data/vendor',str(calls))
                        self.assertTrue((out/'ram-command-observations.json').exists())
                        for name,digest in result['artifacts'].items():self.assertEqual(m.sha((out/name).read_bytes()),digest)


if __name__=="__main__":unittest.main()
