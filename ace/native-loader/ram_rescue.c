/* SPDX-License-Identifier: MIT */
#include "../initrd_rescue.h"
#include "../pstore_rescue.h"
#include "../pstore_trial.h"
#include "ram_rescue.h"
#include "native_config.h"
#if NATIVE_RAM_RESCUE
extern const uint8_t _start[],image_end[],ram_rescue_start[],ram_rescue_end[];
static struct ace_initrd_rescue_result result;
static uint64_t begun;
static struct ace_initrd_rescue_progress hash_progress;
static unsigned failure_trace_attempted;
static int same(const unsigned char *p,const char *s,unsigned n) {
    for(unsigned i=0;i<n;i++)if(p[i]!=(unsigned char)s[i])return 0;
    return 1;
}
/* Grant is an Image-local epoch: keep it across RESCUE commit consuming STOP,
 * never infer it on a fresh Image from a previous trace. */
static unsigned ce_attempted,ce_authorized;
extern int native_sha_ce_probe(uint64_t observed[2]);
int native_sha_ce_allowed(void) {return ce_authorized==1;}
static void native_sha_ce_authorize(int expected_state) {
    if(ce_attempted)return;
    ce_attempted=1;
    void *zone=(void *)0x48160000;const size_t bytes=65536;
    static const char token[]=NATIVE_RUN_TOKEN;
    if(expected_state!=ACE_RAM_FIRST && expected_state!=ACE_RAM_RESCUE)return;
    if(ace_pstore_trial_pending(zone,bytes,token)!=1 ||
       ace_pstore_ram_attempt(zone,bytes,token)!=expected_state)return;
    struct ace_pstore_ring_info ring;
    if(ace_pstore_ring_validate(zone,bytes,&ring) || ring.size>=ring.capacity || ring.start!=ring.size)return;
    char prefix[]="\nACECE1:0000000000000000: F ";
    for(unsigned i=0;i<16;i++)prefix[8+i]=token[i];
    prefix[26]=expected_state==ACE_RAM_FIRST?'F':'R';
    const uint8_t *data=(const uint8_t *)zone+12;
    for(size_t i=0;i<ring.size;i++) {
        size_t left=ring.size-i;
        if(sizeof(prefix)-1<=left && same(data+i,prefix,sizeof(prefix)-1))return;
        /* A truncated current-token prefix cannot grant a second attempt. */
        if(left>=25 && left<sizeof(prefix)-1 && same(data+i,prefix,25))return;
    }
    enum { line_bytes=(sizeof(prefix)-1)+(sizeof("before-first-SIMD")-1)+
                       2*((sizeof(" isar0=")-1)+16)+1 };
    if(line_bytes>=ring.capacity-ring.size)return; /* remain nonwrapped */
    /* Probe may itself trap under EL2/EL3. Existing exception ABI diagnoses it;
     * a successful trace is evidence of observation, never permission proof. */
    uint64_t observed[2];
    if(native_sha_ce_probe(observed))return;
    char line[128];unsigned n=0;
    for(unsigned i=0;i<sizeof(prefix)-1;i++)line[n++]=prefix[i];
    static const char phase[]="before-first-SIMD";
    for(unsigned i=0;i<sizeof(phase)-1;i++)line[n++]=phase[i];
    static const char hex[]="0123456789abcdef";
    static const char labels[2][9]={" isar0="," cpacr="};
    for(unsigned k=0;k<2;k++) {
        for(unsigned j=0;labels[k][j];j++)line[n++]=labels[k][j];
        for(unsigned j=0;j<16;j++)line[n++]=hex[(observed[k]>>(60-4*j))&15];
    }
    line[n++]='\n';
    if(n!=line_bytes || n>=ring.capacity-ring.size)return; /* never evict or repair */
    if(ace_pstore_ring_append(zone,bytes,line,n))return;
    __asm__ volatile("dsb sy":::"memory");
    /* Require the exact append result before enabling the Image-local gate. */
    struct ace_pstore_ring_info after;
    if(ace_pstore_ring_validate(zone,bytes,&after) || after.start!=ring.size+n || after.size!=ring.size+n)return;
    for(unsigned i=0;i<n;i++)if(data[ring.size+i]!=(uint8_t)line[i])return;
    unsigned sha2=(unsigned)((observed[0]>>12)&15);
    if(sha2==1 || sha2==2)ce_authorized=1;
}

void native_ram_rescue_failure_trace(const struct ace_fdt *f,char phase,int rc) {
    void *zone=(void *)0x48160000;const size_t bytes=65536;static const char token[]=NATIVE_RUN_TOKEN;
    /* Once per Image invocation even when refused; durable token prefix below
     * prevents another completed append after a subsequent warm reset. */
    if(failure_trace_attempted)return;
    failure_trace_attempted=1;
    if((phase!='P'&&phase!='C') || rc>=0 || rc< -127)return;
    if(ace_pstore_trial_pending(zone,bytes,token)!=1)return;
    int state=ace_pstore_ram_attempt(zone,bytes,token);
    if(state!=ACE_RAM_FIRST && state!=ACE_RAM_RESCUE)return;
    struct ace_pstore_ring_info r;
    if(ace_pstore_ring_validate(zone,bytes,&r) || r.size>=r.capacity || r.start!=r.size)return;
    const unsigned char *data=(const unsigned char *)zone+12;
    char armed[]="\nACETRIAL1:0000000000000000: armed\n";
    char prefix[]="\nACERAMERR1:0000000000000000:";
    for(unsigned i=0;i<16;i++){armed[11+i]=token[i];prefix[12+i]=token[i];}
    unsigned count=0;
    for(size_t i=0;i<r.size;i++) {
        if(sizeof(armed)-1<=r.size-i && same(data+i,armed,sizeof(armed)-1))count++;
        /* Any exact current-token error prefix, regardless of phase/rc, blocks
         * a further append. Opaque record coincidence refuses conservatively. */
        if(sizeof(prefix)-1<=r.size-i && same(data+i,prefix,sizeof(prefix)-1))return;
    }
    if(count!=1)return;
    char line[160];unsigned n=0;
    for(unsigned i=0;i<sizeof(prefix)-1;i++)line[n++]=prefix[i];
    line[n++]=' ';line[n++]=phase;line[n++]=' ';line[n++]='r';line[n++]='c';line[n++]='=';line[n++]='-';
    unsigned error=(unsigned)-rc;
    line[n++]='0'+error/100;line[n++]='0'+error/10%10;line[n++]='0'+error%10;
    uint64_t now;__asm__ volatile("mrs %0,cntpct_el0":"=r"(now));
    uint64_t values[3]={begun?now-begun:UINT64_MAX,UINT64_MAX,UINT64_MAX};
    if(f && f->valid) {
        int chosen=ace_fdt_find(f,"/chosen");
        static const char names[2][19]={"linux,initrd-start","linux,initrd-end"};
        if(chosen>=0)for(unsigned k=0;k<2;k++) {
            uint32_t size=0;const uint8_t *v=ace_fdt_get(f,chosen,names[k],&size);
            if(v && (size==4 || size==8))values[k+1]=size==4?ace_fdt_be32(v):ace_fdt_be64(v);
        }
    }
    static const char hex[]="0123456789abcdef";
    static const char labels[3][8]={" ticks="," start="," end="};
    for(unsigned k=0;k<3;k++) {
        for(unsigned j=0;labels[k][j];j++)line[n++]=labels[k][j];
        for(unsigned j=0;j<16;j++)line[n++]=hex[(values[k]>>(60-4*j))&15];
    }
    /* Progress is emitted only here, once on an owned failure ring. Each
     * count is completed hashed bytes, not unvalidated input or a digest pass. */
    static const char progress_labels[2][8]={" done="," total="};
    if(hash_progress.stream<=6 && hash_progress.completed<=hash_progress.total &&
       hash_progress.completed<=ACE_INITRD_RESCUE_MAX &&
       hash_progress.total<=ACE_INITRD_RESCUE_MAX) {
        line[n++]=' ';line[n++]='s';line[n++]='=';line[n++]='0'+hash_progress.stream;
        size_t counts[2]={hash_progress.completed,hash_progress.total};
        for(unsigned k=0;k<2;k++) {
            for(unsigned j=0;progress_labels[k][j];j++)line[n++]=progress_labels[k][j];
            for(unsigned j=0;j<8;j++)line[n++]=hex[(counts[k]>>(28-4*j))&15];
        }
    }
    line[n++]='\n';
    /* Never evict a prior token, native/refusal record or latch. A full/near
     * full ring yields no new trace. No pmsg seed or header repair exists. */
    if(n>r.capacity-r.size)return;
    (void)ace_pstore_ring_append(zone,bytes,line,n);
    __asm__ volatile("dsb sy":::"memory");
}

static int overlap(uint64_t a,uint64_t n,uint64_t b,uint64_t m) {
    return !n || !m || n>UINT64_MAX-a || m>UINT64_MAX-b || (a<b+m && b<a+n);
}
static int budget(void *unused) {
    (void)unused;uint64_t now;__asm__ volatile("mrs %0,cntpct_el0":"=r"(now));
    return now-begun<1560000000; /* 120s at measured13MHz; physical vendor26738688B/20.052s, two full hash passes need ~73s. */
}
/* Validate the actual firmware extent before reading one initrd byte. The
 * immutable FDT, whole Image (incl embedded rescue), XNU window, and every
 * concrete firmware reservation are excluded. LK releases temporary mb_ramdisk
 * before final FDT mblock emission; future alloc-ranges are candidate domains,
 * not instantiated reservations. Exact chosen start is pinned to LK allocation. */
static int extent(const struct ace_fdt *f,uint64_t fdt_pa,uint64_t *start,uint64_t *end) {
    int chosen=ace_fdt_find(f,"/chosen"),reserved=ace_fdt_find(f,"/reserved-memory");
    uint32_t a=0,b=0;const uint8_t *s=ace_fdt_get(f,chosen,"linux,initrd-start",&a);
    const uint8_t *e=ace_fdt_get(f,chosen,"linux,initrd-end",&b);
    if(chosen<0 || reserved<0 || !s || !e || (a!=4&&a!=8) || (b!=4&&b!=8))return -101;
    uint64_t first=a==4?ace_fdt_be32(s):ace_fdt_be64(s),last=b==4?ace_fdt_be32(e):ace_fdt_be64(e);
    if(first!=0x66f00000 || last<=first || last-first>ACE_INITRD_RESCUE_MAX || last>(1ULL<<40))return -102;
    uint64_t size=last-first;int bank=0;
    if(overlap(first,size,(uintptr_t)_start,(uintptr_t)image_end-(uintptr_t)_start) ||
       overlap(first,size,NATIVE_RAM_BASE,NATIVE_RAM_BYTES) || overlap(first,size,fdt_pa,f->total) ||
       overlap(first,size,(uintptr_t)f,sizeof(*f)))return -103;
    for(uint32_t i=0;i<f->reserves;i++)
        if(overlap(first,size,f->reserve[i].base,f->reserve[i].size))return -103;
    for(uint32_t i=1;i<f->nodes;i++) {
        uint32_t n=0;const uint8_t *p;
        p=ace_fdt_get(f,i,"device_type",&n);
        if(p && n==7 && p[0]=='m'&&p[1]=='e'&&p[2]=='m'&&p[3]=='o'&&p[4]=='r'&&p[5]=='y'&&!p[6]) {
            uint32_t st=0;const uint8_t *status=ace_fdt_get(f,i,"status",&st);
            if(status && !((st==5&&status[0]=='o'&&status[1]=='k'&&status[2]=='a'&&status[3]=='y'&&!status[4]) ||
                           (st==3&&status[0]=='o'&&status[1]=='k'&&!status[2])))continue;
            p=ace_fdt_get(f,i,"reg",&n);if(!p || !n || n%16)return -104;
            for(uint32_t j=0;j<n;j+=16) {
                uint64_t base=ace_fdt_be64(p+j),length=ace_fdt_be64(p+j+8);
                if(length>UINT64_MAX-base)return -104;
                if(first>=base && last<=base+length)bank=1;
            }
        }
        if(f->node[i].parent!=(uint32_t)reserved)continue;
        p=ace_fdt_get(f,i,"reg",&n);
        if(!p)continue; /* pre-Linux: alloc-ranges alone has not allocated a pool */
        if(!n || n%16)return -104;
        for(uint32_t j=0;j<n;j+=16)if(overlap(first,size,ace_fdt_be64(p+j),ace_fdt_be64(p+j+8)))return -103;
    }
    if(!bank)return -104;
    *start=first;*end=last;return 0;
}
int native_ram_rescue_prepare(const struct ace_fdt *f,uint64_t fdt_pa,struct native_rescue_plan *p) {
    uint64_t freq;__asm__ volatile("mrs %0,cntfrq_el0":"=r"(freq));if(freq!=13000000)return -105;
    __asm__ volatile("mrs %0,cntpct_el0":"=r"(begun));
    int state=ace_pstore_ram_attempt((void *)0x48160000,65536,NATIVE_RUN_TOKEN);
    if(state!=ACE_RAM_FIRST && state!=ACE_RAM_RESCUE)return -106;
    uint64_t start,end;int rc=extent(f,fdt_pa,&start,&end);if(rc)return rc;
    native_sha_ce_authorize(state);
    rc=ace_initrd_rescue_with_progress((void *)(uintptr_t)start,end-start,&native_rescue_policy,
        ram_rescue_start,ram_rescue_end-ram_rescue_start,&result,0,budget,0,&hash_progress);if(rc)return rc;
    p->start=start;p->end=end;p->new_end=state==ACE_RAM_RESCUE?start+result.new_bytes:end;p->state=state;
    static const char magic[]="ACERAMR1";static const char token[]=NATIVE_RUN_TOKEN;
    for(unsigned i=0;i<8;i++)p->capability[i]=(uint8_t)magic[i];
    for(unsigned i=0;i<16;i++)p->capability[8+i]=(uint8_t)token[i];
    return 0;
}
int native_ram_rescue_commit(const struct native_rescue_plan *p,const uint8_t *record,size_t bytes) {
    if(!budget(0))return -108;
    if(p->state==ACE_RAM_FIRST)return 0;
    /* All FDT/extent/pin dry-runs have passed. Consume first; never retry a
     * selected or partially mutated rescue. No reboot occurs in this helper. */
    int rc=ace_pstore_rescue_selected((void *)0x48160000,65536,NATIVE_RUN_TOKEN,record,bytes);
    __asm__ volatile("dsb sy":::"memory");if(rc)return rc;
    rc=ace_initrd_rescue_with_progress((void *)(uintptr_t)p->start,p->end-p->start,&native_rescue_policy,
        ram_rescue_start,ram_rescue_end-ram_rescue_start,&result,1,budget,0,&hash_progress);
    __asm__ volatile("dsb sy":::"memory");
    if(rc || p->start+result.new_bytes!=p->new_end)return rc?rc:-109;
    return 0;
}
#endif
