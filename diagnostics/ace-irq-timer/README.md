# Ace GICv3 / virtual timer observation

Normal GPL module for the exact running Android kernel. It reads CurrentEL,
MPIDR, DAIF, CNTFRQ, CNTVCT twice, CNTV_CTL and ICC_SRE. Only if SRE is enabled
it also reads ICC_CTLR/PMR/IGRPEN1/BPR1. It never reads ICC_IAR (which would
acknowledge an IRQ), writes a system register, maps MMIO or programs a timer.
Ordinary printk/tracing/module allocation/SCS still write kernel RAM and logs.
This is not a baremetal interrupt-delivery test or an iOS kernel.

Kbuild retains the original CFI/LTO/SCS/PAC/BTI configuration, authentic
module_layout/printk CRCs, and restores the original prepared Module.symvers.
The build first verifies8830 exact headers and430 scripts. Private artifacts
and all actual device identifiers stay under ignored research/.

```sh
python3 diagnostics/ace-irq-timer/rebuild.py --output research/ace-irq-timer-live-20261019/new-module
python3 diagnostics/ace-irq-timer/qemu.py research/ace-irq-timer-live-20261019/new-module/ace_irq_timer.ko --output research/ace-irq-timer-live-20261019/new-qemu
# Without the explicit flag live.py performs preflight only.
python3 diagnostics/ace-irq-timer/live.py --module research/ace-irq-timer-live-20261019/new-module/ace_irq_timer.ko --qemu-result research/ace-irq-timer-live-20261019/new-qemu/result.json --output research/ace-irq-timer-live-20261019/new-phone --load-readonly-module
```

The runner validates module/source/QEMU hashes, exact model/kernel/slot,
root/Enforcing, online CPUs0-7, and the existing GICv3 arch_timer INTID27.
It runs eight ordinary insmod/rmmod pairs pinned to CPU0..7, checks unique
MPIDRs, unchanged boot ID and taint, progressing per-CPU Android timer IRQ
counts and temporary file/module cleanup. No force load, reboot or partition
operation is used. Optimized Python verification is explicitly refused.

Actual2026-10-19 results: normal QEMU load/unload PASS15.118s; then all eight
phone load/unload pairs PASS. All cores report EL1,13MHz, CNTV_CTL1,
ICC_SRE7, ICC_CTLR8400, PMRf0, IGRPEN1=1, BPR1=3. MPIDR values are
81000000,81000100,...81000700: **Aff1 varies and Aff0 is zero**. Future
boot/SMP code must match full affinity (mask0xff00ffffff),
not assume Aff0 is a linear CPU index. These are observations under Android;
they do not prove cold-boot CPU topology, secondary release or PSCI CPU_ON.

Module134816B SHA256:
6e19e1b09c6d57d02131716b9c36fd458e495bd47fafd068660415737dc69398.
Raw evidence: research/ace-irq-timer-live-20261019/phone-run1.
Initial result.json remains passed=false because an overly strict parser
required adjacent counter reads to differ. On13MHz hardware, three cores'
reads legitimately fall within the same tick. The corrected parser allows
equality within a sample, rejects backwards time, and requires progression
between CPU samples; regression cases cover this and stale/malformed logs.
result-verified.json rechecks the SAME saved captures without rerunning the
module. Actual IRQ deltas across the measurement were870,644,418,528,463,415,
536,366. There was no new kernel failure and cleanup succeeded.

REA Ghidra review of this exact .ko init, evidence
`ev_4abd9b6776711ada83514d1bb6f4dee418c21c9fbcdeae3c1da7c43d55c3c935`,
corroborates the reads, SRE guard and printk-only external call. Its unknown
system-register labels are resolved independently against exact live headers
and llvm-objdump instruction encodings. SCS RAM stores are expected, not a
claim of zero RAM writes. Closed snapshot: research/ace-irq-timer-live-20261019/
rea-module-snapshot.json.

Architectural register definitions/accessors are corroborated by the local
OEM headers and the upstream Linux5.10 primary sources:
[arch_gicv3.h](https://github.com/torvalds/linux/blob/v5.10/arch/arm64/include/asm/arch_gicv3.h),
[sysreg.h](https://github.com/torvalds/linux/blob/v5.10/arch/arm64/include/asm/sysreg.h).
The separate ace/irq-probe diagnostic actively initializes only QEMU virt
GICv3 and receives timer IRQs. Never enter that cold-boot probe through this
live module: it would overwrite Linux's GIC, timer and vector context.
