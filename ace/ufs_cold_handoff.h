/* SPDX-License-Identifier: MIT
 * Cold boot only, before the first owned DMA request. No register accesses.
 * UFSHCI error-code words are meaningful only when bit31 is set. */
#ifndef ACE_UFS_COLD_HANDOFF_H
#define ACE_UFS_COLD_HANDOFF_H
#include <stdint.h>
static inline uint32_t ace_ufs_error_mask(unsigned layer) {
    const uint32_t masks[5]={0x1f,0xffff,7,0x7f,1};
    return layer<5?masks[layer]:0;
}
static inline int ace_ufs_codes_defined(const uint32_t *words) {
    if(!words) return 0;
    for(unsigned i=0;i<5;i++) if(words[i]&~(0x80000000u|ace_ufs_error_mask(i))) return 0;
    return 1;
}
static inline int ace_ufs_active_error(uint32_t word,unsigned layer) {
    return (word&0x80000000u) && (word&ace_ufs_error_mask(layer));
}
static inline int ace_ufs_codes_quiet(const uint32_t *words) {
    if(!ace_ufs_codes_defined(words)) return 0;
    for(unsigned i=0;i<5;i++) if(ace_ufs_active_error(words[i],i)) return 0;
    return 1;
}
/* Only pending PHY/DL indications can be drained during idle cold handoff.
 * PA_INIT, NAC/replay timeout, NL/TL/DME or any unknown bits need recovery
 * that this probe does not implement. Never classify those as startup noise. */
static inline int ace_ufs_cold_first_allowed(uint32_t status,const uint32_t *words) {
    if((status&~4u) || !ace_ufs_codes_defined(words)) return 0;
    if(ace_ufs_active_error(words[1],1) && (words[1]&0x2003)) return 0;
    for(unsigned i=2;i<5;i++) if(ace_ufs_active_error(words[i],i)) return 0;
    return 1;
}
static inline int ace_ufs_cold_can_ack(uint32_t first_status,const uint32_t *first,
    uint32_t second_status,const uint32_t *second) {
    return ace_ufs_cold_first_allowed(first_status,first) && !(second_status&~4u) && ace_ufs_codes_quiet(second);
}
static inline int ace_ufs_cold_final_ready(uint32_t status,const uint32_t *words) {
    return status==0 && ace_ufs_codes_quiet(words);
}
#endif
