/* SPDX-License-Identifier: MIT */
#ifndef ACE_XNU_CPU_H
#define ACE_XNU_CPU_H
#include "xnu_handoff.h"

/* Fresh privileged snapshot taken on the boot CPU before loading. A saved
 * Android/host snapshot cannot establish the current native CPU state. */
struct ace_xnu_cpu_state {
    uint64_t current_el, sctlr, midr, mpidr, mmfr0, cntfrq, daif;
};
enum ace_xnu_cpu_error {
    ACE_XNU_CPU_ARGUMENT=-16, ACE_XNU_CPU_EL=-17,
    ACE_XNU_CPU_CONTROL=-18, ACE_XNU_CPU_MODEL=-19,
    ACE_XNU_CPU_AFFINITY=-20, ACE_XNU_CPU_MEMORY=-21,
    ACE_XNU_CPU_TIMER=-22, ACE_XNU_CPU_INTERRUPTS=-23
};
/* AArch64-only leaf. Caller supplies aligned, writable normal RAM for out.
 * No stack, MSR, MMIO, SMC or CPU-state changes. EL3 refuses without an output
 * store; EL1/EL2 read their active SCTLR. EL0 cannot read CurrentEL and may
 * trap: this MUST NOT be invoked from Android userspace. Only consume out
 * after a zero return; a trapped MRS may leave a partial snapshot. Firmware
 * traps remain the caller's privileged exception-handler responsibility. */
int ace_xnu_cpu_capture(struct ace_xnu_cpu_state *out);
/* Initial target is EL1, CPU affinity0, Cortex-A55, 40-bit/16K-capable,
 * all DAIF masked, MMU/D-cache/I-cache off, LE, exactly13MHz. A caller at EL2
 * must perform a separate reviewed transition and take a fresh EL1 snapshot.
 * Checks no FDT, firmware/DMA ownership, RAM coherence or secondary quiescence. */
int ace_xnu_cpu_check(const struct ace_xnu_cpu_state *state);
/* CPU gate before the existing bounded loader. No stores on a CPU refusal.
 * Still requires ALL xnu_handoff caller contracts, live FDT validation and
 * exclusive RAM ownership. These wrappers do not make an image deployable. */
int ace_xnu_prepare_cpu(const void *payload, size_t bytes,
    const struct ace_xnu_policy *policy, const struct ace_xnu_cpu_state *state,
    struct ace_xnu_plan *out);
int ace_xnu_materialize_cpu(const void *payload, size_t bytes,
    const struct ace_xnu_policy *policy, const struct ace_xnu_cpu_state *state,
    void *mapping, size_t mapped_bytes, struct ace_xnu_plan *out);
#endif
