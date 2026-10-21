/* Start the fixed RAM loader once, bound userspace waiting, verify its receipt.
 * Never restarts, unloads, reboots or changes persistent storage/USB state.
 * A kernel-stalled child may remain unreaped; that is explicitly NOT success. */
typedef unsigned long u64;
#include "aarch64_flags.h"
#include "supervisor_config.h"
static long call6(long nr,long a,long b,long c,long d,long e,long f) {
    register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,x3 asm("x3")=d,
      x4 asm("x4")=e,x5 asm("x5")=f,x8 asm("x8")=nr;
    asm volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x5),"r"(x8):"memory");return x0;
}
#define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
static u64 length(const char *s){u64 n=0;while(s[n])n++;return n;}
static void text(const char *s){C3(64,1,s,length(s));}
static void number(long v){char b[24];unsigned n=0;u64 u=v<0?-v:v;if(v<0)text("-");do{b[n++]='0'+u%10;u/=10;}while(u);while(n)C3(64,1,&b[--n],1);}
static void done(long rc) __attribute__((noreturn));
static void done(long rc){C3(93,rc,0,0);for(;;){}}
static void fail(const char *s,long rc) __attribute__((noreturn));
static void fail(const char *s,long rc){text("ACE_MODULE_SUPERVISOR: FAIL ");text(s);text(" rc=");number(rc);text("\n");done(1);}
struct stamp {long sec,nsec;};
static struct stamp now(void){struct stamp s;if(C3(113,1,&s,0))fail("clock",-1);return s;}
static int expired(struct stamp current,struct stamp start,long seconds){long d=current.sec-start.sec;return d>seconds || (d==seconds && current.nsec>=start.nsec);}
static void pause_poll(void){struct stamp d={0,100000000};long r=C3(101,&d,0,0);if(r && r!=-4)fail("sleep",r);}
static void require_absent(const char *path) {
    long fd=C3(56,-100,path,ACE_O_PATH|ACE_O_NOFOLLOW|ACE_O_CLOEXEC);
    if(fd>=0){C3(57,fd,0,0);fail("preexisting loader state",-17);}
    if(fd!=-2)fail(path,fd);
}
static int receipt_matches(void) {
    long fd=C3(56,-100,"/tmp/ace-ramdiag-modules-complete",ACE_O_NOFOLLOW|ACE_O_CLOEXEC);
    if(fd==-2)return 0;
    if(fd<0)fail("completion receipt open",fd);
    u64 status[32];long r=C3(80,fd,status,0);
    if(r || (((unsigned *)status)[4]&0170000)!=0100000)fail("receipt must be regular",r?r:-22);
    unsigned char data[66];unsigned n=0;
    while(n<sizeof(data)){r=C3(63,fd,data+n,sizeof(data)-n);if(r<0)fail("receipt read",r);if(!r)break;n+=r;}
    C3(57,fd,0,0);if(n!=65 || data[64]!='\n')return 0;
    unsigned diff=0;for(unsigned i=0;i<64;i++)diff|=data[i]^(unsigned char)expected_bundle_id[i];return !diff;
}
void init_main(void) {
    if(C3(174,0,0,0) || C3(175,0,0,0) || C3(172,0,0,0)<=1)fail("root nonPID1",-1);
    u64 fs[32];long r=C3(43,"/",fs,0);if(r || (fs[0]!=0x858458f6 && fs[0]!=0x01021994))fail("RAM root",r?r:-22);
    r=C3(43,"/tmp",fs,0);if(r || fs[0]!=0x01021994)fail("RAM scratch",r?r:-22);
    require_absent("/data");require_absent("/tmp/ace-ramdiag-modules.consumed");
    require_absent("/tmp/ace-ramdiag-modules-complete");require_absent("/tmp/ace-ramdiag-return-checkpoint");
    long fd=call6(56,-100,(long)"/tmp/ace-ramdiag-supervisor.consumed",1|0100|0200|ACE_O_NOFOLLOW|ACE_O_CLOEXEC,0600,0,0);
    if(fd<0)fail("one-pass latch",fd);
    C3(57,fd,0,0);
    struct stamp start=now();
    long child=call6(220,17,0,0,0,0,0);if(child<0)fail("clone",child);
    if(child==0) {
        char *argv[]={"/ace-ramdiag/module-loader",0};char *env[]={"PATH=/system/bin",0};
        r=C3(221,argv[0],argv,env);fail("loader exec",r);
    }
    text("ACE_MODULE_SUPERVISOR: child started once\n");
    int status=0;
    for(unsigned polls=0;polls<2000;polls++) {
        r=call6(260,child,(long)&status,1,0,0,0);if(r<0)fail("wait child",r);
        if(r==child) {
            text("ACE_MODULE_SUPERVISOR: child status=");number(status);text("\n");
            if(status)fail("child failure; no retry",status);
            if(!receipt_matches())fail("missing or wrong identity receipt",-22);
            text("ACE_MODULE_SUPERVISOR: completion identity verified; operations unproven\n");done(0);
        }
        struct stamp current=now();if(expired(current,start,SUPERVISOR_TIMEOUT_SECONDS))break;
        pause_poll();
    }
    text("ACE_MODULE_SUPERVISOR: deadline; SIGKILL sent once\n");
    r=C3(129,child,9,0);if(r && r!=-3)fail("kill child",r);
    start=now();
    for(unsigned polls=0;polls<60;polls++) {
        r=call6(260,child,(long)&status,1,0,0,0);if(r<0)fail("reap child",r);
        if(r==child){text("ACE_MODULE_SUPERVISOR: timed-out child reaped; no retry\n");done(124);}
        struct stamp current=now();if(expired(current,start,5))break;
        pause_poll();
    }
    text("ACE_MODULE_SUPERVISOR: child unreaped; no retry, no ready\n");done(125);
}
