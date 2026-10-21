"""Analysis metadata must preserve exact input bytes and expose no fake physical map."""
import hashlib
import importlib.util
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('lk_analysis',Path(__file__).resolve().parents[1]/'tools/ace-lk-analysis-elf.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class LkAnalysisElfTests(unittest.TestCase):
    def test_changed_or_unselected_firmware_is_refused(self):
        for data in [b'',b'ANDROID!',bytes(65536)]:
            with self.assertRaises(ValueError):m.wrap(data)

    def test_analysis_container_preserves_payload_and_has_no_physical_or_bss_claim(self):
        data=bytes(range(256))*256
        with patch.object(m,'PIN',hashlib.sha256(data).hexdigest()):elf,meta=m.wrap(data)
        self.assertEqual(elf[:7],b'\x7fELF\x02\x01\x01')
        self.assertEqual(struct.unpack_from('<H',elf,18)[0],183)
        self.assertEqual(struct.unpack_from('<Q',elf,24)[0],m.VBASE+0x5f50)
        ph=struct.unpack_from('<IIQQQQQQ',elf,64)
        self.assertEqual(ph,(1,5,4096,m.VBASE,0,len(data),len(data),4096))
        self.assertEqual(elf[ph[2]:ph[2]+ph[5]],data)
        self.assertTrue(meta['analysis_only']);self.assertFalse(meta['firmware_deployable'])
        self.assertTrue(meta['no_synthetic_bss'])

    def test_symbols_are_explicit_analyst_labels_at_exact_offsets(self):
        data=bytes(65536)
        with patch.object(m,'PIN',hashlib.sha256(data).hexdigest()):elf,_=m.wrap(data)
        shoff=struct.unpack_from('<Q',elf,40)[0]
        sym=struct.unpack_from('<IIQQQQIIQQ',elf,shoff+2*64)
        names=struct.unpack_from('<IIQQQQIIQQ',elf,shoff+3*64)
        strings=elf[names[4]:names[4]+names[5]]
        found={}
        for i in range(24,sym[5],24):
            off,info,other,section,va,size=struct.unpack_from('<IBBHQQ',elf,sym[4]+i)
            label=strings[off:].split(b'\0',1)[0].decode()
            self.assertTrue(label.startswith('analyst_'))
            self.assertEqual((info,other,section,size),(0x12,0,1,0))
            found[va-m.VBASE]=label
        self.assertEqual(found,m.LABELS)


if __name__=='__main__':unittest.main()
