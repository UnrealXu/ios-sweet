# Ace XNU earliest entry marker

Patch `0087` inlines a stackless Ace-only writer before `OSLAR_EL1` in
`start_first_cpu`. It emits `ACEXNU1:<16 lowercase hex>: entry EL1\n` only
with exact `ace_pmsg=1` and `ace_run=<token>` command-line tokens. Missing,
duplicated or malformed recognized options refuse logging. The command line
must terminate within its generated 608-byte BootArgs bound.

The writer preserves x0 and x17–x30. It checks EL1, disabled MMU/data and
instruction caches, little endian, BootArgs revision/version, nonoverflowing
40-bit managed RAM, BootArgs containment, ring disjointness and a canonical
existing DBGC header. It neither initializes an unknown ring nor uses a stack,
calls, MMIO, SMC or reset. The fixed pmsg range is the reviewed Ace resource
`0x48160000 + 0x10000`; exclusive ordinary RAM, ECC0/type0 and quiescent DMA
remain native-loader/firmware contracts, not facts inferred from the header.

`tools/ace-mknative.py --pmsg` now generates and records a fresh run token.
An explicit `--run-token` permits reproducible fixtures. A reused image has a
reused token: physical trial collection must use a freshly built image and
reject a matching marker already present before that trial. This is diagnostic
provenance, not cryptographic authentication or proof of usable iOS.

Run the patch's actual assembly instructions in isolated QEMU RAM:

```sh
python3 diagnostics/ace-early-entry/verify.py research/entry-marker-new
```

The 19 cases cover empty/partial/wrapped rings, option order, malformed or
missing/duplicate options and run tokens, bounded termination, invalid header,
cursor, BootArgs revision and RAM layouts. They compare the entire ring and
BootArgs, plus selected preserved registers. They do not test every SCTLR
state, persistent RAM across physical resets, or MTK controllers.

Local evidence also compiles the real XNU assembly using the CI build-tree
flags and generated ABI offsets, compares all SWEET sections and relocations
with the unpatched source, and compares the Ace Mach-O entry-marker bytes with
the QEMU-executed fixture. Full-kernel CI and real-phone validation are separate
requirements. A marker proves execution through this writer only; it does not
prove page-table initialization, C entry, drivers or iOS userspace.
