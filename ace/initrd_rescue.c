/* SPDX-License-Identifier: MIT */
#include "initrd_rescue.h"
#include "../diagnostics/ace-ramdiag/sha256.h"
#if defined(ACE_INITRD_NATIVE_CE) && ACE_INITRD_NATIVE_CE
#include "native_config.h"
#if !NATIVE_RAM_RESCUE
#error "native CE SHA is restricted to RAM_RESCUE profile"
#endif
#include "sha_ce_update.h"
#define initrd_sha_update private_ce_update
#else
#define initrd_sha_update ace_sha_update
#endif
static int overlap(const void *a,size_t n,const void *b,size_t m) {
    uintptr_t x=(uintptr_t)a,y=(uintptr_t)b;
    return n>UINTPTR_MAX-x || m>UINTPTR_MAX-y || (x<y+m && y<x+n);
}
static uint32_t le32(const uint8_t *p) {
    uint32_t n=0;for(unsigned i=0;i<4;i++)n|=(uint32_t)p[i]<<(8*i);return n;
}
static int equal(const uint8_t *a,const uint8_t *b,size_t n) {
    unsigned different=0;for(size_t i=0;i<n;i++)different|=a[i]^b[i];return !different;
}
static int zeros(const uint8_t *p,size_t n) {
    for(size_t i=0;i<n;i++)if(p[i])return 0;
    return 1;
}
static int pinned(const uint8_t *p,size_t n,const uint8_t expected[32],int (*allowed)(void *),void *context,struct ace_initrd_rescue_progress *progress,unsigned stream) {
    if(progress) {progress->stream=stream;progress->completed=0;progress->total=n;}
    struct ace_sha256 sha;uint8_t digest[32];
    ace_sha_init(&sha);
    while(n) {
        if(allowed && !allowed(context))return -8;
        size_t part=n>65536?65536:n;initrd_sha_update(&sha,p,part);p+=part;n-=part;
        if(progress)progress->completed+=part;
    }
    ace_sha_final(&sha,digest);
    return equal(digest,expected,32)?0:-4;
}
int ace_initrd_rescue_with_progress(void *initrd,size_t bytes,
    const struct ace_initrd_rescue_policy *p,const void *replacement,size_t rbytes,
    struct ace_initrd_rescue_result *result,unsigned apply,int (*allowed)(void *),void *context,struct ace_initrd_rescue_progress *progress) {
    if(!initrd || !p || !replacement || !result || apply>1 || !bytes ||
       bytes>ACE_INITRD_RESCUE_MAX || !rbytes || rbytes>bytes ||
       overlap(initrd,bytes,p,sizeof(*p)) || overlap(initrd,bytes,replacement,rbytes) ||
       overlap(initrd,bytes,result,sizeof(*result)) ||
       overlap(result,sizeof(*result),p,sizeof(*p)) ||
       overlap(result,sizeof(*result),replacement,rbytes))return -1;
    if(progress && (overlap(progress,sizeof(*progress),initrd,bytes) ||
       overlap(progress,sizeof(*progress),p,sizeof(*p)) ||
       overlap(progress,sizeof(*progress),replacement,rbytes) ||
       overlap(progress,sizeof(*progress),result,sizeof(*result))))return -1;
    if(progress) {progress->stream=0;progress->completed=0;progress->total=0;}
    if(p->require_bootconfig>1 || !p->vendor_bytes || !p->generic_bytes ||
       p->vendor_bytes>bytes || p->generic_offset<p->vendor_bytes ||
       p->generic_offset>bytes || p->generic_offset-p->vendor_bytes>4095 ||
       p->generic_bytes>bytes-p->generic_offset || rbytes>p->generic_bytes)return -2;
    uint8_t *b=initrd;const uint8_t *r=replacement;
    size_t old_end=p->generic_offset+p->generic_bytes;
    if(!zeros(b+p->vendor_bytes,p->generic_offset-p->vendor_bytes))return -3;
    int status=pinned(b,p->vendor_bytes,p->vendor_sha256,allowed,context,progress,1);
    if(status)return status;
    status=pinned(b+p->generic_offset,p->generic_bytes,p->generic_sha256,allowed,context,progress,2);
    if(status)return status;
    status=pinned(r,rbytes,p->rescue_sha256,allowed,context,progress,3);if(status)return status;
    if(progress) {progress->stream=4;progress->completed=0;progress->total=0;}
    struct ace_initrd_rescue_result plan={bytes,0,p->generic_offset,0,0,0};
    size_t new_end=p->generic_offset+rbytes;
    /* Linux 5.10 permits at most three bytes following #BOOTCONFIG\n.
     * Require explicit zero padding, bounded data, LE size/checksum (unaligned permitted),
     * a complete checksum and no unrecognized bytes between known streams. */
    static const uint8_t magic[]="#BOOTCONFIG\n";
    size_t footer=0;int found=0;
    for(size_t trailing=0;trailing<4;trailing++) {
        if(bytes-old_end<20+trailing)continue;
        size_t at=bytes-12-trailing;
        if(equal(b+at,magic,12) && zeros(b+at+12,trailing)) {
            footer=at-8;found=1;break;
        }
    }
    if(found) {
        uint32_t size=le32(b+footer),checksum=le32(b+footer+4);
        if(!size || size>=65536 || size>footer-old_end)return -5;
        size_t begin=footer-size;
        if(begin-old_end>4095 || !zeros(b+old_end,begin-old_end))return -5;
        uint32_t actual=0;for(size_t i=0;i<size;i++)actual+=b[begin+i];
        if(actual!=checksum)return -6;
        size_t padding=(begin-new_end)&3u;
        plan.old_config_offset=begin;plan.new_config_offset=new_end+padding;
        plan.config_extent=bytes-begin;
        plan.new_bytes=plan.new_config_offset+plan.config_extent;
        if(plan.new_bytes>bytes)return -7;
    } else {
        if(p->require_bootconfig || bytes-old_end>4095 || !zeros(b+old_end,bytes-old_end))return -5;
        plan.new_bytes=new_end+(bytes-old_end);
    }
    if(allowed && !allowed(context))return -8;
    if(apply) {
        if(progress)progress->stream=5;
        for(size_t i=0;i<rbytes;i++)b[p->generic_offset+i]=r[i];
        if(found) {
            for(size_t i=new_end;i<plan.new_config_offset;i++)b[i]=0;
            /* Destination is never above source; forward copy is overlap-safe. */
            for(size_t i=0;i<plan.config_extent;i++)b[plan.new_config_offset+i]=b[plan.old_config_offset+i];
        } else for(size_t i=new_end;i<plan.new_bytes;i++)b[i]=0;
    }
    *result=plan;if(progress)progress->stream=6;return 0;
}

int ace_initrd_rescue_with_budget(void *initrd,size_t bytes,
    const struct ace_initrd_rescue_policy *policy,const void *replacement,size_t replacement_bytes,
    struct ace_initrd_rescue_result *result,unsigned apply,int (*allowed)(void *),void *context) {
    return ace_initrd_rescue_with_progress(initrd,bytes,policy,replacement,replacement_bytes,
        result,apply,allowed,context,0);
}

int ace_initrd_rescue(void *initrd,size_t bytes,
    const struct ace_initrd_rescue_policy *policy,const void *replacement,size_t replacement_bytes,
    struct ace_initrd_rescue_result *result,unsigned apply) {
    return ace_initrd_rescue_with_budget(initrd,bytes,policy,replacement,replacement_bytes,result,apply,0,0);
}
