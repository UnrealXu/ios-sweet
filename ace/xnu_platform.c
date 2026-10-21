/* SPDX-License-Identifier: MIT */
#include "xnu_platform.h"
static int match(const uint8_t *p,uint32_t n,const char *s) {
    if(!p) return 0;
    for(uint32_t i=0;i<n;i++) {if(p[i]!=(uint8_t)s[i]) return 0;if(!s[i]) return i+1==n;}
    return 0;
}
static int text(const struct ace_fdt *f,uint32_t id,const char *key,const char *s) {
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,id,key,&n);return match(p,n,s);
}
static int u32(const struct ace_fdt *f,uint32_t id,const char *key,uint32_t *out) {
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,id,key,&n);
    if(!p || n!=4) return 0;
    *out=ace_fdt_be32(p);return 1;
}
static int cell(const struct ace_fdt *f,uint32_t id,const char *key,uint32_t value) {
    uint32_t n;return u32(f,id,key,&n) && n==value;
}
static int active(const struct ace_fdt *f,uint32_t id) {
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,id,"status",&n);
    return !p || match(p,n,"okay") || match(p,n,"ok");
}
static int one(const struct ace_fdt *f,const char *compatible) {
    int result=-1;
    for(uint32_t i=0;i<f->nodes;i++) if(ace_fdt_compatible(f,i,compatible)) {
        if(result!=-1 || !active(f,i)) return -1;
        result=(int)i;
    }
    return result;
}
static int unique_handle(const struct ace_fdt *f,uint32_t id,uint32_t *handle) {
    uint32_t value;
    if(!u32(f,id,"phandle",&value) || !value || value==UINT32_MAX) return 0;
    for(uint32_t i=0;i<f->nodes;i++) {
        uint32_t a=0,b=0,na=0,nb=0;
        const uint8_t *pa=ace_fdt_get(f,i,"phandle",&na),*pb=ace_fdt_get(f,i,"linux,phandle",&nb);
        if((pa && na!=4) || (pb && nb!=4)) return 0;
        if(pa) a=ace_fdt_be32(pa);
        if(pb) b=ace_fdt_be32(pb);
        if((pa && pb && a!=b) || ((a==value || b==value) && i!=id)) return 0;
    }
    *handle=value;return 1;
}
static int named(const struct ace_fdt *f,uint32_t id,const char *name) {
    const uint8_t *p=f->blob+f->node[id].name;uint32_t n=0;while(p[n]) n++;
    return match(p,n+1,name);
}
static int partitions(const struct ace_fdt *f,uint32_t gic,const uint32_t *cpus) {
    if(!f->node[gic].children) return 1;
    if(f->node[gic].children!=1) return 0;
    int container=-1;
    for(uint32_t i=1;i<f->nodes;i++) if(f->node[i].parent==gic) container=(int)i;
    if(container<0 || !named(f,container,"ppi-partitions") || f->node[container].count || f->node[container].children!=2) return 0;
    uint32_t seen=0;
    for(uint32_t i=1;i<f->nodes;i++) if(f->node[i].parent==(uint32_t)container) {
        unsigned group=named(f,i,"interrupt-partition-0")?0:1;uint32_t handle,n=0;
        if((group && !named(f,i,"interrupt-partition-1")) || (seen&(1u<<group)) ||
           f->node[i].children || !unique_handle(f,i,&handle)) return 0;
        const uint8_t *affinity=ace_fdt_get(f,i,"affinity",&n);
        if(!affinity || n!=16) return 0;
        uint32_t cores=0;
        for(unsigned j=0;j<4;j++) {
            uint32_t value=ace_fdt_be32(affinity+4*j);unsigned core=0;
            while(core<8 && cpus[core]!=value) core++;
            if(core==8 || core/4!=group || (cores&(1u<<core))) return 0;
            cores|=1u<<core;
        }
        if(cores!=(group?0xf0u:0xfu)) return 0;
        struct ace_fdt_node node=f->node[i];
        for(uint32_t j=0;j<node.count;j++) {
            const uint8_t *key=f->blob+f->prop[node.first+j].name;uint32_t len=0;while(key[len]) len++;
            if(!match(key,len+1,"affinity") && !match(key,len+1,"phandle") && !match(key,len+1,"linux,phandle")) return 0;
        }
        seen|=1u<<group;
    }
    return seen==3;
}
static int hardware(const struct ace_fdt *f,uint32_t *cpu_clock) {
    if(!ace_fdt_compatible(f,0,"mediatek,MT6895") ||
       !cell(f,0,"#address-cells",2) || !cell(f,0,"#size-cells",2)) return ACE_XNU_PLATFORM_ARGUMENT;
    int cpus=ace_fdt_find(f,"/cpus");
    if(cpus<0 || !active(f,cpus) || !cell(f,cpus,"#address-cells",1) ||
       !cell(f,cpus,"#size-cells",0)) return ACE_XNU_PLATFORM_CPUS;
    uint32_t seen=0,handles[8];
    for(uint32_t i=0;i<f->nodes;i++) if(text(f,i,"device_type","cpu")) {
        uint32_t affinity,clock;
        if(f->node[i].parent!=(uint32_t)cpus || !active(f,i) ||
           !u32(f,i,"reg",&affinity) || (affinity&255) || affinity>0x700 ||
           !text(f,i,"enable-method","psci")) return ACE_XNU_PLATFORM_CPUS;
        unsigned core=affinity>>8;
        if((seen&(1u<<core)) || !ace_fdt_compatible(f,i,core<4?"arm,cortex-a55":"arm,cortex-a78") ||
           !unique_handle(f,i,&handles[core]))
            return ACE_XNU_PLATFORM_CPUS;
        seen|=1u<<core;
        if(!core) {
            if(!u32(f,i,"clock-frequency",&clock) || !clock) return ACE_XNU_PLATFORM_CPUS;
            *cpu_clock=clock;
        }
    }
    if(seen!=255) return ACE_XNU_PLATFORM_CPUS;
    int gic=one(f,"arm,gic-v3"),timer=one(f,"arm,armv8-timer"),psci=one(f,"arm,psci-1.0");
    uint32_t n=0,handle;
    if(gic<0 || f->node[gic].parent!=0 || !partitions(f,gic,handles) ||
       !cell(f,gic,"#interrupt-cells",4) || !unique_handle(f,gic,&handle))
        return ACE_XNU_PLATFORM_GIC;
    const uint8_t *flag=ace_fdt_get(f,gic,"interrupt-controller",&n);
    if(!flag || n) return ACE_XNU_PLATFORM_GIC;
    const uint8_t *reg=ace_fdt_get(f,gic,"reg",&n);
    const uint64_t expected[]={0xc000000,0x40000,0xc040000,0x200000};
    if(!reg || n!=32) return ACE_XNU_PLATFORM_GIC;
    for(unsigned i=0;i<4;i++) if(ace_fdt_be64(reg+8*i)!=expected[i]) return ACE_XNU_PLATFORM_GIC;
    if(timer<0 || f->node[timer].parent!=0 || !cell(f,timer,"clock-frequency",13000000))
        return ACE_XNU_PLATFORM_TIMER;
    uint32_t parent;
    const uint8_t *ip=ace_fdt_get(f,timer,"interrupt-parent",&n);
    if(ip) {if(n!=4) return ACE_XNU_PLATFORM_TIMER;parent=ace_fdt_be32(ip);}
    else if(!u32(f,0,"interrupt-parent",&parent)) return ACE_XNU_PLATFORM_TIMER;
    if(parent!=handle || ace_fdt_get(f,timer,"interrupts-extended",&n)) return ACE_XNU_PLATFORM_TIMER;
    const uint8_t *irqs=ace_fdt_get(f,timer,"interrupts",&n);
    const uint32_t wanted[]={1,13,4,0,1,14,4,0,1,11,4,0,1,10,4,0};
    if(!irqs || n!=64) return ACE_XNU_PLATFORM_TIMER;
    for(unsigned i=0;i<16;i++) if(ace_fdt_be32(irqs+4*i)!=wanted[i]) return ACE_XNU_PLATFORM_TIMER;
    if(psci<0 || f->node[psci].parent!=0 || !text(f,psci,"method","smc")) return ACE_XNU_PLATFORM_PSCI;
    return 0;
}

/* Opt-in probe profile. Fixed root-addressed MMIO, no bus translation or
 * interrupt/DMA enablement. An FDT declaration is not an ownership proof. */
static int ufs_hardware(const struct ace_fdt *f) {
    int ufs=one(f,"mediatek,mt8183-ufshci"),soc=ace_fdt_find(f,"/soc");
    int gic=one(f,"arm,gic-v3");uint32_t n=0,handle,parent=0;
    if(ufs<0 || soc<0 || gic<0 || f->node[soc].parent!=0 || !active(f,soc) ||
       ufs!=ace_fdt_find(f,"/soc/ufshci@112b0000") || f->node[ufs].parent!=(uint32_t)soc ||
       !cell(f,soc,"#address-cells",2) || !cell(f,soc,"#size-cells",2) ||
       !unique_handle(f,gic,&handle)) return ACE_XNU_PLATFORM_UFS;
    const uint8_t *ranges=ace_fdt_get(f,soc,"ranges",&n);
    if(!ranges || n) return ACE_XNU_PLATFORM_UFS;
    const uint8_t *reg=ace_fdt_get(f,ufs,"reg",&n);
    if(!reg || n!=16 || ace_fdt_be64(reg)!=0x112b0000 || ace_fdt_be64(reg+8)!=0x2300)
        return ACE_XNU_PLATFORM_UFS;
    if(ace_fdt_get(f,ufs,"interrupts-extended",&n)) return ACE_XNU_PLATFORM_UFS;
    const uint8_t *irq=ace_fdt_get(f,ufs,"interrupts",&n);
    if(!irq || n!=16 || ace_fdt_be32(irq)!=0 || ace_fdt_be32(irq+4)!=137 ||
       ace_fdt_be32(irq+8)!=4 || ace_fdt_be32(irq+12)!=0) return ACE_XNU_PLATFORM_UFS;
    for(uint32_t id=(uint32_t)ufs;;id=f->node[id].parent) {
        const uint8_t *ip=ace_fdt_get(f,id,"interrupt-parent",&n);
        if(ip) {if(n!=4) return ACE_XNU_PLATFORM_UFS;parent=ace_fdt_be32(ip);break;}
        if(id==0) break;
    }
    return parent==handle?0:ACE_XNU_PLATFORM_UFS;
}

/* Canonical initial ADT writer, not a parser of arbitrary Apple images.
 * Mirrors ace-mkadt's original9-node or opt-in10-node probe ABI.
 * Compare every byte except
 * opaque seed data, so duplicate/extra/placeholder/foreign device properties
 * cannot sneak through a permissive property lookup. */
struct writer { uint8_t b[4096];uint32_t used,seed;int failed; };
static void byte(struct writer *w,uint8_t b) {
    if(w->used>=sizeof(w->b)) {w->failed=1;return;}w->b[w->used++]=b;
}
static void le(struct writer *w,uint64_t n,unsigned count) {
    for(unsigned i=0;i<count;i++) byte(w,(uint8_t)(n>>(8*i)));
}
static unsigned length(const char *s) {unsigned n=0;while(s[n]) n++;return n;}
static void prop(struct writer *w,const char *name,const uint8_t *value,uint32_t n) {
    unsigned len=length(name);
    if(len>=32) {w->failed=1;return;}
    for(unsigned i=0;i<32;i++) byte(w,i<len?(uint8_t)name[i]:0);
    le(w,n,4);
    for(uint32_t i=0;i<n;i++) byte(w,value?value[i]:0);
    while(w->used&3) byte(w,0);
}
static void string(struct writer *w,const char *key,const char *s) {prop(w,key,(const uint8_t *)s,length(s)+1);}
static void number(struct writer *w,const char *key,uint64_t value,unsigned n) {
    uint8_t b[8];for(unsigned i=0;i<n;i++) b[i]=(uint8_t)(value>>(8*i));prop(w,key,b,n);
}
static void vector(struct writer *w,const char *key,const uint64_t *values,unsigned count) {
    uint8_t b[32];if(count>4) {w->failed=1;return;}
    for(unsigned i=0;i<count;i++) for(unsigned j=0;j<8;j++) b[i*8+j]=(uint8_t)(values[i]>>(8*j));
    prop(w,key,b,count*8);
}
static void node(struct writer *w,const char *name,uint32_t handle,unsigned properties,unsigned children) {
    le(w,properties+2,4);le(w,children,4);string(w,"name",name);number(w,"AAPL,phandle",handle,4);
}
static int adt_check(const uint8_t *adt,size_t bytes,struct ace_xnu_range ram,uint32_t clock,int ufs) {
    struct writer w;w.used=0;w.seed=0;w.failed=0;
    static const char root_compat[]="oneplus,ace-mt6895\0mediatek,MT6895\0AppleARM";
    static const char cpu_compat[]="ace,armv8-cpu\0arm,cortex-a55\0ARM,v8";
    static const char io_compat[]="ace-io\0arm-io";
    node(&w,"device-tree",ufs?10:9,7,ufs?5:4);
    prop(&w,"compatible",(const uint8_t *)root_compat,sizeof(root_compat));
    string(&w,"model","PGKM10");string(&w,"manufacturer","OnePlus");
    string(&w,"target-type","ACE");string(&w,"target-sub-type","PGKM10");
    number(&w,"#address-cells",2,4);number(&w,"#size-cells",2,4);
    node(&w,"chosen",6,3,2);number(&w,"dram-base",ram.base,8);number(&w,"dram-size",ram.size,8);
    w.seed=w.used+36;prop(&w,"random-seed",0,64);
    node(&w,"memory-map",4,0,0);node(&w,"ace-pmsg",5,4,0);
    string(&w,"compatible","ace,ramoops-pmsg-v1");
    const uint64_t pmsg[]={0x48160000,0x10000};vector(&w,"reg",pmsg,2);
    number(&w,"ecc-size",0,4);number(&w,"type-signature",0,4);
    node(&w,"defaults",7,0,0);node(&w,"cpus",8,2,1);
    number(&w,"#address-cells",1,4);number(&w,"#size-cells",0,4);
    node(&w,"cpu0",1,14,0);string(&w,"device_type","cpu");
    prop(&w,"compatible",(const uint8_t *)cpu_compat,sizeof(cpu_compat));
    /* Direct string references remain PC-relative in a relocated native
     * Image. A local pointer-array initializer emitted absolute data relocs. */
    number(&w,"reg",0,4);number(&w,"cpu-id",0,4);number(&w,"cluster-id",0,4);
    number(&w,"cluster-type",0,4);number(&w,"die-cluster-id",0,4);
    number(&w,"cluster-core-id",0,4);number(&w,"l2-cache-id",0,4);number(&w,"l3-cache-id",0,4);
    string(&w,"state","running");number(&w,"timebase-frequency",13000000,4);
    number(&w,"fixed-frequency",13000000,4);number(&w,"clock-frequency",clock,4);
    node(&w,"arm-io",3,5,1);string(&w,"device_type","ace-io");
    prop(&w,"compatible",(const uint8_t *)io_compat,sizeof(io_compat));
    number(&w,"#address-cells",2,4);number(&w,"#size-cells",2,4);
    const uint64_t ranges[]={0,0xc000000,0x240000};vector(&w,"ranges",ranges,3);
    node(&w,"gic",2,4,0);string(&w,"compatible","arm,gic-v3");prop(&w,"interrupt-controller",0,0);
    number(&w,"virtual-timer-intid",27,4);
    const uint64_t gic[]={0,0x40000,0x40000,0x200000};vector(&w,"reg",gic,4);
    if(ufs) {
        node(&w,"ace-ufs",9,ufs==3?5:4,0);string(&w,"compatible",ufs>=2?"ace,mt6895-ufs-read-v1":"ace,mt6895-ufs-hci-probe-v1");
        const uint64_t regs[]={0x112b0000,0x2300};vector(&w,"reg",regs,2);
        number(&w,"interrupt-intid",169,4);number(&w,ufs>=2?"ace,command-read-probe":"ace,read-only-probe",1,4);
        if(ufs==3) number(&w,"ace,root-read-probe",1,4);
    }
    if(w.failed || bytes!=w.used || !w.seed || w.seed+64>w.used) return ACE_XNU_PLATFORM_ADT;
    for(uint32_t i=0;i<w.used;i++) if((i<w.seed || i>=w.seed+64) && adt[i]!=w.b[i]) return ACE_XNU_PLATFORM_ADT;
    return 0;
}
int ace_xnu_platform_check(const struct ace_fdt *f,const void *adt,size_t bytes,struct ace_xnu_range ram) {
    if(!f || !f->valid || !adt || !bytes || !ram.size || ram.base>=(1ULL<<40) ||
       ram.size>(1ULL<<40)-ram.base || (ram.base&0x1ffffff) || (ram.size&0x1ffffff))
        return ACE_XNU_PLATFORM_ARGUMENT;
    uint32_t clock=0;int rc=hardware(f,&clock);if(rc) return rc;
    const uint8_t *a=adt;
    int ufs=bytes>=8 && a[4]==5 && !a[5] && !a[6] && !a[7];
    rc=adt_check(adt,bytes,ram,clock,ufs);
    if(rc && ufs) rc=adt_check(adt,bytes,ram,clock,2);
    if(rc && ufs) rc=adt_check(adt,bytes,ram,clock,3);
    if(rc) return rc;
    return ufs?ufs_hardware(f):0;
}
static int overlaps(const void *a,size_t n,const void *b,size_t m) {
    uintptr_t x=(uintptr_t)a,y=(uintptr_t)b;
    return n>UINTPTR_MAX-x || m>UINTPTR_MAX-y || (x<y+m && y<x+n);
}
static int output_alias(const struct ace_xnu_plan *out,const struct ace_fdt *f,
    const struct ace_xnu_cpu_state *s,const void *b,size_t n,const struct ace_xnu_policy *p) {
    return overlaps(out,sizeof(*out),f,sizeof(*f)) || overlaps(out,sizeof(*out),f->blob,f->total) ||
       overlaps(out,sizeof(*out),s,sizeof(*s)) || (b && overlaps(out,sizeof(*out),b,n)) ||
       overlaps(out,sizeof(*out),p,sizeof(*p)) || (p->reserved && p->reserved_count<=256 &&
       overlaps(out,sizeof(*out),p->reserved,p->reserved_count*sizeof(*p->reserved)));
}
int ace_xnu_prepare_platform(const void *b,size_t n,const struct ace_xnu_policy *p,
    const struct ace_xnu_cpu_state *s,const struct ace_fdt *f,struct ace_xnu_plan *out) {
    if(!f || !f->valid || !out || !s || !p || output_alias(out,f,s,b,n,p)) return ACE_XNU_PLATFORM_ARGUMENT;
    struct ace_xnu_plan plan;int rc=ace_xnu_prepare_cpu(b,n,p,s,&plan);if(rc) return rc;
    rc=ace_xnu_platform_check(f,(const uint8_t *)b+plan.adt_offset,plan.adt_bytes,p->ram);if(rc) return rc;
    uint8_t *to=(uint8_t *)out;const uint8_t *from=(const uint8_t *)&plan;
    for(size_t i=0;i<sizeof(plan);i++) to[i]=from[i];
    return 0;
}
int ace_xnu_materialize_platform(const void *b,size_t n,const struct ace_xnu_policy *p,
    const struct ace_xnu_cpu_state *s,const struct ace_fdt *f,void *mapping,size_t mapped,
    struct ace_xnu_plan *out) {
    if(!p || !f || !f->valid || !mapping || !out || !s ||
       overlaps(mapping,p->ram.size,f,sizeof(*f)) || overlaps(mapping,p->ram.size,f->blob,f->total) ||
       overlaps(mapping,p->ram.size,s,sizeof(*s)) || output_alias(out,f,s,b,n,p)) return ACE_XNU_PLATFORM_ARGUMENT;
    struct ace_xnu_plan plan;int rc=ace_xnu_prepare_platform(b,n,p,s,f,&plan);if(rc) return rc;
    return ace_xnu_materialize_cpu(b,n,p,s,mapping,mapped,out);
}
