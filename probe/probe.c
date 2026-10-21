/* Freestanding, single-CPU register collection after accepted EL1/EL2 entry. */
typedef unsigned long long u64;
struct record {
    u64 magic, version, stage, entry_x0, current_el, sctlr;
    u64 mpidr, mmfr0, cntfrq, tcr, tgran16;
    u64 esr, far, elr, supports_16k;
};
_Static_assert(sizeof(struct record) == 120, "record layout");
#define READ_SYS(r, dst) __asm__ volatile("mrs %0, " #r : "=r"(dst))
void probe_main(volatile struct record *r)
{
    u64 mmfr0;
    READ_SYS(MPIDR_EL1, r->mpidr);
    READ_SYS(ID_AA64MMFR0_EL1, mmfr0);
    r->mmfr0 = mmfr0;
    READ_SYS(CNTFRQ_EL0, r->cntfrq);
    if (r->current_el == 8)
        READ_SYS(TCR_EL2, r->tcr);
    else
        READ_SYS(TCR_EL1, r->tcr);
    r->tgran16 = (mmfr0 >> 20) & 15;
    r->supports_16k = r->tgran16 == 1 || r->tgran16 == 2;
}
