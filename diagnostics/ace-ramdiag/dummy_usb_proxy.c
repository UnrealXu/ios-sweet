/* QEMU-only TCP framing bridge to real in-guest dummy_hcd USB bulk endpoints.
 * Never implements AUTH or shell responses; original stock adbd does that.
 * Requires synthetic serial AND dummy_hcd sysfs ancestry; no physical USB. */
typedef unsigned long u64;
typedef unsigned int u32;
#include "usb_descriptors.h"
#include "aarch64_flags.h"
static long call6(long nr,long a,long b,long c,long d,long e,long f) {
    register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,
      x3 asm("x3")=d,x4 asm("x4")=e,x5 asm("x5")=f,x8 asm("x8")=nr;
    asm volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x5),"r"(x8):"memory");return x0;
}
#define C3(n,a,b,c) call6(n,(long)(a),(long)(b),(long)(c),0,0,0)
static u64 length(const char *s){u64 n=0;while(s[n])n++;return n;}
static void text(const char *s){C3(64,1,s,length(s));}
static void number(long v){char b[24];unsigned n=0;u64 u=v<0?-v:v;if(v<0)text("-");do{b[n++]='0'+u%10;u/=10;}while(u);while(n)C3(64,1,&b[--n],1);}
static void done(long rc) __attribute__((noreturn));
static void done(long rc){C3(93,rc,0,0);for(;;){}}
static void fail(const char *s,long rc) __attribute__((noreturn));
static void fail(const char *s,long rc){text("ACE_USB_PROXY: FAIL ");text(s);text(" rc=");number(rc);text("\n");done(1);}
static int equal(const char *a,const char *b){while(*a && *a==*b){a++;b++;}return *a==*b;}
static int contains(const char *s,const char *part){for(;*s;s++){u64 n=0;while(part[n] && s[n] && part[n]==s[n])n++;if(!part[n])return 1;}return 0;}
static long read_file(const char *path,unsigned char *data,u64 size) {
    long fd=C3(56,-100,path,02000000);if(fd<0)fail(path,fd);
    u64 n=0;while(n<size){long r=C3(63,fd,data+n,size-n);if(r<0)fail(path,r);if(!r)break;n+=r;}
    unsigned char extra;long r=C3(63,fd,&extra,1);C3(57,fd,0,0);if(r)fail("file limit",r);return n;
}
static char device[128]={1};
static void attribute(const char *name,char value[512]) {
    char path[256];u64 n=0;for(u64 i=0;device[i];i++)path[n++]=device[i];path[n++]='/';
    for(u64 i=0;name[i];i++)path[n++]=name[i];
    path[n]=0;
    long size=read_file(path,(unsigned char *)value,511);
    while(size && (value[size-1]=='\n' || value[size-1]=='\r'))size--;
    value[size]=0;
}
static unsigned decimal(const char *p){unsigned n=0;if(!*p)fail("empty decimal",-22);for(;*p;p++){if(*p<'0'||*p>'9'||n>6553)fail("decimal",-22);n=n*10+*p-'0';}return n;}
static unsigned char data[4120]={1};
static u32 get32(const unsigned char *p){return (u32)p[0]|((u32)p[1]<<8)|((u32)p[2]<<16)|((u32)p[3]<<24);}
static unsigned header(void) {
    u32 command=get32(data),bytes=get32(data+12);
    if((command^get32(data+20))!=0xffffffffU || bytes>4096)fail("ADB frame header",-22);
    return bytes;
}
static void checksum(unsigned size){u32 sum=0;for(unsigned i=0;i<size;i++)sum+=data[24+i];if(sum!=get32(data+16))fail("ADB frame checksum",-22);}
static void frame_log(const char *direction,unsigned bytes) {
    char line[96],digits[16];unsigned at=0,n=0;
    const char prefix[]="ACE_USB_PROXY: ",label[]=" bytes=";
    for(unsigned i=0;i<sizeof(prefix)-1;i++)line[at++]=prefix[i];
    for(unsigned i=0;direction[i];i++)line[at++]=direction[i];
    line[at++]=' ';for(unsigned i=0;i<4;i++)line[at++]=data[i];
    for(unsigned i=0;i<sizeof(label)-1;i++)line[at++]=label[i];
    do{digits[n++]='0'+bytes%10;bytes/=10;}while(bytes);
    while(n)line[at++]=digits[--n];
    line[at++]='\n';C3(64,1,line,at);
}
static long bulk(long fd,unsigned ep,unsigned char *p,unsigned size,unsigned timeout) {
    struct {unsigned ep,len,timeout,pad;void *data;} transfer={ep,size,timeout,0,p};
    return C3(29,fd,0xc0185502,&transfer);
}
static int socket_read(long fd,unsigned char *p,unsigned n) {
    unsigned at=0;while(at<n){long r=C3(63,fd,p+at,n-at);if(!r)return 0;if(r<0)fail("socket read",r);at+=r;}return 1;
}
static int socket_write(long fd,const unsigned char *p,unsigned n) {
    unsigned at=0;while(at<n){long r=call6(206,fd,(long)(p+at),n-at,0x4000,0,0);if(r==-32 || r==-104)return 0;if(r<=0)fail("socket send",r);at+=r;}return 1;
}
static void network_to_usb(long socket,long usb,struct ace_usb_endpoints ep) {
    for(unsigned frames=0;frames<128;frames++) {
        if(!socket_read(socket,data,24))done(0);
        unsigned n=header();if(n && !socket_read(socket,data+24,n))fail("partial socket frame",-22);checksum(n);
        long r=bulk(usb,ep.out,data,24,10000);if(r!=24)fail("USB OUT header",r);
        if(n){r=bulk(usb,ep.out,data+24,n,10000);if(r!=(long)n)fail("USB OUT payload",r);}
        if(n && n%ep.packet==0){r=bulk(usb,ep.out,data,0,10000);if(r)fail("USB OUT ZLP",r);}
        frame_log("USB OUT",n);
    }
    fail("USB OUT frame bound",-22);
}
void init_main(void) {
    if(C3(174,0,0,0) || C3(172,0,0,0)<=1)fail("root nonPID1",-1);
    u64 fs[32];long r=C3(43,"/",fs,0);if(r || (fs[0]!=0x858458f6 && fs[0]!=0x01021994))fail("RAM root",r?r:-22);
    long n=read_file("/tmp/ace-usb-device",(unsigned char *)device,sizeof(device)-1);
    while(n && (device[n-1]=='\n' || device[n-1]=='\r'))n--;
    device[n]=0;
    const char prefix[]="/sys/bus/usb/devices/";
    for(unsigned i=0;i<sizeof(prefix)-1;i++)if(device[i]!=prefix[i])fail("USB sysfs path",-22);
    for(u64 i=sizeof(prefix)-1;device[i];i++)if((device[i]<'0'||device[i]>'9') && device[i]!='-' && device[i]!='.')fail("USB sysfs name",-22);
    char link[512];n=call6(78,-100,(long)device,(long)link,sizeof(link)-1,0,0);if(n<=0 || n>=(long)sizeof(link)-1)fail("USB ancestry",n);link[n]=0;
    if(!contains(link,"/dummy_hcd.0/"))fail("not dummy_hcd",-22);
    char value[512];attribute("serial",value);if(!equal(value,"RAMDIAG_QEMU_FIXTURE"))fail("synthetic serial",-22);
    attribute("idVendor",value);if(!equal(value,"18d1"))fail("USB vendor",-22);
    attribute("idProduct",value);if(!equal(value,"d001"))fail("USB product",-22);
    attribute("busnum",value);unsigned bus=decimal(value);attribute("devnum",value);unsigned dev=decimal(value);
    if(bus<1 || bus>255 || dev<1 || dev>127)fail("USB address bound",-22);
    char descriptor_path[256];u64 at=0;for(;device[at];at++)descriptor_path[at]=device[at];
    const char suffix[]="/descriptors";for(unsigned i=0;i<sizeof(suffix);i++)descriptor_path[at+i]=suffix[i];
    n=read_file(descriptor_path,data,sizeof(data));struct ace_usb_endpoints ep;
    if(!ace_usb_descriptors(data,n,&ep))fail("single ADB descriptors",-22);
    char node[]="/dev/bus/usb/000/000";
    for(unsigned i=0,power=100;i<3;i++,power/=10){node[13+i]='0'+(bus/power)%10;node[17+i]='0'+(dev/power)%10;}
    /* ueventd creates this device. Never synthesize or reset USB device nodes. */
    long usb=C3(56,-100,node,2|ACE_O_NOFOLLOW|ACE_O_CLOEXEC);if(usb<0)fail("identity USB node",usb);
    u64 status[32];r=C3(80,usb,status,0);unsigned minor=(bus-1)*128+dev-1;
    u64 encoded=(minor&255)|((u64)189<<8)|((u64)(minor&~255U)<<12);
    if(r || (((u32 *)status)[4]&0170000)!=0020000 || status[4]!=encoded)fail("USB char device identity",r?r:-22);
    struct {unsigned devnum;unsigned char slow,pad[3];} info;
    r=C3(29,usb,0x40085511,&info);if(r || info.devnum!=dev)fail("USB connect identity",r?r:-22);
    unsigned interface=0;r=C3(29,usb,0x8004550f,&interface);if(r)fail("claim ADB interface",r);
    text("ACE_USB_PROXY: claimed synthetic identity and ADB bulk endpoints\n");
    long listener=C3(198,2,1|02000000,0);if(listener<0)fail("socket",listener);
    unsigned yes=1;r=call6(208,listener,1,2,(long)&yes,sizeof(yes),0);if(r)fail("reuseaddr",r);
    struct {long sec,usec;} timeout={25,0};
    r=call6(208,listener,1,20,(long)&timeout,sizeof(timeout),0);if(r)fail("socket timeout",r);
    struct {unsigned short family,port;unsigned char address[4],zero[8];} addr={2,0xb315,{0,0,0,0},{0}};
    r=C3(200,listener,&addr,sizeof(addr));if(r)fail("bind proxy",r);
    r=C3(201,listener,2,0);if(r)fail("listen",r);
    text("ACE_USB_PROXY: ready two-session USB-only bridge\n");
    for(unsigned session=0;session<2;session++) {
        long socket=call6(242,listener,0,0,02000000,0,0);if(socket<0)fail("accept",socket);
        long child=call6(220,17,0,0,0,0,0);if(child<0)fail("clone",child);
        if(child==0){C3(57,listener,0,0);network_to_usb(socket,usb,ep);}
        int child_status=0;unsigned idle=0,allow_zlp=0,frames=0;
        for(;;) {
            r=bulk(usb,ep.in,data,24,1000);
            if(r==0 && allow_zlp){allow_zlp=0;text("ACE_USB_PROXY: consumed expected USB IN ZLP\n");continue;}
            if(r==-110) {
                long waited=call6(260,child,(long)&child_status,1,0,0,0);
                if(waited==child){child=0;break;}
                if(waited<0)fail("child observation",waited);
                if(++idle>=25)fail("USB idle deadline",-110);
                continue;
            }
            if(r!=24)fail("USB IN header",r);
            idle=0;allow_zlp=0;
            if(++frames>128)fail("USB IN frame bound",-22);
            unsigned bytes=header();if(bytes){r=bulk(usb,ep.in,data+24,bytes,10000);if(r!=(long)bytes)fail("USB IN payload",r);}checksum(bytes);
            allow_zlp=bytes && bytes%ep.packet==0;frame_log("USB IN",bytes);
            if(!socket_write(socket,data,24+bytes))break;
        }
        C3(210,socket,2,0);C3(57,socket,0,0);
        if(child){C3(129,child,15,0);call6(260,child,(long)&child_status,0,0,0,0);}
        text("ACE_USB_PROXY: session closed, USB identity retained\n");
    }
    C3(29,usb,0x80045510,&interface);C3(57,usb,0,0);C3(57,listener,0,0);done(0);
}
