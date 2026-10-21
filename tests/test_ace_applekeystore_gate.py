"""Execute actual patched ACE AppleKeyStore start/gate with narrow DT/IOKit stubs."""
from pathlib import Path
import ctypes as c
import re
import shutil
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
REL='iokit/Kernel/arm/SweetKeyStore.cpp'


def patched_provider(directory):
    # Reconstruct the shipped provider from its actual ordered patch hunks.
    # No ignored buildtree, device dump or Apple binary is needed by this test.
    for patch in sorted((ROOT/'xnu/patches').glob('*.patch')):
        raw=patch.read_bytes()
        if ('+++ b/'+REL+'\n').encode() not in raw:
            continue
        text=raw.decode('utf-8')
        for match in re.finditer(r'^--- [^\n]+\n\+\+\+ b/([^\n]+)\n',text,re.M):
            if match.group(1)!=REL:
                continue
            end=re.search(r'^diff --git |^--- ',text[match.end():],re.M)
            section=text[match.start():match.end()+end.start() if end else len(text)]
            result=subprocess.run(['patch','--batch','--fuzz=0','-p1'],cwd=directory,
                                  input=section,capture_output=True,text=True)
            if result.returncode:
                raise AssertionError(patch.name+'\n'+result.stdout+result.stderr)
    return (directory/REL).read_text()

SOURCE=None
def function(start):
 begin=SOURCE.index(start);brace=SOURCE.index('{',begin);level=1;i=brace+1
 while level:
  if SOURCE[i]=='{':level+=1
  elif SOURCE[i]=='}':level-=1
  i+=1
 return SOURCE[begin:i]

prefix=r'''
#include <cstdint>
#include <cstring>
#include <cstdarg>
#define ARM64_BOARD_CONFIG_ACE 1
using DTEntry=const void *;
static const int kSuccess=1;
static const char *kIOUserClientClassKey="IOUserClientClass";
static const char *root_arg;static const unsigned char *property_data;
static int defaults_ok,property_ok,property_bytes,base_ok,base_calls,published,properties,logs;
static bool PE_parse_boot_argn(const char *key,void *out,int count) {
 if(std::strcmp(key,"rd") || !root_arg)return false;
 size_t n=std::strlen(root_arg)+1;std::memcpy(out,root_arg,n<(size_t)count?n:(size_t)count);return true;
}
static int SecureDTLookupEntry(DTEntry,const char *path,DTEntry *entry) {
 if(std::strcmp(path,"/defaults") || !defaults_ok)return 0;*entry=(const void *)1;return kSuccess;
}
static int SecureDTGetProperty(DTEntry,const char *name,const void **data,unsigned int *size) {
 if(std::strcmp(name,"no-effaceable-storage") || !property_ok)return 0;
 *data=property_data;*size=property_bytes;return kSuccess;
}
static void IOLog(const char *,...){logs++;}
class IOService {public:bool start(IOService *) {base_calls++;return base_ok;}};
class AppleKeyStore:public IOService {public:bool start(IOService *provider);void setProperty(const char *,const char *){properties++;}void registerService(){published++;}};
'''
suffix=r'''
extern "C" int check_start(const char *root,int found_defaults,int found_property,const unsigned char *data,int bytes,int base_result) {
 root_arg=root;defaults_ok=found_defaults;property_ok=found_property;property_data=data;property_bytes=bytes;base_ok=base_result;base_calls=published=properties=logs=0;
 AppleKeyStore store;bool result=store.start(nullptr);
 return result|(base_calls<<1)|(properties<<2)|(published<<3)|(logs<<4);
}
'''
@unittest.skipUnless(shutil.which('c++') and shutil.which('patch'), 'C++ compiler and patch required')
class AppleKeyStoreGateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  global SOURCE
  cls.tmp=tempfile.TemporaryDirectory()
  directory=Path(cls.tmp.name)
  SOURCE=patched_provider(directory)
  helper=function('static bool\nace_development_aks_enabled(void)')
  start=function('bool\nAppleKeyStore::start(IOService *provider)')
  (directory/'gate-harness.cpp').write_text(prefix+helper+'\n'+start+'\n'+suffix)
  subprocess.run(['c++','-std=c++17','-O2','-Wall','-Wextra','-Werror',
                  '-Wno-misleading-indentation','-shared','-fPIC',str(directory/'gate-harness.cpp'),
                  '-o',str(directory/'gate.so')],check=True)
  cls.lib=c.CDLL(str(directory/'gate.so'))
  cls.lib.check_start.argtypes=[c.c_char_p,c.c_int,c.c_int,c.c_void_p,c.c_int,c.c_int]
 @classmethod
 def tearDownClass(cls):
  cls.tmp.cleanup()
 def check(self,root=b'aceufsroot0',defaults=1,prop=1,data=b'\1\0\0\0',size=4,base=1):
  buf=c.create_string_buffer(data) if data is not None else None
  return self.lib.check_start(root,defaults,prop,buf,size,base)
 def test_exact_profile4_and_base_start_success_publish_once(self):self.assertEqual(self.check(),31)
 def test_missing_wrong_or_truncated_root_never_starts_or_publishes(self):
  for root in [None,b'',b'ufsroot0',b'aceufsroot00',b'aceufsroot0suffix',b'a'*64]:
   with self.subTest(root=root):self.assertEqual(self.check(root=root),0)
 def test_missing_defaults_property_or_null_value_reject(self):
  for opts in [dict(defaults=0),dict(prop=0),dict(data=None)]:
   with self.subTest(opts=opts):self.assertEqual(self.check(**opts),0)
 def test_only_exact_four_byte_little_endian_one_is_accepted(self):
  for data,size in [(b'\1',1),(b'\1\0',2),(b'\1\0\0',3),(b'\1\0\0\0\0',5),(b'',0),(b'\0'*4,4),(b'\0\0\0\1',4),(b'\2\0\0\0',4),(b'\1\0\1\0',4)]:
   with self.subTest(data=data,size=size):self.assertEqual(self.check(data=data,size=size),0)
 def test_failed_iokit_start_never_registers_or_logs_success(self):self.assertEqual(self.check(base=0),2)
if __name__=='__main__':
 unittest.main()
