/* SPDX-License-Identifier: MIT
 * Static Linux/AArch64 EL0 probe. Requires the caller to pin CPU0. Only the
 * process's own BSS is written. SIGILL is attributed to the exact test PC;
 * the handler exits without returning to or skipping the faulting instruction.
 * Syscalls: getcpu168, rt_sigaction134, write64, exit93. No privileged access.
 */
.macro address reg, label
    adrp \reg, \label
    add \reg, \reg, :lo12:\label
.endm
.macro report label, end, status
    mov x0, #1
    address x1, \label
    mov x2, #(\end - \label)
    mov x8, #64
    svc #0
    mov x0, #\status
    mov x8, #93
    svc #0
    brk #0
.endm
.section .text
.balign 4
.global _start
_start:
    address x0, cpu_number
    mov x1, xzr
    mov x2, xzr
    mov x8, #168
    svc #0
    cbnz x0, setup_failed
    address x0, cpu_number
    ldr w1, [x0]
    cbnz w1, wrong_cpu
    mov x0, #4                /* SIGILL */
    address x1, action
    mov x2, xzr
    mov x3, #8                /* kernel sigset_t */
    mov x8, #134
    svc #0
    cbnz x0, setup_failed
    address x0, scratch
    mov w1, #0x1234
    str w1, [x0, #16]
.global stlur_probe_instruction
stlur_probe_instruction:
    .inst 0x9901001f           /* STLUR WZR,[X0,#16], FEAT_LRCPC2 */
    ldr w1, [x0, #16]
    cbnz w1, store_failed
    report supported, supported_end, 0

ill_handler:
    cmp x0, #4
    b.ne unexpected_ill
    cbz x1, unexpected_ill
    ldr w2, [x1, #8]         /* positive kernel-generated si_code */
    cmp w2, #0
    b.le unexpected_ill
    ldr x3, [x1, #16]        /* AArch64 siginfo_t.si_addr */
    address x4, stlur_probe_instruction
    cmp x3, x4
    b.ne unexpected_ill
    report unsupported, unsupported_end, 3
setup_failed:
    report setup, setup_end, 2
wrong_cpu:
    report wrong, wrong_end, 5
store_failed:
    report store_error, store_error_end, 6
unexpected_ill:
    report unexpected, unexpected_end, 7
.section .rodata
.balign 8
action:
    .quad ill_handler, 4, 0, 0 /* handler, SA_SIGINFO, restorer, empty mask */
supported: .ascii "ACEISA CPU0 STLUR executed and own-buffer store verified\n"
supported_end:
unsupported: .ascii "ACEISA CPU0 STLUR SIGILL attributed to exact instruction\n"
unsupported_end:
setup: .ascii "ACEISA setup failed; no instruction result\n"
setup_end:
wrong: .ascii "ACEISA not on CPU0; no instruction result\n"
wrong_end:
store_error: .ascii "ACEISA store comparison failed\n"
store_error_end:
unexpected: .ascii "ACEISA unrelated SIGILL; no instruction result\n"
unexpected_end:
.section .bss
.balign 16
scratch: .skip 32
cpu_number: .skip 4
.section .note.GNU-stack,"",%progbits
