/* SPDX-License-Identifier: MIT */
#include "native_config.h"
#include "../xnu_fdt.h"
#include "../xnu_platform.h"
#include "../pstore_ring.h"
#include "../pstore_seed.h"
#include "../pstore_trial.h"
extern const uint8_t _start[],image_end[],bundle_start[],bundle_end[];
#if NATIVE_PMSG_RESEED_CAPTURE && (!NATIVE_PMSG || !NATIVE_INIT_EMPTY_PMSG || !NATIVE_AUTO_READOUT || !NATIVE_REFUSAL_ANDROID || NATIVE_DIAGNOSTIC_READOUT)
#error "exact archived reseed requires the complete normal automatic diagnostic contract"
#endif
#if NATIVE_PMSG_RESEED_CAPTURE
extern const uint8_t pmsg_reseed_snapshot[],pmsg_reseed_snapshot_end[];
#endif
extern uint8_t stack_guard[];
extern void *memcpy(void *,const void *,size_t);
extern void native_jump(uint64_t,uint64_t) __attribute__((noreturn));
volatile uint64_t native_record[32];
static struct ace_fdt native_fdt;
static struct ace_xnu_fdt_policy native_policy;
static struct ace_xnu_cpu_state native_cpu;
static struct ace_xnu_plan native_plan;
#if NATIVE_PMSG && NATIVE_INIT_EMPTY_PMSG && !NATIVE_DIAGNOSTIC_READOUT
/* BSS belongs to this Image, never the pstore zone. Exported only for the
 * same-image Android refusal handoff after a failed, non-mutating seed. */
uint8_t native_pmsg_snapshot[65536];
uint32_t native_pmsg_snapshot_ready;
#endif

static int overlaps(uint64_t a,uint64_t n,uint64_t b,uint64_t m) {
    return n>UINT64_MAX-a || m>UINT64_MAX-b || (a<b+m && b<a+n);
}
/* The Image itself must already be bootloader-owned RAM to enter/clear BSS.
 * After parsing, also refuse any declared firmware/initrd alias before logs
 * or destination writes. Known deferred CMA pools are handled by fdt_policy. */
int native_image_exclusions(const struct ace_fdt *fdt) {
    uint64_t base=(uintptr_t)_start,size=(uintptr_t)image_end-base;
    for(uint32_t i=0;i<fdt->reserves;i++)
        if(overlaps(base,size,fdt->reserve[i].base,fdt->reserve[i].size)) return -62;
    int r=ace_fdt_find(fdt,"/reserved-memory");
    if(r<0) return -62;
    for(uint32_t i=1;i<fdt->nodes;i++) if(fdt->node[i].parent==(uint32_t)r) {
        uint32_t n=0;const uint8_t *p=ace_fdt_get(fdt,i,"reg",&n);
        if(!p) p=ace_fdt_get(fdt,i,"alloc-ranges",&n);
        if(!p) continue;
        if(n%16) return -62;
        for(uint32_t j=0;j<n;j+=16)
            if(overlaps(base,size,ace_fdt_be64(p+j),ace_fdt_be64(p+j+8))) return -62;
    }
    int chosen=ace_fdt_find(fdt,"/chosen");uint32_t a=0,b=0;
    if(chosen<0) return -62;
    const uint8_t *s=ace_fdt_get(fdt,chosen,"linux,initrd-start",&a);
    const uint8_t *e=ace_fdt_get(fdt,chosen,"linux,initrd-end",&b);
    if((s!=0)!=(e!=0) || (s && (a!=4 && a!=8)) || (e && (b!=4 && b!=8))) return -62;
    if(s && e) {
        uint64_t first=a==4?ace_fdt_be32(s):ace_fdt_be64(s);
        uint64_t last=b==4?ace_fdt_be32(e):ace_fdt_be64(e);
        if(last<first) return -62;
        if(overlaps(base,size,first,last-first)) return -62;
    }
    return 0;
}
static int log_bytes(const void *p,size_t n) {
#if NATIVE_PMSG
    if(overlaps((uintptr_t)_start,(uintptr_t)image_end-(uintptr_t)_start,0x48160000,0x10000) ||
       overlaps(NATIVE_RAM_BASE,NATIVE_RAM_BYTES,0x48160000,0x10000)) return -63;
    if(native_record[19]==(uint64_t)-9) {
        const volatile uint8_t *header=(const volatile uint8_t *)0x48160000;
        uint64_t first=0;for(unsigned i=0;i<8;i++) first|=(uint64_t)header[i]<<(8*i);
        native_record[23]=first;
    }
#if NATIVE_INIT_EMPTY_PMSG
    /* Called only after CPU/live-FDT/platform/whole-Image exclusions pass.
     * Ownership/ECC0/type0 are explicit caller contracts, not inferred from
     * a zero header. The seed operation checks EVERY byte before any store. */
#if NATIVE_PMSG_RESEED_CAPTURE
    int seed=ace_pstore_seed_from_snapshot((void *)0x48160000,0x10000,
        pmsg_reseed_snapshot,(size_t)((uintptr_t)pmsg_reseed_snapshot_end-(uintptr_t)pmsg_reseed_snapshot));
#else
    int seed=ace_pstore_seed_empty((void *)0x48160000,0x10000);
#endif
    if(seed) native_record[31]=(uint64_t)(int64_t)seed;
    if(seed<0) {
        /* Failed seed never stores to the zone. Preserve the remaining header
         * word and a full-zone nonzero count in the otherwise not-yet-used
         * branch flag. Only stage5/error-64 with seed<0 has this word25 ABI;
         * a successful branch still publishes word25=1 below. */
        const volatile uint8_t *zone=(const volatile uint8_t *)0x48160000;
        uint32_t tail=0,count=0;
        for(unsigned i=0;i<4;i++) tail|=(uint32_t)zone[8+i]<<(8*i);
        for(unsigned i=0;i<65536;i++) if(zone[i]) count++;
        native_record[25]=(uint64_t)tail<<32|count;
#if !NATIVE_DIAGNOSTIC_READOUT
        /* Separate freestanding copy unit keeps both addresses in registers;
         * GCC otherwise emits an absolute destination-minus-source literal. */
        memcpy(native_pmsg_snapshot,(const void *)zone,65536);
        __asm__ volatile("dsb sy":::"memory");
        native_pmsg_snapshot_ready=1;
#endif
        __asm__ volatile("dsb sy":::"memory");
        native_record[19]=(uint64_t)(int64_t)seed;return seed;
    }
#endif
#if NATIVE_PMSG_RESEED_CAPTURE && NATIVE_INIT_EMPTY_PMSG
    if(seed==ACE_PSTORE_SEED_ARCHIVED_MATCH) {
        static const char reseeded[]="ACENATIVE1 pmsg rebuilt from exact archived snapshot; seed=2\n";
        int note=ace_pstore_ring_append((void *)0x48160000,0x10000,reseeded,sizeof(reseeded)-1);
        if(note) {__asm__ volatile("dsb sy":::"memory");native_record[19]=(uint64_t)(int64_t)note;return note;}
    }
#endif
    int rc=ace_pstore_ring_append((void *)0x48160000,0x10000,p,n);
    __asm__ volatile("dsb sy":::"memory");native_record[19]=(uint64_t)(int64_t)rc;
    return rc;
#else
    (void)p;(void)n;return 0;
#endif
}
static int capture(void) {
    int rc=ace_xnu_cpu_capture(&native_cpu);if(rc) return rc;
    native_record[12]=native_cpu.current_el;native_record[13]=native_cpu.sctlr;
    native_record[14]=native_cpu.midr;native_record[15]=native_cpu.mpidr;
    native_record[16]=native_cpu.mmfr0;native_record[17]=native_cpu.cntfrq;native_record[18]=native_cpu.daif;
    return ace_xnu_cpu_check(&native_cpu);
}
static void fail(int rc) {native_record[3]=(uint64_t)(int64_t)rc;}
void native_main(uint64_t fdt_pa) {
    native_record[0]=0x313054414e454341ULL;native_record[1]=1;native_record[2]=1;
    native_record[4]=fdt_pa;native_record[5]=(uintptr_t)_start;native_record[6]=(uintptr_t)image_end;
    native_record[7]=(uintptr_t)bundle_start;native_record[8]=(uintptr_t)bundle_end;
    native_record[19]=(uint64_t)-9;
    for(unsigned i=0;i<64;i++) stack_guard[i]=0xa5;
    int rc=capture();if(rc) {fail(rc);return;}native_record[2]=2;
#if NATIVE_DIAGNOSTIC_READOUT
    /* Explicit evidence-collection image: never attempt XNU or touch pmsg.
     * The optional Android handoff exposes this deliberate -66 separately
     * from the previous trial's preserved firmware/pstore records. */
    fail(-66);return;
#endif
    if(fdt_pa!=NATIVE_FDT_PA) {fail(-61);return;}
    const uint8_t *dtb=(const uint8_t *)(uintptr_t)fdt_pa;
    uint32_t bytes=ace_fdt_be32(dtb+4);
    if(bytes<40 || bytes>ACE_FDT_BYTES) {fail(-61);return;}
    rc=ace_fdt_open(dtb,bytes,&native_fdt);if(rc) {fail(rc);return;}
    native_record[2]=3;native_record[29]=native_fdt.nodes;native_record[30]=native_fdt.props;
    struct ace_xnu_range image={(uintptr_t)_start,(uintptr_t)image_end-(uintptr_t)_start};
    struct ace_xnu_policy caller={{NATIVE_RAM_BASE,NATIVE_RAM_BYTES},
        {(uintptr_t)bundle_start,(uintptr_t)bundle_end-(uintptr_t)bundle_start},&image,1};
    /* This raw Image is entered via the reviewed pre-Linux firmware ABI,
     * never from Android. The phase parameter is a contract, not discovery. */
    rc=ace_xnu_fdt_policy(&native_fdt,fdt_pa,&caller,1,&native_policy);
    if(rc) {fail(rc);return;}
    rc=native_image_exclusions(&native_fdt);if(rc) {fail(rc);return;}native_record[2]=4;
    native_record[24]=native_policy.policy.reserved_count;
    native_record[26]=NATIVE_RAM_BASE;native_record[27]=NATIVE_RAM_BYTES;
    size_t payload=(size_t)((uintptr_t)bundle_end-(uintptr_t)bundle_start);
    rc=ace_xnu_prepare_platform(bundle_start,payload,&native_policy.policy,&native_cpu,&native_fdt,&native_plan);
    if(rc) {fail(rc);return;}native_record[2]=5;
    native_record[9]=native_plan.entry_pa;native_record[10]=native_plan.args_pa;
    native_record[11]=native_plan.adt_pa;native_record[28]=native_plan.count;
#if NATIVE_AUTO_READOUT
    /* CPU/FDT/platform/whole-Image exclusions have passed. Read before any
     * append can evict a prior marker. A new build token gets one XNU attempt;
     * a retained pending attempt returns normally through Android diagnostics.
     * Unknown headers still go through the existing explicit seed/refusal path.
     */
    rc=ace_pstore_trial_pending((const void *)0x48160000,65536,NATIVE_RUN_TOKEN);
    if(rc==1) {fail(-67);return;}
    if(rc<0 && rc!=ACE_PSTORE_RING_E_HEADER) {fail(-64);return;}
#endif
    static const char ready[]="ACENATIVE1 prepared actual XNU payload\n";
    rc=log_bytes(ready,sizeof(ready)-1);if(rc) {fail(-64);return;}
    rc=ace_xnu_materialize_platform(bundle_start,payload,&native_policy.policy,&native_cpu,&native_fdt,
        (void *)(uintptr_t)NATIVE_RAM_BASE,NATIVE_RAM_BYTES,&native_plan);
    if(rc) {fail(rc);return;}native_record[2]=6;
    rc=capture();if(rc) {fail(rc);return;}
    for(unsigned i=0;i<64;i++) if(stack_guard[i]!=0xa5) {fail(-65);return;}
    native_record[25]=1;native_record[2]=7;
    static const char branch[]="ACENATIVE1 branching actual XNU entry\n";
    rc=log_bytes(branch,sizeof(branch)-1);if(rc) {fail(-64);return;}
    rc=log_bytes((const void *)native_record,sizeof(native_record));if(rc) {fail(-64);return;}
#if NATIVE_AUTO_READOUT
    static const char armed[]="\nACETRIAL1:" NATIVE_RUN_TOKEN ": armed\n";
    rc=log_bytes(armed,sizeof(armed)-1);if(rc) {fail(-64);return;}
#endif
    native_jump(native_plan.entry_pa,native_plan.args_pa);
}
