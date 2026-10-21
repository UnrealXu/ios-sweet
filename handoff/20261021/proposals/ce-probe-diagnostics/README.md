# Private diagnostic probe proposal, not integrated

Adds `native_sha_ce_probe_diag(uint64_t observed[4])` to the existing RAM rescue assembly. Output slots are CurrentEL, DAIF, ID_AA64ISAR0_EL1 and CPACR_EL1. Each begins UINT64_MAX; each completed read is stored immediately. Returns0 on completion, -1 for wrong EL, -2 for unmasked DAIF, -3 for absent/unknown SHA2. Reads CPACR only after known SHA2 field1/2. It never enables FP/SIMD or authorizes CE; the existing two-slot probe and guarded hash routine remain unchanged. A higher-EL trap can prevent return; this proposal does not recover traps or change VBAR/exception ABI.

Caller integration remains WIP: publish a current-token, owned, phase-specific durable before-probe marker before calling; publish returned status/fields afterward. Preserve original exact CPU trace append authorization, full hashing, budget and STOP refusal. Sentinel values indicate incomplete reads, not guaranteed RAM preservation after hardware reset.

`probe-diag.patch` is review-only; do not deploy this file in isolation. Parent integration agent owns return-chain hooks.

Historical private tests of these exact assembly/header/test-C bytes passed four actual ARM QEMU profiles: production EL1 with live fields and real DAIF refusal; controlled SHA2-absent, SHA2-unknown and wrong-EL fixtures. Forbidden later reads are replaced by undefined instructions in fixtures to prove refusal precedes them. Each profile also fingerprints all Q0..Q31 lanes, FPCR/FPSR/CPACR/VBAR with initial FPEN0 and3. The test harness changes only fixture-directory resolution in this portable copy; it has not been rerun after handoff. No physical CE permission is established.

To reproduce with aarch64-linux-gnu GCC/binutils and qemu-system-aarch64 installed, run `python3 test-arm.py` once in a fresh directory. It creates arm-test/ and refuses overwrite. Fixture/test files must never be included in deployed native images. No device files, serials, downloaded Apple files or ELF binaries are included here.
