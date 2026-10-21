/* Synthetic entry-contract receiver, NOT XNU. PC-relative after copying. */
.section .text,"ax"
.global payload_entry
payload_entry:
 adr x19,payload_record
 str x0,[x19]
 str x1,[x19,#8]
 str x2,[x19,#16]
 str x3,[x19,#24]
 mrs x4,CurrentEL
 str x4,[x19,#32]
 mrs x4,SCTLR_EL1
 str x4,[x19,#40]
 ldr x4,[x0,#96]
 str x4,[x19,#48]
 ldr x4,[x0,#32]
 str x4,[x19,#56]
 dsb sy
.global payload_halt
payload_halt:
 wfe
 b payload_halt
.balign 4096
.global payload_record
payload_record:
 .zero 64
