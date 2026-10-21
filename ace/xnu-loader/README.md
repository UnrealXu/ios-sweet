# Ace XNU flat-segment handoff foundation

The real freestanding C implementation is `ace/xnu_handoff.c/.h`. It prepares
XNU8796 Revision2/Version2 BootArgs, copies pre-rebased kernel segments,
zeroes BSS, places ADT/BootArgs after the kernel and reports the physical entry
and BootArgs addresses. It is independent of the original Qualcomm sweet shim.

Host packing is now available in `tools/ace-mkpayload.py`, with a hash-bound
Ace ADT from `tools/ace-mkadt.py`. See `docs/ACE-XNU-PAYLOAD.zh-CN.md` for its
supported linked format and refusal cases. Neither tool proves kernel platform
provenance, physical RAM ownership or hardware execution.

The initial native CPU gate is `ace/xnu_cpu.c/.h`, with the privileged leaf
`ace/xnu_cpu_capture.S`. Take a fresh successful snapshot after entering EL1
and masking DAIF, then use `ace_xnu_prepare_cpu`/`ace_xnu_materialize_cpu`.
The wrappers check CPU state before calling the same bounded loader. They
require affinity0/Cortex-A55, the initial 40-bit/16K feature contract and13MHz,
LE, MMU/D-cache/I-cache off and all DAIF masked. They refuse EL2 rather than
perform a hidden transition. Full MPIDR affinity is checked because actual
Ace CPU indices vary in Aff1. EL0 cannot call this MRS helper safely.

CPU admission does not establish FDT validity, writable/executable RAM,
firmware/DMA ownership, secondary quiescence or cache coherence. Native Image
integration is in `ace/native-loader`; phone execution remains unverified.
See `docs/ACE-XNU-CPU.zh-CN.md` for the
real-observation/host/QEMU boundaries. The existing QEMU harness below still
uses its simulator-specific contract; it is not promoted to a phone loader.

`ace/fdt.c/.h` now indexes a bounded live DTB, and `ace/xnu_fdt.c/.h` builds
memory exclusions for the bounded loader. The caller must reserve the index,
stack, source and records outside the entire destination window. The output
policy has a self-pointer into its embedded reserve array; keep it at its
original address through materialization. See `docs/ACE-XNU-FDT.zh-CN.md`.
This checks memory declarations, not firmware/DMA ownership or the complete
CPU/GIC/timer/PSCI-to-ADT platform contract. The new C parser/policy was also
executed in a real phone EL0 process; the numeric policy replay does not prove
pre-Linux access to RAM. The native Image integration is a separate component.

`ace/xnu_platform.c/.h` now checks the initial CPU/GIC/timer/PSCI declarations
and canonical Ace ADT against that FDT. Its prepare/materialize wrappers gate
the same bounded copier before target writes; memory policy and fresh CPU
sampling remain separate caller requirements. See
`docs/ACE-XNU-PLATFORM-CHECK.zh-CN.md`. Phone EL0 execution verifies the pure
checker, including damaged-ADT refusal, without driving hardware or loading XNU.

`ace/native-loader` now executes these components and the real linked XNU
through16K bootstrap/first C instruction in QEMU. This synthetic-receiver
harness remains a unit fixture; see `docs/ACE-XNU-NATIVE-ENTRY.zh-CN.md`.

There is **no Ace hardware deployment or bootable iOS image** here. This
portable C component does not parse/rebase Mach-O or IMG4, construct an ADT,
initialize16K page tables, implement an XNU Ace platform,
start secondary CPUs or drive UFS/DSI/touch. The caller must establish those
prerequisites separately. ADT is treated as opaque bytes: copying it is not
proof its platform properties are correct or that XNU can initialize it.

The old sweet loader is unsuitable for Ace: it writes a Qualcomm framebuffer
address, trusts segment arithmetic/offsets and rounds copies to8-byte units.
The Ace implementation has no default physical address or framebuffer, checks
all ranges before writing, and copies exact file/BSS tails without rounded
source reads or destination overruns. Existing sweet and ace/entry sources and
their diagnostic baseline artifacts are unchanged.

## Contract

- Flat bundle magic is `ACEXNU01`, version1. All field offsets match the
  documented old SWEETXNU/v1 bundle layout; the old target magic is rejected.
  Header680bytes: magic8/version4/count4; virtBase,entryVA,ADT offset/length,
  page-rounded highest segment endVA,physBase,memSize (seven LE uint64);
  CommandLine608; then count×32byte segments (VA,memSize,fileOffset,fileSize).
-1..32segments, nonzero memory size, fileSize<=memSize, all file bytes inside
  actual input, no header/table/ADT alias, nonoverlapping destination spans.
  Entry must be4-byte aligned and backed by at least4file bytes, not BSS/gap.
- Explicit16K-aligned physical RAM window must match bundle physBase/memSize.
  Overflow, source/window overlap, and any reserved region anywhere in the
  whole XNU-managed window are rejected. Loader/stack/records belong in the
  caller-supplied reservations. No subtraction of holes or assumption that
  Linux MemAvailable constitutes physically free RAM.
- ADT follows the exact page-rounded highest kernel segment; BootArgs gets
  the next16K page, and topOfKernelData is its physical end. deviceTreeP is
  the corresponding VA, while the entry and incoming x0 are physical.
  Video fields remain zero. CommandLine must contain NUL within608bytes.
- `prepare` writes only its plan on success. `materialize` independently
  validates before copying any target byte and rejects host/mapped aliases
  of source, output and policy metadata. Caller provides a valid mapping of
  the entire exclusive destination window and honest physical source metadata.
  No MMIO, DMA, cache operation, register change, jump or storage command
  occurs inside the portable C component. Source and policy must remain stable
  throughout validation/materialization; no concurrent mutation is supported.

ABI offsets are statically asserted (736byte args; Video40,deviceTreeP96,
CommandLine108,bootFlags720). Host tests also compile the actual Boot_Video /
boot_args declarations extracted unchanged from the private cached XNU8796
build artifact and compare every field's offset. Artifact provenance is
research/ci-0081/provenance.json, successful prior CI39158169212; this test is
skipped when that private artifact is absent. No new full XNU build is implied.

## Execution verification

```sh
python3 -m unittest discover -s tests -p test_ace_xnu_handoff.py -v
python3 ace/xnu-loader/verify.py
```

The **QEMU-only** harness executes the same C materializer, performs explicit
DSB/I-cache invalidation, clears x1..x3 and branches with x0=BootArgs PA to an
independent **synthetic receiver, not XNU**. Simulator constants are only in
this harness: destination0x41000000,size256KiB, oneCPU/QEMU128MiB. Never copy
these addresses into the Ace profile or deploy this harness on a phone.

Five actual QEMU cases: EL1,EL2->EL1 and relocatedEL2 successfully reach the
copied receiver; entry-in-BSS and overlapping segments refuse. Receiver records
incoming x0..x3, EL1 and MMU/cache state, DT VA and topOfKernelData. Every case
compares the entire256KiB destination dump, covering precise non-eight-byte
file/BSS tails, untouched gaps, ADT, all BootArgs bytes and refusal/no-change.
The generated ADT is only a minimal syntactically shaped root-name fixture.
There is no hardware platform tree or XNU execution claim.

GDB binds loopback only;20s per-case host deadline and unconditional QEMU
cleanup. Builds/commands/raw RAM/source/Image/ELF/log hashes stay ignored in
research/ace-xnu-handoff-20261019; prior success is invalidated before a build,
stale dumps are removed and QEMU exits before log hashing. Optimized Python
verification refuses before modifying evidence. Earlier assembler/fixture
failures are development failures, not kernel failures; the first whole-RAM
fixture mismatch log is preserved privately.

Host regression tests cover malformed/truncated input, integer overflow,
source/reserved/mapping aliases, insufficient destination RAM and exact copies.
ASan+UBSan execute5000 bounded mutated/truncated payload cases and require
unchanged target RAM/output on every refusal. ARM64 freestanding compilation
must have no undefined libc/runtime symbols; byte loops avoid implicit
memcpy/memset dependencies with MMU off.
