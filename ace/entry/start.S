#include "entry_config.h"
/* Independent boot-entry foundation; no MTK MMIO, storage or XNU payload. */
.section .text.boot,"ax"
.global _start
_start:
    b bridge_entry
    .long 0
    .quad 0x80000
    .quad image_end - _start
    .quad 8                    /* LE, unspecified page size, anywhere */
    .quad 0, 0, 0
    .long 0x644d5241
    .long 0
bridge_entry:
    mov x19, x0
    adr x20, bridge_record
    mov x1, #1
    str x1, [x20, #16]
    str x19, [x20, #24]
    mrs x1, CurrentEL
    str x1, [x20, #32]
    cmp x1, #8
    b.eq from_el2
    cmp x1, #4
    b.eq from_el1
    mov x1, #2
    b refuse
from_el2:
    mrs x1, SCTLR_EL2
    str x1, [x20, #40]
    tbnz x1, #0, bad_control  /* Require MMU and D-cache off, never turn off. */
    tbnz x1, #2, bad_control
    msr DAIFSet, #15
#if ACE_ENTRY_PMSG_ENABLED
    adr x0, pmsg_accepted_el2
    mov x1, #(pmsg_accepted_el2_end - pmsg_accepted_el2)
    bl bridge_pmsg_append
    adr x2, bridge_pmsg_results
    str w0, [x2]
#endif
    mov x1, #0x80000000        /* HCR.RW=1; no stage2, VHE or TGE. */
    msr HCR_EL2, x1
    mov x1, #0x33ff            /* ARMv8 CPTR_EL2 RES1, no FP/SIMD trap. */
    msr CPTR_EL2, x1
    mov x1, #3
    msr CNTHCTL_EL2, x1
    msr CNTVOFF_EL2, xzr
    mov x1, #0x0800
    movk x1, #0x30d0, lsl #16 /* SCTLR_EL1 RES1; M/C/I=0, LE. */
    msr SCTLR_EL1, x1
    adr x1, at_el1
    msr ELR_EL2, x1
    mov x1, #0x3c5           /* Mask DAIF, EL1h; payload must own SP_EL1. */
    msr SPSR_EL2, x1
    isb
    eret
from_el1:
    mrs x1, SCTLR_EL1
    str x1, [x20, #40]
    tbnz x1, #0, bad_control
    tbnz x1, #2, bad_control
    msr DAIFSet, #15
#if ACE_ENTRY_PMSG_ENABLED
    adr x0, pmsg_accepted_el1
    mov x1, #(pmsg_accepted_el1_end - pmsg_accepted_el1)
    bl bridge_pmsg_append
    adr x2, bridge_pmsg_results
    str w0, [x2]
#endif
at_el1:
    mrs x1, CurrentEL
    str x1, [x20, #48]
    mrs x1, SCTLR_EL1
    str x1, [x20, #56]
    mov x1, #4
    str x1, [x20, #16]
#if ACE_ENTRY_PMSG_ENABLED
    adr x0, pmsg_payload_el1
    mov x1, #(pmsg_payload_el1_end - pmsg_payload_el1)
    bl bridge_pmsg_append
    adr x2, bridge_pmsg_results
    str w0, [x2, #4]
#endif
    mov x0, x19
    mov x1, xzr
    mov x2, xzr
    mov x3, xzr
    adr x16, bridge_payload
    dsb sy
    br x16
bad_control:
    mov x1, #3
refuse:
    str x1, [x20, #16]
    dsb sy
.global bridge_halt
bridge_halt:
    wfe
    b bridge_halt

#if ACE_ENTRY_PMSG_ENABLED
#include "pmsg.S"
#endif

.balign 64
.global bridge_record
bridge_record:
    .ascii "ACEENTRY"
    .quad 1
    .zero 48
.balign 4096
.global bridge_payload
bridge_payload:
    .incbin "probe.Image"
image_end:
.section .note.GNU-stack,"",%progbits
