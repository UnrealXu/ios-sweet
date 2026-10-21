// Register-only diagnostic. Build output requires independent validation.
#include <linux/init.h>
#include <linux/module.h>
#include <linux/printk.h>

static int __init ace_read_regs_init(void)
{
    unsigned long midr, mmfr0, cntfrq;
    /* No writes to system registers, MMIO, memory maps, or device/storage state.
     * These samples describe the CPU executing module_init, not all CPUs. */
    asm volatile("mrs %0, MIDR_EL1" : "=r" (midr));
    asm volatile("mrs %0, ID_AA64MMFR0_EL1" : "=r" (mmfr0));
    asm volatile("mrs %0, CNTFRQ_EL0" : "=r" (cntfrq));
    pr_info("ACE_READ_REGS: MIDR_EL1=%#lx ID_AA64MMFR0_EL1=%#lx CNTFRQ_EL0=%lu\n",
            midr, mmfr0, cntfrq);
    return 0;
}
static void __exit ace_read_regs_exit(void) {}
module_init(ace_read_regs_init);
module_exit(ace_read_regs_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Read three CPU identification/timer registers only");
