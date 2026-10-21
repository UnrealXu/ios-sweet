/* Read current native envelope once before module insertion; RAM output only. */
typedef unsigned long u64;
#include "aarch64_flags.h"
#include "native_record_guard.h"
#include "native_config.h"
static long call6(long nr,long a,long b,long c,long d,long e,long f) {
    register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,x3 asm("x3")=d,
      x4 asm("x4")=e,x5 asm("x5")=f,x8 asm("x8")=nr;
    asm volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x5),"r"(x8):"memory");return x0;
}
#define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
static void done(int code) __attribute__((noreturn));
static void done(int code){C3(93,code,0,0);for(;;){}}
static void fail(void) __attribute__((noreturn));
static void fail(void){const char s[]="ACE_NATIVE_GATE: FAIL; no modules or ADB readiness\n";C3(64,2,s,sizeof(s)-1);done(1);}
void init_main(void) {
    if(C3(174,0,0,0) || C3(175,0,0,0) || C3(172,0,0,0)<=1)fail();
    u64 fs[32];long r=C3(43,"/",fs,0);
    if(r || (fs[0]!=0x858458f6 && fs[0]!=0x01021994))fail();
    r=C3(43,"/tmp",fs,0);if(r || fs[0]!=0x01021994)fail();
    long fd=C3(56,-100,"/data",ACE_O_PATH|ACE_O_NOFOLLOW|ACE_O_CLOEXEC);
    if(fd!=-2)fail();
    fd=C3(56,-100,"/sys/firmware/devicetree/base/chosen/ace,native-refusal",ACE_O_NOFOLLOW|ACE_O_CLOEXEC);
    if(fd<0)fail();
    unsigned char record[289];u64 n=0;
    while(n<sizeof(record)) {r=C3(63,fd,record+n,sizeof(record)-n);if(r<0)fail();if(!r)break;n+=r;}
    if(C3(57,fd,0,0) || !ace_native_refusal_record(record,n,expected_native_token))fail();
    fd=call6(56,-100,(long)"/tmp/ace-ramdiag-native-checked",1|0100|0200|ACE_O_NOFOLLOW|ACE_O_CLOEXEC,0400,0,0);
    if(fd<0)fail();
    if(C3(64,fd,record,288)!=288 || C3(57,fd,0,0))fail();
    const char s[]="ACE_NATIVE_GATE: current refusal record saved; iOS unproven\n";
    C3(64,1,s,sizeof(s)-1);done(0);
}
