// Observe the running kernel's virtual timer and GICv3 CPU interface.
#include <linux/init.h>
#include <linux/module.h>
#include <linux/printk.h>
#include <asm/sysreg.h>

static int __init ace_irq_timer_init(void)
{
    unsigned long el, mpidr, daif, freq, first, last, ctl, sre;
    unsigned long gctl = 0, pmr = 0, group = 0, bpr = 0;
    asm volatile("mrs %0, CurrentEL" : "=r" (el));
    asm volatile("mrs %0, MPIDR_EL1" : "=r" (mpidr));
    asm volatile("mrs %0, DAIF" : "=r" (daif));
    asm volatile("mrs %0, CNTFRQ_EL0" : "=r" (freq));
    asm volatile("isb; mrs %0, CNTVCT_EL0" : "=r" (first) :: "memory");
    ctl = read_sysreg_s(SYS_CNTV_CTL_EL0);
    sre = read_sysreg_s(SYS_ICC_SRE_EL1);
    /* Without SRE, do not access the other GIC system registers. Never read
     * IAR (acknowledges IRQs) or write timer/GIC registers or controller MMIO.
     * The caller pins insmod to one CPU; otherwise migration is possible. */
    if (sre & 1) {
        gctl = read_sysreg_s(SYS_ICC_CTLR_EL1);
        pmr = read_sysreg_s(SYS_ICC_PMR_EL1);
        group = read_sysreg_s(SYS_ICC_IGRPEN1_EL1);
        bpr = read_sysreg_s(SYS_ICC_BPR1_EL1);
    }
    asm volatile("isb; mrs %0, CNTVCT_EL0" : "=r" (last) :: "memory");
    pr_info("ACE_IRQ_TIMER: el=%lu mpidr=%lx daif=%lx freq=%lu first=%llu last=%llu ctl=%lx sre=%lx gctl=%lx pmr=%lx group=%lx bpr=%lx\n",
            el >> 2, mpidr, daif, freq, (unsigned long long)first,
            (unsigned long long)last, ctl, sre, gctl, pmr, group, bpr);
    return 0;
}
static void __exit ace_irq_timer_exit(void) {}
module_init(ace_irq_timer_init);
module_exit(ace_irq_timer_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Read virtual timer and GICv3 CPU interface state; never acknowledge IRQs");
