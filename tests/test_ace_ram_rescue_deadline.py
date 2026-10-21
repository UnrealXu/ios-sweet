"""Execute the actual bounded RAM guard with synthetic syscall outcomes."""
from pathlib import Path
import ctypes as c
import subprocess,tempfile,unittest
class DeadlineGuardTests(unittest.TestCase):
    def test_same_context_once_reset_and_changed_contexts_park(self):
        ROOT=Path(__file__).resolve().parents[1];tmp=tempfile.TemporaryDirectory();P=Path(tmp.name);s=(ROOT/'diagnostics/ace-ramdiag/preinit.c').read_text();s=s[s.index('#ifndef ACE_RAM_GUARD_SECONDS'):s.index('void init_main(void) {')]
        pre='''#include <setjmp.h>
        #include <string.h>
        typedef unsigned long u64;
        static unsigned rescue_enabled=1,rescue_capable=1;static long trace_fd=3;
        static unsigned char rescue_refusal[288];static int mode,calls,context,clones,reboots,timeout_messages;static jmp_buf escape;
        static void text(const char *s){if(strstr(s,"RAM deadline expired"))timeout_messages++;}
        static void fail(const char *s,long error){(void)s;(void)error;longjmp(escape,3);}
        static long call6(long nr,long a,long b,long z,long d,long e,long f) {
         (void)a;(void)d;(void)e;(void)f;
         if(nr==220){clones++;return 0;}
         if(nr==113){long *t=(void *)b;t[0]=calls++?151:0;t[1]=0;return 0;}
         if(nr==174){context++;return mode==1&&context==2?1000:0;}
         if(nr==172)return 2;
         if(nr==43){*(u64 *)b=mode==2&&context==2?0x1234:0x858458f6;return 0;}
         if(nr==79)return mode==3&&context==2?0:-2;
         if(nr==56)return 5;
         if(nr==63){memcpy((void *)b,rescue_refusal,288);if(mode==4&&context==2)((unsigned char *)b)[8]^=1;return mode==5&&context==2?287:288;}
         if(nr==57)return 0;
         if(nr==142){reboots++;return -5;}
         if(nr==101)longjmp(escape,1);
         return -1;
        }
        #define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
        '''
        post='''int test_guard(int which,int enabled){mode=which;rescue_enabled=rescue_capable=enabled;trace_fd=enabled?3:-1;calls=context=clones=reboots=timeout_messages=0;int r=setjmp(escape);if(!r)start_rescue_deadline();return r;}
        int guard_reboots(void){return reboots;}int guard_clones(void){return clones;}int guard_timeout_messages(void){return timeout_messages;}
        '''
        O=P/'deadline-host.c';O.write_text(pre+s+post);r=subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Wno-unused-parameter','-shared','-fPIC',str(O),'-o',str(P/'deadline.so')],capture_output=True,text=True);assert r.returncode==0,r.stderr
        l=c.CDLL(str(P/'deadline.so'));assert l.test_guard(0,1)==1 and l.guard_reboots()==1 and l.guard_timeout_messages()==1 and l.guard_clones()==1
        for mode in range(1,6):assert l.test_guard(mode,1)==1 and l.guard_reboots()==0 and l.guard_timeout_messages()==0
        assert l.test_guard(0,0)==0 and l.guard_clones()==0 and l.guard_reboots()==0
        print('actual deadline C: one timeout message/one failed restart->park; five changed contexts->park with no reset; no cap->no fork PASS')

        tmp.cleanup()

if __name__=='__main__':unittest.main()
