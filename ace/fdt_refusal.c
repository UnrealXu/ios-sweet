/* SPDX-License-Identifier: MIT */
#include "fdt_refusal.h"
static int alias(const void *a,size_t n,const void *b,size_t m) {
    uintptr_t x=(uintptr_t)a,y=(uintptr_t)b;
    return n>UINTPTR_MAX-x || m>UINTPTR_MAX-y || (x<y+m && y<x+n);
}
static void copy(uint8_t *d,const uint8_t *s,size_t n) {
    for(size_t i=0;i<n;i++) d[i]=s[i];
}
static void be32(uint8_t *p,uint32_t n) {
    for(unsigned i=0;i<4;i++) p[i]=(uint8_t)(n>>(24-8*i));
}
int ace_fdt_copy_refusal_rescue(const struct ace_fdt *f,void *output,size_t capacity,
    const void *record,size_t record_bytes,const void *snapshot,size_t snapshot_bytes,const uint8_t *capability,uint64_t initrd_end,size_t *written) {
    static const char name[]=ACE_REFUSAL_PROPERTY;
    static const char snapshot_name[]=ACE_PMSG_SNAPSHOT_PROPERTY;
    static const char rescue_name[]="ace,ram-rescue";
    if(!f || !f->valid || !output || !record || !written ||
       ((uintptr_t)output&7) || capacity>ACE_FDT_BYTES ||
       (snapshot?(snapshot_bytes!=65536):(snapshot_bytes!=0)) ||
       record_bytes!=ACE_REFUSAL_BYTES || f->total<40 || f->total>ACE_FDT_BYTES)
        return -90;
    const uint8_t *b=f->blob;uint8_t *d=output;
    int chosen=ace_fdt_find(f,"/chosen");
    if(chosen<0) return -91;
    uint32_t unused;
    uint32_t end_bytes=0;const uint8_t *old_end=ace_fdt_get(f,chosen,"linux,initrd-end",&end_bytes);
    if(initrd_end) {
        uint32_t start_bytes=0;const uint8_t *start=ace_fdt_get(f,chosen,"linux,initrd-start",&start_bytes);
        if(!old_end || !start || (end_bytes!=4 && end_bytes!=8) || (start_bytes!=4 && start_bytes!=8) ||
           (end_bytes==4 && initrd_end>UINT32_MAX))return -90;
        uint64_t first=start_bytes==4?ace_fdt_be32(start):ace_fdt_be64(start);
        uint64_t last=end_bytes==4?ace_fdt_be32(old_end):ace_fdt_be64(old_end);
        if(initrd_end<=first || initrd_end>last)return -90;
    }
    if(ace_fdt_get(f,(uint32_t)chosen,name,&unused) ||
       (snapshot && ace_fdt_get(f,(uint32_t)chosen,snapshot_name,&unused)) ||
       (capability && ace_fdt_get(f,(uint32_t)chosen,rescue_name,&unused))) return -92;
    uint32_t ss=ace_fdt_be32(b+12),ns=ace_fdt_be32(b+32),nt=ace_fdt_be32(b+36);
    struct ace_fdt_node node=f->node[chosen];
    uint32_t insert=node.name;
    /* Parsed names are terminated/bounded and properties precede children. */
    while(b[insert]) insert++;
    insert=(insert+4)&~3u;
    if(node.count) {
        struct ace_fdt_prop last=f->prop[node.first+node.count-1];
        insert=(last.value+last.bytes+3)&~3u;
    }
    const uint32_t snapshot_prop=snapshot?12+65536:0;
    const uint32_t prop_bytes=12+ACE_REFUSAL_BYTES+snapshot_prop+(capability?36:0);
    const uint32_t name_bytes=sizeof(name)+(snapshot?sizeof(snapshot_name):0)+(capability?sizeof(rescue_name):0);
    size_t total=(size_t)f->total+prop_bytes+name_bytes;
    if((capability && (alias(output,total,capability,24) || alias(written,sizeof(*written),capability,24))) || total>capacity || total>ACE_FDT_BYTES || insert>ss ||
       alias(output,total,b,f->total) || alias(output,total,f,sizeof(*f)) ||
       alias(output,total,record,record_bytes) || alias(output,total,written,sizeof(*written)) ||
       alias(written,sizeof(*written),b,f->total) || alias(written,sizeof(*written),f,sizeof(*f)) ||
       alias(written,sizeof(*written),record,record_bytes) ||
       (snapshot && (alias(output,total,snapshot,snapshot_bytes) ||
                     alias(written,sizeof(*written),snapshot,snapshot_bytes)))) return -93;
    copy(d,b,insert);
    be32(d+insert,3);be32(d+insert+4,ACE_REFUSAL_BYTES);be32(d+insert+8,ns);
    copy(d+insert+12,record,record_bytes);
    if(snapshot) {
        uint32_t pos=insert+12+ACE_REFUSAL_BYTES;
        be32(d+pos,3);be32(d+pos+4,65536);be32(d+pos+8,ns+sizeof(name));
        copy(d+pos+12,snapshot,snapshot_bytes);
    }
    if(capability) {
        uint32_t pos=insert+12+ACE_REFUSAL_BYTES+snapshot_prop;
        be32(d+pos,3);be32(d+pos+4,24);be32(d+pos+8,ns+sizeof(name)+(snapshot?sizeof(snapshot_name):0));
        copy(d+pos+12,capability,24);
    }
    copy(d+insert+prop_bytes,b+insert,ss+ns-insert);
    copy(d+ss+prop_bytes+ns,(const uint8_t *)name,sizeof(name));
    if(snapshot) copy(d+ss+prop_bytes+ns+sizeof(name),(const uint8_t *)snapshot_name,sizeof(snapshot_name));
    if(capability) copy(d+ss+prop_bytes+ns+sizeof(name)+(snapshot?sizeof(snapshot_name):0),(const uint8_t *)rescue_name,sizeof(rescue_name));
    copy(d+ss+prop_bytes+ns+name_bytes,b+ss+ns,f->total-ss-ns);
    if(initrd_end) {
        size_t offset=(size_t)(old_end-b);if(offset>=insert)offset+=prop_bytes;
        for(unsigned i=0;i<end_bytes;i++)d[offset+i]=(uint8_t)(initrd_end>>(8*(end_bytes-1-i)));
    }
    be32(d+4,(uint32_t)total);be32(d+12,ss+prop_bytes);
    be32(d+32,ns+name_bytes);be32(d+36,nt+prop_bytes);
    *written=total;
    return 0;
}

int ace_fdt_copy_refusal(const struct ace_fdt *f,void *output,size_t capacity,
    const void *record,size_t record_bytes,size_t *written) {
    return ace_fdt_copy_refusal_snapshot(f,output,capacity,record,record_bytes,0,0,written);
}

int ace_fdt_copy_refusal_snapshot(const struct ace_fdt *f,void *output,size_t capacity,
    const void *record,size_t record_bytes,const void *snapshot,size_t snapshot_bytes,size_t *written) {
    return ace_fdt_copy_refusal_rescue(f,output,capacity,record,record_bytes,snapshot,snapshot_bytes,0,0,written);
}
