/* SPDX-License-Identifier: MIT */
#include "pstore_seed.h"
#include "pstore_ring.h"
int ace_pstore_seed_empty(void *zone,size_t bytes) {
    if(bytes!=65536) return ACE_PSTORE_RING_E_ARGUMENT;
    int rc=ace_pstore_ring_validate(zone,bytes,0);
    if(!rc) return 0;
    if(rc!=ACE_PSTORE_RING_E_HEADER) return rc;
    volatile unsigned char *p=zone;
    for(size_t i=0;i<bytes;i++) if(p[i]) return ACE_PSTORE_RING_E_HEADER;
    /* No clearing, cursor reset or unknown-header repair. Other bytes already
     * proved zero; publish the type0 signature with exclusive access held. */
    const unsigned signature=ACE_PSTORE_RING_SIGNATURE;
    for(unsigned i=0;i<4;i++) p[i]=(unsigned char)(signature>>(8*i));
    return 1;
}

int ace_pstore_seed_from_snapshot(void *zone,size_t bytes,
    const void *expected,size_t expected_bytes) {
    if(!zone || !expected || bytes!=65536 || expected_bytes!=65536)
        return ACE_PSTORE_RING_E_ARGUMENT;
    uintptr_t z=(uintptr_t)zone,e=(uintptr_t)expected;
    if(z>UINTPTR_MAX-bytes || e>UINTPTR_MAX-expected_bytes)
        return ACE_PSTORE_RING_E_RANGE;
    if(z<e+expected_bytes && e<z+bytes) return ACE_PSTORE_RING_E_ALIAS;
    int rc=ace_pstore_seed_empty(zone,bytes);
    if(rc!=ACE_PSTORE_RING_E_HEADER) return rc;
    volatile unsigned char *p=zone;
    const unsigned char *capture=expected;
    unsigned mismatch=0;
    for(size_t i=0;i<bytes;i++) mismatch|=(unsigned)(p[i]^capture[i]);
    if(mismatch) return ACE_PSTORE_RING_E_HEADER;
    /* Full matching bytes are recoverable from the archived capture. Publish
     * signature last; no valid intermediate ring is exposed while clearing.
     * Caller still holds exclusive access and performs cache/order handling. */
    for(size_t i=0;i<bytes;i++) p[i]=0;
    const unsigned signature=ACE_PSTORE_RING_SIGNATURE;
    for(unsigned i=0;i<4;i++) p[i]=(unsigned char)(signature>>(8*i));
    return ACE_PSTORE_SEED_ARCHIVED_MATCH;
}
