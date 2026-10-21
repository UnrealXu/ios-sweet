/* SPDX-License-Identifier: MIT
 * Recognize ONLY the observed startup LINERESET followed by empty errors.
 * A classification is not link recovery or proof of a successful command. */
#ifndef ACE_UFS_BOOT_HANDOFF_H
#define ACE_UFS_BOOT_HANDOFF_H
#include <stdint.h>
static inline int ace_ufs_boot_linereset(uint32_t status,const uint32_t *codes) {
    if(!codes || (status&0x70880) || codes[0]!=0x80000010u) return 0;
    for(unsigned i=1;i<5;i++) if(codes[i]&0x7fffffff) return 0;
    return 1;
}
static inline int ace_ufs_boot_linereset_cleared(uint32_t first_status,
    const uint32_t *first,uint32_t next_status,const uint32_t *next) {
    if(!ace_ufs_boot_linereset(first_status,first) || !next || (next_status&0x70880)) return 0;
    for(unsigned i=0;i<5;i++) if(next[i]&0x7fffffff) return 0;
    return 1;
}
#endif
