"""Run the real 0118 failure branch; mocked WFE exits only the host harness."""
from pathlib import Path
import unittest
from test_ace_ufs_bsd_root import execute
ROOT=Path(__file__).resolve().parents[1]
class RootMountFailureTests(unittest.TestCase):
    def test_exact_explicit_root_parks_once_other_paths_continue(self):
        patch=(ROOT/'xnu/patches/0118-ace-preserve-first-explicit-root-mount-failure.patch').read_text()
        branch='\n'.join(line[1:] for line in patch.splitlines() if line.startswith('+') and not line.startswith('+++'))
        self.assertEqual(branch.count('__asm__ volatile ("wfe" ::: "memory");'),1)
        self.assertNotIn('SMC',branch)
        self.assertNotIn('IOSleep',branch)
        branch=branch.replace('__asm__ volatile ("wfe" ::: "memory");','park();')
        execute(r'''
#include <cassert>
#include <cstring>
#include <string>
#include <initializer_list>
#define ARM64_BOARD_CONFIG_ACE 1
static const char *requested;
static int logs,parses,parks,calls,limit;
static void park(){parks++;throw 19;}
static bool PE_parse_boot_argn(const char *key,char *buf,unsigned n){
    assert(!strcmp(key,"rd"));parses++;if(!requested)return false;
    strncpy(buf,requested,n-1);return true;
}
#define printf(...) (++logs)
static void run(){
    for(;;){
        calls++;
        int err=calls<=limit?19:0;
        if(!err)break;
        BRANCH
    }
}
int main(){
    requested="aceufsroot0";limit=0;run();assert(calls==1&&!parses&&!parks&&!logs);
    calls=0;limit=124;
    try{run();assert(false);}catch(int e){assert(e==19);}
    assert(calls==1&&parses==1&&parks==1&&logs==1);
    for(const char *s:{(const char *)nullptr,"","ufsroot0","aceufsroot1","aceufsroot0suffix","md0"}){
        requested=s;calls=parses=parks=logs=0;limit=2;run();
        assert(calls==3&&parses==2&&!parks&&!logs);
    }
}
'''.replace('BRANCH',branch))
