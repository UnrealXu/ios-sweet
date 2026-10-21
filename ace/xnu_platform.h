/* SPDX-License-Identifier: MIT */
#ifndef ACE_XNU_PLATFORM_H
#define ACE_XNU_PLATFORM_H
#include "fdt.h"
#include "xnu_cpu.h"
enum ace_xnu_platform_error {
    ACE_XNU_PLATFORM_ARGUMENT=-40, ACE_XNU_PLATFORM_CPUS=-41,
    ACE_XNU_PLATFORM_GIC=-42, ACE_XNU_PLATFORM_TIMER=-43,
    ACE_XNU_PLATFORM_PSCI=-44, ACE_XNU_PLATFORM_ADT=-45, ACE_XNU_PLATFORM_UFS=-46
};
/* Read-only initial Ace contract: eight described CPU affinities/models,
 * GICv3, all four timer specs/provider, 13MHz, PSCI/SMC; compare the supplied
 * ADT with the canonical single-CPU Ace tree derived from these values/RAM.
 * Only the64 random-seed bytes are opaque; they are not entropy-validated.
 * Optional root UFS probe profile additionally requires exact live FDT
 * address translation, enabled controller and GIC SPI169 resources.
 * Canonical ADT ordering/phandles are deliberately fixed for each profile.
 * Does not touch a controller, measure clocks, invoke PSCI, or prove ownership.
 * Requires a successfully opened immutable FDT and stable ADT buffers. */
int ace_xnu_platform_check(const struct ace_fdt *f,const void *adt,size_t bytes,
    struct ace_xnu_range ram);
/* Caller supplies the freshly FDT-derived memory policy and CPU snapshot,
 * plus ALL native loader ownership/coherence/quiescence contracts. Plan and
 * destination stay unchanged on a platform refusal. No native entry/flash. */
int ace_xnu_prepare_platform(const void *payload,size_t bytes,
    const struct ace_xnu_policy *policy,const struct ace_xnu_cpu_state *cpu,
    const struct ace_fdt *f,struct ace_xnu_plan *out);
int ace_xnu_materialize_platform(const void *payload,size_t bytes,
    const struct ace_xnu_policy *policy,const struct ace_xnu_cpu_state *cpu,
    const struct ace_fdt *f,void *mapping,size_t mapped_bytes,
    struct ace_xnu_plan *out);
#endif
