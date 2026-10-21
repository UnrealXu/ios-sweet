/* SPDX-License-Identifier: MIT */
#ifndef ACE_XNU_HANDOFF_H
#define ACE_XNU_HANDOFF_H
#include <stddef.h>
#include <stdint.h>
#define ACE_XNU_PAGE 16384u
#define ACE_XNU_LINE 608u
#define ACE_XNU_HEADER 680u
#define ACE_XNU_MAX_SEGS 32u
struct ace_xnu_range { uint64_t base, size; };
/* Caller establishes exclusive writable/executable RAM, with MMU/cache off.
 * No default phone address. reserved includes the loader/stack/records. The
 * entire XNU-managed window must be free of reservations (not just segments).
 * This describes physical addresses independently of host test mappings. */
struct ace_xnu_policy {
    struct ace_xnu_range ram, source;
    const struct ace_xnu_range *reserved;
    size_t reserved_count;
};
struct ace_xnu_video { uint64_t base, display, row_bytes, width, height, depth; };
struct ace_xnu_boot_args {
    uint16_t revision, version;
    uint64_t virt_base, phys_base, mem_size, top_of_kernel_data;
    struct ace_xnu_video video;
    uint32_t machine_type;
    uint64_t device_tree;
    uint32_t device_tree_length;
    char command_line[ACE_XNU_LINE];
    uint64_t boot_flags, mem_size_actual;
};
struct ace_xnu_segment { uint64_t destination, memory_bytes, file_offset, file_bytes; };
struct ace_xnu_plan {
    struct ace_xnu_boot_args args;
    uint64_t entry_pa, adt_pa, args_pa, adt_offset, adt_bytes;
    uint32_t count;
    struct ace_xnu_segment segments[ACE_XNU_MAX_SEGS];
};
enum ace_xnu_error {
    ACE_XNU_OK=0, ACE_XNU_ARGUMENT=-1, ACE_XNU_FORMAT=-2,
    ACE_XNU_RANGE=-3, ACE_XNU_OVERLAP=-4, ACE_XNU_ENTRY=-5
};
/* ACEXNU01/v1: same field offsets as old SWEETXNU/v1, distinct target magic.
 * Input is a PRE-REBASED flat-segment bundle, not a Mach-O/IMG4 parser. ADT
 * semantics must be supplied/validated by a future Ace platform builder.
 * Refuses old SWEETXNU. Video is deliberately disabled: no Ace framebuffer PA
 * is established. prepare writes output only on success, never target RAM. */
int ace_xnu_prepare(const void *payload, size_t bytes,
                    const struct ace_xnu_policy *policy, struct ace_xnu_plan *out);
/* Validate first; then exact byte copies/BSS zeroing and BootArgs/ADT writes.
 * ram_mapping must map all policy.ram, be disjoint from payload/policy/out,
 * and have at least policy.ram.size bytes. Caller must establish real mapping
 * ownership/coherence; this API cannot infer it from a numeric address.
 * No MMIO, DMA, CPU register changes, jump or storage I/O here. */
int ace_xnu_materialize(const void *payload, size_t bytes,
                        const struct ace_xnu_policy *policy,
                        void *ram_mapping, size_t mapped_bytes,
                        struct ace_xnu_plan *out);
#endif
