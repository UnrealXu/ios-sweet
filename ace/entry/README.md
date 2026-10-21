# Ace boot entry foundation

This independent ARM64 Image bridges a single boot CPU from nonsecure EL2 to
EL1, or passes an existing EL1 entry through, then executes the already-tested
register probe. **It does not load XNU, implement an MTK driver, or boot iOS.**
It is not packaged for flashing and has no physical-device logging channel.

```sh
./ace/entry/build.sh
python3 ace/entry/verify.py
```

Dependencies: existing GNU AArch64 compiler/binutils, Python 3, ripgrep;
verification also uses QEMU and gdb-multiarch. All generated files stay under
ignored `research/ace-entry-20261019/`. No downloads, sudo, ADB, fastboot or
partition access occur. The build checks the diagnostic payload's image hash,
all seven source hashes and eight successful execution cases through the shared
probe validator. Starting a build invalidates any prior entry PASS record.

The bridge accepts only EL1/EL2 with the **currently active** MMU and D-cache
disabled. It refuses other ELs or active M/C without turning them off. The
payload/record must already reside in executable, writable, coherent RAM; it
does not validate an arbitrary existing mapping. At EL2 it masks DAIF,
initializes HCR_EL2 for AArch64 EL1 without stage-2/VHE/TGE, permits EL1 timers,
sets CNTVOFF to zero, initializes CPTR_EL2 and the inactive EL1 SCTLR, and uses
SPSR_EL2=0x3c5 plus ERET. It preserves incoming x0, clears x1..x3, and jumps
PC-relative into the payload. The probe establishes its own SP_EL1 and VBAR.
There is no MMIO, DMA, storage, secure-monitor call, CPU_ON, or reset in this
bridge. It changes CPU control registers and exception level; it is not the
read-only Linux register module.

The Linux Image header, timer and boot-entry conventions were cross-checked
against [Linux ARM64 booting](https://www.kernel.org/doc/html/latest/arch/arm64/booting.html)
and [Linux v5.10 head.S](https://github.com/torvalds/linux/blob/v5.10/arch/arm64/kernel/head.S).
REA of the byte-matched Ace ATF supports a conditional EL2h/EL1h incoming
path; see `docs/ACE-BOOT-ENTRY.zh-CN.md`. This is a minimal tested foundation,
not an exhaustive initialization contract for every ARM architecture extension.

## Execution evidence

Four actual QEMU Cortex-A76 / 128MiB / one-CPU cases pass:

- EL1 MMU/cache-off entry reaches probe stage5 at EL1.
- EL2 entry executes ERET to EL1 and reaches probe stage5.
- The same EL2 image relocated to a second RAM address still reaches EL1
  probe stage5, preserving x0. No embedded absolute destination is needed.
- An independent trampoline establishes a valid EL2 identity page table and
  enables MMU; the bridge records refusal stage3, preserves SCTLR_EL2.M and
  leaves all page-table bytes unchanged without executing the payload.

GDB listens on loopback only, each case is bounded to20seconds with unconditional
QEMU cleanup. The verification binds image/payload/source hashes and retains raw
records and command/log evidence. EL0/EL3 and D-cache-on refusal have not been
executed in this test matrix. No physical Ace entry, storage access, 16KiB page
table, XNU, display/USB output or bootloader authentication has been tested.

`ACEENTRY` v1 is64bytes (8 little-endian uint64 values): magic, version,
stage, incoming x0, incoming CurrentEL, incoming active SCTLR, resulting
CurrentEL, resulting SCTLR_EL1. Stages1=entered,2=EL refusal,3=M/C refusal,
4=about to enter payload. The payload's independent `ACEPROBE` v2 record follows
its own documented layout. Writes have no cross-reset persistence guarantee.

## Optional experimental RAM log

The default Image contains no logger and remains byte-identical to the original
bridge (`ff298998dfbc9b05a26904b095dabd90fb75f2293fa3abd31e6788d6ad965838`).
An explicit build option enables a caller-selected ring; there is no default
physical target:

```sh
./ace/entry/build.sh --output-dir research/entry-log-example --pmsg-ram 0x43000000 128
python3 ace/entry/verify_pmsg.py
python3 ace/entry/verify_pmsg.py --output-dir research/ace-entry-pmsg-ace-address-20261019 --ring-address 0x48160000 --ring-bytes 0x10000 --qemu-mib 256
```

This leaf assembly logger uses the existing Linux persistent RAM format:
12-byte little-endian DBGC signature/start/size header, followed by data. Its
single writer appends `ACEENTRY accepted EL1\n` or `ACEENTRY accepted EL2\n`,
then `ACEENTRY payload EL1\n`; it retains old data until capacity requires
wrapping and finishes each successful append with `dsb sy`. It never initializes
an unknown header or changes its signature. The caller must establish exclusive
ownership, writable coherent RAM, and ECC0 beforehand; ECC configuration cannot
be inferred from the header. Address must be four-byte aligned, size at least13,
and capacity at most INT32_MAX. Runtime image overlap is refused before reading
the target. There is no stack allocation, physical-address discovery or probe
of inaccessible RAM.

Both calls occur only after the active EL1/EL2 M/C refusal checks. The logger
additionally rejects big-endian operation. Optional `bridge_pmsg_results` holds
two signed32-bit statuses: zero=appended, -1=unsafe EL/SCTLR, -2=image alias or
address overflow, -3=invalid signature/header bounds, -4=noncanonical cursor.
The not-called sentinel is INT32_MAX. A partial ring requires start=size; a
full ring requires start<capacity, matching the strict `ace/pstore_ring` append
contract. Header read/modify/write is single-writer only. No ECC, concurrent
writer, cache maintenance, atomic crash consistency, hardware reset or persistence
claim is made. RAM which is inaccessible can still fault; this is an explicit
experiment requiring a proven caller-owned mapping.

Each optional verification run executes14 QEMU cases: default EL1/EL2 target
unchanged; logged EL1/EL2/relocated EL2; bad signature EL1/EL2; bad cursor and
noncanonical partial header; active-MMU EL1/EL2 refusal; wrapped EL1/EL2; and
runtime image-alias refusal. The two address matrices use ordinary simulated
RAM, including the run numerically matching the Ace address. They do not test
Ace hardware access, LK/ATF entry, cache state across reset or log recovery.
Reports include the complete entry source hashes, build manifests, per-case
commands, raw bridge/probe records, ring before/after and their SHA256 values.
Source or artifact changes invalidate the evidence. Optional logger code is
not connected to a physical boot/deployment path.
