/* RAM-only selected-rescue wrapper. No block device, mount or reboot request.
 * Original Magiskinit is separately hash-pinned and executed unchanged.
 * Failure stays here; it never retries, clears raw pstore, or starts Android. */
#include "sha256.h"
#include "pmsg_trace.h"
#include "../../ace/pstore_ring.c"
#include "../../ace/pstore_trial.c"
#include "../../ace/pstore_rescue.c"
#include "rescue_init_config.h"
typedef unsigned long u64;
static long call6(long nr,long a,long b,long c,long d,long e,long f) {
    register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,
      x3 asm("x3")=d,x4 asm("x4")=e,x5 asm("x5")=f,x8 asm("x8")=nr;
    asm volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x5),"r"(x8):"memory");return x0;
}
#define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
static unsigned char buffer[65536]={1},record[289]={1};
static long logfd=-1;
static u64 len(const char *s) {u64 n=0;while(s[n])n++;return n;}
static void logtext(const char *s) {if(logfd>=0)C3(64,logfd,s,len(s));}
static void stop(const char *where) __attribute__((noreturn));
static void stop(const char *where) {
    logtext("ACE_RESCUE_WRAPPER: STOP ");logtext(where);logtext("\n");
    struct {long sec,nsec;} delay={1,0};for(;;)C3(101,&delay,0,0);
}
static void directory(const char *s) {long r=C3(34,-100,s,0755);if(r && r!=-17)stop(s);}
static void mount_virtual(const char *type,const char *path,u64 flags) {
    directory(path);long r=call6(40,(long)type,(long)path,(long)type,flags,0,0);if(r)stop(path);
}
static long bounded_read(const char *path,unsigned char *out,u64 capacity) {
    long fd=C3(56,-100,path,02000000|0400000);if(fd<0)stop(path);
    u64 size=0;while(size<capacity) {long n=C3(63,fd,out+size,capacity-size);if(n<0)stop(path);if(!n)break;size+=(u64)n;}
    unsigned char extra;long n=C3(63,fd,&extra,1);C3(57,fd,0,0);if(n)stop("oversized input");return (long)size;
}
void init_main(void) {
    if(C3(172,0,0,0)!=1 || C3(174,0,0,0)!=0)stop("not PID1");
    u64 fs[32];if(C3(43,"/",fs,0) || (fs[0]!=0x858458f6 && fs[0]!=0x01021994))stop("not RAM root");
    mount_virtual("tmpfs","/dev",2);
    if(call6(33,-100,(long)"/dev/kmsg",0020000|0600,(1<<8)|11,0,0))stop("kmsg node");
    logfd=C3(56,-100,"/dev/kmsg",1|02000000);
    mount_virtual("proc","/proc",2|4|8);mount_virtual("sysfs","/sys",2|4|8);
    if(bounded_read("/sys/firmware/devicetree/base/chosen/ace,native-refusal",record,sizeof(record))!=288)stop("current record length");
    static const char token[]=RESCUE_TOKEN,magic[]="ACEFALL1";
    if(sizeof(token)!=17)stop("token length");
    for(unsigned i=0;i<8;i++)if(record[i]!=(unsigned char)magic[i] || record[24+i])stop("record header");
    for(unsigned i=0;i<16;i++)if(record[8+i]!=(unsigned char)token[i] ||
        !((token[i]>='0'&&token[i]<='9') || (token[i]>='a'&&token[i]<='f')))stop("current token");
    if(word(record+32)!=0x313054414e454341ULL || word(record+40)!=1 || word(record+48)!=5 ||
       word(record+56)!=(uint64_t)(int64_t)-67 || word(record+192) || word(record+280)!=ACE_RAM_RESCUE_WORD)stop("not selected rescue");
    /* Keep the verified original ELF FD across unmount, then exec exactly this
     * inode with AT_EMPTY_PATH. No pathname race or replacement is accepted. */
    long original=C3(56,-100,"/ace-rescue/original-init",02000000|0400000);if(original<0)stop("original init open");
    struct ace_sha256 hash;ace_sha_init(&hash);u64 total=0;
    for(;;) {long n=C3(63,original,buffer,sizeof(buffer));if(n<0)stop("original init read");if(!n)break;
        if((u64)n>RESCUE_ORIGINAL_BYTES-total)stop("original init size");
        total+=(u64)n;ace_sha_update(&hash,buffer,(u64)n);}
    unsigned char digest[32];ace_sha_final(&hash,digest);static const unsigned char expected[32]=RESCUE_ORIGINAL_SHA256;
    if(total!=RESCUE_ORIGINAL_BYTES)stop("original init size");
    for(unsigned i=0;i<32;i++)if(digest[i]!=expected[i])stop("original init hash");
    mount_virtual("pstore","/sys/fs/pstore",2|4|8);
    long size=bounded_read("/sys/fs/pstore/pmsg-ramoops-0",buffer+12,65524);if(size<288)stop("old pmsg length");
    for(unsigned i=0;i<4;i++) {buffer[i]=(unsigned char)(0x43474244U>>(8*i));buffer[4+i]=(unsigned char)((u64)size>>(8*i));buffer[8+i]=buffer[4+i];}
    if(ace_pstore_ram_attempt(buffer,65536,token)!=ACE_RAM_STOP)stop("old pmsg selected state");
    for(unsigned i=0;i<288;i++)if(buffer[12+size-288+i]!=record[i])stop("old/current selected mismatch");
    unsigned char dev[16];long n=bounded_read("/sys/class/pmsg/pmsg0/dev",dev,sizeof(dev));int major=ace_pmsg_major(dev,(u64)n);if(major<0)stop("pmsg device identity");
    if(call6(33,-100,(long)"/dev/ace-pmsg",0020000|0600,(unsigned)major<<8,0,0))stop("pmsg node");
    long fd=C3(56,-100,"/dev/ace-pmsg",1|02000000);if(fd<0)stop("pmsg open");
    if(C3(64,fd,buffer+12,(u64)size)!=size)stop("selected republish");
    static const char receipt[]="\nACERESCUEPID1:" RESCUE_TOKEN ": selected republished; exec pinned original init\n";
    if(C3(64,fd,receipt,sizeof(receipt)-1)!=(long)sizeof(receipt)-1)stop("selected receipt");
    C3(57,fd,0,0);logtext("ACE_RESCUE_WRAPPER: selected republished; exec pinned original init\n");
    if(logfd>=0) {C3(57,logfd,0,0);logfd=-1;}
    if(C3(39,"/sys/fs/pstore",0,0) || C3(39,"/sys",0,0) || C3(39,"/proc",0,0) || C3(39,"/dev",0,0))stop("virtual unmount");
    char *argv[]={"/init",0};char *env[]={"PATH=/sbin:/system/bin","HOME=/","TERM=linux",0};
    call6(281,original,(long)"",(long)argv,(long)env,0x1000,0);
    stop("original init exec failed");
}
