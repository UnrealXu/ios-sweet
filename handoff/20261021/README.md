# 2026-10-21 computer transfer handoff

This snapshot includes the current source at local commit `5e5f7cd` plus this handoff and a review-only probe proposal. It is based on remote kernel branch `codex/ace-initial-platform` at `2d756a8910d2651ed48f122b0a1478f30546d7db`. No new phone experiment was performed for this transfer. Read `AGENTS.md` and the newest entry in `NOTES.md` first.

## Continue on another computer

```sh
git clone --branch codex/ace-handoff-20261021 https://github.com/UnrealXu/ios-sweet.git
cd ios-sweet
```

A clone contains source and public documentation. The ignored `research/` tree, original device partition backups, transport identity, downloaded Apple inputs, compiled kernels and trial evidence are deliberately outside Git. Copy those privately from the old computer, retaining their relative paths. The local transfer inventory is `research/ace-git-handoff-20261021/`; bring that directory too. Its private dependency list and analysis handoff describe the required evidence and incomplete proposals. To preserve *all* current private work, copy the entire ignored `research/` directory; it can be very large. A source-only clone cannot safely resume physical trials. Recreate the USB transport for the new host and verify the expected device before any operation; never reuse an old host's USB address blindly.

## Last observed physical state

- OnePlus Ace PGKM10 / MT6895, retained forensic `boot_b` SHA256 `1711085c34bcb4c399ac67e08885b5f13e6327a8e9d418d259bcd1bd659d944c`, full readback verified. Diagnostic controller completed and returned to firmware Fastboot. No phone handles remain live. This is the last observed state, not a promise about a later connection.
- No userdata, GPT, protected partition or slot change in this round. Original backups remain private. Retain the experimental image; do not routinely restore or repeat a consumed writer/controller. Ace rejects `fastboot boot`.
- Real XNU previously reached read-only UFS/GPT/userdata reads, then root-mount-failure park. Android remains in userdata. Actual iOS boot, screen, touch and usability are **not achieved**. Android fallback screenshots establish Android behavior only.
- Current forensic AEE identifies the XNU root-failure WFE at `_bsd_init+0x8e4`; current CE probe/native return execution is unproved. Historical AEE03 belongs to an older token and must be excluded. LK expdb restoration is a captured clue, not proof that CE evidence was overwritten.

## Next engineering work

Review the private return-chain WIP with the probe proposal under `proposals/ce-probe-diagnostics/`; that proposal is **not integrated or deployed**. Establish owned, current-token return/probe evidence before changing the established failure. Keep source-only tests separate from device proof.

The early firmware Fastboot detector is integrated in source commit `5e5f7cd`. A future paired forensic gate must accept its new terminal phase only with its receipt and a fresh independent physical Fastboot verification; old private gates accept only timeout and need updating. Never rerun a consumed controller or blindly retry a write.

Before any iOS userdata write, obtain the required independent RAM diagnostic success and guarded terminal handoff. Neither exists yet. See private writer/terminal proposals for unfinished work. No root write is authorized merely by cloning this branch.

For kernel CI retain cached mode, diagnostic_artifacts=false, and the current patched workflow; do not dispatch the old upstream default workflow. Use the existing `codex/ace-initial-platform` lineage. Record exact build provenance/hashes and device results in NOTES.md.
