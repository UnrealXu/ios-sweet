/* Explicit QEMU negative fixture; never included in a physical module bundle. */
#include "fault_config.h"
#include "aarch64_flags.h"
static long call6(long nr,long a,long b,long c,long d,long e,long f) {
    register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,x3 asm("x3")=d,
      x4 asm("x4")=e,x5 asm("x5")=f,x8 asm("x8")=nr;
    asm volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x5),"r"(x8):"memory");return x0;
}
#define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
void init_main(void) {
    const char start[]="ACE_MODULE_FAULT: child started once\n";C3(64,1,start,sizeof(start)-1);
#if MODULE_FAULT_MODE == 1
    struct {long sec,nsec;} delay={1,0};for(;;)C3(101,&delay,0,0);
#elif MODULE_FAULT_MODE == 2
    const char wrong[]="0000000000000000000000000000000000000000000000000000000000000000\n";
    long fd=call6(56,-100,(long)"/tmp/ace-ramdiag-modules-complete",1|0100|0200|ACE_O_NOFOLLOW|ACE_O_CLOEXEC,0600,0,0);
    if(fd<0){C3(93,2,0,0);for(;;){}}
    C3(64,fd,wrong,sizeof(wrong)-1);C3(57,fd,0,0);
#endif
    C3(93,0,0,0);for(;;){}
}
