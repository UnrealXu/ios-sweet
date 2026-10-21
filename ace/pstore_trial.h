/* SPDX-License-Identifier: MIT */
#ifndef ACE_PSTORE_TRIAL_H
#define ACE_PSTORE_TRIAL_H
#include "pstore_ring.h"
/* Read-only warm-reset trial latch. Same exclusive ordinary-RAM/ECC0/type0
 * contract as pstore_ring; requires exactly64KiB and a17B lowercase token.
 * Return1 for an exact chronological armed record,0 absent,negative on error.
 * This is a bounded retry policy, not authentication or XNU execution proof.
 * Retention across power loss or arbitrary firmware resets is not guaranteed.
 */
int ace_pstore_trial_pending(const void *zone,size_t bytes,const char token[17]);
#endif
