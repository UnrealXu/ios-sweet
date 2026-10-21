/* QEMU-only PID1 verifies that Linux exposes the loader's real FDT record,
 * then runs the existing normal module load/unload and poweroff checks. */
#define init_main irq_module_main
#include "../ace-irq-timer/qemu-init.c"
#undef init_main
static long call5(long nr,long a,long b,long c,long d,long e) {
 register long x0 asm("x0")=a,x1 asm("x1")=b,x2 asm("x2")=c,
   x3 asm("x3")=d,x4 asm("x4")=e,x8 asm("x8")=nr;
 asm volatile("svc #0" : "+r"(x0) : "r"(x1),"r"(x2),"r"(x3),"r"(x4),"r"(x8) : "memory");
 return x0;
}
static u64 le64(const unsigned char *p) {
 u64 value=0;for(unsigned i=0;i<8;i++) value|=(u64)p[i]<<(8*i);return value;
}
void init_main(void) {
 long fd=call3(56,-100,(long)"/dev/console",2);
 if(fd>=0) {call3(24,fd,0,0);call3(24,fd,1,0);call3(24,fd,2,0);}
 call3(34,-100,(long)"/proc",0755);
 long mounted=call5(40,(long)"proc",(long)"/proc",(long)"proc",0,0);
 call3(34,-100,(long)"/sys",0755);
 long sysfs=call5(40,(long)"sysfs",(long)"/sys",(long)"sysfs",0,0);
 unsigned char data[512] __attribute__((aligned(8)));
 fd=call3(56,-100,(long)"/sys/firmware/devicetree/base/chosen/ace,native-refusal",0);
 long n=fd<0?fd:call3(63,fd,(long)data,sizeof(data));
 if(fd>=0) call3(57,fd,0,0);
 int ok=mounted==0 && sysfs==0 && n==288;
 const char *magic="ACEFALL1",*token=REFUSAL_TOKEN,*record="ACENAT01";
 if(n==288) {
  for(unsigned i=0;i<8;i++) if(data[i]!=magic[i] || data[32+i]!=record[i]) ok=0;
  for(unsigned i=0;i<17;i++) if(data[8+i]!=token[i]) ok=0;
  if(le64(data+40)!=1 || le64(data+48)!=EXPECT_STAGE ||
     (long)le64(data+56)!=-EXPECT_CODE) ok=0;
 }
 text(ok?"ACE_REFUSAL_QEMU: RECORD_PASS token=" : "ACE_REFUSAL_QEMU: RECORD_FAIL token=");
 text(REFUSAL_TOKEN);text("\n");
#if EXPECT_PMSG_SNAPSHOT
 /* Keep a file-backed data byte: this shipping Linux rejects the default
  * linker BSS-only PT_LOAD layout for this small standalone fixture. */
 static unsigned char snapshot[65537]={0xff};
 fd=call3(56,-100,(long)"/sys/firmware/devicetree/base/chosen/ace,pmsg-before-seed",0);
 unsigned total=0;
 n=fd;
 if(fd>=0) for(unsigned reads=0;reads<64 && total<sizeof(snapshot);reads++) {
  n=call3(63,fd,(long)(snapshot+total),sizeof(snapshot)-total);
  if(n<=0) break;
  total+=(unsigned)n;
 }
 if(fd>=0) call3(57,fd,0,0);
 int snapshot_ok=total==65536 && n==0;
 if(snapshot_ok) for(unsigned i=0;i<65536;i++)
  if(snapshot[i]!=(i==128?0x71:0)) snapshot_ok=0;
 text(snapshot_ok?"ACE_REFUSAL_QEMU: SNAPSHOT_PASS\n":"ACE_REFUSAL_QEMU: SNAPSHOT_FAIL\n");
#endif
 irq_module_main();
}
