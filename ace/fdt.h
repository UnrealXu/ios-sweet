/* SPDX-License-Identifier: MIT */
#ifndef ACE_FDT_H
#define ACE_FDT_H
#include <stdint.h>
#include <stddef.h>
#define ACE_FDT_NODES 4096u
#define ACE_FDT_PROPS 16384u
#define ACE_FDT_DEPTH 64u
#define ACE_FDT_BYTES (2u*1024u*1024u)
#define ACE_FDT_RESERVES 256u
struct ace_fdt_node { uint32_t name, parent, first, count, children; };
struct ace_fdt_prop { uint32_t name, value, bytes; };
struct ace_fdt_reserve { uint64_t base, size; };
/* Caller-owned normal RAM workspace (~280KiB); never allocate on a small boot
 * stack. Keep it and the immutable DTB outside all destination RAM. Partial
 * workspace contents after failure are invalid; accessors require valid=1. */
struct ace_fdt {
    const uint8_t *blob;
    uint32_t total, nodes, props, reserves, valid;
    struct ace_fdt_node node[ACE_FDT_NODES];
    struct ace_fdt_prop prop[ACE_FDT_PROPS];
    struct ace_fdt_reserve reserve[ACE_FDT_RESERVES];
};
/* Bounded v17/last-compatible<=17 parser. Requires disjoint workspace/input.
 * Enforces header/reserve/structure/strings order, duplicate rejection,
 * properties-before-children and exact terminal FDT_END. No allocation/I/O. */
int ace_fdt_open(const void *blob,size_t bytes,struct ace_fdt *out);
int ace_fdt_find(const struct ace_fdt *f,const char *absolute_path);
const uint8_t *ace_fdt_get(const struct ace_fdt *f,uint32_t node,
    const char *name,uint32_t *bytes);
int ace_fdt_compatible(const struct ace_fdt *f,uint32_t node,const char *name);
uint32_t ace_fdt_be32(const uint8_t *p);
uint64_t ace_fdt_be64(const uint8_t *p);
#endif
