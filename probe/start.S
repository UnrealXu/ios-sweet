/* No absolute addresses, platform MMIO, SMC, PSCI or storage operations. */
.section .text.boot,"ax"
.global _start
_start:
    b entry
    .long 0
    .quad 0x80000                 /* Linux Image text_offset */
    .quad image_end - _start
    .quad 0                      /* little endian, unspecified page size */
    .quad 0, 0, 0
    .long 0x644d5241              /* ARM64 Image magic */
    .long 0
entry:
    mov x19, x0
    adr x20, diagnostic_record
    mov x1, #1
    str x1, [x20, #16]           /* stage: entry */
    str x19, [x20, #24]
    mrs x1, CurrentEL
    str x1, [x20, #32]
    cmp x1, #4
    b.eq el1
    cmp x1, #8
    b.eq el2
    /* EL3 rejected without touching SPSel, VBAR or EL1/EL2 control state. */
    mov x1, #2
    str x1, [x20, #16]
    b halt
el1:
    mrs x1, SCTLR_EL1
    str x1, [x20, #40]
    tbnz x1, #0, reject_mmu
    /* Accepted EL1, MMU off. Only here change our exception/stack state. */
    msr DAIFSet, #15
    msr SPSel, #1
    adr x1, stack_top
    mov sp, x1
    adr x1, vectors_el1
    msr VBAR_EL1, x1
    isb
    b collect
el2:
    mrs x1, SCTLR_EL2
    str x1, [x20, #40]
    tbnz x1, #0, reject_mmu
    /* SP with SPSel=1 at EL2 is SP_EL2; never write SP_EL1 here. */
    msr DAIFSet, #15
    msr SPSel, #1
    adr x1, stack_top
    mov sp, x1
    adr x1, vectors_el2
    msr VBAR_EL2, x1
    isb
collect:
    mov x1, #4
    str x1, [x20, #16]
    mov x0, x20
    bl probe_main
    mov x1, #5
    str x1, [x20, #16]
    b halt
reject_mmu:
    mov x1, #3
    str x1, [x20, #16]
halt:
    dsb sy
.global probe_halt
probe_halt:
    wfe
    b probe_halt

.balign 2048
vectors_el1:
.rept 16
    b exception_el1
    .balign 128
.endr

.balign 2048
vectors_el2:
.rept 16
    b exception_el2
    .balign 128
.endr
exception_el1:
    adr x9, diagnostic_record
    mrs x10, ESR_EL1
    str x10, [x9, #88]
    mrs x10, FAR_EL1
    str x10, [x9, #96]
    mrs x10, ELR_EL1
    str x10, [x9, #104]
    b exception_saved
exception_el2:
    adr x9, diagnostic_record
    mrs x10, ESR_EL2
    str x10, [x9, #88]
    mrs x10, FAR_EL2
    str x10, [x9, #96]
    mrs x10, ELR_EL2
    str x10, [x9, #104]
exception_saved:
    mov x10, #6
    str x10, [x9, #16]
    b halt

.section .data,"aw"
.balign 64
.global diagnostic_record
diagnostic_record:
    .ascii "ACEPROBE"
    .quad 2                    /* v2: control/fault fields use current EL */
    .zero 104

.section .bss,"aw",%nobits
.balign 16
    .skip 4096
stack_top:
.section .note.GNU-stack,"",%progbits
