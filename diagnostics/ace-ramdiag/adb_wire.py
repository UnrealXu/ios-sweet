"""Bounded ADB wire client for a loopback QEMU port; never uses an ADB server.

Protocol reference: AOSP packages/modules/adb/docs/dev/protocol.md.
Public-key format: AOSP system/core/libcrypto_utils/android_pubkey.cpp.
This client sends signatures only, never offers a new key for authorization.
"""
import base64
import hashlib
import os
import socket
import struct
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils


def require(ok,message):
    if not ok:raise ValueError(message)

def adb_public_key(key):
    numbers=key.public_key().public_numbers();n=numbers.n
    require(key.key_size==2048 and numbers.e==65537,'RSA2048/F4 required')
    n0inv=(-pow(n,-1,2**32))%(2**32)
    raw=struct.pack('<II',64,n0inv)+n.to_bytes(256,'little')+pow(2,4096,n).to_bytes(256,'little')+struct.pack('<I',numbers.e)
    return base64.b64encode(raw)+b' ace-qemu-ephemeral\n'

def validate_public_key(data,pin):
    require(isinstance(pin,str) and len(pin)==64 and all(c in '0123456789abcdef' for c in pin),'invalid public key hash pin')
    require(hashlib.sha256(data).hexdigest()==pin,'public key hash mismatch')
    require(b'\0' not in data and data.count(b'\n')==1 and data.endswith(b'\n'),'one newline-terminated key required')
    raw=base64.b64decode(data.split(b' ',1)[0],validate=True)
    require(len(raw)==524,'invalid Android RSA public key length')
    words,n0inv=struct.unpack_from('<II',raw);n=int.from_bytes(raw[8:264],'little')
    rr=int.from_bytes(raw[264:520],'little');exponent=struct.unpack_from('<I',raw,520)[0]
    require(words==64 and n.bit_length()==2048 and n%2 and exponent==65537,'invalid Android RSA public key parameters')
    require(n0inv==(-pow(n,-1,2**32))%(2**32) and rr==pow(2,4096,n),'invalid Montgomery parameters')
    return raw

def generate_key(path):
    key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    # Exclusively create private files. No key contents enter stdout/reports.
    raw=key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption())
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as file:file.write(raw)
    public=adb_public_key(key)
    with path.with_suffix('.pub').open('xb') as file:file.write(public)
    return key,public

class QemuADB:
    def __init__(self,port,*,timeout=25,idle_timeout=5):
        require(isinstance(port,int) and 1024<=port<=65535,'invalid QEMU loopback port')
        require(0<idle_timeout<=timeout<=120,'bounded QEMU wire deadline required')
        self.idle_timeout=idle_timeout
        self.socket=socket.create_connection(('127.0.0.1',port),timeout=5)
        self.socket.settimeout(5);self.deadline=time.monotonic()+timeout
        self.events=[];self.authenticated=False;self.next_local_id=1;self.closed_streams=set()

    def close(self):self.socket.close()

    def send(self,command,arg0=0,arg1=0,data=b''):
        require(len(command)==4 and len(data)<=4096,'bounded packet required')
        number=struct.unpack('<I',command)[0]
        self.socket.sendall(struct.pack('<6I',number,arg0,arg1,len(data),sum(data)&0xffffffff,number^0xffffffff)+data)
        self.events.append({'direction':'send','command':command.decode(),'arg0':arg0,'arg1':arg1,'bytes':len(data)})

    def read_exact(self,size):
        result=bytearray()
        while len(result)<size:
            remaining=self.deadline-time.monotonic()
            require(remaining>0,'QEMU ADB operation deadline exceeded')
            self.socket.settimeout(min(self.idle_timeout,remaining))
            part=self.socket.recv(size-len(result))
            if not part:raise EOFError('QEMU ADB disconnected')
            result.extend(part)
        return bytes(result)

    def receive(self):
        command,a,b,size,checksum,magic=struct.unpack('<6I',self.read_exact(24))
        require(magic==command^0xffffffff and size<=4096,'invalid/big ADB packet')
        data=self.read_exact(size)
        require(checksum==(sum(data)&0xffffffff),'ADB checksum mismatch')
        name=struct.pack('<I',command)
        self.events.append({'direction':'receive','command':name.decode(),'arg0':a,'arg1':b,'bytes':size,'sha256':hashlib.sha256(data).hexdigest()})
        return name,a,b,data

    def authenticate(self,key):
        self.send(b'CNXN',0x01000000,4096,b'host::\0')
        name,a,b,token=self.receive()
        require((name,a,b)==(b'AUTH',1,0) and len(token)==20,'expected authentication challenge; unauthenticated access refused')
        signature=key.sign(token,padding.PKCS1v15(),utils.Prehashed(hashes.SHA1()))
        self.send(b'AUTH',2,0,signature)
        name,a,b,data=self.receive()
        if name==b'AUTH':
            require(a==1 and b==0 and len(data)==20 and data!=token,'invalid rejection challenge')
            return False
        # This exact stock adbd advertises 0x01000001 even to our legacy
        # 0x01000000 client. The transport still uses our negotiated checksum
        # mode; receive() continues checking every packet checksum.
        require(name==b'CNXN' and a in (0x01000000,0x01000001) and b>=4096,'expected authenticated CNXN')
        self.banner=data.decode(errors='replace')
        require(self.banner.startswith('recovery::'),'unexpected QEMU adbd role')
        self.authenticated=True
        return True

    def open_shell(self,command):
        require(self.authenticated,'authenticate before shell')
        local=self.next_local_id;self.next_local_id+=1
        self.send(b'OPEN',local,0,b'shell:'+command.encode()+b'\0')
        return local

    def stream_packet(self):
        # Exact stock adbd can send a late close for an already closed stream.
        # Ignore only that known pair; never accept another stream's data.
        for _ in range(4):
            packet=self.receive()
            name,remote,local,_=packet
            if name==b'CLSE' and (remote,local) in self.closed_streams:
                self.events[-1]['ignored_known_closed_stream']=True
                continue
            return packet
        raise ValueError('too many duplicate closed-stream packets')

    def shell(self,command):
        local_id=self.open_shell(command)
        name,remote,local,data=self.stream_packet()
        require(name==b'OKAY' and remote>0 and local==local_id and not data,'shell OPEN refused')
        output=bytearray()
        for _ in range(512):
            name,a,b,data=self.stream_packet()
            require(a==remote and b==local_id,'wrong shell stream identity')
            if name==b'CLSE':
                self.closed_streams.add((remote,local_id))
                self.send(b'CLSE',local_id,remote)
                return bytes(output)
            require(name==b'WRTE','unexpected shell packet')
            output.extend(data);require(len(output)<=1024*1024,'shell output exceeded bound')
            self.send(b'OKAY',local_id,remote)
        raise ValueError('shell packet count exceeded bound')
