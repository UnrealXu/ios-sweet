/* SPDX-License-Identifier: MIT */
#ifndef ACE_PSTORE_RESCUE_H
#define ACE_PSTORE_RESCUE_H
#include "pstore_trial.h"
#define ACE_RAM_RESCUE_WORD UINT64_C(0x3130455543534552)
enum ace_ram_attempt { ACE_RAM_FIRST=0, ACE_RAM_RESCUE=1, ACE_RAM_STOP=2 };
/* Same exclusive ordinary-RAM/ECC0 contract as pstore_ring. Requires the exact
 * current armed record, followed by at most one complete normal Android handoff
 * and one complete rescue selection. Unknown/truncated/ambiguous state refuses.
 * Read-only: RAM retention and marker authenticity are not established here. */
int ace_pstore_ram_attempt(const void *zone,size_t bytes,const char token[17]);
/* Commit one rescue selection with the exact 288-byte stage5/-67 envelope and
 * ACE_RAM_RESCUE_WORD in word31. Requires ACE_RAM_RESCUE; never initializes RAM.
 * Refusal preserves every byte. The record means selected, not boot success. */
int ace_pstore_rescue_selected(void *zone,size_t bytes,const char token[17],
    const uint8_t *record,size_t record_bytes);
#endif
