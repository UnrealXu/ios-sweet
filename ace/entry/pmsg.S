/* Included only by explicit experimental build. Ordinary caller-owned RAM,
 * ECC=0/type-sig=0, single writer; no stack, MMIO, SMC, reset or allocation.
 * x0=static image-local text, x1=length; returns w0=status. x19/x20 untouched. */
bridge_pmsg_append:
    mrs x4, CurrentEL
    cmp x4, #8
    b.eq pmsg_control_el2
    cmp x4, #4
    b.ne pmsg_bad_control
    mrs x4, SCTLR_EL1
    b pmsg_control_check
pmsg_control_el2:
    mrs x4, SCTLR_EL2
pmsg_control_check:
    tbnz x4, #0, pmsg_bad_control
    tbnz x4, #2, pmsg_bad_control
    tbnz x4, #25, pmsg_bad_control  /* Header LDR/STR assumes LE. */
    movz x9, #(ACE_ENTRY_PMSG_ADDRESS & 0xffff)
    movk x9, #((ACE_ENTRY_PMSG_ADDRESS >> 16) & 0xffff), lsl #16
    movk x9, #((ACE_ENTRY_PMSG_ADDRESS >> 32) & 0xffff), lsl #32
    movk x9, #((ACE_ENTRY_PMSG_ADDRESS >> 48) & 0xffff), lsl #48
    movz x10, #(ACE_ENTRY_PMSG_BYTES & 0xffff)
    movk x10, #((ACE_ENTRY_PMSG_BYTES >> 16) & 0xffff), lsl #16
    adds x5, x9, x10
    b.cs pmsg_bad_address
    adr x6, _start
    adr x7, image_end
    cmp x9, x7
    b.hs pmsg_no_image_alias
    cmp x5, x6
    b.hi pmsg_bad_address
pmsg_no_image_alias:
    sub x10, x10, #12
    ldr w4, [x9]
    movz w5, #0x4244
    movk w5, #0x4347, lsl #16
    cmp w4, w5
    b.ne pmsg_bad_header
    ldr w11, [x9, #4]
    ldr w12, [x9, #8]
    cmp x12, x10
    b.hi pmsg_bad_header
    cmp x11, x12
    b.hi pmsg_bad_header
    cbz x1, pmsg_success
    cmp x11, x10
    b.hs pmsg_bad_state
    cmp x12, x10
    b.eq pmsg_canonical
    cmp x11, x12
    b.ne pmsg_bad_state
pmsg_canonical:
    cmp x1, x10
    csel x8, x1, x10, lo      /* retained suffix size */
    sub x4, x1, x8
    add x14, x0, x4
    mov x13, x8
    mov x15, x11
    add x5, x9, #12
pmsg_copy:
    ldrb w4, [x14], #1
    strb w4, [x5, x15]
    add x15, x15, #1
    cmp x15, x10
    csel x15, xzr, x15, eq
    subs x13, x13, #1
    b.ne pmsg_copy
    add x6, x12, x8
    cmp x6, x10
    csel x6, x6, x10, lo
    str w15, [x9, #4]
    str w6, [x9, #8]
    dsb sy
pmsg_success:
    mov w0, #0
    ret
pmsg_bad_control:
    mov w0, #-1
    ret
pmsg_bad_address:
    mov w0, #-2
    ret
pmsg_bad_header:
    mov w0, #-3
    ret
pmsg_bad_state:
    mov w0, #-4
    ret
.balign 4
.global bridge_pmsg_results
bridge_pmsg_results:
    .long 0x7fffffff, 0x7fffffff /* not called; two successful writes yield0,0 */
pmsg_accepted_el1:
    .ascii "ACEENTRY accepted EL1\n"
pmsg_accepted_el1_end:
pmsg_accepted_el2:
    .ascii "ACEENTRY accepted EL2\n"
pmsg_accepted_el2_end:
pmsg_payload_el1:
    .ascii "ACEENTRY payload EL1\n"
pmsg_payload_el1_end:
