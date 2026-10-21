/* SPDX-License-Identifier: MIT
 * Fixed fDeviceInit QUERY frames only. Include the read-probe protocol first.
 * No descriptor/attribute writes, LU configuration, crypto or storage CDBs.
 */
#ifndef ACE_UFS_DEVICE_INIT_H
#define ACE_UFS_DEVICE_INIT_H
enum { ACE_UFS_INIT_SET=4, ACE_UFS_INIT_READ=5 };
static inline int ace_ufs_device_init_request(uint8_t *a,size_t bytes,uint64_t pa,unsigned opcode) {
    if(opcode!=5 && opcode!=6) return -1;
    if(ace_ufs_read_request(a,bytes,pa,ACE_UFS_NOP,0,0,0)<0) return -1;
    uint8_t *q=a+ACE_UFS_UCD;
    q[0]=0x16;q[5]=opcode==6?0x81:1;q[12]=(uint8_t)opcode;q[13]=1;
    return 0; /* No PRDT/data segment. Value/index/selector all zero. */
}
static inline int ace_ufs_device_init_response(const uint8_t *r,size_t bytes,unsigned opcode,uint32_t *value) {
    if(!r || bytes!=512 || !value || (opcode!=5 && opcode!=6) ||
       r[0]!=0x36 || r[1] || r[2] || r[3] || r[6] || r[7] ||
       r[10] || r[11] || r[12]!=opcode || r[13]!=1 || r[14] || r[15] ||
       r[18] || r[19]) return -1;
    uint32_t v=ace_ufs_be32(r+20);
    if(v>1) return -1;
    *value=v;return 0;
}
#endif
