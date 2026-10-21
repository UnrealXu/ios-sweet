/* SPDX-License-Identifier: MIT */
#ifndef ACE_FDT_REFUSAL_H
#define ACE_FDT_REFUSAL_H
#include "fdt.h"
#define ACE_REFUSAL_BYTES 288u
#define ACE_REFUSAL_PROPERTY "ace,native-refusal"
#define ACE_PMSG_SNAPSHOT_PROPERTY "ace,pmsg-before-seed"
/* Copy an already validated tree and add one opaque diagnostic property to
 * /chosen, before its children. Keep all existing properties/reserves intact.
 * Output, record, parsed workspace and written must be mutually disjoint from
 * the immutable input where applicable. No output/written stores on refusal.
 * This edits normal caller-owned RAM only; it grants no boot/RAM ownership. */
int ace_fdt_copy_refusal(const struct ace_fdt *f,void *output,size_t capacity,
    const void *record,size_t record_bytes,size_t *written);
/* Optional complete 64KiB read-only snapshot, supplied by the caller after
 * independent physical ownership checks. Stored as an opaque second chosen
 * property; never interpret, clear or repair the source. NULL/0 preserves the
 * original one-property ABI. Both inputs and output/written remain unchanged
 * on every refusal; snapshot must be disjoint from output and written. */
int ace_fdt_copy_refusal_snapshot(const struct ace_fdt *f,void *output,size_t capacity,
    const void *record,size_t record_bytes,const void *snapshot,size_t snapshot_bytes,size_t *written);
int ace_fdt_copy_refusal_rescue(const struct ace_fdt *,void *,size_t,const void *,size_t,
    const void *,size_t,const uint8_t *capability,uint64_t initrd_end,size_t *written);
#endif
