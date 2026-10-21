/* SPDX-License-Identifier: MIT */
/* Linux/AArch64 EL0 replay in process memory; no physical mapping, register
 * access, driver invocation, XNU load or reboot. Raw UAPI numbers were checked
 * against the exact live OEM asm-generic/unistd.h, not an Android libc ABI. */
#include "xnu_fdt.h"
#include "xnu_platform.h"
#if !defined(__aarch64__)
#error AArch64 Linux userspace only
#endif
static uint8_t blob[ACE_FDT_BYTES];
static uint8_t adt[4096];
static struct ace_fdt tree;
static struct ace_xnu_fdt_policy out;
static char json[512];
static size_t used;
static long call(long nr,long a,long b,long c,long d) {
    register long x0 __asm__("x0")=a;
    register long x1 __asm__("x1")=b;
    register long x2 __asm__("x2")=c;
    register long x3 __asm__("x3")=d;
    register long x8 __asm__("x8")=nr;
    __asm__ volatile("svc #0":"+r"(x0):"r"(x1),"r"(x2),"r"(x3),"r"(x8):"memory","cc");
    return x0;
}
static void text(const char *s) { while(*s && used<sizeof(json)) json[used++]=*s++; }
static void number(uint64_t n) {
    char digits[20];unsigned count=0;
    do { digits[count++]=(char)('0'+n%10);n/=10; } while(n);
    while(count && used<sizeof(json)) json[used++]=digits[--count];
}
static long load_file(uintptr_t path,uint8_t *buffer,size_t capacity) {
    long fd=call(56,-100,(long)path,0,0);if(fd<0) return -1;
    size_t bytes=0;
    while(bytes<capacity) {
        long n=call(63,fd,(long)(buffer+bytes),(long)(capacity-bytes),0);
        if(n<0) {call(57,fd,0,0,0);return -1;}
        if(!n) break;
        bytes+=(size_t)n;
    }
    uint8_t extra;long n=call(63,fd,(long)&extra,1,0);call(57,fd,0,0,0);
    return n==0?(long)bytes:-1;
}
int probe_main(const uintptr_t *initial_stack) {
    if(initial_stack[0]!=3) return 2;
    long bytes=load_file(initial_stack[2],blob,sizeof(blob));
    long adt_bytes=load_file(initial_stack[3],adt,sizeof(adt));
    if(bytes<0 || adt_bytes<=0) return 5;
    if(ace_fdt_open(blob,(size_t)bytes,&tree)) return 6;
    unsigned cpu=~0u;
    if(call(168,(long)&cpu,0,0,0)) return 7;
    long uid=call(174,0,0,0,0);if(uid!=2000 || cpu!=0) return 7;
    struct ace_xnu_range loader={0x40000000,0x4000000};
    struct ace_xnu_policy p={{0x140000000,0xc0000000},{0x42000000,0x1100000},&loader,1};
    volatile uint8_t *d=(volatile uint8_t *)&out;
    for(size_t i=0;i<sizeof(out);i++) d[i]=0xa5;
    /* Actual Android stage MUST refuse; no true pre-Linux claim is made. */
    int android_rc=ace_xnu_fdt_policy(&tree,0x47c80000,&p,0,&out);
    if(android_rc!=ACE_XNU_FDT_ARGUMENT) return 8;
    for(size_t i=0;i<sizeof(out);i++) if(d[i]!=0xa5) return 9;
    /* Replay the numeric pre-Linux policy ONLY in process memory. Physical
     * addresses are descriptions, never dereferenced or mapped. */
    int replay=ace_xnu_fdt_policy(&tree,0x47c80000,&p,1,&out);if(replay) return 10;
    if(ace_xnu_platform_check(&tree,adt,(size_t)adt_bytes,p.ram)) return 12;
    if(ace_xnu_platform_check(&tree,adt,(size_t)adt_bytes-1,p.ram)!=ACE_XNU_PLATFORM_ADT) return 13;
    adt[adt_bytes-1]^=1;
    int rejected=ace_xnu_platform_check(&tree,adt,(size_t)adt_bytes,p.ram);
    adt[adt_bytes-1]^=1;
    if(rejected!=ACE_XNU_PLATFORM_ADT) return 14;
    text("{\"uid\":");number((uint64_t)uid);text(",\"cpu\":");number(cpu);
    text(",\"dtb_bytes\":");number((uint64_t)bytes);text(",\"nodes\":");number(tree.nodes);
    text(",\"props\":");number(tree.props);text(",\"excluded_ranges\":");number(out.policy.reserved_count);
    text(",\"deferred_cma_nodes\":");number(out.deferred_cma_nodes);
    text(",\"android_stage_rc\":-32,\"policy_replay_rc\":0,\"platform_contract_rc\":0,\"truncated_adt_rc\":-45,\"corrupt_adt_rc\":-45,\"process_memory_only\":true,\"native_boot\":false}\n");
    size_t sent=0;
    while(sent<used) {
        long written=call(64,1,(long)(json+sent),(long)(used-sent),0);
        if(written<=0) return 11;
        sent+=(size_t)written;
    }
    return 0;
}
