"""Preserve the actual boot tree while adding one native-refusal record."""
import ctypes as c
from pathlib import Path
import subprocess
import tempfile
import unittest
from test_ace_mkadt import fixture,pack,node
from test_ace_xnu_fdt import Fdt

ROOT=Path(__file__).resolve().parents[1]
NAME=b'ace,native-refusal'
RECORD=b'ACEFALL1'+b'0123456789abcdef\0'+bytes(7)+bytes(range(256))

class RefusalTreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();lib=Path(cls.tmp.name)/'refusal.so'
        subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-shared','-fPIC',
            str(ROOT/'ace/fdt.c'),str(ROOT/'ace/fdt_refusal.c'),'-o',str(lib)],check=True)
        cls.lib=c.CDLL(str(lib))
        cls.lib.ace_fdt_open.argtypes=[c.c_void_p,c.c_size_t,c.POINTER(Fdt)]
        cls.lib.ace_fdt_find.argtypes=[c.POINTER(Fdt),c.c_char_p]
        cls.lib.ace_fdt_get.argtypes=[c.POINTER(Fdt),c.c_uint32,c.c_char_p,c.POINTER(c.c_uint32)]
        cls.lib.ace_fdt_get.restype=c.c_void_p
        cls.lib.ace_fdt_copy_refusal.argtypes=[c.POINTER(Fdt),c.c_void_p,c.c_size_t,c.c_void_p,c.c_size_t,c.c_void_p]
        cls.lib.ace_fdt_copy_refusal_snapshot.argtypes=[c.POINTER(Fdt),c.c_void_p,c.c_size_t,c.c_void_p,c.c_size_t,c.c_void_p,c.c_size_t,c.c_void_p]
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def opened(self,blob):
        b=c.create_string_buffer(blob);f=Fdt()
        self.assertEqual(self.lib.ace_fdt_open(b,len(blob),c.byref(f)),0)
        return b,f
    def value(self,f,idx,name):
        size=c.c_uint32();p=self.lib.ace_fdt_get(c.byref(f),idx,name,c.byref(size))
        return c.string_at(p,size.value) if p else None
    def check_copy(self,blob):
        source,f=self.opened(blob);record=c.create_string_buffer(RECORD)
        output=c.create_string_buffer(b'\xa5'*(len(blob)+1024));written=c.c_size_t(0xfeed)
        self.assertEqual(self.lib.ace_fdt_copy_refusal(c.byref(f),output,len(output),record,len(RECORD),c.byref(written)),0)
        self.assertEqual(source.raw[:-1],blob)
        self.assertEqual(output.raw[written.value:],b'\xa5'*(len(output)-1-written.value)+b'\0')
        copied,g=self.opened(output.raw[:written.value]);self.assertEqual(f.nodes,g.nodes)
        self.assertEqual(f.reserves,g.reserves)
        self.assertEqual(bytes(f.reserve)[:f.reserves*16],bytes(g.reserve)[:g.reserves*16])
        for idx in range(f.nodes):
            n=f.node[idx]
            for j in range(n.count):
                prop=f.prop[n.first+j];name=c.string_at(f.blob+prop.name)
                self.assertEqual(self.value(g,idx,name),self.value(f,idx,name),(idx,name))
        chosen=self.lib.ace_fdt_find(c.byref(g),b'/chosen')
        self.assertEqual(self.value(g,chosen,NAME),RECORD)
        self.assertEqual(g.props,f.props+1)
        return output.raw[:written.value]
    def test_reserves_children_padding_and_actual_phone_tree_preserved(self):
        root=fixture();chosen=next(n for n in root.children if n.name=='chosen')
        chosen.children.append(node('existing-child',{'opaque':b'unchanged\0'}))
        self.check_copy(pack(root,[(0x4a000000,0x1000)]))
        chosen.props.clear();self.check_copy(pack(root))
        actual=ROOT/'research/ace-xnu-entrylog-20261020/live-fdt.dtb'
        if actual.exists():self.check_copy(actual.read_bytes())
    def test_missing_chosen_duplicate_insufficient_capacity_and_alias_refuse_without_stores(self):
        root=fixture();root.children=[x for x in root.children if x.name!='chosen']
        for blob in [pack(root),self.check_copy(pack(fixture())),pack(fixture())]:
            source,f=self.opened(blob);record=c.create_string_buffer(RECORD)
            output=c.create_string_buffer(b'\xa5'*(len(blob)+1024));written=c.c_size_t(0xfeed)
            cap=len(blob) if blob==pack(fixture()) else len(output)
            before=output.raw
            self.assertNotEqual(self.lib.ace_fdt_copy_refusal(c.byref(f),output,cap,record,len(RECORD),c.byref(written)),0)
            self.assertEqual(output.raw,before);self.assertEqual(written.value,0xfeed)
        source,f=self.opened(pack(fixture()));record=c.create_string_buffer(RECORD)
        output=c.create_string_buffer(8192);written=c.c_size_t(0xfeed)
        cases=[(source,len(source),record,len(RECORD),c.byref(written)),
            (output,len(output),output,len(RECORD),c.byref(written)),
            (output,len(output),record,len(RECORD),output),
            (output,len(output),record,len(RECORD),source),
            (output,len(output),record,len(RECORD)-1,c.byref(written))]
        for dst,cap,rec,size,w in cases:
            original=source.raw;before=output.raw
            self.assertNotEqual(self.lib.ace_fdt_copy_refusal(c.byref(f),dst,cap,rec,size,w),0)
            self.assertEqual(source.raw,original);self.assertEqual(output.raw,before)
            self.assertEqual(written.value,0xfeed)

    def test_complete_snapshot_preserved_and_all_existing_phone_properties_unchanged(self):
        blobs=[pack(fixture())]
        actual=ROOT/'research/ace-xnu-entrylog-20261020/live-fdt.dtb'
        if actual.exists():blobs.append(actual.read_bytes())
        for blob in blobs:
            source,f=self.opened(blob);record=c.create_string_buffer(RECORD)
            raw=bytes((i*37+11)&255 for i in range(65536));snapshot=c.create_string_buffer(raw)
            output=c.create_string_buffer(b'\xa5'*(len(blob)+70000));written=c.c_size_t()
            self.assertEqual(self.lib.ace_fdt_copy_refusal_snapshot(c.byref(f),output,len(output),record,len(RECORD),snapshot,65536,c.byref(written)),0)
            copied,g=self.opened(output.raw[:written.value]);chosen=self.lib.ace_fdt_find(c.byref(g),b'/chosen')
            self.assertEqual(self.value(g,chosen,b'ace,pmsg-before-seed'),raw)
            self.assertEqual(self.value(g,chosen,NAME),RECORD)
            self.assertEqual(source.raw[:-1],blob);self.assertEqual(snapshot.raw[:-1],raw)
            self.assertEqual(g.nodes,f.nodes);self.assertEqual(g.props,f.props+2)
            for idx in range(f.nodes):
                n=f.node[idx]
                for j in range(n.count):
                    prop=f.prop[n.first+j];name=c.string_at(f.blob+prop.name)
                    self.assertEqual(self.value(g,idx,name),self.value(f,idx,name))
            self.assertEqual(bytes(f.reserve),bytes(g.reserve))

    def test_snapshot_bad_extent_alias_capacity_and_duplicate_refuse_before_stores(self):
        source,f=self.opened(pack(fixture()));record=c.create_string_buffer(RECORD)
        snapshot=c.create_string_buffer(b'\x71'*65536);output=c.create_string_buffer(b'\xa5'*80000);written=c.c_size_t(123)
        for snap,n,cap,w in [(None,65536,len(output),c.byref(written)),(snapshot,65535,len(output),c.byref(written)),
                             (snapshot,65536,4096,c.byref(written)),(output,65536,len(output),c.byref(written)),
                             (snapshot,65536,len(output),snapshot),
                             (c.c_void_p(2**64-4),65536,len(output),c.byref(written))]:
            before=output.raw;original=snapshot.raw
            self.assertNotEqual(self.lib.ace_fdt_copy_refusal_snapshot(c.byref(f),output,cap,record,len(RECORD),snap,n,w),0)
            self.assertEqual(output.raw,before);self.assertEqual(snapshot.raw,original);self.assertEqual(written.value,123)
        root=fixture();chosen=next(n for n in root.children if n.name=='chosen');chosen.props['ace,pmsg-before-seed']=b'old'
        source,f=self.opened(pack(root));before=output.raw
        self.assertEqual(self.lib.ace_fdt_copy_refusal_snapshot(c.byref(f),output,len(output),record,len(RECORD),snapshot,65536,c.byref(written)),-92)
        self.assertEqual(output.raw,before)

if __name__=='__main__':unittest.main()
