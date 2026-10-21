/* Diagnostic prefix only; forwards the byte-identical stock kernel.
 * Incoming EL/MMU/cache/GIC/timer state is not changed. No stack or SMC.
 * Optional logger uses explicit exclusive reserved RAM; not a phone default. */
#ifndef CHAIN_PMSG
#define CHAIN_PMSG 0
#endif
.section .text.boot,"ax"
.global _start
_start:
 b chain_entry
 .long 0
 .quad 0 /* Preserve exact stock Image text_offset=0, 2MiB alignment. */
 .quad chain_image_end-_start
 .quad 0xa /* Exact stock flags: LE/4K/anywhere. */
 .quad 0,0,0
 .long 0x644d5241
 .long 0
chain_entry:
 mov x24,x0
 mov x25,x1
 mov x26,x2
 mov x27,x3
 mov x28,x30
 adr x19,chain_record
 mov x4,#1
 str x4,[x19,#8]
 str x0,[x19,#16]
 mrs x4,CurrentEL
 str x4,[x19,#24]
 cmp x4,#8
 b.eq control_el2
 cmp x4,#4
 b.ne forward
 mrs x5,SCTLR_EL1
 b record_control
control_el2:
 mrs x5,SCTLR_EL2
record_control:
 str x5,[x19,#32]
 mrs x4,MIDR_EL1
 str x4,[x19,#40]
 mrs x4,ID_AA64MMFR0_EL1
 str x4,[x19,#48]
 mrs x4,CNTFRQ_EL0
 str x4,[x19,#56]
 adrp x16,stock_payload
 add x16,x16,:lo12:stock_payload
 str x16,[x19,#72]
#if CHAIN_PMSG
 /* The shared logger checks its local code span. Independently exclude the
  * ENTIRE large stock payload from the fixed ring before calling it. */
 adrp x4,_start
 add x4,x4,:lo12:_start
 adrp x5,chain_image_end
 add x5,x5,:lo12:chain_image_end
 movz x6,#(ACE_ENTRY_PMSG_ADDRESS & 0xffff)
 movk x6,#((ACE_ENTRY_PMSG_ADDRESS >> 16) & 0xffff),lsl#16
 movk x6,#((ACE_ENTRY_PMSG_ADDRESS >> 32) & 0xffff),lsl#32
 movk x6,#((ACE_ENTRY_PMSG_ADDRESS >> 48) & 0xffff),lsl#48
 mov x7,#ACE_ENTRY_PMSG_BYTES
 adds x7,x7,x6
 b.cs ring_alias
 cmp x6,x5
 b.hs append
 cmp x7,x4
 b.hi ring_alias
append:
 adr x0,chain_text
 mov x1,#chain_text_end-chain_text
 bl bridge_pmsg_append
 sxtw x4,w0
 str x4,[x19,#64]
 cbnz w0,forward
 mov x0,x19
 mov x1,#80
 bl bridge_pmsg_append
 sxtw x4,w0
 str x4,[x19,#64]
 b forward
ring_alias:
 mov x4,#-2
 str x4,[x19,#64]
#endif
forward:
 adrp x16,stock_payload
 add x16,x16,:lo12:stock_payload
 str x16,[x19,#72]
 mov x4,#2
 str x4,[x19,#8]
 mov x0,x24
 mov x1,x25
 mov x2,x26
 mov x3,x27
 mov x30,x28
 dsb sy
.global chain_jump
chain_jump:
 br x16
#if CHAIN_PMSG
/* Shared leaf uses ADR image_end, so bind it to the small PREFIX code span.
 * Full-image exclusion is enforced above; original entry source is untouched. */
#define image_end chain_code_end
#include "../entry/pmsg.S"
#undef image_end
chain_text:
 .ascii "ACECHAIN1:" CHAIN_TOKEN ": forwarding original Android kernel\n"
chain_text_end:
#endif
.balign 64
.global chain_record
chain_record:
 .ascii "ACECHN01"
 .zero 56
 .quad -9 /* Logger disabled/not attempted. */
 .quad 0
chain_code_end:
.balign 0x200000
.global stock_payload
stock_payload:
 .incbin "stock.Image"
.balign 4096,0
.global chain_image_end
chain_image_end:
.section .note.GNU-stack,"",%progbits
