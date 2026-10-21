/* SPDX-License-Identifier: MIT
 * Classify an empty latched UIC event only. No hardware access or recovery. */
#ifndef ACE_UFS_UIC_POLICY_H
#define ACE_UFS_UIC_POLICY_H
#include <stdint.h>
static inline int ace_ufs_uic_empty_codes(const uint32_t *codes) {
    if(!codes) return 0;
    /* Only zero/error-valid-with-no-code. Reject even reserved unknown bits;
     * never classify PHY lane/LINERESET, DL/NL/TL/DME codes as empty. */
    for(unsigned i=0;i<5;i++) if(codes[i]&0x7fffffff) return 0;
    return 1;
}
static inline int ace_ufs_uic_empty_event(uint32_t status,const uint32_t *codes) {
    return (status&4) && !(status&0x70880) && ace_ufs_uic_empty_codes(codes);
}
#endif
