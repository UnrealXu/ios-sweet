/* SPDX-License-Identifier: MIT
 * Ace LUN2 primary GPT discovery only. No media writes or root publication.
 * Deliberately supports the observed 4096-byte/128x128 layout only.
 * Requires the read-probe header first (also inside the kernel patch). */
#ifndef ACE_UFS_ROOT_GPT_H
#define ACE_UFS_ROOT_GPT_H
#define ACE_UFS_GPT_BYTES 16384u
#define ACE_UFS_GPT_READ 6u
struct ace_ufs_gpt_plan {
    uint64_t last_lba, first_usable, last_usable;
    uint32_t entries_crc;
};
struct ace_ufs_root_bounds { uint64_t first_lba, blocks; };
static inline uint32_t ace_gpt_le32(const uint8_t *p) {
    return (uint32_t)p[0]|(uint32_t)p[1]<<8|(uint32_t)p[2]<<16|(uint32_t)p[3]<<24;
}
static inline uint64_t ace_gpt_le64(const uint8_t *p) {
    return ace_gpt_le32(p)|(uint64_t)ace_gpt_le32(p+4)<<32;
}
static inline int ace_gpt_nonzero(const uint8_t *p,size_t n) {
    unsigned any=0;for(size_t i=0;i<n;i++) any|=p[i];return any!=0;
}
static inline int ace_gpt_same(const uint8_t *a,const uint8_t *b,size_t n) {
    unsigned diff=0;for(size_t i=0;i<n;i++) diff|=a[i]^b[i];return diff==0;
}
static inline int ace_gpt_disjoint(const void *a,size_t n,const void *b,size_t m) {
    uintptr_t x=(uintptr_t)a,y=(uintptr_t)b;
    return x<=UINTPTR_MAX-n && y<=UINTPTR_MAX-m && (x+n<=y || y+m<=x);
}
static inline int ace_gpt_plan_valid(const struct ace_ufs_gpt_plan *p) {
    return p && p->last_lba>=11 && p->last_lba<UINT32_MAX &&
        p->first_usable>=6 && p->first_usable<=p->last_usable &&
        p->last_usable<=p->last_lba-5;
}
/* Caller supplies the independently read capacity. Input is never modified;
 * all refusal paths leave output unchanged, including input/output aliases. */
static inline int ace_ufs_gpt_header(const uint8_t *b,size_t bytes,
    uint64_t last_lba,unsigned block,struct ace_ufs_gpt_plan *out) {
    static const uint8_t magic[8]={'E','F','I',' ','P','A','R','T'};
    if(!b || !out || bytes!=4096 || block!=4096 ||
       !ace_gpt_disjoint(b,bytes,out,sizeof(*out)) || !ace_gpt_same(b,magic,8) ||
       ace_gpt_le32(b+8)!=0x10000 || ace_gpt_le32(b+12)!=92 ||
       ace_gpt_le32(b+20) || ace_gpt_le64(b+24)!=1 ||
       ace_gpt_le64(b+32)!=last_lba ||
       ace_gpt_le64(b+72)!=2 || ace_gpt_le32(b+80)!=128 ||
       ace_gpt_le32(b+84)!=128) return -1;
    struct ace_ufs_gpt_plan p={last_lba,ace_gpt_le64(b+40),ace_gpt_le64(b+48),ace_gpt_le32(b+88)};
    if(!ace_gpt_plan_valid(&p)) return -1;
    uint32_t crc=0xffffffffu;
    for(unsigned i=0;i<92;i++) {
        crc^=(i>=16 && i<20)?0:b[i];
        for(unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320u&(0u-(crc&1)));
    }
    if(~crc!=ace_gpt_le32(b+16)) return -2;
    *out=p;return 0;
}
/* Only the four primary entry-array sectors, after a validated header.
 * This does not extend the historical BLOCK probe beyond LBA0/1. */
static inline int ace_ufs_gpt_request(uint8_t *a,size_t bytes,uint64_t pa,
    const struct ace_ufs_gpt_plan *plan,unsigned lun,unsigned lba,unsigned block) {
    if(!ace_gpt_plan_valid(plan) || !a || bytes!=ACE_UFS_ARENA ||
       !ace_gpt_disjoint(a,bytes,plan,sizeof(*plan)) || lun!=2 ||
       lba<2 || lba>5 || block!=4096) return -1;
    int n=ace_ufs_read_request(a,bytes,pa,ACE_UFS_BLOCK,2,0,4096);
    if(n<0) return n;
    uint8_t *c=a+ACE_UFS_UCD;
    for(unsigned i=0;i<4;i++) c[18+i]=(uint8_t)(lba>>(24-8*i));
    return n;
}
/* Narrow GOOD response for these fixed reads: a zero data-segment length
 * means bytes32+ are not part of the response. Actual Ace leaves those bytes
 * poisoned. Validate the complete 32B header, never unused sense storage.
 * Linux v5.10 ufshcd_scsi_cmd_status handles GOOD without copying sense data:
 * https://raw.githubusercontent.com/torvalds/linux/v5.10/drivers/scsi/ufs/ufshcd.c
 */
static inline int ace_ufs_gpt_good_response(const uint8_t *r,size_t bytes,unsigned lun) {
    if(!r || bytes!=512 || lun!=2 || r[0]!=0x21 || r[2]!=lun) return 0;
    for(unsigned i=0;i<32;i++) if(i!=0 && i!=2 && r[i]) return 0;
    return 1;
}
static inline int ace_gpt_userdata(const uint8_t *p) {
    static const uint8_t name[16]={'u',0,'s',0,'e',0,'r',0,'d',0,'a',0,'t',0,'a',0};
    return ace_gpt_same(p+56,name,16) && !ace_gpt_nonzero(p+72,56);
}
/* Observed PGKM10 256GB primary GPT declares first-usable34 but entry0
 * misc occupies8..135. It is outside the four-block primary array and cannot
 * become userdata. Permit only this exact observed exception; still check its
 * identity, full array CRC and overlap with every other used partition. */
static inline int ace_gpt_ace_misc(const uint8_t *p,unsigned index,
    const struct ace_ufs_gpt_plan *plan,uint64_t first,uint64_t last) {
    static const uint8_t name[8]={'m',0,'i',0,'s',0,'c',0};
    return index==0 && plan->last_lba==62480383 && plan->first_usable==34 &&
        first==8 && last==135 && !ace_gpt_le64(p+48) &&
        ace_gpt_same(p+56,name,8) && !ace_gpt_nonzero(p+64,64);
}
/* Verify the entire array before selecting the exact UTF16LE userdata name.
 * Reject duplicate identities/names, overlaps and out-of-device partitions.
 * No fallback to another partition, and no filesystem claim. */
static inline int ace_ufs_gpt_userdata(const uint8_t *b,size_t bytes,
    const struct ace_ufs_gpt_plan *plan,struct ace_ufs_root_bounds *out) {
    if(!b || !out || bytes!=ACE_UFS_GPT_BYTES || !ace_gpt_plan_valid(plan) ||
       !ace_gpt_disjoint(b,bytes,out,sizeof(*out)) ||
       !ace_gpt_disjoint(plan,sizeof(*plan),out,sizeof(*out))) return -1;
    if(ace_ufs_crc32(b,bytes)!=plan->entries_crc) return -2;
    struct ace_ufs_root_bounds found={0,0};unsigned matches=0;
    for(unsigned i=0;i<128;i++) {
        const uint8_t *p=b+i*128;
        if(!ace_gpt_nonzero(p,16)) continue;
        uint64_t first=ace_gpt_le64(p+32),last=ace_gpt_le64(p+40);
        if(!ace_gpt_nonzero(p+16,16) || first>last ||
           (first<plan->first_usable && !ace_gpt_ace_misc(p,i,plan,first,last)) ||
           last>plan->last_usable) return -3;
        for(unsigned j=0;j<i;j++) {
            const uint8_t *q=b+j*128;
            if(!ace_gpt_nonzero(q,16)) continue;
            if(ace_gpt_same(p+16,q+16,16) ||
               (first<=ace_gpt_le64(q+40) && ace_gpt_le64(q+32)<=last)) return -3;
        }
        if(ace_gpt_userdata(p)) {
            if(++matches!=1) return -4;
            found.first_lba=first;found.blocks=last-first+1;
        }
    }
    if(matches!=1) return -4;
    *out=found;return 0;
}
#endif
