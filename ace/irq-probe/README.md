# QEMU GICv3 / virtual timer diagnostic

This independent single-CPU cold-boot Image initializes a **QEMU virt** GICv3
and receives exactly three generic virtual timer PPI27 interrupts at EL1.
It also tests EL2 entry with ICC_SRE_EL2.SRE/Enable, ERET to EL1 and
ICC_SRE_EL1, plus relocation, a disabled-timer deadline and BRK exception.
It does not modify the existing entry/probe Images or their baseline cases.

```sh
./ace/irq-probe/build.sh
python3 ace/irq-probe/verify.py
```

Requires GNU AArch64 tools, QEMU and gdb-multiarch. All output is ignored under
`research/ace-irq-probe-20261019`. Five cases run one CPU, 128MiB, networking
and serial disabled, loopback-only GDB, with a15-second host deadline each.
CPU counter deadlines bound redistributor wakeup and IRQ polling to about200ms.
QEMU MMIO accesses themselves and synchronous traps to EL2 are bounded by the
host deadline, not a recoverable hardware bus timeout.

Only an explicit `QEMU_VIRT_ONLY` build is accepted. GICD0x08000000 and
GICR0x080a0000 are **simulator constants**, never Ace addresses. The actual
Ace profile/live-DT reports GICD0x0c000000/GICR0x0c040000, PPI27 and13MHz;
this diagnostic does not run those addresses or establish their hardware
behavior. No phone transport, deploy command, storage, SMC or reset is provided.

The probe requires active MMU/D-cache off, masks DAIF, owns its stack/vectors,
programs nonsecure Group1 with ARE, wakes the single redistributor, sets the
private interrupt group and enables only PPI27. It sets ICC_CTLR_EL1.EOImode=0,
PMR/BPR/group enable. Every interrupt reads IAR1 and handles/EOIs **only27**;
an unexpected ID stops without EOI. It does not preserve a running Linux GIC
or timer context and must never be entered as a live-kernel callback. It does
not initialize an SMP topology or implement a reusable production GIC driver.
Distributor initialization is valid only for this reset/cold-boot QEMU model.

Timer period is CNTFRQ/100 ticks; all deadlines use CNTVCT. Successful cases
require three increasing IRQ timestamps, each period at least CNTFRQ/100,
three completed EOIR writes, resulting EL1, and INTID27. QEMU currently reports
62500000Hz, unlike Ace; verifier requires a nonzero actual register result and
uses that value for all comparisons. The last IRQ disables the timer before
EOI; normal completion masks IRQ and leaves the timer disabled. No previous
timer state reuse is claimed.

`ACEIRQ01` record is176bytes, 22 little-endian uint64 words: magic; stage;
incoming CurrentEL; active CurrentEL; IRQ count; CNTFRQ; start/end CNTVCT;
last IAR INTID; ESR/ELR/FAR; reserved; ICC_SRE_EL1/EL2 readback; GICD_CTLR;
GICR_WAKER; last IRQ CNTVCT; three individual IRQ timestamps; EOI count.
Stages2=waiting,5=three IRQs,6=counter deadline,7=entry refusal,
8=unexpected interrupt,9=synchronous/unhandled-vector exception.
RAM records have no cross-reset guarantee. Ordinary GDB dumps, actual commands,
source/Image/ELF/log hashes are retained in `verification.json`; QEMU is stopped
before hashing its log. Optimized Python verification is explicitly refused.
EL0/EL3, active-MMU/cache refusal, big-endian entry and unexpected real IRQs
are not tested. No Ace interrupt delivery, SMP, XNU or iOS claim follows.
