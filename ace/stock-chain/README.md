# Stock-kernel forwarding diagnostic prefix

This prefix provides a candidate for a first physical Ace custom-entry test
while continuing into the **byte-identical current Android kernel**. It is not
XNU or iOS. No phone deployment is built into these tools.

```sh
python3 ace/stock-chain/build.py
python3 ace/stock-chain/verify.py
python3 tools/ace-stock-chain-boot.py --output research/ace-stock-chain-20261019/new-review-candidate
```

The pinned original stock Image SHA is
8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0.
It is embedded unchanged at offset2MiB after a small diagnostic prefix. The
outer Linux Image preserves original text_offset0 and flags0xa; image_size
covers the whole new Image. The prefix has no stack, no EL switch, no MSR,
SMC, controller/DMA operation or reset. It records EL,active SCTLR,MIDR,MMFR0,
CNTFRQ and incoming x0 in local RAM, restores x0..x3/LR and branches directly
into the stock Image. Other general registers are scratch under Linux boot ABI.

Build emits plain, explicit pmsg and overlap-test variants. Only explicit pmsg
uses0x48160000/65536, the observed Ace ramoops resource; this is not enabled
by default in assembly. Shared ace/entry/pmsg.S is unchanged. A distinct guard
excludes the ENTIRE large Image from the ring; the shared leaf additionally
checks its small prefix span, MMU/D-cache/endianness and existing canonical
DBGC header. Bad/absent headers/control/aliases fail open into stock, without
initializing arbitrary RAM. Two bounded appends store a unique build-token
text marker and the80byte pre-handoff record. Physical ownership/cache/reset
retention and LK handling are still unverified on hardware.

`ACECHN01` record10 LE uint64: magic,stage,x0,CurrentEL,activeSCTLR,MIDR,
MMFR0,CNTFRQ,logger_status,stock_entryPA. Stage1 is logged before branch;
stage2 in local prefix RAM is about-to-branch. Logger status0 success,
-1control/-2address/-3header/-4state refusal, -9disabled/not attempted.
The raw logged record contains the first append status; observing its full
80bytes confirms the second append reached the ring. Android returning is
separate evidence that the original kernel continued; marker alone is not.

Six actual QEMU tests run this prefix, stop immediately before stock entry,
independently hash a full49,185,772byte runtime kernel dump, check restored
arguments/current EL and exact ring bytes, then continue the real stock kernel
through normal module load/unload and natural poweroff. Cases cover plainEL2,
pmsgEL1/EL2,relocation,bad DBGC header and full-Image ring alias refusal. This
proves the stock-kernel forward path in QEMU, NOT acceptance by physical LK,
MTK peripherals or iOS. Loopback GDB only,30s debugger and45s guest deadlines,
unconditional cleanup; logs hashed after QEMU exits. Each build invalidates
old PASS; unique token and source/runtime artifact hashes prevent stale reuse.

Packager revalidates all six cases/raw artifacts and exact source hashes,
then pins the CURRENT Magisk boot_b backup SHAee817627...; it does not use the
old stock ramdisk. Gzip is independently inflated and the original kernel,
header(other than kernel_size),Magisk ramdisk and zero legacy GKI area checked.
Final candidate overwrites the full64MiB partition, avoiding stale suffix data.
It preserves the exact existing obsolete-payload AVB metadata bytes, relocates
them behind the new payload and updates footer geometry. This mirrors the
observed current Magisk layout: current and original metadata are byte-identical
while ramdisk length/footer offsets differ. It is NOT valid authentication of
the new payload. Physical acceptance on this unlocked LK remains untested.

Private final candidate and exact rollback plan are documented in
`docs/ACE-STOCK-CHAIN-PLAN.zh-CN.md`. The earlier bare review-candidate folder
predates the AVB layout correction and MUST NOT be deployed. Any partition
write requires explicit individual confirmation under project AGENTS.md.
