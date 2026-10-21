/* QEMU-only PID1. Normal pmsg driver write is a test fixture, not module code. */
static long call5(long nr, long a, long b, long c, long d, long e)
{
    register long x0 asm("x0")=a, x1 asm("x1")=b, x2 asm("x2")=c;
    register long x3 asm("x3")=d, x4 asm("x4")=e, x8 asm("x8")=nr;
    asm volatile("svc #0" : "+r"(x0) : "r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x8) : "memory");
    return x0;
}
#define C(n,a,b,c) call5(n,(long)(a),(long)(b),(long)(c),0,0)
static void text(const char *s)
{
    unsigned long n=0; while (s[n]) n++; C(64,1,s,n);
}
static void number(long v)
{
    char b[24]; unsigned long n=v<0 ? -(unsigned long)v : (unsigned long)v; int i=0;
    if(v<0)text("-");
    do {b[i++]='0'+n%10;n/=10;} while(n);
    while(i) {C(64,1,&b[--i],1);}
    text("\n");
}
static int load_unload(void)
{
    long fd=C(56,-100,"/ace_pmsg_header.ko",0);
    long ret=fd<0 ? fd : C(273,fd,"",0);
    if (fd>=0) C(57,fd,0,0);
    if (ret) {text("ACE_PMSG_QEMU: LOAD_FAIL\n");return -1;}
    text("ACE_PMSG_QEMU: LOAD_PASS\n");
    ret=C(106,"ace_pmsg_header",0,0);
    text(ret ? "ACE_PMSG_QEMU: UNLOAD_FAIL\n" : "ACE_PMSG_QEMU: UNLOAD_PASS\n");
    return ret ? -1 : 0;
}
void init_main(void)
{
    long fd=C(56,-100,"/dev/console",2);
    if (fd>=0) {C(24,fd,0,0); C(24,fd,1,0); C(24,fd,2,0);}
    text("ACE_PMSG_QEMU: PID1\n");
    int ok=C(172,0,0,0)==1 && !load_unload();
    long ret=call5(40,(long)"proc",(long)"/proc",(long)"proc",0,0);
    text("ACE_PMSG_QEMU: proc_mount_rc=");number(ret);
    char buf[4096]; long count=-1;
    if (!ret) {fd=C(56,-100,"/proc/devices",0); if(fd>=0) {count=C(63,fd,buf,sizeof(buf));C(57,fd,0,0);}}
    int major=-1;
    for (long i=0;i<count;) {
        int n=0,digits=0;
        while(i<count && buf[i]==' ')i++;
        while(i<count && buf[i]>='0' && buf[i]<='9') {n=n*10+buf[i++]-'0';digits++;}
        while(i<count && buf[i]==' ')i++;
        if(digits && i+5<=count && buf[i]=='p' && buf[i+1]=='m' && buf[i+2]=='s' && buf[i+3]=='g' && buf[i+4]=='\n')major=n;
        while(i<count && buf[i++]!='\n') {}
    }
    text("ACE_PMSG_QEMU: pmsg_major=");number(major);
    if(major<0 && count>0)C(64,1,buf,count);
    static const char payload[]="ACE_PMSG_QEMU_NORMAL_WRITE\n";
    ret=major>=0 && major<256 ? call5(33,-100,(long)"/dev/pmsg0",0020000|0600,major<<8,0) : -1;
    text("ACE_PMSG_QEMU: mknod_rc=");number(ret);
    if (ok && !ret) {
        fd=C(56,-100,"/dev/pmsg0",1);
        ret=fd<0 ? fd : C(64,fd,payload,sizeof(payload)-1);
        if(fd>=0)C(57,fd,0,0);
        text("ACE_PMSG_QEMU: pmsg_write_rc=");number(ret);
        if(ret==(long)sizeof(payload)-1) {text("ACE_PMSG_QEMU: NORMAL_PMSG_WRITE_PASS\n");ok=!load_unload();}
        else ok=0;
    } else ok=0;
    text(ok ? "ACE_PMSG_QEMU: ALL_PASS\n" : "ACE_PMSG_QEMU: FAILED\n");
    C(142,0xfee1dead,0x28121969,0x4321fedc);
    for(;;) {}
}
