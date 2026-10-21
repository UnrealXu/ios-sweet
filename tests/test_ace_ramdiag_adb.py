"""Offline authentication/input guards. No ADB server, QEMU or phone I/O."""
import base64
import hashlib
import importlib.util
from pathlib import Path
import struct
import time
import unittest

from cryptography.hazmat.primitives.asymmetric import rsa

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ramdiag_wire',ROOT/'diagnostics/ace-ramdiag/adb_wire.py')
wire=importlib.util.module_from_spec(spec);spec.loader.exec_module(wire)

class BufferSocket:
    def __init__(self,data):self.data=data;self.sent=[]
    def settimeout(self,value):pass
    def recv(self,size):
        part=self.data[:size];self.data=self.data[size:];return part
    def sendall(self,data):self.sent.append(data)

def packet(command,data=b'',a=0,b=0):
    number=int.from_bytes(command,'little')
    return struct.pack('<6I',number,a,b,len(data),sum(data),number^0xffffffff)+data

def client(data):
    result=wire.QemuADB.__new__(wire.QemuADB)
    result.socket=BufferSocket(data);result.deadline=time.monotonic()+1;result.idle_timeout=5
    result.events=[];result.authenticated=False;result.next_local_id=1;result.closed_streams=set()
    return result

class RamDiagADBGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        cls.public=wire.adb_public_key(cls.key)

    def test_invalid_waits_fail_before_any_socket_connection(self):
        from unittest.mock import patch
        with patch.object(wire.socket,'create_connection') as connect:
            for timeout,idle in [(121,5),(25,26),(0,0),(-1,1)]:
                with self.assertRaises(ValueError):wire.QemuADB(5555,timeout=timeout,idle_timeout=idle)
            connect.assert_not_called()

    def test_public_key_pin_and_montgomery_corruption_rejected(self):
        public=self.public;pin=hashlib.sha256(public).hexdigest()
        self.assertEqual(len(wire.validate_public_key(public,pin)),524)
        with self.assertRaisesRegex(ValueError,'hash mismatch'):wire.validate_public_key(public,'0'*64)
        raw=bytearray(base64.b64decode(public.split(b' ')[0]));raw[300]^=1
        changed=base64.b64encode(raw)+b' fixture\n'
        with self.assertRaisesRegex(ValueError,'Montgomery'):wire.validate_public_key(changed,hashlib.sha256(changed).hexdigest())

    def test_multiple_authorized_keys_and_nul_refused(self):
        for public in [self.public+self.public,self.public.replace(b' fixture',b' fixture\0')+b'\0']:
            with self.subTest(length=len(public)),self.assertRaises(ValueError):
                wire.validate_public_key(public,hashlib.sha256(public).hexdigest())

    def test_unauthenticated_cnxn_never_counts_as_success(self):
        connection=client(packet(b'CNXN',b'recovery::\0',0x01000001,4096))
        with self.assertRaisesRegex(ValueError,'challenge'):connection.authenticate(self.key)
        self.assertFalse(connection.authenticated)
        self.assertEqual(len(connection.socket.sent),1)

    def test_shell_cannot_open_before_authentication(self):
        connection=client(b'')
        with self.assertRaisesRegex(ValueError,'authenticate'):connection.shell('id')
        self.assertEqual(connection.socket.sent,[])

    def test_authenticated_wrong_role_does_not_unlock_shell(self):
        incoming=packet(b'AUTH',b'x'*20,1)+packet(b'CNXN',b'device::\0',0x01000001,4096)
        connection=client(incoming)
        with self.assertRaisesRegex(ValueError,'role'):connection.authenticate(self.key)
        self.assertFalse(connection.authenticated)

    def test_consecutive_shell_streams_use_fresh_ids_and_close_ack(self):
        incoming=packet(b'OKAY',a=77,b=1)+packet(b'WRTE',b'first',77,1)+packet(b'CLSE',a=77,b=1)
        incoming+=packet(b'CLSE',a=77,b=1)+packet(b'OKAY',a=88,b=2)+packet(b'WRTE',b'second',88,2)+packet(b'CLSE',a=88,b=2)
        connection=client(incoming);connection.authenticated=True
        self.assertEqual(connection.shell('first'),b'first')
        self.assertEqual(connection.shell('second'),b'second')
        self.assertTrue(any(event.get('ignored_known_closed_stream') for event in connection.events))
        sent=[struct.unpack('<6I',raw[:24])[:3] for raw in connection.socket.sent]
        self.assertEqual(sent,[(int.from_bytes(b'OPEN','little'),1,0),
                               (int.from_bytes(b'OKAY','little'),1,77),
                               (int.from_bytes(b'CLSE','little'),1,77),
                               (int.from_bytes(b'OPEN','little'),2,0),
                               (int.from_bytes(b'OKAY','little'),2,88),
                               (int.from_bytes(b'CLSE','little'),2,88)])

    def test_corrupt_oversize_and_truncated_wire_packets_refused(self):
        corrupt=bytearray(packet(b'AUTH',bytes(20),1));corrupt[-1]=1
        oversized=bytearray(packet(b'AUTH',b'',1));struct.pack_into('<I',oversized,12,4097)
        badmagic=bytearray(packet(b'AUTH',b'',1));badmagic[20]^=1
        for raw,error in [(corrupt,ValueError),(oversized,ValueError),(badmagic,ValueError),(b'x',EOFError)]:
            with self.subTest(raw=len(raw)),self.assertRaises(error):client(bytes(raw)).receive()

    def test_deadline_cannot_be_extended_by_partial_reads(self):
        connection=client(packet(b'AUTH',bytes(20),1));connection.deadline=time.monotonic()-1
        with self.assertRaisesRegex(ValueError,'deadline'):connection.receive()

if __name__=='__main__':unittest.main()
