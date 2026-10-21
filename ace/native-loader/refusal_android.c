/* SPDX-License-Identifier: MIT */
#include "native_config.h"
#if NATIVE_REFUSAL_ANDROID
#include "../fdt_refusal.h"
#include "../xnu_cpu.h"
#include "../pstore_ring.h"
#if NATIVE_RAM_RESCUE
#include "ram_rescue.h"
#include "../pstore_rescue.h"
static struct native_rescue_plan rescue_plan;
#endif
#if NATIVE_PMSG && NATIVE_AUTO_READOUT && !NATIVE_DIAGNOSTIC_READOUT
#include "../pstore_handoff.h"
#endif
extern volatile uint64_t native_record[32];
extern const uint8_t android_payload[],android_payload_end[];
extern int native_image_exclusions(const struct ace_fdt *);
extern void native_jump(uint64_t,uint64_t) __attribute__((noreturn));
/* Linux requires an 8-byte-aligned FDT within one 2MiB block. Keep it beyond
 * the whole immutable stock payload, outside Linux Image's own footprint. */
static uint8_t android_dtb[ACE_FDT_BYTES] __attribute__((aligned(0x200000)));
static struct ace_fdt fallback_fdt;
static struct ace_xnu_cpu_state fallback_cpu;
static uint8_t refusal[ACE_REFUSAL_BYTES];
#if NATIVE_PMSG && NATIVE_INIT_EMPTY_PMSG && !NATIVE_DIAGNOSTIC_READOUT
extern uint8_t native_pmsg_snapshot[65536];
extern uint32_t native_pmsg_snapshot_ready;
#endif
#if NATIVE_DIAGNOSTIC_READOUT
static void prior_pmsg(const struct ace_fdt *f) {
    if(native_record[2]!=2 || (int64_t)native_record[3]!=-66) return;
    native_record[23]=(uint64_t)-95;
    int parent=ace_fdt_find(f,"/reserved-memory"),found=0;
    if(parent<0) return;
    for(uint32_t i=0;i<f->nodes;i++) if(f->node[i].parent==(uint32_t)parent &&
        ace_fdt_compatible(f,i,"mediatek,pstore")) {
        uint32_t n=0;const uint8_t *p=ace_fdt_get(f,i,"reg",&n);
        if(p && n==16 && ace_fdt_be64(p)==0x48090000 && ace_fdt_be64(p+8)==0xe0000) found=1;
    }
    if(!found) return;
    const volatile uint8_t *zone=(const volatile uint8_t *)0x48160000;
    for(unsigned k=0;k<3;k++) {
        uint64_t value=0;for(unsigned j=0;j<4;j++) value|=(uint64_t)zone[4*k+j]<<(8*j);
        native_record[9+k]=value;
    }
    for(unsigned i=0;i<65536;i++) if(zone[i]) native_record[31]++;
    struct ace_pstore_ring_info ring;
    int rc=ace_pstore_ring_validate((const void *)0x48160000,65536,&ring);
    native_record[23]=(uint64_t)(int64_t)rc;native_record[25]=UINT64_MAX;
    static const char token[]=NATIVE_PRIOR_RUN_TOKEN;
    static const char marker[]="ACEXNU1:" NATIVE_PRIOR_RUN_TOKEN ": entry EL1\n";
    const unsigned len=sizeof(marker)-1;
    if(rc || sizeof(token)!=17 || ring.size<len) return;
    uint32_t start=ring.size==ring.capacity?ring.start:0;
    for(uint32_t i=0;i<=ring.size-len;i++) {
        unsigned j=0;
        for(;j<len;j++) if(zone[12+(start+i+j)%ring.capacity]!=(uint8_t)marker[j]) break;
        if(j!=len) continue;
        if(!native_record[24]) {
            native_record[25]=i;
            for(j=0;j<40;j++) ((volatile uint8_t *)&native_record[26])[j]=j<len?(uint8_t)marker[j]:0;
        }
        native_record[24]++;
    }
}
#endif

int native_refusal_android(uint64_t incoming) {
    int rc=-94;
    native_record[20]=(uint64_t)(int64_t)rc;
    if(native_record[2]<1 || native_record[2]>7 ||
       (int64_t)native_record[3]>=0 || (int64_t)native_record[3]<-127 ||
       incoming!=NATIVE_FDT_PA || ((uintptr_t)android_payload&0x1fffff)) return rc;
    if(ace_xnu_cpu_capture(&fallback_cpu) || fallback_cpu.current_el!=4 ||
       (fallback_cpu.sctlr&((1ULL<<25)|(1ULL<<12)|5)) ||
       (fallback_cpu.daif&0x3c0)!=0x3c0) return rc;
    const uint8_t *input=(const uint8_t *)(uintptr_t)incoming;
    uint32_t bytes=ace_fdt_be32(input+4);
    if(bytes<40 || bytes>ACE_FDT_BYTES || ace_fdt_open(input,bytes,&fallback_fdt)) return rc;
    /* Never turn a destination/firmware alias refusal into an Android write. */
    rc=native_image_exclusions(&fallback_fdt);
    if(rc) {native_record[20]=(uint64_t)(int64_t)rc;return rc;}
#if NATIVE_DIAGNOSTIC_READOUT
    prior_pmsg(&fallback_fdt);
#endif
    #if NATIVE_RAM_RESCUE
    if(native_record[2]!=5 || (int64_t)native_record[3]!=-67)return -110;
    rc=native_ram_rescue_prepare(&fallback_fdt,incoming,&rescue_plan);
    if(rc) {native_record[20]=(uint64_t)(int64_t)rc;native_ram_rescue_failure_trace(&fallback_fdt,'P',rc);return rc;}
    if(rescue_plan.state==ACE_RAM_RESCUE)native_record[31]=ACE_RAM_RESCUE_WORD;
#endif
    static const char marker[]="ACEFALL1";
    static const char token[]=NATIVE_RUN_TOKEN;
    for(unsigned i=0;i<8;i++) refusal[i]=(uint8_t)marker[i];
    for(unsigned i=0;i<17;i++) refusal[8+i]=(uint8_t)token[i];
    for(unsigned i=25;i<32;i++) refusal[i]=0;
    native_record[20]=0;native_record[21]=(uintptr_t)android_dtb;
    native_record[22]=(uintptr_t)android_payload;
    for(unsigned i=0;i<256;i++) refusal[32+i]=((const volatile uint8_t *)native_record)[i];
    size_t written=0;
    const void *snapshot=0;size_t snapshot_bytes=0;
#if NATIVE_PMSG && NATIVE_INIT_EMPTY_PMSG && !NATIVE_DIAGNOSTIC_READOUT
    if(native_pmsg_snapshot_ready==1 && native_record[2]==5 &&
       (int64_t)native_record[3]==-64 && (int64_t)native_record[31]==ACE_PSTORE_RING_E_HEADER) {
        snapshot=native_pmsg_snapshot;snapshot_bytes=sizeof(native_pmsg_snapshot);
    }
#endif
    #if NATIVE_RAM_RESCUE
    rc=ace_fdt_copy_refusal_rescue(&fallback_fdt,android_dtb,sizeof(android_dtb),
        refusal,sizeof(refusal),snapshot,snapshot_bytes,
        rescue_plan.state==ACE_RAM_FIRST?rescue_plan.capability:0,rescue_plan.new_end,&written);
#else
    rc=ace_fdt_copy_refusal_snapshot(&fallback_fdt,android_dtb,sizeof(android_dtb),
        refusal,sizeof(refusal),snapshot,snapshot_bytes,&written);
#endif
    if(rc) {native_record[20]=(uint64_t)(int64_t)rc;return rc;}
#if NATIVE_PMSG && NATIVE_AUTO_READOUT && !NATIVE_DIAGNOSTIC_READOUT
    /* Only the exact pending return already passed ownership/exclusion and
     * FDT-copy gates. Best effort: a tracing error must not prevent readout.
     * The record itself is not modified; diagnostic-only mode never writes. */
    if(native_record[2]==5 && (int64_t)native_record[3]==-67) {
#if NATIVE_RAM_RESCUE
        rc=native_ram_rescue_commit(&rescue_plan,refusal,sizeof(refusal));
        if(rc) {native_record[20]=(uint64_t)(int64_t)rc;native_ram_rescue_failure_trace(&fallback_fdt,'C',rc);return rc;}
        if(rescue_plan.state==ACE_RAM_FIRST) {
            rc=ace_pstore_android_handoff((void *)0x48160000,65536,NATIVE_RUN_TOKEN,refusal,sizeof(refusal));
            if(rc) {native_record[20]=(uint64_t)(int64_t)rc;return rc;}
        }
#else
        (void)ace_pstore_android_handoff((void *)0x48160000,65536,NATIVE_RUN_TOKEN,
                                        refusal,sizeof(refusal));
#endif
        __asm__ volatile("dsb sy":::"memory");
    }
#endif
    /* The kernel bytes were hash-pinned and header-checked before embedding.
     * No boot partition, FDT source, pstore header or kernel payload is edited. */
    native_jump((uintptr_t)android_payload,(uintptr_t)android_dtb);
}
#endif
