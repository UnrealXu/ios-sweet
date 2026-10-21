.text
.global _start
_start:
 ldr x0,=stack_top
 mov sp,x0
 ldr x0,=vectors
 msr VBAR_EL1,x0
 isb
 bl test_main
 ldr x1,=exitargs
 str x0,[x1,#8]
 mov x0,#0x20
 hlt #0xf000
 b .
.balign 2048
vectors:
 .rept 16
 b trap
 .space 124
 .endr
trap:
 mov x0,#4
 ldr x1,=traptext
 hlt #0xf000
 b .
traptext: .asciz "TRAP_FAIL\n"
.bss
.balign 16
.space 32768
stack_top:

.data
.balign 8
exitargs: .quad 0x20026,0
