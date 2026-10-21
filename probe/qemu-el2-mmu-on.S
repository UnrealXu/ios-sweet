/* TEST ONLY. Never linked into probe.Image. Fixed QEMU virt RAM addresses.
 * EL2 TCR RES1/PS encoding agrees with Linux 5.10 arch/arm64/include/asm/kvm_arm.h. */
.text
.global mmu_test_entry
mmu_test_entry:
    dsb sy
    mov x1, #0x44               /* AttrIdx0 Normal non-cacheable */
    msr MAIR_EL2, x1
    ldr x1, =0x41000000
    msr TTBR0_EL2, x1
    ldr x1, =0x80823019         /* RES1[31,23], PS=40b, SH0=Inner,
                                  TG0=4K, NC walks, T0SZ=25 (39b VA) */
    msr TCR_EL2, x1
    isb
    tlbi ALLE2
    dsb sy
    isb
    mrs x1, SCTLR_EL2
    orr x1, x1, #1
    msr SCTLR_EL2, x1
    isb
    ldr x15, =0x40080000
    br x15
.ltorg
.section .note.GNU-stack,"",%progbits
