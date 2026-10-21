/* TEST ONLY. Not linked into probe.Image. Fixed QEMU virt RAM addresses. */
.text
.global mmu_test_entry
mmu_test_entry:
    /* x0 remains the Linux loader's DTB argument. GDB installed L1 table. */
    dsb sy
    mov x1, #0x44               /* AttrIdx 0 = Normal, non-cacheable */
    msr MAIR_EL1, x1
    ldr x1, =0x41000000
    msr TTBR0_EL1, x1
    ldr x1, =0x200803019        /* IPS=40bit, EPD1=1, SH0=Inner,
                                 4K TG0, NC walks, T0SZ=25 (39bit VA) */
    msr TCR_EL1, x1
    isb
    tlbi VMALLE1
    dsb sy
    isb
    mrs x1, SCTLR_EL1
    orr x1, x1, #1
    msr SCTLR_EL1, x1
    isb
    /* This and target fetches now use the real identity map. */
    ldr x15, =0x40080000
    br x15
.ltorg
.section .note.GNU-stack,"",%progbits
