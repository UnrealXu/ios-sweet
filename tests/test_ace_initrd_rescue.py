"""Execute the freestanding RAM rewrite codec; no phone or firmware writes."""
import ctypes as c
import hashlib,random,struct,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Policy(c.Structure):
    _fields_=[('vendor_bytes',c.c_size_t),('generic_offset',c.c_size_t),('generic_bytes',c.c_size_t),('vendor_sha256',c.c_ubyte*32),('generic_sha256',c.c_ubyte*32),('rescue_sha256',c.c_ubyte*32),('require_bootconfig',c.c_uint)]
class Result(c.Structure):
    _fields_=[(n,c.c_size_t) for n in ['old_bytes','new_bytes','generic_offset','old_config_offset','new_config_offset','config_extent']]
def pin(data):return (c.c_ubyte*32).from_buffer_copy(hashlib.sha256(data).digest())
def bootconfig(prefix,data=b'androidboot.slot_suffix="_b"\n\0',trail=0):
    data+=bytes(-(len(prefix)+len(data)+20)%4)
    return prefix+data+struct.pack('<II',len(data),sum(data)&0xffffffff)+b'#BOOTCONFIG\n'+bytes(trail)
class InitrdRescueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();p=Path(cls.tmp.name)
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-shared','-fPIC',str(ROOT/'ace/initrd_rescue.c'),'-o',str(p/'test.so')],check=True,capture_output=True)
        cls.lib=c.CDLL(str(p/'test.so'));cls.run_codec=cls.lib.ace_initrd_rescue
        cls.run_codec.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.c_void_p,c.c_size_t,c.c_void_p,c.c_uint]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def fixture(self,vendor=b'VENDOR',generic=b'RAM-GENERIC'*8,rescue=b'STOCK',gap=0,config=True,trail=0):
        prefix=vendor+bytes(gap)+generic
        data=bootconfig(prefix,trail=trail) if config else prefix
        return data,Policy(len(vendor),len(vendor)+gap,len(generic),pin(vendor),pin(generic),pin(rescue),int(config)),rescue
    def invoke(self,data,p,rescue,apply=1,expected=0):
        b=c.create_string_buffer(data+b'GUARD');r=c.create_string_buffer(rescue);out=Result(*([0x55]*6));before=b.raw
        rc=self.run_codec(b,len(data),c.byref(p),r,len(rescue),c.byref(out),apply)
        if expected==0:self.assertEqual(rc,0)
        else:
            self.assertLess(rc,0);self.assertEqual(b.raw,before);self.assertEqual(bytes(out),bytes(Result(*([0x55]*6))))
        self.assertEqual(b.raw[len(data):len(data)+5],b'GUARD')
        return b,out
    def test_plan_is_readonly_and_apply_preserves_vendor_and_config_exactly(self):
        data,p,rescue=self.fixture(gap=2,trail=3)
        before,out=self.invoke(data,p,rescue,apply=0);self.assertEqual(before.raw[:len(data)],data)
        after,result=self.invoke(data,p,rescue)
        self.assertEqual(bytes(out),bytes(result));self.assertLess(result.new_bytes,len(data))
        self.assertEqual(after.raw[:p.generic_offset],data[:p.generic_offset])
        self.assertEqual(after.raw[p.generic_offset:p.generic_offset+len(rescue)],rescue)
        self.assertEqual(after.raw[result.new_config_offset:result.new_bytes],data[result.old_config_offset:])
        self.assertEqual((result.new_config_offset+result.config_extent-3-20)%4,0)
    def test_all_padding_and_size_combinations(self):
        randomizer=random.Random(8610)
        for i in range(96):
            vendor=randomizer.randbytes(randomizer.randrange(1,65));generic=randomizer.randbytes(randomizer.randrange(16,180));rescue=randomizer.randbytes(randomizer.randrange(1,len(generic)+1))
            data,p,rescue=self.fixture(vendor,generic,rescue,gap=i%4,trail=i%4)
            after,result=self.invoke(data,p,rescue)
            self.assertEqual(after.raw[:p.generic_offset],data[:p.generic_offset])
            self.assertEqual(after.raw[result.new_config_offset:result.new_bytes],data[result.old_config_offset:])
            self.assertLessEqual(result.new_bytes,len(data))
            self.assertEqual((result.new_config_offset-result.old_config_offset)%4,0)
    def test_no_bootconfig_only_when_explicitly_optional_and_zero_tail(self):
        for pad in [0,1,3,4095]:
            data,p,rescue=self.fixture(config=False);data+=bytes(pad);after,result=self.invoke(data,p,rescue)
            self.assertEqual(result.config_extent,0);self.assertEqual(after.raw[:result.new_bytes],data[:p.generic_offset]+rescue+bytes(pad))
        data,p,rescue=self.fixture(config=False);p.require_bootconfig=1;self.invoke(data,p,rescue,expected=-1)
        p.require_bootconfig=0
        for suffix in [b'x',bytes(4096),b'#BOOTCONFIG\n']:
            self.invoke(data+suffix,p,rescue,expected=-1)
    def test_every_input_pin_and_footer_error_refuses_without_writes(self):
        data,p,rescue=self.fixture()
        for offset in [0,p.generic_offset,len(data)-1,len(data)-13,len(data)-20]:
            changed=bytearray(data);changed[offset]^=1;self.invoke(bytes(changed),p,rescue,expected=-1)
        self.invoke(data,p,rescue+b'!',expected=-1)
        for field,value in [('vendor_bytes',0),('vendor_bytes',len(data)+1),('generic_offset',0),('generic_offset',len(data)),('generic_bytes',len(data)),('require_bootconfig',2)]:
            changed=Policy.from_buffer_copy(p);setattr(changed,field,value);self.invoke(data,changed,rescue,expected=-1)
        self.invoke(data,p,rescue,apply=2,expected=-1)
        # A broken config checksum with its framing intact cannot pass.
        changed=bytearray(data);changed[p.generic_offset+p.generic_bytes]^=1;self.invoke(bytes(changed),p,rescue,expected=-1)
    def test_budget_cancellation_preserves_all_inputs_and_result(self):
        data,p,rescue=self.fixture(vendor=b'v'*150000,generic=b'g'*150000,rescue=b'r'*100000)
        callback=c.CFUNCTYPE(c.c_int,c.c_void_p)
        method=self.lib.ace_initrd_rescue_with_budget
        method.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Policy),c.c_void_p,c.c_size_t,c.c_void_p,c.c_uint,callback,c.c_void_p]
        # Eight chunks plus a final pre-store check; refuse at every point.
        for stop in range(9):
            calls=[]
            def allowed(context):
                calls.append(context);return int(len(calls)<=stop)
            hook=callback(allowed);target=c.create_string_buffer(data);source=c.create_string_buffer(rescue);result=Result(*([0x55]*6));before=target.raw
            self.assertEqual(method(target,len(data),c.byref(p),source,len(rescue),c.byref(result),1,hook,None),-8)
            self.assertEqual(target.raw,before);self.assertEqual(bytes(result),bytes(Result(*([0x55]*6))))
        hook=callback(lambda context:1);target=c.create_string_buffer(data);source=c.create_string_buffer(rescue);result=Result()
        self.assertEqual(method(target,len(data),c.byref(p),source,len(rescue),c.byref(result),1,hook,None),0)
    def test_overlap_null_truncation_and_integer_ranges(self):
        data,p,rescue=self.fixture();b=c.create_string_buffer(data);r=c.create_string_buffer(rescue);out=Result(*([0x55]*6));before=b.raw;original=bytes(out)
        variants=[(None,len(data),c.byref(p),r,len(rescue),c.byref(out),1),
                  (b,0,c.byref(p),r,len(rescue),c.byref(out),1),
                  (b,64*1024*1024+1,c.byref(p),r,len(rescue),c.byref(out),1),
                  (b,len(data),None,r,len(rescue),c.byref(out),1),
                  (b,len(data),c.byref(p),b,len(rescue),c.byref(out),1),
                  (b,len(data),c.byref(p),r,len(rescue),b,1),
                  (b,len(data),c.byref(p),r,len(rescue),c.byref(p),1),
                  (b,len(data),c.byref(p),None,len(rescue),c.byref(out),1),
                  (c.c_void_p((1<<64)-10),len(data),c.byref(p),r,len(rescue),c.byref(out),1)]
        for args in variants:
            self.assertLess(self.run_codec(*args),0);self.assertEqual(b.raw,before);self.assertEqual(bytes(out),original)
        for length in range(1,len(data)):
            self.assertLess(self.run_codec(b,length,c.byref(p),r,len(rescue),c.byref(out),1),0);self.assertEqual(b.raw,before)
    def test_lk_config_length_alignment_allows_unaligned_footer(self):
        # Actual LK aligns only strlen(config)+1, then appends it directly
        # after vendor+generic. The footer can lie at any physical residue.
        for residue in range(4):
            vendor=b'VENDOR';generic=b'G'*(81+residue);rescue=b'STOCK'
            config=b'androidboot.slot_suffix="_b"\n\0';config+=bytes(-len(config)%4)
            raw=vendor+generic+config+struct.pack('<II',len(config),sum(config))+b'#BOOTCONFIG\n'
            p=Policy(len(vendor),len(vendor),len(generic),pin(vendor),pin(generic),pin(rescue),1)
            after,result=self.invoke(raw,p,rescue)
            self.assertEqual(after.raw[result.new_config_offset:result.new_bytes],raw[result.old_config_offset:])
            self.assertEqual(after.raw[:len(vendor)+len(rescue)],vendor+rescue)
    def test_unaligned_footer_bad_checksum_still_refuses_without_store(self):
        vendor=b'VENDOR';generic=b'G'*81;rescue=b'STOCK';config=b'k="v"\n\0\0'
        raw=vendor+generic+config+struct.pack('<II',len(config),sum(config)^1)+b'#BOOTCONFIG\n'
        p=Policy(len(vendor),len(vendor),len(generic),pin(vendor),pin(generic),pin(rescue),1)
        self.invoke(raw,p,rescue,expected=-1)
if __name__=='__main__':unittest.main()
