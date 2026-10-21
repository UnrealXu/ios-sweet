/* QEMU virt cold-boot ONLY. No phone deployment contract. */
#ifndef QEMU_VIRT_ONLY
#error Explicit QEMU-only configuration required
#endif
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
 adr x19, record
 mrs x0,CurrentEL
 str x0,[x19,#16]
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
 mov x0,#9
 msr ICC_SRE_EL2,x0
 isb
 mrs x0,ICC_SRE_EL2
 str x0,[x19,#112]
 mov x0,#0x80000000
 msr HCR_EL2,x0
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
 mrs x0,CurrentEL
 str x0,[x19,#24]
#ifdef TEST_BRK
 brk #0x51
#endif
 mov x0,#1
 msr ICC_SRE_EL1,x0
 isb
 mrs x0,ICC_SRE_EL1
 str x0,[x19,#104]
 /* Explicit QEMU virt GICv3 addresses, unrelated to MT6895. */
 movz x10,#0x0800,lsl#16
 mov w0,#0x12
 str w0,[x10]
 ldr w0,[x10]
 str x0,[x19,#120]
 movz x11,#0x080a,lsl#16
 ldr w0,[x11,#0x14]
 bic w0,w0,#2
 str w0,[x11,#0x14]
 mrs x0,CNTFRQ_EL0
 str x0,[x19,#40]
 cbz x0,refused
 mov x2,#5
 udiv x21,x0,x2
 mrs x1,CNTVCT_EL0
 add x21,x21,x1
1: ldr w0,[x11,#0x14]
 tbz w0,#2,2f
 mrs x1,CNTVCT_EL0
 cmp x1,x21
 b.lo 1b
 b timeout
2: str x0,[x19,#128]
 add x11,x11,#0x10,lsl#12
 mov w0,#-1
 str w0,[x11,#0x80] /* IGROUPR0: all private interrupts Group1NS */
 mov w0,#0x80
 strb w0,[x11,#0x41b] /* PPI27 priority */
 mov w0,#0x08000000
 str w0,[x11,#0x100] /* enable ONLY virtual timer PPI27 */
 dsb sy
 /* Wait for redistributor enable write completion with same counter bound. */
5: sub x12,x11,#0x10,lsl#12
 ldr w0,[x12]
 tbz w0,#3,6f
 mrs x0,CNTVCT_EL0
 cmp x0,x21
 b.lo 5b
 b timeout
6: msr ICC_CTLR_EL1,xzr /* EOImode=0: EOIR also deactivates our PPI. */
 mov x0,#255
 msr ICC_PMR_EL1,x0
 msr ICC_BPR1_EL1,xzr
 mov x0,#1
 msr ICC_IGRPEN1_EL1,x0
 isb
 mrs x0,CNTFRQ_EL0
 mov x1,#100
 udiv x20,x0,x1
 cbz x20,refused
 mrs x1,CNTVCT_EL0
 str x1,[x19,#48]
 add x0,x1,x20
 msr CNTV_CVAL_EL0,x0
#ifndef TEST_TIMEOUT
 mov x0,#1
 msr CNTV_CTL_EL0,x0
#endif
 isb
 mov x0,#2
 str x0,[x19,#8]
 msr daifclr,#2
3: ldr x0,[x19,#32]
 cmp x0,#3
 b.hs success
 mrs x0,CNTVCT_EL0
 cmp x0,x21
 b.lo 3b
 b timeout
success:
 msr daifset,#15
 msr CNTV_CTL_EL0,xzr
 mrs x0,CNTVCT_EL0
 str x0,[x19,#56]
 mov x0,#5
 b finish
timeout:
 msr daifset,#15
 msr CNTV_CTL_EL0,xzr
 mrs x0,CNTVCT_EL0
 str x0,[x19,#56]
 mov x0,#6
 b finish
refused:
 mov x0,#7
finish:
 str x0,[x19,#8]
 dsb sy
.global halt
halt:
 wfe
 b halt
.balign 2048
vectors:
 .rept 4
 b exception
 .space 124
 .endr
 b exception
 .space 124
 b irq
 .space 124
 .rept 10
 b exception
 .space 124
 .endr
irq:
 /* Main uses x19..x21; handler only x0..x3, saved explicitly. */
 stp x0,x1,[sp,#-32]!
 stp x2,x3,[sp,#16]
 mrs x0,ICC_IAR1_EL1
 str x0,[x19,#64]
 cmp x0,#27
 b.ne unexpected_irq
 msr CNTV_CTL_EL0,xzr
 ldr x1,[x19,#32]
 add x1,x1,#1
 str x1,[x19,#32]
 mrs x2,CNTVCT_EL0
 str x2,[x19,#136]
 sub x3,x1,#1
 add x3,x19,x3,lsl#3
 str x2,[x3,#144]
 add x2,x2,x20
 msr CNTV_CVAL_EL0,x2
 cmp x1,#3
 b.hs 4f
 mov x2,#1
 msr CNTV_CTL_EL0,x2
4: dsb sy
 msr ICC_EOIR1_EL1,x0
 isb
 ldr x1,[x19,#168]
 add x1,x1,#1
 str x1,[x19,#168]
 ldp x2,x3,[sp,#16]
 ldp x0,x1,[sp],#32
 eret
unexpected_irq:
 mov x0,#8
 b finish /* Never EOI an interrupt this probe does not own. */
exception:
 mrs x0,ESR_EL1
 str x0,[x19,#72]
 mrs x0,ELR_EL1
 str x0,[x19,#80]
 mrs x0,FAR_EL1
 str x0,[x19,#88]
 mov x0,#9
 b finish
.balign 64
.global record
record:
 .ascii "ACEIRQ01"
 .zero 168
.balign 16
.space 4096
stack_top:
