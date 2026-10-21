/* One-pass RAM module loader. No persistent device/mount/reboot operations.
 * Bundle entries and identity are compile-time constants, never shell input. */
typedef unsigned long u64;
#include "sha256.h"
#include "slot_guard.h"
#include "aarch64_flags.h"
struct module_entry {const char *path;u64 size;unsigned char hash[32];const char *gate;};
struct property_entry {const char *name;unsigned size;unsigned char data[64];};
struct binding_entry {const char *dt_path,*driver,*module,*class_path;const struct property_entry *properties;unsigned early;};
#include "module_bundle.h"
static long call6(long nr,long a,long b,long c,long d,long e,long f) {
    register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,
      x3 asm("x3")=d,x4 asm("x4")=e,x5 asm("x5")=f,x8 asm("x8")=nr;
    asm volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x5),"r"(x8):"memory");
    return x0;
}
#define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
static u64 length(const char *s){u64 n=0;while(s[n])n++;return n;}
static void text(const char *s){C3(64,1,s,length(s));}
static int equal(const char *a,const char *b){while(*a && *a==*b){a++;b++;}return *a==*b;}
static void number(long v) {
    char b[24];unsigned n=0;u64 u=v<0?-v:v;
    if(v<0)text("-");
    do {b[n++]='0'+u%10;u/=10;}while(u);
    while(n)C3(64,1,&b[--n],1);
}
static void finish(long code) __attribute__((noreturn));
static void finish(long code){C3(93,code,0,0);for(;;){}}
static void fail(const char *where,long error) __attribute__((noreturn));
static void fail(const char *where,long error) {
    text("ACE_MODULE_LOADER: FAIL ");text(where);text(" rc=");number(error);text("\n");finish(1);
}
static unsigned char buffer[65536]={1};
static long read_text(const char *path,int optional) {
    long fd=C3(56,-100,path,02000000);
    if(fd==-2 && optional)return 0;
    if(fd<0)fail(path,fd);
    u64 n=0;long r;
    while(n<sizeof(buffer)) {
        r=C3(63,fd,buffer+n,sizeof(buffer)-n);if(r<0)fail(path,r);
        if(!r)break;
        n+=r;
    }
    unsigned char extra;r=C3(63,fd,&extra,1);C3(57,fd,0,0);
    if(r)fail("identity text limit",r);
    return (long)n;
}
/* 0 absent, 1 all exact, -1 conflicting/malformed. Same authority rule as B. */
static int serial_text(const unsigned char *p,u64 n,int bootconfig) {
    const char key[]="androidboot.serialno";int found=0;
    for(u64 at=0;at<n;) {
        while(at<n && ace_slot_space(p[at]))at++;
        u64 end=at;while(end<n && (bootconfig?p[end]!='\n':!ace_slot_space(p[end])))end++;
        if(ace_slot_prefix(p+at,end-at,key,sizeof(key)-1)) {
            u64 value=at+sizeof(key)-1;
            if(value==end)return -1;
            if(p[value]=='=' || (bootconfig && ace_slot_space(p[value]))) {
                while(value<end && ace_slot_space(p[value]))value++;
                if(value==end || p[value++]!='=')return -1;
                while(value<end && ace_slot_space(p[value]))value++;
                while(end>value && ace_slot_space(p[end-1]))end--;
                if(end>value && p[value]=='"' && p[end-1]=='"'){value++;end--;}
                u64 size=length(expected_serial);
                if(end-value!=size || !ace_slot_prefix(p+value,end-value,expected_serial,size))return -1;
                found=1;
            }
        }
        /* Trimming a bootconfig value must not alter iteration's line end. */
        if(bootconfig){while(end<n && p[end]!='\n')end++;if(end<n)end++;}
        at=end;
    }
    return found;
}
static void ram_fs(const char *path,u64 type) {
    u64 s[32];long r=C3(43,path,s,0);
    if(r || (type?s[0]!=type:(s[0]!=0x858458f6 && s[0]!=0x01021994)))fail(path,r?r:-22);
}
static void guards(void) {
    if(C3(174,0,0,0) || C3(175,0,0,0) || C3(172,0,0,0)<=1)fail("root non-PID1",-1);
    ram_fs("/",0);ram_fs("/tmp",0x01021994);
    long fd=C3(56,-100,"/data",010000000|02000000);
    if(fd!=-2)fail("no data directory",fd<0?fd:-17);
    struct {char sysname[65],nodename[65],release[65],version[65],machine[65],domainname[65];} uts;
    long r=C3(160,&uts,0,0);
    if(r || !equal(uts.release,expected_release) || !equal(uts.machine,"aarch64"))fail("kernel identity",r?r:-22);
    long n=read_text("/proc/cmdline",0);
    int a=ace_slot_cmdline(buffer,(u64)n),sa=serial_text(buffer,(u64)n,0);
    n=read_text("/proc/bootconfig",1);
    int b=ace_slot_bootconfig(buffer,(u64)n),sb=serial_text(buffer,(u64)n,1);
    if(!ace_slot_states_valid(a,b))fail("B-slot identity",-22);
    if(sa<0 || sb<0 || !(sa==1 || sb==1))fail("serial identity",-22);
    /* Consumed even on preflight failure. No restart, unload, force or retries. */
    fd=call6(56,-100,(long)"/tmp/ace-ramdiag-modules.consumed",1|0100|0200|ACE_O_NOFOLLOW|ACE_O_CLOEXEC,0600,0,0);
    if(fd<0)fail("one-pass latch",fd);
    C3(57,fd,0,0);
    text("ACE_MODULE_LOADER: root/RAM/kernel/B/serial/one-pass verified\n");
}
static long checked_copy(const struct module_entry *m) {
    if(!m->size || m->size>2*1024*1024)fail("module size bound",-22);
    long input=C3(56,-100,m->path,ACE_O_NOFOLLOW|ACE_O_CLOEXEC);if(input<0)fail(m->path,input);
    long copy=C3(279,"ace-ramdiag-module",1|2,0);if(copy<0)fail("memfd",copy);
    struct ace_sha256 hash;ace_sha_init(&hash);u64 total=0;
    while(total<m->size) {
        u64 want=m->size-total;if(want>sizeof(buffer))want=sizeof(buffer);
        long n=C3(63,input,buffer,want);if(n<=0)fail("module short read",n);
        ace_sha_update(&hash,buffer,(u64)n);
        for(long at=0;at<n;) {long r=C3(64,copy,buffer+at,n-at);if(r<=0)fail("memfd copy",r);at+=r;}
        total+=n;
    }
    unsigned char extra;long r=C3(63,input,&extra,1);C3(57,input,0,0);
    if(r)fail("module trailing bytes",r);
    unsigned char digest[32];ace_sha_final(&hash,digest);unsigned difference=0;
    for(unsigned i=0;i<32;i++)difference|=digest[i]^m->hash[i];
    if(difference)fail("module SHA256",-22);
    r=C3(25,copy,1033,15);if(r)fail("memfd seals",r);
    r=C3(25,copy,1034,0);if(r!=15)fail("verify memfd seals",r);
    if(C3(62,copy,0,0))fail("memfd rewind",-1);
    return copy;
}
static void wait_gate(const char *path) {
    if(!path || !*path)return;
    text("ACE_MODULE_LOADER: waiting gate ");text(path);text("\n");
    struct {long sec,nsec;} now,start,delay={0,500000000};
    if(C3(113,1,&start,0))fail("monotonic clock",-1);
    for(unsigned polls=0;polls<64;polls++) {
        long fd=C3(56,-100,path,ACE_O_PATH|ACE_O_DIRECTORY|ACE_O_CLOEXEC);
        if(fd>=0) {
            u64 fs[32];long r=C3(44,fd,fs,0);C3(57,fd,0,0);
            if(r || fs[0]!=0x62656572)fail("gate must be sysfs",r?r:-22);
            text("ACE_MODULE_LOADER: gate verified ");text(path);text("\n");return;
        }
        if(fd!=-2)fail("gate open",fd);
        if(C3(113,1,&now,0))fail("monotonic clock",-1);
        if(now.sec-start.sec>=15)break;
        long r=C3(101,&delay,0,0);if(r && r!=-4)fail("gate wait",r);
    }
    fail("gate deadline",-110);
}
static void join(char out[512],const char *a,const char *b) {
    u64 n=0;while(*a){if(n>=511)fail("binding path bound",-36);out[n++]=*a++;}
    while(*b){if(n>=511)fail("binding path bound",-36);out[n++]=*b++;}out[n]=0;
}
static int suffix(const char *s,const char *tail) {
    u64 n=length(s),m=length(tail);return n>=m && equal(s+n-m,tail);
}
static long link_text(long fd,const char *path,char out[512]) {
    long n=call6(78,fd,(long)path,(long)out,511,0,0);
    if(n>=511)fail("binding link bound",n);
    if(n>=0)out[n]=0;
    else if(n!=-2)fail(path,n);
    return n;
}
/* Inspect real platform-device -> OF-node -> driver -> owning module links.
 * No driver bind/unbind, register I/O, device-node creation or persistent I/O. */
static int binding_present(const struct binding_entry *b) {
    const char base[]="/sys/bus/platform/devices/";
    long dir=C3(56,-100,base,ACE_O_DIRECTORY|ACE_O_CLOEXEC);if(dir<0)fail("platform devices",dir);
    u64 fs[32];long r=C3(44,dir,fs,0);if(r || fs[0]!=0x62656572)fail("platform must be sysfs",r?r:-22);
    char target[512],tail[512],relative[512],chosen[512];unsigned matches=0,entries=0;
    join(tail,"/firmware/devicetree/base",b->dt_path);
    unsigned char directory[4096];
    for(;;) {
        long size=C3(61,dir,directory,sizeof(directory));if(size<0)fail("platform getdents",size);if(!size)break;
        for(u64 at=0;at<(u64)size;) {
            if((u64)size-at<20)fail("platform dirent header",-22);
            unsigned record=directory[at+16]|((unsigned)directory[at+17]<<8);
            if(record<20 || record>(u64)size-at || ++entries>4096)fail("platform dirent bound",-22);
            char *name=(char *)directory+at+19;u64 n=0;
            while(n<record-19 && name[n])n++;
            if(n==record-19 || n>255)fail("platform name bound",-22);
            if(!equal(name,".") && !equal(name,"..")) {
                for(u64 i=0;i<n;i++)if(name[i]=='/')fail("platform name slash",-22);
                join(relative,name,"/of_node");
                if(link_text(dir,relative,target)>=0 && suffix(target,tail)) {
                    if(++matches>1)fail("ambiguous OF binding",-17);
                    join(chosen,base,name);
                }
            }
            at+=record;
        }
    }
    C3(57,dir,0,0);if(!matches)return 0;
    char path[512];join(path,chosen,"/driver");if(link_text(-100,path,target)<0)return 0;
    text("ACE_MODULE_LOADER: observed driver link ");text(target);text("\n");
    join(tail,"/",b->driver);if(!suffix(target,tail))fail("binding driver identity",-22);
    join(path,chosen,"/driver/module");long n=link_text(-100,path,target);
    text("ACE_MODULE_LOADER: observed module link ");text(n>=0?target:"builtin");text("\n");
    if(*b->module) {
        join(tail,"/module/",b->module);
        if(n<0 || !suffix(target,tail))fail("binding module identity",-22);
    } else if(n>=0)fail("expected builtin driver",-22);
    return 1;
}
static void verify_binding(const struct binding_entry *b) {
    text("ACE_MODULE_LOADER: checking OF binding ");text(b->dt_path);text("\n");
    struct {long sec,nsec;} start,now,delay={0,500000000};
    if(C3(113,1,&start,0))fail("binding clock",-1);
    for(unsigned polls=0;polls<64;polls++) {
        if(binding_present(b)) {
            char base[512],path[512];join(base,"/sys/firmware/devicetree/base",b->dt_path);
            for(unsigned i=0;b->properties[i].name;i++) {
                char tail[512];join(tail,"/",b->properties[i].name);join(path,base,tail);
                long n=read_text(path,0);const struct property_entry *p=&b->properties[i];
                if(n!=(long)p->size)fail("binding DT property size",-22);
                unsigned difference=0;for(unsigned j=0;j<p->size;j++)difference|=buffer[j]^p->data[j];
                if(difference)fail("binding DT property bytes",-22);
            }
            wait_gate(b->class_path);
            text("ACE_MODULE_LOADER: OF binding verified ");text(b->dt_path);text(" driver=");text(b->driver);
            text(" module=");text(*b->module?b->module:"builtin");text("\n");return;
        }
        if(C3(113,1,&now,0))fail("binding clock",-1);
        if(now.sec-start.sec>=15)break;
        long r=C3(101,&delay,0,0);if(r && r!=-4)fail("binding wait",r);
    }
    fail("OF binding deadline",-110);
}
static void receipt(const char *path) {
    long fd=call6(56,-100,(long)path,1|0100|0200|ACE_O_NOFOLLOW|ACE_O_CLOEXEC,0600,0,0);
    if(fd<0)fail(path,fd);
    long r=C3(64,fd,expected_bundle_id,64);if(r!=64)fail("receipt identity write",r);
    r=C3(64,fd,"\n",1);if(r!=1)fail("receipt newline",r);
    r=C3(57,fd,0,0);if(r)fail("receipt close",r);
}
void init_main(void) {
    guards();
    long copies[sizeof(modules)/sizeof(modules[0])];
    for(unsigned i=0;i<sizeof(modules)/sizeof(modules[0]);i++)copies[i]=checked_copy(&modules[i]);
    text("ACE_MODULE_LOADER: every module SHA256 verified and RAM copy sealed\n");
    for(unsigned i=0;i<sizeof(modules)/sizeof(modules[0]);i++) {
        wait_gate(modules[i].gate);
        text("ACE_MODULE_LOADER: inserting ");text(modules[i].path);text("\n");
        long r=C3(273,copies[i],"",0);C3(57,copies[i],0,0);
        if(r)fail("finit_module",r);
        text("ACE_MODULE_LOADER: inserted ");text(modules[i].path);text("\n");
        if(i+1==return_prefix_count) {
            for(unsigned j=0;bindings[j].dt_path;j++)if(bindings[j].early)verify_binding(&bindings[j]);
            receipt("/tmp/ace-ramdiag-return-checkpoint");
            text("ACE_MODULE_LOADER: return bindings checkpoint; firmware operation unproven\n");
        }
    }
    for(unsigned i=0;bindings[i].dt_path;i++)if(!bindings[i].early)verify_binding(&bindings[i]);
    receipt("/tmp/ace-ramdiag-modules-complete");
    text("ACE_MODULE_LOADER: complete insertion only; hardware readiness unproven\n");
    finish(0);
}
