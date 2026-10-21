/* SPDX-License-Identifier: MIT */
#include "fdt.h"
uint32_t ace_fdt_be32(const uint8_t *p) {
    uint32_t n=0;for(unsigned i=0;i<4;i++) n=(n<<8)|p[i];return n;
}
uint64_t ace_fdt_be64(const uint8_t *p) {
    return ((uint64_t)ace_fdt_be32(p)<<32)|ace_fdt_be32(p+4);
}
static int equal(const uint8_t *a,const uint8_t *b) {
    for(unsigned i=0;i<=127;i++) { if(a[i]!=b[i]) return 0;if(!a[i]) return 1; }
    return 0;
}
static int name_end(const uint8_t *b,uint32_t p,uint32_t end,uint32_t *out) {
    for(unsigned n=0;p<end && n<=127;n++,p++) {
        if(!b[p]) { *out=p;return 1; }
        if(b[p]<33 || b[p]>126 || b[p]=='/') return 0;
    }
    return 0;
}
int ace_fdt_open(const void *blob,size_t bytes,struct ace_fdt *f) {
    if(!blob || !f || bytes<40 || bytes>ACE_FDT_BYTES) return -1;
    uintptr_t a=(uintptr_t)blob,w=(uintptr_t)f;
    if(bytes>UINTPTR_MAX-a || sizeof(*f)>UINTPTR_MAX-w ||
       (a<w+sizeof(*f) && w<a+bytes)) return -1;
    f->valid=0;f->blob=blob;f->nodes=0;f->props=0;f->reserves=0;
    const uint8_t *b=blob;
    uint32_t total=ace_fdt_be32(b+4),st=ace_fdt_be32(b+8),ss=ace_fdt_be32(b+12);
    uint32_t rv=ace_fdt_be32(b+16),ns=ace_fdt_be32(b+32),nt=ace_fdt_be32(b+36);
    if(ace_fdt_be32(b)!=0xd00dfeed || total<40 || total>bytes ||
       ace_fdt_be32(b+20)!=17 || ace_fdt_be32(b+24)>17 ||
       rv<40 || (rv&7) || (st&3) || nt<12 || (nt&3) ||
       rv>st || st-rv<16 || st>ss || nt>ss-st || ss>total || ns>total-ss)
        return -1;
    f->total=total;
    int terminated=0;
    for(uint32_t p=rv;p<=st-16;p+=16) {
        uint64_t base=ace_fdt_be64(b+p),size=ace_fdt_be64(b+p+8);
        if(!base && !size) { terminated=1;break; }
        if(!size || size>UINT64_MAX-base || f->reserves==ACE_FDT_RESERVES) return -1;
        for(uint32_t i=0;i<f->reserves;i++) {
            struct ace_fdt_reserve r=f->reserve[i];
            if(base<r.base+r.size && r.base<base+size) return -1;
        }
        f->reserve[f->reserves++]=(struct ace_fdt_reserve){base,size};
    }
    if(!terminated) return -1;
    uint32_t stack[ACE_FDT_DEPTH],depth=0,p=st,end=st+nt;
    while(p<=end-4) {
        uint32_t token=ace_fdt_be32(b+p);p+=4;
        if(token==1) {
            uint32_t z;
            if(f->nodes==ACE_FDT_NODES || depth==ACE_FDT_DEPTH ||
               !name_end(b,p,end,&z) || (!depth && (f->nodes || z!=p)) ||
               (depth && z==p)) return -1;
            uint32_t parent=depth?stack[depth-1]:UINT32_MAX;
            for(uint32_t i=0;i<f->nodes;i++)
                if(f->node[i].parent==parent && equal(b+f->node[i].name,b+p)) return -1;
            uint32_t next=(z+4)&~3u;
            /* OEM live DTB has nonzero padding. As in libfdt, skip these
             * alignment bytes without interpreting them as payload/tokens. */
            if(next>end) return -1;
            uint32_t index=f->nodes++;
            f->node[index]=(struct ace_fdt_node){p,parent,f->props,0,0};
            if(depth) f->node[parent].children++;
            stack[depth++]=index;p=next;
        } else if(token==2) {
            if(!depth) return -1;
            depth--;
        } else if(token==3) {
            if(!depth || p>end || end-p<8 || f->props==ACE_FDT_PROPS) return -1;
            struct ace_fdt_node *node=&f->node[stack[depth-1]];
            uint32_t len=ace_fdt_be32(b+p),off=ace_fdt_be32(b+p+4),z;
            p+=8;
            if(node->children || off>=ns || len>end-p ||
               !name_end(b,ss+off,ss+ns,&z) || z==ss+off) return -1;
            uint32_t next=(p+len+3)&~3u;
            if(next>end) return -1;
            for(uint32_t i=0;i<node->count;i++)
                if(equal(b+f->prop[node->first+i].name,b+ss+off)) return -1;
            f->prop[f->props++]=(struct ace_fdt_prop){ss+off,p,len};
            node->count++;p=next;
        } else if(token==4) {
            continue;
        } else if(token==9) {
            if(depth || !f->nodes || p!=end) return -1;
            f->valid=1;return 0;
        } else return -1;
    }
    return -1;
}
int ace_fdt_find(const struct ace_fdt *f,const char *path) {
    if(!f || !f->valid || !path || *path!='/') return -1;
    uint32_t parent=0;path++;
    if(!*path) return 0;
    unsigned consumed=0;
    while(*path) {
        char part[128];unsigned n=0;
        while(*path && *path!='/') {
            if(n==127 || ++consumed>1024) return -1;
            part[n++]=*path++;
        }
        if(!n) return -1;
        part[n]=0;
        int found=-1;
        for(uint32_t i=1;i<f->nodes;i++)
            if(f->node[i].parent==parent && equal(f->blob+f->node[i].name,(const uint8_t *)part)) { found=(int)i;break; }
        if(found<0) return -1;
        parent=(uint32_t)found;
        if(*path=='/' && !*++path) return -1;
    }
    return (int)parent;
}
const uint8_t *ace_fdt_get(const struct ace_fdt *f,uint32_t index,const char *name,uint32_t *bytes) {
    if(!f || !f->valid || index>=f->nodes || !name || !bytes) return 0;
    struct ace_fdt_node n=f->node[index];
    for(uint32_t i=0;i<n.count;i++) {
        struct ace_fdt_prop p=f->prop[n.first+i];
        if(equal(f->blob+p.name,(const uint8_t *)name)) { *bytes=p.bytes;return f->blob+p.value; }
    }
    return 0;
}
int ace_fdt_compatible(const struct ace_fdt *f,uint32_t node,const char *name) {
    uint32_t n=0;const uint8_t *p=ace_fdt_get(f,node,"compatible",&n);
    if(!p || !n || p[n-1]) return 0;
    int found=0;
    for(uint32_t i=0;i<n;) {
        uint32_t z=i;while(z<n && p[z]) z++;
        if(z==i || z-i>127) return 0;
        if(equal(p+i,(const uint8_t *)name)) found=1;
        i=z+1;
    }
    return found;
}
