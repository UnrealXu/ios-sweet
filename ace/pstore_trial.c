/* SPDX-License-Identifier: MIT */
#include "pstore_trial.h"
int ace_pstore_trial_pending(const void *zone,size_t bytes,const char token[17]) {
    if(!token || bytes!=65536) return ACE_PSTORE_RING_E_ARGUMENT;
    for(unsigned i=0;i<16;i++)
        if(!((token[i]>='0' && token[i]<='9') || (token[i]>='a' && token[i]<='f')))
            return ACE_PSTORE_RING_E_ARGUMENT;
    if(token[16]) return ACE_PSTORE_RING_E_ARGUMENT;
    struct ace_pstore_ring_info ring;
    int rc=ace_pstore_ring_validate(zone,bytes,&ring);if(rc) return rc;
    char marker[]="\nACETRIAL1:0000000000000000: armed\n";
    for(unsigned i=0;i<16;i++) marker[11+i]=token[i];
    const unsigned length=sizeof(marker)-1;
    if(ring.size<length) return 0;
    const volatile uint8_t *data=(const volatile uint8_t *)zone+12;
    uint32_t start=ring.size==ring.capacity?ring.start:0;
    for(uint32_t i=0;i<=ring.size-length;i++) {
        unsigned j=0;
        for(;j<length;j++) if(data[(start+i+j)%ring.capacity]!=(uint8_t)marker[j]) break;
        if(j==length) return 1;
    }
    return 0;
}
