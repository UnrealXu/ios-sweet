/* SPDX-License-Identifier: MIT */
#include "xnu_handoff.h"
_Static_assert(sizeof(struct ace_xnu_boot_args)==736,"XNU8796 boot_args size");
_Static_assert(offsetof(struct ace_xnu_boot_args,video)==40,"video offset");
_Static_assert(offsetof(struct ace_xnu_boot_args,device_tree)==96,"ADT pointer offset");
_Static_assert(offsetof(struct ace_xnu_boot_args,command_line)==108,"cmdline offset");
_Static_assert(offsetof(struct ace_xnu_boot_args,boot_flags)==720,"flags offset");
static void copy_bytes(void *,const void *,uint64_t);
static void zero_bytes(void *,uint64_t);
static uint32_t le32(const uint8_t *p) {
    uint32_t n=0; for(unsigned i=0;i<4;i++) n|=(uint32_t)p[i]<<(8*i); return n;
}
static uint64_t le64(const uint8_t *p) {
    uint64_t n=0; for(unsigned i=0;i<8;i++) n|=(uint64_t)p[i]<<(8*i); return n;
}
static int end(struct ace_xnu_range r,uint64_t *e) {
    if(!r.size || r.size>UINT64_MAX-r.base) return 0;
    *e=r.base+r.size; return 1;
}
static int overlap(struct ace_xnu_range a,struct ace_xnu_range b) {
    uint64_t ae,be; return !end(a,&ae)||!end(b,&be)||(a.base<be && b.base<ae);
}
static int inside(uint64_t base,uint64_t size,uint64_t outer,uint64_t bytes) {
    return base>=outer && size<=bytes && base-outer<=bytes-size;
}
static int align_page(uint64_t n,uint64_t *o) {
    if(n>UINT64_MAX-(ACE_XNU_PAGE-1)) return 0;
    *o=(n+ACE_XNU_PAGE-1)&~(uint64_t)(ACE_XNU_PAGE-1);return 1;
}
int ace_xnu_prepare(const void *payload,size_t bytes,
                    const struct ace_xnu_policy *p,struct ace_xnu_plan *out) {
    if(!payload||!p||!out||(!p->reserved && p->reserved_count)||p->reserved_count>256)
        return ACE_XNU_ARGUMENT;
    if(bytes<ACE_XNU_HEADER) return ACE_XNU_FORMAT;
    const uint8_t *b=payload;
    const char magic[8]={'A','C','E','X','N','U','0','1'};
    for(unsigned i=0;i<8;i++) if(b[i]!=(uint8_t)magic[i]) return ACE_XNU_FORMAT;
    uint32_t count=le32(b+12);
    if(le32(b+8)!=1||!count||count>ACE_XNU_MAX_SEGS||
       bytes<ACE_XNU_HEADER+(size_t)count*32) return ACE_XNU_FORMAT;
    uint64_t limit,source_end;
    if(!end(p->ram,&limit)||!end(p->source,&source_end)||p->source.size!=bytes||
       (p->ram.base&(ACE_XNU_PAGE-1))||(p->ram.size&(ACE_XNU_PAGE-1))) return ACE_XNU_RANGE;
    if(overlap(p->ram,p->source)) return ACE_XNU_OVERLAP;
    for(size_t i=0;i<p->reserved_count;i++) {
        uint64_t unused;
        if(!end(p->reserved[i],&unused)) return ACE_XNU_RANGE;
        if(overlap(p->ram,p->reserved[i])) return ACE_XNU_OVERLAP;
    }
    struct ace_xnu_plan plan;zero_bytes(&plan,sizeof(plan));
    uint64_t va=le64(b+16),entry=le64(b+24),adt=le64(b+32),adt_size=le64(b+40);
    uint64_t kernel_end=le64(b+48),phys=le64(b+56),mem=le64(b+64);
    if(phys!=p->ram.base||mem!=p->ram.size||(va&(ACE_XNU_PAGE-1))||
       mem>UINT64_MAX-va||(entry&3)||!adt_size||adt_size>UINT32_MAX||
       (adt&7)||adt<ACE_XNU_HEADER+(uint64_t)count*32||!inside(adt,adt_size,0,bytes)||
       kernel_end<va||((kernel_end-va)&(ACE_XNU_PAGE-1))) return ACE_XNU_RANGE;
    int terminated=0;
    for(unsigned i=0;i<ACE_XNU_LINE;i++) {
        plan.args.command_line[i]=(char)b[72+i];
        if(!b[72+i]) terminated=1;
    }
    if(!terminated) return ACE_XNU_FORMAT;
    int entry_found=0;
    uint64_t highest=0;
    for(unsigned i=0;i<count;i++) {
        const uint8_t *s=b+ACE_XNU_HEADER+i*32;
        uint64_t v=le64(s),n=le64(s+8),off=le64(s+16),f=le64(s+24);
        if(!n||f>n||!inside(v,n,va,mem)||off<ACE_XNU_HEADER+(uint64_t)count*32||
           !inside(off,f,0,bytes)||(f && overlap((struct ace_xnu_range){off,f},(struct ace_xnu_range){adt,adt_size})))
            return ACE_XNU_RANGE;
        struct ace_xnu_segment *d=&plan.segments[i];
        d->destination=phys+(v-va);d->memory_bytes=n;d->file_offset=off;d->file_bytes=f;
        for(unsigned j=0;j<i;j++)
            if(overlap((struct ace_xnu_range){d->destination,n},
                       (struct ace_xnu_range){plan.segments[j].destination,plan.segments[j].memory_bytes}))
                return ACE_XNU_OVERLAP;
        /* Entry must have four actual instruction bytes, not BSS or a gap. */
        if(inside(entry,4,v,f)) entry_found=1;
        if(v+n>highest) highest=v+n;
    }
    if(!entry_found) return ACE_XNU_ENTRY;
    uint64_t rounded;
    if(!align_page(highest,&rounded)||kernel_end!=rounded||kernel_end-va>=mem)
        return ACE_XNU_RANGE;
    plan.adt_pa=phys+(kernel_end-va);
    if(!inside(plan.adt_pa,adt_size,phys,mem)||
       !align_page(plan.adt_pa+adt_size,&plan.args_pa)||
       !inside(plan.args_pa,ACE_XNU_PAGE,phys,mem)) return ACE_XNU_RANGE;
    plan.entry_pa=phys+(entry-va);plan.count=count;
    plan.adt_offset=adt;plan.adt_bytes=adt_size;
    plan.args.revision=2;plan.args.version=2;
    plan.args.virt_base=va;plan.args.phys_base=phys;plan.args.mem_size=mem;
    plan.args.mem_size_actual=mem;plan.args.top_of_kernel_data=plan.args_pa+ACE_XNU_PAGE;
    plan.args.device_tree=va+(plan.adt_pa-phys);plan.args.device_tree_length=(uint32_t)adt_size;
    copy_bytes(out,&plan,sizeof(plan));return ACE_XNU_OK;
}
static void copy_bytes(void *to,const void *from,uint64_t n) {
    volatile uint8_t *d=to;const volatile uint8_t *s=from;
    for(uint64_t i=0;i<n;i++) d[i]=s[i];
}
static void zero_bytes(void *to,uint64_t n) {
    volatile uint8_t *d=to;for(uint64_t i=0;i<n;i++) d[i]=0;
}
int ace_xnu_materialize(const void *payload,size_t bytes,const struct ace_xnu_policy *p,
                        void *mapping,size_t mapped,struct ace_xnu_plan *out) {
    if(!p||!mapping||!out||mapped<p->ram.size) return ACE_XNU_ARGUMENT;
    struct ace_xnu_plan plan;
    int rc=ace_xnu_prepare(payload,bytes,p,&plan);if(rc) return rc;
    /* Reject host/identity aliases, including output and policy metadata, before
     * any destination store. Physical source/loader exclusions are separate. */
    struct ace_xnu_range host={(uintptr_t)mapping,p->ram.size};
    if(overlap(host,(struct ace_xnu_range){(uintptr_t)payload,bytes})||
       overlap(host,(struct ace_xnu_range){(uintptr_t)out,sizeof(*out)})||
       overlap(host,(struct ace_xnu_range){(uintptr_t)p,sizeof(*p)})||
       (p->reserved_count && overlap(host,(struct ace_xnu_range){(uintptr_t)p->reserved,p->reserved_count*sizeof(*p->reserved)})))
        return ACE_XNU_OVERLAP;
    uint8_t *ram=mapping;
    for(unsigned i=0;i<plan.count;i++) {
        struct ace_xnu_segment *s=&plan.segments[i];
        uint8_t *d=ram+(s->destination-p->ram.base);
        copy_bytes(d,(const uint8_t *)payload+s->file_offset,s->file_bytes);
        zero_bytes(d+s->file_bytes,s->memory_bytes-s->file_bytes);
    }
    copy_bytes(ram+(plan.adt_pa-p->ram.base),(const uint8_t *)payload+plan.adt_offset,plan.adt_bytes);
    zero_bytes(ram+(plan.args_pa-p->ram.base),ACE_XNU_PAGE);
    copy_bytes(ram+(plan.args_pa-p->ram.base),&plan.args,sizeof(plan.args));
    copy_bytes(out,&plan,sizeof(plan));return ACE_XNU_OK;
}
