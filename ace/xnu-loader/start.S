/* QEMU-only execution harness for the portable loader. */
.section .text.boot,"ax"
.global _start
_start:
 b entry
 .long 0
 .quad 0x80000
 .quad image_end-_start
 .quad 8
 .quad 0,0,0
 .long 0x644d5241
 .long 0
entry:
 msr daifset,#15
 mrs x0,CurrentEL
 cmp x0,#8
 b.eq el2
 cmp x0,#4
 b.ne refused
 mrs x0,SCTLR_EL1
 tbnz x0,#0,refused
 tbnz x0,#2,refused
 b el1
el2:
 mrs x0,SCTLR_EL2
 tbnz x0,#0,refused
 tbnz x0,#2,refused
 mov x0,#0x80000000
 msr HCR_EL2,x0
 mov x0,#0x33ff
 msr CPTR_EL2,x0
 mov x0,#3
 msr CNTHCTL_EL2,x0
 msr CNTVOFF_EL2,xzr
 mov x0,#0x0800
 movk x0,#0x30d0,lsl#16
 msr SCTLR_EL1,x0
 adr x0,el1
 msr ELR_EL2,x0
 mov x0,#0x3c5
 msr SPSR_EL2,x0
 isb
 eret
el1:
 adr x0,stack_top
 mov sp,x0
 adr x0,vectors
 msr VBAR_EL1,x0
 isb
 bl loader_main
 b harness_halt
refused:
 adr x1,harness_record
 mov x0,#99
 str x0,[x1]
.global harness_halt
harness_halt:
 dsb sy
 wfe
 b harness_halt
.balign 2048
vectors:
 .rept 16
 b exception
 .space 124
 .endr
exception:
 adr x1,harness_record
 mov x0,#98
 str x0,[x1]
 mrs x0,ESR_EL1
 str x0,[x1,#8]
 b harness_halt
.global handoff_jump
handoff_jump:
 mov x16,x0
 mov x0,x1
 mov x1,xzr
 mov x2,xzr
 mov x3,xzr
 dsb sy
 ic iallu
 dsb sy
 isb
 br x16
.balign 16
.global harness_record
harness_record:
 .zero 32
.balign 16
.space 16384
stack_top:
.section .note.GNU-stack,"",%progbits
