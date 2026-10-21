import importlib.util
from pathlib import Path
import struct
import unittest
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('chain_record',ROOT/'tools/ace-stock-chain-record.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
TOKEN='1234567890abcdef12345678'
MARKER=('ACECHAIN1:'+TOKEN+': forwarding original Android kernel\n').encode()
RECORD=[int.from_bytes(b'ACECHN01','little'),1,0x48000000,8,0x30c50830,0x412fd050,0x101122,13000000,0,0x40200000]
class ChainRecordTests(unittest.TestCase):
    def test_binary_capture_and_actual_hardware_facts(self):
        r=m.decode(b'\x00old logs\xff'+MARKER+struct.pack('<10Q',*RECORD)+b'\x00after',TOKEN,True)
        self.assertEqual(r['incoming_el'],2);self.assertEqual(r['cntfrq_hz'],13000000)
        self.assertEqual(r['stock_entry_pa'],'0x40200000')
    def test_ambiguous_old_or_truncated_capture_is_not_a_pass(self):
        raw=MARKER+struct.pack('<10Q',*RECORD)
        for data in [b'',raw[:-1],raw+raw,raw.replace(TOKEN.encode(),b'0'*24),MARKER+b'\x00'*80,b'x'*(1024*1024+1)]:
            with self.subTest(length=len(data)),self.assertRaises(ValueError):m.decode(data,TOKEN,True)
    def test_bad_control_cpu_and_missing_raw_fields_refused(self):
        for index,value in [(1,2),(2,0),(2,1),(3,12),(4,RECORD[4]|1),(4,RECORD[4]|4),(4,RECORD[4]|(1<<25)),(5,0),(6,0),(7,62500000),(8,1),(9,0x40201000)]:
            r=RECORD.copy();r[index]=value
            with self.subTest(index=index,value=value),self.assertRaises(ValueError):m.decode(MARKER+struct.pack('<10Q',*r),TOKEN,True)
if __name__=='__main__':unittest.main()
