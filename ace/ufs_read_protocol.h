/* SPDX-License-Identifier: MIT
 * Bounded UFSHCI2 read-probe wire format. No controller or disk writes.
 * Copied byte-for-byte into the kernel patch; host tests exercise this code. */
#ifndef ACE_UFS_READ_PROTOCOL_H
#define ACE_UFS_READ_PROTOCOL_H
#include <stdint.h>
#include <stddef.h>
#define ACE_UFS_ARENA 0x4000u
#define ACE_UFS_UCD 0x1000u
#define ACE_UFS_RESPONSE 0x1200u
#define ACE_UFS_PRDT 0x1400u
#define ACE_UFS_DATA 0x2000u
#define ACE_UFS_GUARD 0x3c00u
enum ace_ufs_read_op { ACE_UFS_NOP=0, ACE_UFS_TUR=1, ACE_UFS_CAPACITY=2, ACE_UFS_BLOCK=3 };
static inline void ace_ufs_le32(uint8_t *p,uint32_t v) {
    for(unsigned i=0;i<4;i++) p[i]=(uint8_t)(v>>(8*i));
}
static inline uint32_t ace_ufs_be32(const uint8_t *p) {
    return (uint32_t)p[0]<<24|(uint32_t)p[1]<<16|(uint32_t)p[2]<<8|p[3];
}
static inline uint64_t ace_ufs_be64(const uint8_t *p) {
    return (uint64_t)ace_ufs_be32(p)<<32|ace_ufs_be32(p+4);
}
/* All refusal checks precede destination stores. Slot0 requires task tag0.
 * Only NOP, TEST UNIT READY, READ CAPACITY(16), READ(10) LBA0/1 are possible. */
static inline int ace_ufs_read_request(uint8_t *a,size_t bytes,uint64_t pa,
    unsigned op,unsigned lun,unsigned lba,unsigned block_bytes) {
    if(!a || bytes!=ACE_UFS_ARENA || !pa || (pa&0x3fff) ||
       pa>=(1ULL<<40)-ACE_UFS_ARENA || op>ACE_UFS_BLOCK || lun>7 ||
       (op==ACE_UFS_NOP && lun) || (op!=ACE_UFS_BLOCK && (lba || block_bytes)) ||
       (op==ACE_UFS_BLOCK && (lba>1 || (block_bytes!=512 && block_bytes!=4096)))) return -1;
    unsigned len=op==ACE_UFS_CAPACITY?32:op==ACE_UFS_BLOCK?block_bytes:0;
    for(unsigned i=0;i<bytes;i++) a[i]=0;
    for(unsigned i=ACE_UFS_GUARD;i<bytes;i++) a[i]=0x5a;
    for(unsigned i=ACE_UFS_RESPONSE;i<ACE_UFS_RESPONSE+512;i++) a[i]=0xa5;
    uint8_t *cmd=a+ACE_UFS_UCD;
    cmd[0]=op==ACE_UFS_NOP?0:1;cmd[1]=len?0x40:0;cmd[2]=(uint8_t)lun;
    cmd[12]=(uint8_t)(len>>24);cmd[13]=(uint8_t)(len>>16);cmd[14]=(uint8_t)(len>>8);cmd[15]=(uint8_t)len;
    if(op==ACE_UFS_CAPACITY) {cmd[16]=0x9e;cmd[17]=0x10;cmd[29]=32;}
    if(op==ACE_UFS_BLOCK) {cmd[16]=0x28;cmd[21]=(uint8_t)lba;cmd[24]=1;}
    ace_ufs_le32(a,0x11000000|(len?0x04000000:0));ace_ufs_le32(a+8,15);
    ace_ufs_le32(a+16,(uint32_t)(pa+ACE_UFS_UCD));ace_ufs_le32(a+20,(uint32_t)((pa+ACE_UFS_UCD)>>32));
    ace_ufs_le32(a+24,(128u<<16)|128u);
    if(len) {
        ace_ufs_le32(a+28,(256u<<16)|1u);
        ace_ufs_le32(a+ACE_UFS_PRDT,(uint32_t)(pa+ACE_UFS_DATA));
        ace_ufs_le32(a+ACE_UFS_PRDT+4,(uint32_t)((pa+ACE_UFS_DATA)>>32));
        ace_ufs_le32(a+ACE_UFS_PRDT+12,len-1);
    }
    return (int)len;
}
static inline uint32_t ace_ufs_crc32(const uint8_t *p,size_t n) {
    uint32_t crc=0xffffffffu;
    for(size_t i=0;i<n;i++) {crc^=p[i];for(unsigned j=0;j<8;j++) crc=(crc>>1)^(0xedb88320u& (0u-(crc&1)));}
    return ~crc;
}
#endif
