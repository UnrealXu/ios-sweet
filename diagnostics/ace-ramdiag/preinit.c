/* Experimental RAM-only PID1 bootstrap; currently QEMU component tests only.
 * No block nodes, module loading, stock first_stage or selinux_setup calls. */
typedef unsigned long u64;
#include "slot_guard.h"
#include "pmsg_trace.h"
#include "../../ace/pstore_ring.c"
#include "../../ace/pstore_trial.c"
#include "../../ace/pstore_rescue.c"
static long call6(long nr,long a,long b,long c,long d,long e,long f) {
    register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,
      x3 asm("x3")=d,x4 asm("x4")=e,x5 asm("x5")=f,x8 asm("x8")=nr;
    asm volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x5),"r"(x8):"memory");
    return x0;
}
#define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
static u64 length(const char *s) {u64 n=0;while(s[n])n++;return n;}
static long trace_fd=-1;
static unsigned rescue_enabled,rescue_capable;
static unsigned char rescue_refusal[288]={1};
static long rescue_rearm(long);
static void rescue_capability(void);
static char trace_token[17];
static void trace_text(const char *s,u64 n) {
    if(trace_fd<0 || n>192)return;
    char packet[240];u64 used=0;const char prefix[]="ACEPID1:";
    for(unsigned i=0;i<sizeof(prefix)-1;i++)packet[used++]=prefix[i];
    for(unsigned i=0;i<16;i++)packet[used++]=trace_token[i];
    packet[used++]=':';packet[used++]=' ';
    for(u64 i=0;i<n;i++)packet[used++]=s[i];
    long r=C3(64,trace_fd,packet,used);
    if(r!=(long)used) {C3(57,trace_fd,0,0);trace_fd=-1;}
}
static void text(const char *s) {u64 n=length(s);C3(64,1,s,n);trace_text(s,n);}
static void number(long value) {
    char reversed[24],output[26];unsigned n=0,used=0;
    u64 v=value<0?0-(u64)value:(u64)value;
    if(value<0)output[used++]='-';
    do {reversed[n++]='0'+v%10;v/=10;}while(v);
    while(n)output[used++]=reversed[--n];
    output[used]=0;text(output);
}
static void fail(const char *where,long error) __attribute__((noreturn));
static void fail(const char *where,long error) {
    text("ACE_RAMDIAG: FAIL ");text(where);text(" rc=");number(error);text("\n");
    C3(142,0xfee1dead,0x28121969,rescue_enabled?0x1234567:0x4321fedc);
    struct {long sec,nsec;} delay={1,0};
    for(;;)C3(101,&delay,0,0);
}
static void directory(const char *path) {
    long r=C3(34,-100,path,0755);if(r && r!=-17)fail(path,r);
}
static void virtual_mount(const char *type,const char *path,u64 flags,const char *opts) {
    directory(path);
    long r=call6(40,(long)type,(long)path,(long)type,flags,(long)opts,0);
    if(r)fail(path,r);
}
static void node(const char *path,unsigned major,unsigned minor) {
    long r=call6(33,-100,(long)path,0020000|0600,(major<<8)|minor,0,0);
    if(r)fail(path,r);
}
static void write_file(const char *path,const void *data,u64 size) {
    long fd=C3(56,-100,path,1|02000000);if(fd<0)fail(path,fd);
    /* Policy loading must use one complete write. */
    long r=C3(64,fd,data,size);if(r<0 || (u64)r!=size)fail(path,r);
    r=C3(57,fd,0,0);if(r)fail(path,r);
}
/* Optional evidence only; failures never change the existing boot decision.
 * /dev, proc and sysfs are newly mounted virtual filesystems. No /data mount. */
static long persistent_trace(void) {
    unsigned char token[18],dev[16];
    long fd=C3(56,-100,"/ace-ramdiag/trace-token",0);
    if(fd<0)return fd;
    long n=C3(63,fd,token,sizeof(token));C3(57,fd,0,0);
    if(n!=17 || token[16]!='\n')return -22;
    for(unsigned i=0;i<16;i++) {
        if(!((token[i]>='0' && token[i]<='9') || (token[i]>='a' && token[i]<='f')))return -22;
        trace_token[i]=(char)token[i];
    }
    fd=C3(56,-100,"/sys/class/pmsg/pmsg0/dev",0);
    if(fd<0)return fd;
    n=C3(63,fd,dev,sizeof(dev));C3(57,fd,0,0);
    if(n<0)return n;
    int major=ace_pmsg_major(dev,(u64)n);if(major<0)return -22;
    long r=call6(33,-100,(long)"/dev/ace-pmsg",0020000|0600,(unsigned)major<<8,0,0);
    if(r)return r;
    fd=C3(56,-100,"/dev/ace-pmsg",1|02000000);if(fd<0)return fd;
    /* Keep the optional descriptor outside stdin/out/err, then close on exec. */
    long saved=C3(25,fd,1030,3);C3(57,fd,0,0);if(saved<0)return saved;
    trace_fd=saved;
    if(rescue_capable) {
        long armed=rescue_rearm(trace_fd);
        if(armed) {C3(57,trace_fd,0,0);trace_fd=-1;return armed;}
        rescue_enabled=1;
    }
    trace_text("virtual mounts ready before stdio\n",sizeof("virtual mounts ready before stdio\n")-1);
    return trace_fd<0?-5:0;
}
static void rescue_capability(void) {
    unsigned char cap[25],record[289],token[18];
    long fd=C3(56,-100,"/ace-ramdiag/trace-token",0);if(fd<0)return;
    long n=C3(63,fd,token,sizeof(token));C3(57,fd,0,0);
    if(n!=17 || token[16]!='\n')return;
    fd=C3(56,-100,"/sys/firmware/devicetree/base/chosen/ace,ram-rescue",0);if(fd<0)return;
    n=C3(63,fd,cap,sizeof(cap));C3(57,fd,0,0);if(n!=24)return;
    const char magic[]="ACERAMR1";
    for(unsigned i=0;i<8;i++)if(cap[i]!=(unsigned char)magic[i])return;
    for(unsigned i=0;i<16;i++)if(cap[8+i]!=token[i] ||
        !((token[i]>='0'&&token[i]<='9') || (token[i]>='a'&&token[i]<='f')))return;
    fd=C3(56,-100,"/sys/firmware/devicetree/base/chosen/ace,native-refusal",0);if(fd<0)return;
    n=C3(63,fd,record,sizeof(record));C3(57,fd,0,0);if(n!=288)return;
    const char envelope[]="ACEFALL1";
    for(unsigned i=0;i<8;i++)if(record[i]!=(unsigned char)envelope[i] || record[24+i])return;
    for(unsigned i=0;i<16;i++)if(record[8+i]!=token[i])return;
    /* Exact native stage5/-67, clear fallback guard and ordinary first RAM handoff. */
    unsigned long words[32];
    for(unsigned i=0;i<32;i++) {words[i]=0;for(unsigned j=0;j<8;j++)words[i]|=(unsigned long)record[32+8*i+j]<<(8*j);}
    if(words[0]!=0x313054414e454341UL || words[1]!=1 || words[2]!=5 ||
       words[3]!=(unsigned long)-67 || words[20] || words[31])return;
    for(unsigned i=0;i<288;i++)rescue_refusal[i]=record[i];
    rescue_capable=1;
}
static void standard_io(void) {
    long fd=C3(56,-100,"/dev/console",2),r;
    if(fd>=0) {
        for(int i=0;i<3;i++)if(fd!=i && (r=C3(24,fd,i,0))<0)fail("stdio",r);
        if(fd>2)C3(57,fd,0,0);
        return;
    }
    /* A console tty may require a module that has not been loaded yet.
     * Keep RAM diagnostics independent of that driver. Unexpected permission
     * or path errors still stop; only unavailable-console errors use kmsg. */
    if(fd!=-19 && fd!=-6 && fd!=-5)fail("console",fd);
    long input=C3(56,-100,"/dev/null",0);
    long output=C3(56,-100,"/dev/kmsg",1);
    if(input<0 || output<0)fail("RAM diagnostic stdio",input<0?input:output);
    if(input!=0 && (r=C3(24,input,0,0))<0)fail("stdin",r);
    for(int i=1;i<3;i++)if(output!=i && (r=C3(24,output,i,0))<0)fail("kmsg stdio",r);
    if(input>2)C3(57,input,0,0);
    if(output>2)C3(57,output,0,0);
    text("ACE_RAMDIAG: unavailable console; stdin null, output kmsg\n");
}
/* Keep a file-backed byte in this writable PT_LOAD. A pure zero-file-size
 * segment placed beyond EOF was rejected by this exact kernel with EFAULT. */
static unsigned char policy[8*1024*1024]={1};
/* ramoops saves the prior native pmsg into old-log RAM and clears its live
 * ring on Linux boot. Preserve exactly that current-token evidence once in
 * the new live pmsg; never seed/clear raw physical memory or invent markers.
 * A missing, truncated, duplicate, selected or differing old envelope refuses
 * before enabling warm restart. Any live duplicate then causes native STOP.
 */
static long rescue_rearm(long fd) {
    directory("/sys/fs/pstore");
    long r=call6(40,(long)"pstore",(long)"/sys/fs/pstore",(long)"pstore",2|4|8,0,0);
    if(r && r!=-16)return r;
    long old=C3(56,-100,"/sys/fs/pstore/pmsg-ramoops-0",0);if(old<0)return old;
    unsigned long size=0;long n;
    while(size<65524) {
        n=C3(63,old,policy+12+size,65524-size);if(n<0) {C3(57,old,0,0);return n;}
        if(!n)break;
        size+=(unsigned long)n;
    }
    unsigned char extra;n=C3(63,old,&extra,1);C3(57,old,0,0);
    if(n || size<288)return -22;
    for(unsigned i=0;i<4;i++) {policy[i]=(unsigned char)(0x43474244U>>(8*i));policy[4+i]=(unsigned char)(size>>(8*i));policy[8+i]=policy[4+i];}
    if(ace_pstore_ram_attempt(policy,65536,trace_token)!=ACE_RAM_RESCUE)return -22;
    for(unsigned i=0;i<288;i++)if(policy[12+size-288+i]!=rescue_refusal[i])return -22;
    r=C3(64,fd,policy+12,size);
    return r==(long)size?0:r<0?r:-5;
}
static long read_slot_file(const char *path,int optional) {
    long fd=C3(56,-100,path,0);if(fd==-2 && optional)return 0;
    if(fd<0)fail(path,fd);
    u64 size=0;long n;
    while(size<65536) {
        n=C3(63,fd,policy+size,65536-size);if(n<0)fail(path,n);
        if(!n)break;
        size+=(u64)n;
    }
    unsigned char extra;n=C3(63,fd,&extra,1);C3(57,fd,0,0);
    if(n)fail("slot text limit",n);
    return (long)size;
}
static void require_b_slot(void) {
    long n=read_slot_file("/proc/cmdline",0);
    int cmdline=ace_slot_cmdline(policy,(u64)n);
    n=read_slot_file("/proc/bootconfig",1);
    int bootconfig=ace_slot_bootconfig(policy,(u64)n);
    if(!ace_slot_states_valid(cmdline,bootconfig))fail("B-slot gate",-22);
    text("ACE_RAMDIAG: B-slot gate verified before stock init\n");
}
static void observe_pid1(void) {
    long flag=C3(56,-100,"/ace-ramdiag/observe-pid1",0);
    if(flag<0)return;
    C3(57,flag,0,0);
    long child=call6(220,17,0,0,0,0,0);
    if(child<0)fail("observer clone",child);
    if(child)return;
    struct {long sec,nsec;} delay={12,0};C3(101,&delay,0,0);
    const char *paths[]={"/proc/1/syscall","/proc/1/wchan","/proc/1/stack","/proc/1/maps",0};
    char data[4096];
    for(unsigned i=0;paths[i];i++) {
        text("ACE_RAMDIAG_OBSERVER: ");text(paths[i]);text("\n");
        long fd=C3(56,-100,paths[i],0);
        if(fd<0){number(fd);text("\n");continue;}
        long n;while((n=C3(63,fd,data,sizeof(data)))>0)C3(64,1,data,n);
        C3(57,fd,0,0);text("\n");
    }
    text("ACE_RAMDIAG_OBSERVER: ending diagnostic observation\n");
    C3(142,0xfee1dead,0x28121969,0x4321fedc);
    for(;;)C3(101,&delay,0,0);
}
#ifndef ACE_RAM_GUARD_SECONDS
#define ACE_RAM_GUARD_SECONDS 150
#endif
/* One root child survives exact recovery-init exec, covering later module/USB
 * failures without starting any second init or touching persistent storage.
 * Normal successful readout reboots to Fastboot before this child can fire. */
static void guard_park(void) __attribute__((noreturn));
static void guard_park(void) {struct {long sec,nsec;} d={1,0};for(;;)C3(101,&d,0,0);}
static int guard_context_valid(void) {
    if(C3(174,0,0,0) || C3(172,0,0,0)<=1)return 0;
    u64 fs[32];if(C3(43,"/",fs,0) || (fs[0]!=0x858458f6 && fs[0]!=0x01021994))return 0;
    unsigned char status[256];
    if(call6(79,-100,(long)"/data",(long)status,0x100,0,0)!=-2)return 0;
    unsigned char current[289];long fd=C3(56,-100,"/sys/firmware/devicetree/base/chosen/ace,native-refusal",0);
    if(fd<0)return 0;
    long n=C3(63,fd,current,sizeof(current));C3(57,fd,0,0);
    if(n!=288)return 0;
    for(unsigned i=0;i<288;i++)if(current[i]!=rescue_refusal[i])return 0;
    return 1;
}
static void start_rescue_deadline(void) {
    if(!rescue_enabled || !rescue_capable || trace_fd<3)return;
    struct {long sec,nsec;} started,now,delay={1,0};
    if(C3(113,1,&started,0))fail("rescue deadline monotonic clock",-1);
    long child=call6(220,17,0,0,0,0,0);if(child<0)fail("rescue deadline clone",child);
    if(child)return;
    if(!guard_context_valid()) {text("ACE_RAMDIAG: deadline context invalid; parked\n");guard_park();}
    text("ACE_RAMDIAG: one current-token RAM deadline guard armed\n");
    for(;;) {
        if(C3(113,1,&now,0)) {text("ACE_RAMDIAG: deadline clock failed; parked\n");guard_park();}
        long elapsed=now.sec-started.sec;
        if(elapsed>ACE_RAM_GUARD_SECONDS || (elapsed==ACE_RAM_GUARD_SECONDS && now.nsec>=started.nsec))break;
        long r=C3(101,&delay,0,0);if(r && r!=-4) {text("ACE_RAMDIAG: deadline sleep failed; parked\n");guard_park();}
    }
    if(!guard_context_valid()) {text("ACE_RAMDIAG: deadline current record/RAM/no-data changed; parked\n");guard_park();}
    text("ACE_RAMDIAG: RAM deadline expired; one verified warm rescue request\n");
    C3(142,0xfee1dead,0x28121969,0x1234567);
    text("ACE_RAMDIAG: deadline restart returned; parked without retry\n");guard_park();
}
void init_main(void) {
    long r=C3(172,0,0,0);if(r!=1)fail("PID1",r);
    u64 fs[32];r=C3(43,"/",fs,0);
    if(r || (fs[0]!=0x858458f6 && fs[0]!=0x01021994))fail("RAM root",r?r:(long)fs[0]);
    virtual_mount("tmpfs","/dev",2,"mode=0755");
    node("/dev/console",5,1);node("/dev/null",1,3);node("/dev/kmsg",1,11);
    node("/dev/kmsg_debug",1,11);
    node("/dev/random",1,8);node("/dev/urandom",1,9);node("/dev/ptmx",5,2);
    virtual_mount("proc","/proc",2|4|8,0);
    virtual_mount("sysfs","/sys",2|4|8,0);
    rescue_capability();
    long trace_result=persistent_trace();
    standard_io();
    if(trace_result) {text("ACE_RAMDIAG: persistent trace unavailable rc=");number(trace_result);text("\n");}
    else text("ACE_RAMDIAG: persistent pmsg trace active\n");
    long fd;
    text("ACE_RAMDIAG: PID1 RAM root verified\n");
    require_b_slot();
    fd=C3(56,-100,"/ace-ramdiag/vendor-overlay",0);
    if(fd>=0) {
        C3(57,fd,0,0);directory("/lib");
        virtual_mount("tmpfs","/lib/modules",2|4|8,"mode=0700");
        /* The pinned archive supplies /data/vendor and its parent, both
         * containing no files. Remove only these RAM-only empty directories;
         * refuse nonempty directories rather than deleting their contents. */
        r=C3(35,-100,"/data/vendor",0x200);
        if(r && r!=-2)fail("empty RAM vendor data directory",r);
        r=C3(35,-100,"/data",0x200);
        if(r && r!=-2)fail("empty RAM data directory",r);
        text("ACE_RAMDIAG: stock module tree hidden\n");
    }
    const char *dirs[]={"/dev/socket","/dev/pts","/apex","/linkerconfig","/tmp","/mnt",0};
    for(unsigned i=0;dirs[i];i++)directory(dirs[i]);
    virtual_mount("devpts","/dev/pts",2|8,"mode=0620,ptmxmode=0666");
    virtual_mount("tmpfs","/tmp",2|4,"mode=0700");
    directory("/sys/fs/selinux");
    r=call6(40,(long)"selinuxfs",(long)"/sys/fs/selinux",(long)"selinuxfs",2|8,0,0);
    if(r) {
        if(r!=-19)fail("selinuxfs",r);
        text("ACE_RAMDIAG: SELinux unavailable; disabled-policy branch\n");
    } else {
        fd=C3(56,-100,"/sepolicy",02000000);if(fd<0)fail("policy input",fd);
        u64 size=0;
        while(size<sizeof(policy)) {
            r=C3(63,fd,policy+size,sizeof(policy)-size);if(r<0)fail("policy read",r);
            if(!r)break;
            size+=(u64)r;
        }
        unsigned char extra;r=C3(63,fd,&extra,1);C3(57,fd,0,0);
        if(r || !size)fail("policy size",r?r:-1);
        write_file("/sys/fs/selinux/load",policy,size);
        /* Diagnostic guest only; no persistent policy/firmware write. */
        write_file("/sys/fs/selinux/enforce","0",1);
        const char label[]="u:object_r:init_exec:s0";
        r=call6(5,(long)"/system/bin/init",(long)"security.selinux",(long)label,sizeof(label),0,0);
        if(r)fail("init label",r);
        text("ACE_RAMDIAG: monolithic policy loaded; permissive diagnostic guest\n");
    }
    text("ACE_RAMDIAG: exec exact recovery init second_stage\n");
    start_rescue_deadline();
    observe_pid1();
    char *argv[]={"/system/bin/init","second_stage",0};
    char *env[]={"PATH=/system/bin",0};
    r=C3(221,argv[0],argv,env);fail("second_stage exec",r);
}
