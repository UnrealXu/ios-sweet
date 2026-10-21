/* SPDX-License-Identifier: MIT */
/* AAPCS64 leaf: no stack, no writes except the caller-owned snapshot. */
.text
.balign 4
.global ace_xnu_cpu_capture
.type ace_xnu_cpu_capture,%function
ace_xnu_cpu_capture:
    cbz x0, bad_argument
    tst x0, #7
    b.ne bad_argument
    mrs x1, CurrentEL
    cmp x1, #4
    b.eq at_el1
    cmp x1, #8
    b.ne bad_el
    mrs x2, SCTLR_EL2
    b captured_control
at_el1:
    mrs x2, SCTLR_EL1
captured_control:
    stp x1, x2, [x0]
    mrs x1, MIDR_EL1
    mrs x2, MPIDR_EL1
    stp x1, x2, [x0, #16]
    mrs x1, ID_AA64MMFR0_EL1
    mrs x2, CNTFRQ_EL0
    stp x1, x2, [x0, #32]
    mrs x1, DAIF
    str x1, [x0, #48]
    mov w0, #0
    ret
bad_argument:
    mov w0, #-16
    ret
bad_el:
    mov w0, #-17
    ret
.size ace_xnu_cpu_capture, .-ace_xnu_cpu_capture
.section .note.GNU-stack,"",%progbits
