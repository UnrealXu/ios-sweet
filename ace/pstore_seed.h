/* SPDX-License-Identifier: MIT */
#ifndef ACE_PSTORE_SEED_H
#define ACE_PSTORE_SEED_H
#include <stddef.h>
/* Explicit lifecycle operation for a caller-owned ordinary-RAM pmsg zone.
 * Caller MUST establish exclusive access, ECC0/type0 and exact zone ownership
 * independently. A zero header alone establishes none of these conditions.
 * Only a wholly zero 64KiB zone is initialized. Preserve any reader-valid ring
 * byte-for-byte; refuse every other nonzero zone without a store. Returns1 for
 * a new empty DBGC ring,0 for an existing valid ring, or a negative codec error.
 * No physical mapping/cache maintenance/partition operation is performed. */
int ace_pstore_seed_empty(void *zone,size_t bytes);
/* Separate explicitly authorized lifecycle extension. The full immutable
 * expected capture MUST already be archived on the host and hash-pinned by
 * the Image builder, and be disjoint from this caller-owned ordinary-RAM zone.
 * Exclusive ownership/ECC0/type0 and disabled other access remain caller
 * obligations. All declared spans are validated before any store.
 * Existing valid/all-zero zones retain the old0/1 result and exact behavior.
 * Only after the old API refuses a nonzero invalid-header zone, compare ALL
 * 65536 bytes to the archived capture. A complete match permits rebuilding an
 * empty DBGC ring and returns2, distinct from initial all-zero seeding. Every
 * unknown/mismatching zone remains byte-for-byte unchanged; no partial match,
 * offset exception, header repair, allocation or physical I/O is performed. */
#define ACE_PSTORE_SEED_ARCHIVED_MATCH 2
int ace_pstore_seed_from_snapshot(void *zone,size_t bytes,
    const void *expected,size_t expected_bytes);
#endif
