/* SPDX-License-Identifier: MIT */
/* Native EL1 Image, not an Android process or the synthetic QEMU receiver. */
#include "native_config.h"
.section .text.boot,"ax"
.global _start
_start:
    b native_entry
    .long 0
    .quad NATIVE_TEXT_OFFSET
    .quad image_end-_start
    .quad 8 /* LE, unspecified page size, relocatable Image. */
    .quad 0,0,0
    .long 0x644d5241
    .long 0
native_entry:
    mov x19,x0
    mrs x1,CurrentEL
    cmp x1,#4
    b.ne native_early_halt
    mrs x1,SCTLR_EL1
    tbnz x1,#0,native_early_halt
    tbnz x1,#2,native_early_halt
    tbnz x1,#12,native_early_halt
    tbnz x1,#25,native_early_halt
    /* Before any Image-data store, require reviewed low boot-program RAM,
     * page alignment and separation from the pinned incoming FDT mapping. */
    adr x1,_start
    tst x1,#0xfff
    b.ne native_early_halt
    mov x2,#0x40000000
    cmp x1,x2
    b.lo native_early_halt
    adrp x3,image_end
    add x3,x3,:lo12:image_end
    mov x2,#NATIVE_IMAGE_LIMIT
    cmp x3,x2
    b.hi native_early_halt
    movz x2,#(NATIVE_FDT_PA & 0xffff)
    movk x2,#((NATIVE_FDT_PA >> 16) & 0xffff),lsl#16
    cmp x19,x2
    b.ne native_early_halt
    add x4,x2,#0x200,lsl#12 /* max2MiB FDT mapping, before reading header */
    cmp x1,x4
    b.hs separate_fdt
    cmp x2,x3
    b.lo native_early_halt
separate_fdt:
    msr daifset,#15
    /* Exact BSS/stack clearing uses no stack or implicit runtime helper. */
    adrp x1,__bss_start
    add x1,x1,:lo12:__bss_start
    adrp x2,__bss_end
    add x2,x2,:lo12:__bss_end
1:  cmp x1,x2
    b.hs 2f
    strb wzr,[x1],#1
    b 1b
2:  msr SPSel,#1
    adrp x1,stack_top
    add x1,x1,:lo12:stack_top
    mov sp,x1
    adrp x1,native_vectors
    add x1,x1,:lo12:native_vectors
    msr VBAR_EL1,x1
    isb
    mov x0,x19
    bl native_main
#if NATIVE_REFUSAL_ANDROID
    /* Only a normal native_main refusal may forward to the stock kernel.
     * Early entry gates and exceptions always retain their halt paths. */
    mov x0,x19
    bl native_refusal_android
#endif
    b native_halt
.global native_early_halt
native_early_halt:
    wfe
    b native_early_halt
.global native_halt
native_halt:
    dsb sy
    /* The phone's EL3 watchdog dump retains PC/LR/SP even when pstore RAM
     * is lost. Encode the completed stage and negative refusal code in PC,
     * without changing SP or touching any extra RAM/MMIO. This is diagnostic
     * evidence only: none of these slots means that XNU executed. */
    adrp x0,native_record
    add x0,x0,:lo12:native_record
    ldp x1,x2,[x0,#16] /* stage, signed error */
#if NATIVE_RAM_RESCUE
    /* Version2: stage9 is fallback-guard failure, distinct from the existing
     * stage8 exception/unknown bucket. Keep all record words and SP intact. */
    cmp x1,#7
    b.hi 3f
    ldr x3,[x0,#160] /* native_record[20], signed fallback guard result */
    tbz x3,#63,3f
    mov x1,#9
    mov x2,x3
    b 4f
3:
#endif
    cmp x1,#7
    mov x0,#8 /* exceptional/unknown stage bucket */
    csel x1,x1,x0,ls
4:
    neg x2,x2
    cmp x2,#127
    mov x0,#127 /* positive or out-of-range errors remain bounded */
    csel x2,x2,x0,ls
    add x2,x2,x1,lsl#7
    adr x0,native_halt_slots
    add x0,x0,x2,lsl#3
    br x0
.balign 8
.global native_halt_slots,native_halt_slots_end
native_halt_slots:
#if NATIVE_RAM_RESCUE
    .rept 10*128
#else
    .rept 9*128
#endif
    wfe
    b .-4
    .endr
native_halt_slots_end:
.balign 2048
native_vectors:
    .rept 16
    b native_exception
    .space 124
    .endr
native_exception:
    adrp x0,native_record
    add x0,x0,:lo12:native_record
    mov x1,#98
    str x1,[x0,#16]
    mov x1,#-80
    str x1,[x0,#24]
    mrs x1,ESR_EL1
    str x1,[x0,#160]
    mrs x1,FAR_EL1
    str x1,[x0,#168]
    mrs x1,ELR_EL1
    str x1,[x0,#176]
    mrs x1,SPSR_EL1
    str x1,[x0,#184]
    b native_halt
.global native_jump
native_jump:
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
.section .bss.stack,"aw",%nobits
.balign 16
.global stack_guard,stack_top
stack_guard:
    .space 64
    .space 65536
stack_top:
.section .note.GNU-stack,"",%progbits
