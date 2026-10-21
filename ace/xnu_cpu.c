/* SPDX-License-Identifier: MIT */
#include "xnu_cpu.h"
_Static_assert(sizeof(struct ace_xnu_cpu_state)==56,"capture ABI size");
_Static_assert(offsetof(struct ace_xnu_cpu_state,daif)==48,"capture ABI tail");

int ace_xnu_cpu_check(const struct ace_xnu_cpu_state *s) {
    if(!s) return ACE_XNU_CPU_ARGUMENT;
    if(s->current_el!=4) return ACE_XNU_CPU_EL;
    /* Check the active EL1 SCTLR; never switch off a live mapping/cache. */
    if(s->sctlr & ((1ULL<<0)|(1ULL<<2)|(1ULL<<12)|(1ULL<<25)))
        return ACE_XNU_CPU_CONTROL;
    /* ARM implementor/architecture/part; variant and revision may differ. */
    if((s->midr & 0xff0ffff0ULL)!=0x410fd050ULL || s->midr>>32)
        return ACE_XNU_CPU_MODEL;
    /* Aff0 alone is insufficient: actual Ace core numbers occupy Aff1. */
    if((s->mpidr & 0xff00ffffffULL) || (s->mpidr & ~0xffc1ffffffULL))
        return ACE_XNU_CPU_AFFINITY;
    unsigned pa=(unsigned)(s->mmfr0 & 15), gran=(unsigned)((s->mmfr0>>20)&15);
    /* Deliberately retain the observed 16K encoding1; unknown future formats
     * need a reviewed bootstrap contract, not guessed support. */
    if(pa<2 || pa>6 || gran!=1) return ACE_XNU_CPU_MEMORY;
    if(s->cntfrq!=13000000) return ACE_XNU_CPU_TIMER;
    if((s->daif & 0x3c0)!=0x3c0) return ACE_XNU_CPU_INTERRUPTS;
    return 0;
}
static int check(const struct ace_xnu_policy *p,const struct ace_xnu_cpu_state *s) {
    int rc=ace_xnu_cpu_check(s);if(rc) return rc;
    if(!p) return ACE_XNU_CPU_ARGUMENT;
    /* The initial Ace RAM contract is bounded to the observed40-bit PA,
     * irrespective of what a substituted feature value might advertise. */
    const uint64_t limit=1ULL<<40;
    if(p->ram.base>=limit || p->ram.size>limit-p->ram.base)
        return ACE_XNU_RANGE;
    return 0;
}
int ace_xnu_prepare_cpu(const void *b,size_t n,const struct ace_xnu_policy *p,
    const struct ace_xnu_cpu_state *s,struct ace_xnu_plan *out) {
    int rc=check(p,s);if(rc) return rc;
    return ace_xnu_prepare(b,n,p,out);
}
int ace_xnu_materialize_cpu(const void *b,size_t n,const struct ace_xnu_policy *p,
    const struct ace_xnu_cpu_state *s,void *mapping,size_t mapped,
    struct ace_xnu_plan *out) {
    int rc=check(p,s);if(rc) return rc;
    /* state is consumed before any materialization; no later state reads. */
    return ace_xnu_materialize(b,n,p,mapping,mapped,out);
}
