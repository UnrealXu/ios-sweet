/* SPDX-License-Identifier: MIT */
#ifndef ACE_XNU_FDT_H
#define ACE_XNU_FDT_H
#include "fdt.h"
#include "xnu_handoff.h"
struct ace_xnu_fdt_policy {
    struct ace_xnu_policy policy;
    struct ace_xnu_range reserved[256];
    uint32_t deferred_cma_nodes;
};
enum ace_xnu_fdt_error {
    ACE_XNU_FDT_ARGUMENT=-32, ACE_XNU_FDT_FORMAT=-33,
    ACE_XNU_FDT_MEMORY=-34, ACE_XNU_FDT_RESERVE=-35,
    ACE_XNU_FDT_OVERLAP=-36
};
/* Build bounded memory exclusions from a SUCCESSFULLY opened immutable live
 * FDT. source/ram plus all caller.reserved (image/stack/workspace/records)
 * must fit declared memory; these caller spans are physical, not host VAs.
 * Caller must establish the pre-Linux native stage independently (argument1).
 * The output excludes FDT, initrd, firmware ranges, dynamic allocation domains,
 * source and every caller reserve from the WHOLE XNU RAM window.
 * Only two exact known Linux CMA declarations may remain uninstantiated.
 * No physical writes/probes; writes only the disjoint caller-owned output.
 * THIS IS NOT RAM ownership/DMA/coherence or full platform/ADT validation. */
int ace_xnu_fdt_policy(const struct ace_fdt *f,uint64_t fdt_pa,
    const struct ace_xnu_policy *caller,unsigned pre_linux_native,
    struct ace_xnu_fdt_policy *out);
#endif
