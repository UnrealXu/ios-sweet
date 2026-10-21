#include <stddef.h>
#include <asm/signal.h>
#include <asm/siginfo.h>
_Static_assert(sizeof(struct sigaction)==32, "raw AArch64 kernel sigaction");
_Static_assert(offsetof(struct sigaction,sa_flags)==8, "flags");
_Static_assert(offsetof(struct sigaction,sa_mask)==24, "mask");
_Static_assert(offsetof(siginfo_t,si_code)==8, "si_code");
_Static_assert(offsetof(siginfo_t,si_addr)==16, "fault address");
_Static_assert(sizeof(sigset_t)==8, "kernel sigset");
_Static_assert(SA_SIGINFO==4 && SIGILL==4, "signal constants");
