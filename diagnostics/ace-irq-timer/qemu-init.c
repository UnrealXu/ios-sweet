/* QEMU-only init: loads the explicitly supplied diagnostic module, then unloads. */
typedef unsigned long u64;
static long call3(long nr, long a, long b, long c) {
 register long x0 asm("x0")=a, x1 asm("x1")=b, x2 asm("x2")=c, x8 asm("x8")=nr;
 asm volatile("svc #0" : "+r"(x0) : "r"(x1),"r"(x2),"r"(x8) : "memory");
 return x0;
}
static void text(const char *s) {u64 n=0; while(s[n]) n++; call3(64,1,(long)s,n);}
struct uts {char sysname[65], nodename[65], release[65], version[65], machine[65], domainname[65];};
void init_main(void) {
 long fd=call3(56,-100,(long)"/dev/console",2);
 if(fd>=0) {call3(24,fd,0,0);call3(24,fd,1,0);call3(24,fd,2,0);}
 text("ACE_STOCK_QEMU: static init entered\n");
 long pid=call3(172,0,0,0);
 text(pid==1 ? "ACE_STOCK_QEMU: PID1 verified\n" : "ACE_STOCK_QEMU: ERROR not PID1\n");
 struct uts u;
 if(call3(160,(long)&u,0,0)==0) {text("ACE_STOCK_QEMU: uname release=");text(u.release);text(" machine=");text(u.machine);text("\n");}
 struct {long sec,nsec;} t={1,0};
 long module_fd=call3(56,-100,(long)"/ace_irq_timer.ko",0);
 long load=module_fd < 0 ? module_fd : call3(273,module_fd,(long)"",0);
 text(load==0 ? "ACE_MODULE_QEMU: LOAD_PASS\n" : "ACE_MODULE_QEMU: LOAD_FAIL errno=");
 if(load!=0) {char n[24]; unsigned long v=-load; int len=0; do {n[len++]='0'+v%10;v/=10;}while(v);while(len)call3(64,1,(long)&n[--len],1);text("\n");}
 if(module_fd>=0)call3(57,module_fd,0,0);
 if(load==0) {long unload=call3(106,(long)"ace_irq_timer",0,0);text(unload==0 ? "ACE_MODULE_QEMU: UNLOAD_PASS\n" : "ACE_MODULE_QEMU: UNLOAD_FAIL\n");}
 text("ACE_MODULE_QEMU: requesting guest poweroff\n");
 call3(142,0xfee1dead,0x28121969,0x4321fedc);
 text("ACE_STOCK_QEMU: poweroff syscall returned; host timeout will stop guest\n");
 for(;;) call3(101,(long)&t,0,0);
}
