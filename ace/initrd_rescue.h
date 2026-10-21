/* SPDX-License-Identifier: MIT */
#ifndef ACE_INITRD_RESCUE_H
#define ACE_INITRD_RESCUE_H
#include <stddef.h>
#include <stdint.h>
#define ACE_INITRD_RESCUE_MAX (64u*1024u*1024u)
struct ace_initrd_rescue_policy {
    size_t vendor_bytes, generic_offset, generic_bytes;
    uint8_t vendor_sha256[32], generic_sha256[32], rescue_sha256[32];
    unsigned require_bootconfig;
};
struct ace_initrd_rescue_result {
    size_t old_bytes, new_bytes, generic_offset;
    size_t old_config_offset, new_config_offset, config_extent;
};
/* Caller owns the complete exclusive ordinary-RAM initrd extent. No allocation,
 * physical address, FDT edits, device access or reboot. This grants no ownership.
 * Verify exact vendor/generic/replacement SHA256 before ANY RAM/output stores.
 * Only a same-size or shorter, disjoint replacement is supported. Preserve
 * vendor bytes and validated Linux bootconfig data/footer/trailing padding;
 * footer size/checksum are decoded bytewise and may be physically unaligned
 * (actual LK aligns the config length, not the preceding generic size).
 * zero-fill only alignment between replacement and moved bootconfig. Source
 * layout is an explicit pinned contract, never guessed from compression magic.
 * apply=0 validates/plans without touching initrd; apply=1 performs the plan.
 * Any refusal leaves initrd/result unchanged. Caller supplies readable inputs
 * and a writable, disjoint result; all arithmetic/overlap/format is checked.
 */
int ace_initrd_rescue(void *initrd,size_t bytes,
    const struct ace_initrd_rescue_policy *policy,
    const void *replacement,size_t replacement_bytes,
    struct ace_initrd_rescue_result *result,unsigned apply);
/* Optional trusted, read-only budget hook, checked per <=64KiB hash chunk and
 * immediately before stores. A zero return refuses with -8, unchanged input.
 * The hook/context are caller-owned; it must not mutate inputs or perform I/O.
 * The bounded copy after the final check is deliberately not interruptible. */
int ace_initrd_rescue_with_budget(void *initrd,size_t bytes,
    const struct ace_initrd_rescue_policy *policy,
    const void *replacement,size_t replacement_bytes,
    struct ace_initrd_rescue_result *result,unsigned apply,
    int (*allowed)(void *),void *context);
/* Optional caller-owned bounded progress. Hash completion is a byte count,
 * not a successful digest comparison. Stream1=vendor,2=generic,3=replacement,
 * 4=footer/final gate,5=apply,6=complete; zero means not started. */
struct ace_initrd_rescue_progress {unsigned stream;size_t completed,total;};
int ace_initrd_rescue_with_progress(void *initrd,size_t bytes,
    const struct ace_initrd_rescue_policy *policy,
    const void *replacement,size_t replacement_bytes,
    struct ace_initrd_rescue_result *result,unsigned apply,
    int (*allowed)(void *),void *context,struct ace_initrd_rescue_progress *progress);
#endif
