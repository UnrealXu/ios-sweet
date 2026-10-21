/* SPDX-License-Identifier: MIT
 * Original caller-owned RAM codec for a little-endian persistent_ram ring.
 * No physical addresses, MMIO, cache maintenance, SMC, storage or allocation.
 */
#ifndef ACE_PSTORE_RING_H
#define ACE_PSTORE_RING_H
#include <stddef.h>
#include <stdint.h>

#define ACE_PSTORE_RING_SIGNATURE UINT32_C(0x43474244)
#define ACE_PSTORE_RING_HEADER_BYTES 12u

enum ace_pstore_ring_error {
    ACE_PSTORE_RING_OK = 0,
    ACE_PSTORE_RING_E_ARGUMENT = -1,
    ACE_PSTORE_RING_E_RANGE = -2,
    ACE_PSTORE_RING_E_HEADER = -3,
    ACE_PSTORE_RING_E_ALIAS = -4,
    ACE_PSTORE_RING_E_STATE = -5,
    ACE_PSTORE_RING_E_SPACE = -6
};
struct ace_pstore_ring_info {
    size_t capacity;
    uint32_t start;
    uint32_t size;
};

/* Caller supplies one complete, accessible ordinary-RAM zone with ECC disabled,
 * type signature zero (pmsg/console), and no simultaneous access by another CPU,
 * interrupt, DMA engine or reader. This codec neither reserves nor maps RAM.
 * Header: LE u32 DBGC signature/start/size, then capacity=zone_bytes-12 bytes.
 * No API initializes an unknown signature. Zone may be byte-unaligned.
 * capacity must be 1..INT32_MAX. info is optional, aligned and disjoint.
 * Validation follows the official reader's size<=capacity, start<=size bounds.
 * All APIs leave outputs and zone unchanged on any error. */
int ace_pstore_ring_validate(const void *zone, size_t zone_bytes,
                            struct ace_pstore_ring_info *info);

/* Append retains existing chronological data until full, then drops oldest.
 * More than capacity input bytes retains only the input's last capacity bytes.
 * Source must not overlap any part of zone (even when input is truncated).
 * For nonempty append, stable producer state is required: partial start==size,
 * or full start<capacity. Other reader-valid headers return E_STATE rather than
 * silently overwriting old partial data. Zero length is a validated no-op;
 * source may be NULL only for zero length. Signature is never modified. */
int ace_pstore_ring_append(void *zone, size_t zone_bytes,
                          const void *source, size_t source_bytes);

/* Copy the ENTIRE chronological record; no implicit output truncation.
 * out_bytes<stored size returns E_SPACE, with all outputs unchanged. written
 * is required and receives stored size on success. out may be NULL iff
 * out_bytes==0 (which succeeds only for an empty record). All declared output
 * ranges and written must be disjoint from zone and from each other. */
int ace_pstore_ring_read(const void *zone, size_t zone_bytes,
                        void *out, size_t out_bytes, size_t *written);
#endif
