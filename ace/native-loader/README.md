# Native Ace EL1 Image

This is actual native-entry integration, separate from the synthetic receiver
in `ace/xnu-loader`. It embeds the checked Ace XNU payload, establishes its
stack/BSS/vectors, captures CPU state, checks live FDT memory/canonical ADT,
materializes the real kernel, then branches with x0=BootArgs PA and x1..x3=0.
Actual phone pmsg logs now prove XNU entry, C execution and virtual-memory
bootstrap. The seeded trial repeatedly panicked in `pe_init.c` progress-image
sizing with zero video dimensions. The builder now passes `-noprogress` while
BootArgs remain intentionally headless; this does not implement a display.
Usable iOS and MTK storage/display/touch are unfinished. The separate readonly
diagnostic image boots the exact Android kernel and exposes the prior-ring
marker counts; root, B-slot and installed boot/vendor hashes were checked.
Other refusals, early gates and exceptions remain separate cases.

With `--pmsg`, new builds record a fresh `ace_run` token in the manifest and
BootArgs; `--run-token` accepts exactly 16 lowercase hexadecimal digits for
reproducible fixtures. Patch0087 uses that token for an earliest XNU marker
before OSLAR. Images made before this change do not contain that token.
See `diagnostics/ace-early-entry/README.md` for its limits and trial rules.

```sh
python3 tools/ace-mknative.py KERNEL ACE_ADT_DIR NEW_RESEARCH_OUTPUT \
  --expected-kernel-sha256 EXACT_REVIEWED_SHA256 --fdt-pa 0x47c80000 --pmsg
python3 ace/native-loader/verify.py IMAGE_DIR KERNEL CAPTURED_FDT NEW_QEMU_OUTPUT
python3 ace/native-loader/verify_c_entry.py IMAGE_DIR KERNEL CAPTURED_FDT NEW_C_ENTRY_OUTPUT
```

The builder creates raw ARM64 Image/analysis ELF, not Android boot.img. It has
no transport/signing/flash/reboot operation. Verify kernel provenance using CI
evidence independently. The manifest retains hardware/iOS readiness=false.

Entry requires firmware-owned executable/writable/coherent Image RAM, EL1,
MMU/D-cache/I-cache/EE off, a4KiB-aligned Image contained in
`0x40000000..0x44000000`, and explicitly pinned incoming FDT PA. Before Image
data stores it checks numeric guards and separation from the maximum FDT span.
Ownership, secondary quiescence and DMA remain caller contracts. EL0 must not
invoke this privileged entry. EL2 is refused without a transition.

An optional `--refusal-android-image PATH --expected-android-sha256 SHA
--text-offset 0` profile embeds the exact current stock Android Image. On a
normal `native_main` refusal, it copies the incoming FDT into private aligned
Image RAM and adds `/chosen/ace,native-refusal`, then forwards the unchanged
Android kernel. The experimental boot image stays installed. This does not
restore a partition and is not used after an early entry gate, exception or
XNU hang. Android appearing through this path means the native loader refused
XNU, not that iOS ran.

The larger optional image uses the numerical window
`0x40000000..0x45000000`, below the captured LK `mb_kernel` allocation ending
at `0x47c80000`. Declared FDT exclusions, initrd separation and stock entry
alignment are still checked. This is not proof of firmware/DMA ownership or
of larger-image acceptance by the physical bootloader. Only the hash-pinned
current stock kernel and its existing ramdisk/boot configuration are intended.

The diagnostic property is 288 bytes: `ACEFALL1`, 16 ASCII token bytes plus
NUL and seven zero padding bytes, then the 256-byte little-endian native
record. Stage and signed error are record words 2 and 3. The immutable incoming
tree, kernel and pstore header are unchanged. The copy refuses duplicate
diagnostic properties, aliases and insufficient output capacity.

```sh
python3 ace/native-loader/verify_refusal.py IMAGE_DIR NEW_QEMU_OUTPUT
```

This executes two normal native refusals through the real stock kernel and
checks guest userspace readback, module load/unload and poweroff. Separate
alignment and firmware-alias cases must halt without building an output tree.
Run the full XNU load/relocation and C-entry verifiers on the same image too.

BSS/workspace/64KiB stack are included in image_size; BSS is explicitly
cleared and a low stack canary checked. EL1 vectors retain ESR/FAR/ELR/SPSR in
the Image record. Absolute data relocations/imports are refused. GCC can lower
strict-alignment aggregate initialization to memcpy; `memory.c` supplies the
real exact volatile-byte freestanding operation.

Optional pmsg assumes exclusive ordinary RAM with ECC0/type0. It preserves a
valid DBGC ring and refuses unknown headers. Its preparation/about-to-branch
markers do not prove XNU execution. Early failures leave only volatile Image
data; XNU replaces the native VBAR later. Physical entry, retention and earliest
XNU logging remain unverified. See [中文记录](../../docs/ACE-XNU-NATIVE-ENTRY.zh-CN.md).

`--init-empty-pmsg` requires `--pmsg` and adds an explicit lifecycle operation
after the live FDT/platform/range gates. It initializes only a wholly zero
64KiB zone, preserves valid rings, and refuses nonzero corrupt data. Exclusive
caller-owned ordinary RAM and ECC0/type0 remain prerequisites; a zero header
proves neither. The general ring codec still never initializes unknown
headers. Native record word23 retains the first signature/start bytes; word31
retains initialization1 or a negative seeding error. The seeded profile adds
an eighth actual-XNU-entry verifier case starting from a completely zero ring,
while corrupt-ring refusal and valid-ring preservation remain separate cases.

`--diagnostic-readout --prior-run-token TOKEN` is an explicit evidence image,
requiring the Android handoff and forbidding initialization. It deliberately
returns stage2/error-66 before preparing/copying/jumping to XNU, then reads
the FDT-declared exact pstore range without writing it. In this mode alone,
record words9..11 contain the old ring header, word23 its validation result,
word24 exact prior-marker count, word25 first chronological offset,
words26..30 the first40 marker bytes, and word31 the zone's nonzero-byte count.
The existing Android handoff exposes that record; this is not a partition
backup restoration. A missing marker does not prove XNU did not execute or
that the RAM survived reset. Do not count the literal marker in this image's
own readout code, or the verifier's explicitly synthetic positive fixture,
as execution evidence. Only preserved ring data with provenance is relevant.

`--auto-readout-after-reset` requires `--pmsg` and the pinned Android fallback;
it cannot combine with readout-only mode. Before jumping, the loader appends
an exact token-bound `ACETRIAL1` armed line. After a firmware reset, the same
Image validates CPU/FDT/platform/exclusions and checks the chronological ring
before appending or materializing XNU. A retained current-token armed record
returns stage5/error-67 through Android. It does not prove XNU executed. Every
new candidate needs a fresh token and a pretrial absence check. While that marker is retained, the same token selects diagnostics instead of
repeating XNU. This is a RAM latch, not a permanent boot-attempt counter; Android
log initialization can replace it. The host therefore consumes each trial state
once and leaves the phone in Fastboot. Never rely on another reboot of an old
candidate to preserve this decision. Ring overwrite, power loss and early
firmware/entry failures can defeat the latch.

`tools/ace-auto-trial.py TRANSPORT_JSON PRIVATE_TRIAL_DIR` consumes a guarded
successful flash state once. It issues one normal reboot, waits for diagnostic
ADB, verifies the current token, root/B-slot and actual boot/vendor hashes,
saves pstore/dmesg/AEE, then issues `adb reboot bootloader`. It never flashes,
restores a backup, changes slots or edits source. The agent reviews the captured
failure, makes a concrete fix and checks a new candidate before the next trial.
