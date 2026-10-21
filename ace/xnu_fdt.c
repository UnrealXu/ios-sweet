/* SPDX-License-Identifier: MIT */
#include "xnu_fdt.h"
static int bytes_equal(const uint8_t *p,uint32_t n,const char *s) {
    if(!p) return 0;
    for(uint32_t i=0;i<n;i++) { if(p[i]!=(uint8_t)s[i]) return 0;if(!s[i]) return i+1==n; }
    return 0;
}
static int property(const struct ace_fdt *f,uint32_t id,const char *key,const char *s) {
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,id,key,&n);return bytes_equal(p,n,s);
}
static int cell(const struct ace_fdt *f,uint32_t id,const char *key,uint32_t v) {
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,id,key,&n);return p && n==4 && ace_fdt_be32(p)==v;
}
static int empty(const struct ace_fdt *f,uint32_t id,const char *key) {
    uint32_t n=1;return ace_fdt_get(f,id,key,&n) && n==0;
}
static int span(uint64_t b,uint64_t n) { return n && b<(1ULL<<40) && n<=(1ULL<<40)-b; }
static int inside(struct ace_xnu_range a,struct ace_xnu_range b) {
    return span(a.base,a.size) && span(b.base,b.size) &&
        a.base>=b.base && a.size<=b.size && a.base-b.base<=b.size-a.size;
}
static int overlap(struct ace_xnu_range a,struct ace_xnu_range b) {
    return a.base<b.base+b.size && b.base<a.base+a.size;
}
static int host_overlap(const void *a,size_t n,const void *b,size_t m) {
    uintptr_t x=(uintptr_t)a,y=(uintptr_t)b;
    return n>UINTPTR_MAX-x || m>UINTPTR_MAX-y || (x<y+m && y<x+n);
}
/* Return enabled1, disabled0, malformed-1; only exact standard strings. */
static int enabled(const struct ace_fdt *f,uint32_t id) {
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,id,"status",&n);
    if(!p || bytes_equal(p,n,"okay") || bytes_equal(p,n,"ok")) return 1;
    if(bytes_equal(p,n,"disabled")) return 0;
    return -1;
}
static int bank_contains(const struct ace_fdt *f,struct ace_xnu_range range) {
    for(uint32_t i=1;i<f->nodes;i++) if(property(f,i,"device_type","memory") && enabled(f,i)==1) {
        uint32_t n=0;const uint8_t *p=ace_fdt_get(f,i,"reg",&n);
        for(uint32_t j=0;p && j+16<=n;j+=16)
            if(inside(range,(struct ace_xnu_range){ace_fdt_be64(p+j),ace_fdt_be64(p+j+8)})) return 1;
    }
    return 0;
}
static int add(struct ace_xnu_fdt_policy *o,uint64_t base,uint64_t size) {
    if(!span(base,size) || o->policy.reserved_count==256) return ACE_XNU_FDT_RESERVE;
    struct ace_xnu_range r={base,size};
    if(overlap(r,o->policy.ram)) return ACE_XNU_FDT_OVERLAP;
    o->reserved[o->policy.reserved_count++]=r;return 0;
}
static int add_pairs(struct ace_xnu_fdt_policy *o,const uint8_t *p,uint32_t n) {
    if(!p || !n || n%16) return ACE_XNU_FDT_FORMAT;
    for(uint32_t i=0;i<n;i+=16) { int rc=add(o,ace_fdt_be64(p+i),ace_fdt_be64(p+i+8));if(rc) return rc; }
    return 0;
}
static int known_cma(const struct ace_fdt *f,uint32_t id) {
    const uint8_t *name=f->blob+f->node[id].name;
    uint64_t size,alignment;
    /* Names below only compare already validated bounded DTB strings. */
    uint32_t length=0;while(name[length]) length++;
    if(bytes_equal(name,length+1,"ssmr-reserved-cma_memory")) {size=0x6000000;alignment=0x1000000;}
    else if(bytes_equal(name,length+1,"ssheap-reserved-cma_memory")) {size=0x400000;alignment=0x200000;}
    else return 0;
    struct ace_fdt_node node=f->node[id];
    for(uint32_t i=0;i<node.count;i++) {
        struct ace_fdt_prop p=f->prop[node.first+i];
        uint32_t len=0;while(f->blob[p.name+len]) len++;
        /* Avoid linker-fixed pointer arrays in an otherwise PC-relative
         * native Image; these calls address string literals directly. */
        const uint8_t *key=f->blob+p.name;
        if(!bytes_equal(key,len+1,"compatible") && !bytes_equal(key,len+1,"reusable") &&
           !bytes_equal(key,len+1,"size") && !bytes_equal(key,len+1,"alignment") &&
           !bytes_equal(key,len+1,"phandle") && !bytes_equal(key,len+1,"linux,phandle") &&
           !bytes_equal(key,len+1,"status")) return -1;
    }
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,id,"size",&n);
    if(!p || n!=8 || ace_fdt_be64(p)!=size) return -1;
    p=ace_fdt_get(f,id,"alignment",&n);
    if(!p || n!=8 || ace_fdt_be64(p)!=alignment ||
       !property(f,id,"compatible","shared-dma-pool") || !empty(f,id,"reusable") || enabled(f,id)!=1) return -1;
    return 1;
}
int ace_xnu_fdt_policy(const struct ace_fdt *f,uint64_t fdt_pa,
    const struct ace_xnu_policy *p,unsigned native,struct ace_xnu_fdt_policy *out) {
    if(!f || !f->valid || !p || !out || native!=1 || p->reserved_count>128 ||
       (p->reserved_count && !p->reserved)) return ACE_XNU_FDT_ARGUMENT;
    if(host_overlap(out,sizeof(*out),f,sizeof(*f)) || host_overlap(out,sizeof(*out),f->blob,f->total) ||
       host_overlap(out,sizeof(*out),p,sizeof(*p)) ||
       (p->reserved_count && host_overlap(out,sizeof(*out),p->reserved,p->reserved_count*sizeof(*p->reserved))))
        return ACE_XNU_FDT_ARGUMENT;
    if(!ace_fdt_compatible(f,0,"mediatek,MT6895") || !cell(f,0,"#address-cells",2) ||
       !cell(f,0,"#size-cells",2)) return ACE_XNU_FDT_FORMAT;
    if(!span(p->ram.base,p->ram.size) || (p->ram.base&0x1ffffff) || (p->ram.size&0x1ffffff) ||
       !span(p->source.base,p->source.size) || (fdt_pa&7)) return ACE_XNU_FDT_MEMORY;
    unsigned banks=0;
    for(uint32_t i=1;i<f->nodes;i++) {
        const uint8_t *name=f->blob+f->node[i].name;
        int memory=property(f,i,"device_type","memory");
        /* Named memory nodes must not silently disappear from this policy. */
        if(name[0]=='m' && name[1]=='e' && name[2]=='m' && name[3]=='o' && name[4]=='r' && name[5]=='y' &&
           (name[6]=='@' || !name[6]) && !memory) return ACE_XNU_FDT_FORMAT;
        if(!memory) continue;
        if(f->node[i].parent!=0 || enabled(f,i)<0) return ACE_XNU_FDT_FORMAT;
        uint32_t n=0;const uint8_t *reg=ace_fdt_get(f,i,"reg",&n);
        if(!reg || !n || n%16) return ACE_XNU_FDT_FORMAT;
        for(uint32_t j=0;j<n;j+=16)
            if(!span(ace_fdt_be64(reg+j),ace_fdt_be64(reg+j+8))) return ACE_XNU_FDT_MEMORY;
        if(enabled(f,i)) banks++;
    }
    struct ace_xnu_range incoming={fdt_pa,f->total};
    if(!banks || !bank_contains(f,p->ram) || !bank_contains(f,p->source) || !bank_contains(f,incoming))
        return ACE_XNU_FDT_MEMORY;
    /* Temporary small plan; the large DTB index is always caller-owned. */
    struct ace_xnu_fdt_policy o;o.policy.ram=p->ram;o.policy.source=p->source;
    o.policy.reserved=0;o.policy.reserved_count=0;o.deferred_cma_nodes=0;
    int rc;
    for(uint32_t i=0;i<f->reserves;i++) if((rc=add(&o,f->reserve[i].base,f->reserve[i].size))) return rc;
    if((rc=add(&o,incoming.base,incoming.size)) || (rc=add(&o,p->source.base,p->source.size))) return rc;
    int chosen=ace_fdt_find(f,"/chosen"),reserved=ace_fdt_find(f,"/reserved-memory");
    if(chosen<0 || reserved<0 || !cell(f,reserved,"#address-cells",2) ||
       !cell(f,reserved,"#size-cells",2) || !empty(f,reserved,"ranges")) return ACE_XNU_FDT_FORMAT;
    uint32_t n=0,m=0;const uint8_t *s=ace_fdt_get(f,chosen,"linux,initrd-start",&n);
    const uint8_t *e=ace_fdt_get(f,chosen,"linux,initrd-end",&m);
    if(s || e) {
        if(!s || !e || (n!=4 && n!=8) || (m!=4 && m!=8)) return ACE_XNU_FDT_FORMAT;
        uint64_t start=n==4?ace_fdt_be32(s):ace_fdt_be64(s),end=m==4?ace_fdt_be32(e):ace_fdt_be64(e);
        if(end<=start || !bank_contains(f,(struct ace_xnu_range){start,end-start})) return ACE_XNU_FDT_MEMORY;
        if((rc=add(&o,start,end-start))) return rc;
    }
    int pstore=0;
    for(uint32_t i=1;i<f->nodes;i++) if(f->node[i].parent==(uint32_t)reserved) {
        if(f->node[i].children) return ACE_XNU_FDT_FORMAT;
        const uint8_t *reg=ace_fdt_get(f,i,"reg",&n);
        if(reg) {
            if((rc=add_pairs(&o,reg,n))) return rc;
            if(ace_fdt_compatible(f,i,"mediatek,pstore") && enabled(f,i)==1)
                for(uint32_t j=0;j<n;j+=16)
                    if(inside((struct ace_xnu_range){0x48160000,0x10000},
                       (struct ace_xnu_range){ace_fdt_be64(reg+j),ace_fdt_be64(reg+j+8)})) pstore=1;
        } else {
            int known=known_cma(f,i);if(known<0) return ACE_XNU_FDT_RESERVE;
            if(known) { o.deferred_cma_nodes++;continue; }
            const uint8_t *domains=ace_fdt_get(f,i,"alloc-ranges",&n);
            const uint8_t *size=ace_fdt_get(f,i,"size",&m);
            if(!domains || !n || n%16 || !size || m!=8 || !ace_fdt_be64(size)) return ACE_XNU_FDT_RESERVE;
            int fits=0;
            for(uint32_t j=0;j<n;j+=16) if(ace_fdt_be64(domains+j+8)>=ace_fdt_be64(size)) fits=1;
            if(!fits) return ACE_XNU_FDT_RESERVE;
            if((rc=add_pairs(&o,domains,n))) return rc;
        }
    }
    if(!pstore || o.deferred_cma_nodes!=2) return ACE_XNU_FDT_RESERVE;
    for(size_t i=0;i<p->reserved_count;i++) {
        if(!bank_contains(f,p->reserved[i])) return ACE_XNU_FDT_MEMORY;
        if((rc=add(&o,p->reserved[i].base,p->reserved[i].size))) return rc;
    }
    /* Byte loops avoid freestanding memcpy helpers and uninitialized padding. */
    uint8_t *dst=(uint8_t *)out;for(size_t i=0;i<sizeof(*out);i++) dst[i]=0;
    out->policy.ram=o.policy.ram;out->policy.source=o.policy.source;
    out->policy.reserved_count=o.policy.reserved_count;out->policy.reserved=out->reserved;
    for(size_t i=0;i<o.policy.reserved_count;i++) out->reserved[i]=o.reserved[i];
    out->deferred_cma_nodes=o.deferred_cma_nodes;return 0;
}
