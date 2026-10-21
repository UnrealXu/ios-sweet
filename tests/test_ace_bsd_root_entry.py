"""Exercise the actual explicit root selector before generic IOBSD waits."""
from pathlib import Path
import re,unittest
from test_ace_ufs_bsd_root import execute
ROOT=Path(__file__).resolve().parents[1]
class RootEntryTests(unittest.TestCase):
    def test_exact_root_selection_propagates_errors_and_defaults_unchanged(self):
        patch=(ROOT/'xnu/patches/0117-ace-select-explicit-bsd-root-before-generic-resource-wait.patch').read_text()
        added='\n'.join(l[1:] for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++'))
        start=added.index('static bool ace_find_explicit_root(');end=added.index('\n#endif',start)
        self.assertIn('if(ace_find_explicit_root(rootName,rootNameSize,root,oflags)) return kIOReturnSuccess;',added)
        self.assertNotIn('waitForMatchingService',added[start:end])
        execute(r'''
#include <cassert>
#include <cstring>
#include <cstdint>
#include <stdexcept>
#include <string>
using u_int32_t=uint32_t;
#define dev_t int
#define major(d) ((d)>>8)
#define minor(d) ((d)&255)
#define IOLog(...) ((void)0)
static const char *requested;
static int calls,error,media_calls;
static bool PE_parse_boot_argn(const char *key,char *dst,unsigned n) {
    assert(!strcmp(key,"rd"));if(!requested)return false;
    strncpy(dst,requested,n-1);return true;
}
static int ace_ufs_rootdev(int *dev){calls++;if(!error)*dev=0x1200;return error;}
static size_t strlcpy(char *dst,const char *src,unsigned n){if(n){strncpy(dst,src,n-1);dst[n-1]=0;}return strlen(src);}
static void panic(const char *,int code){throw code;}
struct IOService {static void setRootMedia(void *p){assert(!p);media_calls++;}};
HELPER
int main() {
    char name[32]="untouched";int dev=777;uint32_t flags=9;
    for(const char *s:{(const char *)nullptr,"","ufsroot0","aceufsroot1","aceufsroot0suffix","md0"}) {
        requested=s;assert(!ace_find_explicit_root(name,sizeof(name),&dev,&flags));
        assert(!calls && !media_calls && flags==9 && dev==777 && !strcmp(name,"untouched"));
    }
    requested="aceufsroot0";
    assert(ace_find_explicit_root(name,sizeof(name),&dev,&flags));
    assert(calls==1 && media_calls==1 && dev==0x1200 && !flags && !strcmp(name,requested));
    for(int failure:{6,11,5,12}) {
        error=failure;flags=9;dev=777;strcpy(name,"untouched");
        try{ace_find_explicit_root(name,sizeof(name),&dev,&flags);assert(false);}catch(int actual){assert(actual==failure);}
        assert(media_calls==1 && flags==9 && dev==777 && !strcmp(name,"untouched"));
    }
}
'''.replace('HELPER',added[start:end]))
