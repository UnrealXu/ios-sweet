/* SPDX-License-Identifier: MIT
 * Read-only userdata mapping. Include the read protocol and GPT headers first.
 * Refusal never changes the DMA arena or output plan. */
#ifndef ACE_UFS_ROOT_IO_H
#define ACE_UFS_ROOT_IO_H
#define ACE_UFS_ROOT_READ 7u
#define ACE_UFS_ROOT_MAX_IO 65536u
struct ace_ufs_root_slice { uint32_t lba, skip, bytes; };
static inline int ace_ufs_root_bounds_valid(const struct ace_ufs_gpt_plan *p,
    const struct ace_ufs_root_bounds *r) {
    return ace_gpt_plan_valid(p) && r && r->blocks &&
        r->first_lba>=p->first_usable && r->first_lba<=p->last_usable &&
        r->blocks<=p->last_usable-r->first_lba+1;
}
static inline int ace_ufs_root_slice(const struct ace_ufs_gpt_plan *p,
    const struct ace_ufs_root_bounds *r,uint64_t offset,size_t count,
    struct ace_ufs_root_slice *out) {
    if(!ace_ufs_root_bounds_valid(p,r) || !out || count>ACE_UFS_ROOT_MAX_IO ||
       !ace_gpt_disjoint(p,sizeof(*p),out,sizeof(*out)) ||
       !ace_gpt_disjoint(r,sizeof(*r),out,sizeof(*out))) return -1;
    uint64_t capacity=r->blocks*4096;
    if(offset>capacity || count>capacity-offset) return -1;
    struct ace_ufs_root_slice s={0,0,0};
    if(count) {
        s.lba=(uint32_t)(r->first_lba+offset/4096);
        s.skip=(uint32_t)(offset%4096);
        s.bytes=(uint32_t)(count<4096-s.skip?count:4096-s.skip);
    }
    *out=s;return 0;
}
static inline int ace_ufs_root_request(uint8_t *a,size_t bytes,uint64_t pa,
    const struct ace_ufs_gpt_plan *p,const struct ace_ufs_root_bounds *r,
    unsigned lun,unsigned lba,unsigned block) {
    if(!ace_ufs_root_bounds_valid(p,r) || !a || bytes!=ACE_UFS_ARENA ||
       !ace_gpt_disjoint(a,bytes,p,sizeof(*p)) ||
       !ace_gpt_disjoint(a,bytes,r,sizeof(*r)) || lun!=2 || block!=4096 ||
       lba<r->first_lba || lba-r->first_lba>=r->blocks) return -1;
    int n=ace_ufs_read_request(a,bytes,pa,ACE_UFS_BLOCK,2,0,4096);
    if(n<0) return n;
    for(unsigned i=0;i<4;i++) a[ACE_UFS_UCD+18+i]=(uint8_t)(lba>>(24-8*i));
    return n;
}
#endif
