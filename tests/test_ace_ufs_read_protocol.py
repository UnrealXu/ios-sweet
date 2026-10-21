"""Exact read-only command frames used by the actual kernel patch."""
import ctypes as c
from pathlib import Path
import struct,subprocess,tempfile,unittest,zlib
ROOT=Path(__file__).resolve().parents[1]
class UfsReadProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();p=Path(cls.temp.name)
        (p/'wrap.c').write_text('#include "ufs_read_protocol.h"\nint build(unsigned char *a,size_t n,uint64_t pa,unsigned op,unsigned lun,unsigned lba,unsigned block) {return ace_ufs_read_request(a,n,pa,op,lun,lba,block);}\nuint32_t crc(const uint8_t *p,size_t n) {return ace_ufs_crc32(p,n);}\n')
        subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror','-I',str(ROOT/'ace'),str(p/'wrap.c'),'-o',str(p/'wrap.so')],check=True)
        cls.lib=c.CDLL(str(p/'wrap.so'));cls.lib.build.argtypes=[c.c_void_p,c.c_size_t,c.c_uint64,*[c.c_uint]*4];cls.lib.crc.argtypes=[c.c_void_p,c.c_size_t];cls.lib.crc.restype=c.c_uint32
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def make(self,op,lun=0,lba=0,block=0):
        a=c.create_string_buffer(b'\xa5'*0x4000,0x4000);rc=self.lib.build(a,0x4000,0x1fed00000,op,lun,lba,block);return rc,a.raw
    def test_nop_exact_high_address_utrd_and_zero_data(self):
        rc,a=self.make(0);self.assertEqual(rc,0)
        self.assertEqual(struct.unpack_from('<8I',a),(0x11000000,0,15,0,0xfed01000,1,0x00800080,0))
        self.assertEqual(a[0x1000:0x1020],bytes(32));self.assertEqual(a[0x1200:0x1400],b'\xa5'*512)
        self.assertEqual(a[0x3c00:],b'\x5a'*1024)
    def test_only_read_cap_tur_and_single_block_cdb_exist(self):
        for op,lun,lba,block,length,opcode in [(1,0,0,0,0,0),(2,0,0,0,32,0x9e),(3,0,0,4096,4096,0x28),(3,7,1,512,512,0x28)]:
            with self.subTest(op=op,lun=lun,lba=lba,block=block):
                rc,a=self.make(op,lun,lba,block);self.assertEqual(rc,length)
                self.assertEqual(a[0x1000],1);self.assertEqual(a[0x1001],0x40 if length else 0);self.assertEqual(a[0x1002],lun)
                self.assertEqual(a[0x1003],0);self.assertEqual(a[0x1010],opcode)
                self.assertEqual(struct.unpack_from('>I',a,0x100c)[0],length)
                if length:self.assertEqual(struct.unpack_from('<4I',a,0x1400),(0xfed02000,1,0,length-1))
                if op==2:self.assertEqual(a[0x1011],0x10);self.assertEqual(struct.unpack_from('>I',a,0x101a)[0],32)
                if op==3:self.assertEqual(struct.unpack_from('>I',a,0x1012)[0],lba);self.assertEqual(a[0x1017:0x1019],b'\0\1')
    def test_bad_frames_refuse_without_destination_store(self):
        for n,pa,op,lun,lba,block in [(0x3fff,0x140000000,0,0,0,0),(0x4000,0,0,0,0,0),(0x4000,0x140000001,0,0,0,0),(0x4000,1<<40,0,0,0,0),(0x4000,0x140000000,4,0,0,0),(0x4000,0x140000000,0,1,0,0),(0x4000,0x140000000,3,8,0,4096),(0x4000,0x140000000,3,0,2,4096),(0x4000,0x140000000,3,0,0,8192),(0x4000,0x140000000,2,0,0,32)]:
            a=c.create_string_buffer(b'\xa5'*0x4000,0x4000)
            with self.subTest(n=n,pa=pa,op=op,lun=lun,lba=lba,block=block):
                self.assertEqual(self.lib.build(a,n,pa,op,lun,lba,block),-1);self.assertEqual(a.raw,b'\xa5'*0x4000)
        self.assertEqual(self.lib.build(None,0x4000,0x140000000,0,0,0,0),-1)
    def test_crc_matches_independent_implementation(self):
        for data in [b'',b'123456789',bytes(range(256))*16]:
            a=c.create_string_buffer(data);self.assertEqual(self.lib.crc(a,len(data)),zlib.crc32(data))
    def test_kernel_patch_embeds_exact_host_tested_protocol(self):
        patch=(ROOT/'xnu/patches/0091-ace-bounded-ufs-read-command-probe.patch').read_text()
        header=patch.split('+++ b/iokit/Kernel/arm/AceUFSReadProtocol.h\n',1)[1].split('--- a/iokit/KernelConfigTables.cpp',1)[0]
        content=''.join(line[1:]+'\n' for line in header.splitlines() if line.startswith('+'))
        self.assertEqual(content,(ROOT/'ace/ufs_read_protocol.h').read_text())
