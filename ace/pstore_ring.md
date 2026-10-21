# Caller-owned persistent RAM ring codec

`pstore_ring.c` provides an ordinary-RAM byte codec for the zero-type-signature,
ECC-disabled `persistent_ram` layout used by ramoops console/pmsg. It does not
map RAM, choose addresses, reserve a region, initialize unknown memory, or call
firmware, devices, partitions or a boot bridge. All calls require caller-owned,
fully accessible buffers and exclusive access for their duration. There is no
allocation, libc dependency, internal global state or synchronization.

## Format and API

The header contains three little-endian u32 values: signature `0x43474244`
(`DBGC` bytes), next-write cursor `start`, and valid byte count `size`. Payload
starts at byte12; capacity is `zone_bytes - 12`, restricted to1..INT32_MAX.
Byte-unaligned zones work because headers are decoded/encoded by bytes. Typed
output pointers must satisfy their C alignment requirements. No API changes the
signature or offers an initialization operation.

- `ace_pstore_ring_validate` checks the signature and official reader bounds
  `size <= capacity`, `start <= size`; optionally returns capacity/cursor/size.
- `ace_pstore_ring_append` retains chronological bytes until full and then
  overwrites the oldest. An oversized input retains its last capacity bytes.
  Empty input is a validated no-op; it may have a NULL source.
- `ace_pstore_ring_read` copies the entire chronological record, returning its
  size through `written`. Too little output space returns `E_SPACE` without
  changing the zone, destination or `written`. It never silently truncates.
  Validate first to obtain the required allocation size.

All errors preserve both zone and outputs. Declared source/output ranges may
not alias the zone; output metadata/count pointers may not alias the zone or
payload destination. Integer range checks reject address wrap before pointer
arithmetic or dereference. Actual allocation ownership/lifetime cannot be
inferred from a pointer and remains the caller's responsibility. ECC status and
zone boundaries also cannot be inferred from this signature: a caller must
independently establish that ECC is disabled and the supplied region is exact.

## Official compatibility and a stricter append boundary

The reference is the official OnePlus public
[fs/pstore/ram_core.c](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/fs/pstore/ram_core.c).
It is a format/algorithm reference, not established as the exact running
`g6973d81` source. This implementation is original code expressing that format.

Recovery concatenates `data[start:size]` and `data[0:start]`, matching
`persistent_ram_save_old`. For stable producer states, completed appends match
`persistent_ram_write` byte-for-byte: retain the input suffix that fits, saturate
size, advance cursor modulo capacity, and write across the wrap if necessary.
The signature and untouched payload bytes remain unchanged. Partial appends
preserve prior chronological data; full rings discard only the overwritten
oldest data.

The official recovery bounds also admit unusual partial records such as
`start=1,size=4`, or a full record with `start=capacity`. These can be decoded, but
continuing to write them can silently overwrite earlier partial bytes or relies
on a noncanonical cursor. Nonempty append therefore returns `E_STATE` unless
partial `start==size`, or full `start<capacity`. It does not normalize or erase
these records. Empty append preserves them unchanged. This stricter producer
precondition is intentional; it accepts states produced by ordinary completed
writes, while preserving evidence in other reader-valid states.

The codec reproduces completed-call data, not the kernel's concurrent atomic or
crash timing. It writes payload before the two header fields, with no persistence
barriers. The two fields are not an atomic commit. There is no guarantee against
torn writes, asynchronous observation, reset during a call, stale caches, DMA,
ECC mismatch or firmware clearing. It neither compresses payloads nor adds the
separate dmesg timestamp format. It does not certify MMIO/physical mappings or
which CPU/exception level may access a real reserved region.

## Verification

Run:

```sh
python3 -m unittest discover -s tests -p test_ace_pstore_ring.py -v
```

Tests compile the actual C implementation as a host shared library. Fixed
vectors and1600 deterministic append sequences across capacities1..257 compare
all resulting header/payload bytes and chronological recovery with an independent
Python model of the official write/save-old equations. Coverage includes partial,
full, wrapped, oversized/truncated input; too-small output; unknown signature;
corrupt size/cursor; noncanonical append states; aliases; pointer overflow;
unaligned zones and typed-output alignment. Errors must leave evidence and
outputs unchanged. A UBSan executable exercises NULL and overflowing-pointer
rejection. A freestanding ARM64 cross-compile must have no undefined symbols
(the cross-compile test explicitly skips if its compiler is absent).

No test touches physical RAM or a device. This codec is not linked into the
entry bridge or any boot image. Separately, the project's actual Android test
recovered a normal `/dev/pmsg0` marker after a normal Android reboot with a changed
boot ID. That establishes that particular Android path only; it does not validate
this codec on hardware, a baremetal producer, PSCI/watchdog reset or safe flash.
