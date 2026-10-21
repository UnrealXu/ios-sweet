# Ace diagnostics independent of userdata

Status (2026-10-21): three RAM diagnostic trials have ended without diagnostic
ADB. Physical RAM diagnostics remain unproven. The paired normal-auto control
with the original generic ramdisk returned diagnostic ADB in 76.1 seconds,
collected verified logs and returned to firmware Fastboot automatically.
Installed/readback-verified boot_b is control
`2b17ee490950ec29faf3fc0c88d52f72fee3c00b10deb75d3999904f7a90ac58`.
Usable iOS, XNU display/touch and BSD root mount remain unverified.

## Why this precedes the iOS root write

The current automatic trial reaches Android/Magisk to collect the token-bound
native refusal record, pstore, dmesg and AEE, then returns to firmware Fastboot.
`tools/ace-auto-trial.py` calls `su -c`, waits for `sys.boot_completed`, reads
properties and by-name block nodes, and attempts `/data/vendor/aee_exp`.
Those source dependencies do not prove which Magisk files are needed at
runtime, but the path has not been proven independent of Android userdata.
Replacing userdata before establishing another path would discard a proven
diagnostic dependency.

## Exact stock artifact observations

Private extraction and REA snapshots are under `research/ace-ramdiag-20261020/`.
The inputs are the original pinned boot_b and vendor_boot_b backups, not files
read from the live phone during this investigation. Both pins remain enforced.

- Boot ramdisk has Magisk `/init` and compressed original init. Vendor ramdisk
  supplies recovery init, adbd, the Android dynamic linker/libraries and 270
  kernel modules. This inventory alone does not prove firmware unpack order.
- Recovery `system/etc/init/hw/init.rc` runs e2fsck on userdata/cache and mounts
  persist read/write. It also starts OEM recovery services. Do not reuse this
  script for the RAM profile. `ace-recovery-diag.py` remains an offline
  vendor_boot prototype, not authorization to write vendor_boot.
- Stock recovery adbd SHA256 is
  `6a8701a25bba906fb4c8f0e698bd5f62652466f60d15d86554ba5ae0b22d1840`.
  ELF linkage requires `/system/bin/linker64` and eleven direct libraries,
  including `libadbd_auth.so`. A recursive host `readelf` check of init, adbd,
  sh, toybox and linker64 covers 42 ELF files with no missing DT_NEEDED files
  in the extracted vendor ramdisk. This does not validate linker namespaces,
  runtime-loaded libraries or execution; hashes are in `linkage-closure.json`.
- REA `ev_b4ffea880845fb96e0fab13016effb1d77bab1ec6ecd2e0b4ff221c0c1f259d9`
  observes property-dependent authentication/root decisions and FunctionFS
  `/dev/usb-ffs/adb/ep0` in recovered `adbd_main`. The supplied default properties
  have `ro.secure=1`, `ro.adb.secure=1`, `ro.debuggable=0`; merely copying adbd
  cannot establish root diagnostics.
- In exact `libadbd_auth.so` SHA256
  `f7505ef1768169207b0b2d9a2d6bb2ab37390ebdee9cd01da66cfb3933bc3f3e`,
  `AdbdAuthContext::IteratePublicKeys` iterates two readable key files and feeds
  their lines to its callback. REA
  `ev_472304e9bcfae4dd7ba335093373aa29e057a8ed8b9738b9d3fd73c1e11e03d5`
  plus complete 16-byte pointer-table read
  `ev_1a9fff3a14552430ea58fbcb980725ae7485a8bbebc592191c37b97f5c10099e`
  establish `/adb_keys` first, `/data/misc/adb/adb_keys` second. This supports
  designing a ramdisk-provided trusted host key; it is not a connection test.

These are static observations, not target execution. Ghidra pseudocode is
recovered code with provider flow/type limitations; full limitations are in
the private snapshots. No absent-string search is treated as absence proof.

Exact recovery init SHA256
`53e5fb487c3333e350ecfd5a33da14e4524eb36712cc59b46f48d64e119ce221`
has an explicit `second_stage` dispatch before its first-stage fallback (REA
`ev_c4e29866eefbf0fc6f8670549de726a641adbe76582feabba93fc24a81f31fed`).
Recovered second stage initializes the property area/service and SELinux
labels, then chooses init scripts using `ro.boot.init_rc`, falling back to
`/system/etc/init/hw/init.rc` and additional init directories
(`ev_f6739ce7a04c2b02fe51714b52d868c50d20646b8cbd2db612e1dd57057f2b23`).
This is a possible controlled entry, not proof it works without first stage.
The ramdisk contains a monolithic `/sepolicy` and context files. Importantly,
calling stock `selinux_setup` is not a demonstrated way to avoid disk mounts:
its recovered body calls `MountMissingSystemPartitions()` before loading policy
and executing second stage
(`ev_1359a69ef25d4562c1d5b5c4122a35d29202127831b014e86e99abf74596635c`).
Either inspect that call's exact conditions or supply a controlled policy/init
setup. Do not claim `second_stage` alone establishes a safe complete PID1.

## Packaging support implemented

`ace-stock-chain-boot.package` accepts keyword-only `diagnostic_ramdisk` bytes
and `diagnostic_ramdisk_sha256`. Both are required together. It rejects wrong
hashes, invalid/empty inputs and partition overflow. Only kernel_size and,
when explicitly replacing the ramdisk, ramdisk_size may change in the header.
It independently reparses payload geometry, checks both extracted payloads,
preserves the exact obsolete AVB metadata and returns a full partition image.
Preserved metadata is not a signature/authentication claim.

Without those arguments the original ramdisk is preserved. Rebuilding actual
0112 with this default produces byte-identical 64 MiB output. The explicit
original-ramdisk path also reproduces it; this tests format compatibility,
not a new RAM environment. Eight stock-chain tests and seven boot-format tests
pass. There is deliberately no new CLI or claim that an arbitrary ramdisk has
passed the native automatic-trial validation.

The native refusal Android Image pin stays
`8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0`.
Do not relax it to accommodate the ramdisk.

## Required implementation and acceptance

1. Establish actual PID1/first-stage behavior and firmware ramdisk precedence.
   Provide a controlled init path, complete pinned linker/library closure,
   necessary USB/UFS module dependencies, property service and trusted ADB key.
   Do not import stock fstab, fsck, recovery or firmware-update actions blindly.
2. Mount only virtual filesystems and RAM scratch for diagnostics. Retain
   observed mountinfo and PID1/service configuration demonstrating that
   userdata and protected persistent filesystems are not mounted or formatted.
3. Add an explicit controller profile: direct uid0 diagnostics, its own ready
   marker, no Android boot-completed or `su` assumption, and explicit unavailable
   AEE/screenshot evidence when those services are absent. Never claim headless
   readout establishes visible iOS behavior.
4. Keep identity-bound USB transport/serial, current 288-byte `ACEFALL1` record,
   fresh token, B-slot, complete boot_b/vendor_boot_b hash checks, pstore/dmesg
   collection, refreshed identity/token before return, bounded record reads and
   the existing one-command reboot/error rules. Verify firmware Fastboot
   physically afterward. Keep all observations.
5. Run offline/QEMU checks against the actual new ramdisk. Existing native
   refusal QEMU tests replace PID1 with a fixture; their success does not prove
   this environment, physical USB or device module loading.
6. Only after those gates, package a fresh-token boot_b candidate and use the
   guarded one-time writer/automatic trial. Preserve original backups and the
   retain-experimental-image workflow. Do not write userdata until the new
   no-userdata diagnostic loop is physically proven.

Afterward, persist/serialize the proven Ace UFS controller and bound BSD root
requests to validated userdata GPT extents. A root mount and iOS userspace,
display, touch and persistent basic operations each still need real evidence.

## Diskless QEMU component probe

`diagnostics/ace-ramdiag/qemu_stage2.py` builds a new private ramdisk from the
hash-pinned vendor backup and boots the exact pinned refusal Android Image.
It does not create an Android boot partition image or contact the phone or a
host ADB server. Default mode attaches no disk/network; the explicit
`--tcp-auth-test` attaches restricted QEMU networking through emulated USB
Ethernet and a loopback-only forwarded port. It retains source snapshots, input/member
hashes, compile command, serial/host logs and a passing or failing report.
Give it a new output path under `research/` for each run.

The freestanding preinit checks PID1 and RAM root, creates only character
devices, mounts virtual filesystems, directly loads the pinned monolithic
policy into the guest kernel, selects permissive diagnostics and labels init.
It executes exact stock init with `second_stage`, never `first_stage` or
`selinux_setup`. Its bounded failure action powers off the guest; **it is not
yet a physical-device recovery design**. No module or block node is supplied.

The controlled rc starts stock ueventd in early-init, then stock adbd and a
stock-shell observation workload. Ueventd is necessary for the coldboot
completion gate; omitting it left PID1 in epoll_pwait, established by a separate
guest observer reading `/proc/1/syscall`, wchan, stack and maps. The observer
run remains failed and cannot satisfy the acceptance report.

Recovery mode is selected by an empty, non-executable `/system/bin/recovery`
marker; exact stock `IsRecoveryMode` checks existence (REA
`ev_60350633e525812a76e4ff0708207f02e72967999a2b34eaeb9a1dddc800d48c`).
No recovery program or service runs. A synthetic QEMU B-slot boot property
selects `/prop.default`. Without the slot suffix, OEM recovery defaults can
fork ueventd and attempt cache/system mounts (REA
`ev_3f00c0ae1767bdde29b530dbd8d3dfc657c17a3e9190a6e847d4531d8531b6b9`).
Do not transplant that unsafe defaults branch into a device environment.

Attempt5 passed the enabled-SELinux-policy branch: stock shell uid0,
`ro.adb.secure=1`, synthetic serial, property set/readback, live adbd with all
four UIDs zero, no `/data` directory, only virtual filesystems in PID1 mountinfo,
and orderly guest poweroff. Its ramdisk was 6,453,075 bytes, SHA256
`ed4752d50f00739bff0818fa6c35f3be5565c3af1a59470fe55fe82b7a0b649c`;
serial SHA256
`e1455eba507cf25e6fa99b10e7570a0d9b0c9f0c10ba9905614eb9b0092e96bc`.
The final runner additionally requires the observed policy-load marker unless
the limited disabled-policy comparison is explicitly requested. Final7 passes
that stricter runner, with ramdisk 6,452,678 bytes SHA256
`77b69c6a849e6f6306dd8ccc8f0c0eb1b94288d3c19930498e612fc98d61c7a0`
and serial SHA256
`81efa4bfc125cd350a4d34c9be5d84c21a9214cadd624edd4a1cd3eadc2e1114`.
An independent host rebuild produced byte-identical preinit and entire ramdisk
(`stage2-rebuild7/reproducibility.json`). The link strips local symbols to avoid
GCC random temporary object names changing otherwise identical file hashes.

Scope remains **QEMU components and authentication only**. Physical USB,
MT6895 modules, pstore/token/full-partition hash collection, automatic firmware
return, screen/touch and iOS userland have not passed this probe. The full vendor/generic overlay is now separately
controlled and verified in QEMU as described below; firmware precedence remains
a physical acceptance gate. Preserve all failed attempts alongside passing ones.

## Authenticated root ADB in RAM

`--tcp-auth-test` generates separate trusted/untrusted ephemeral RSA keys in
the private run directory. It validates the exact trusted public-key hash and
Android Montgomery encoding before embedding a single root-readable
`/adb_keys`; private keys remain mode0600 on the host. Authentication stays
enabled. The bounded `adb_wire.py` client connects only to `127.0.0.1`, sends
signatures rather than authorization requests, and never starts an ADB server
or enumerates USB devices. Protocol/encoding references are the
[AOSP protocol](https://android.googlesource.com/platform/packages/modules/adb/+/refs/heads/main/docs/dev/protocol.md)
and [AOSP public-key implementation](https://android.googlesource.com/platform/system/core/+/refs/heads/main/libcrypto_utils/android_pubkey.cpp).

Actual `tcp-auth-attempt6` passed: the wrong signature received a fresh AUTH
challenge; the pinned signature received recovery CNXN. Over that authenticated
connection the stock shell returned uid0, synthetic serial, secure=1, slot_b,
no `/data`, and the current random command nonce. A second stream wrote and
read that nonce in RAM. Only after receiving the complete receipt did the host
send one authenticated `reboot -p` request, followed by observed guest poweroff
and QEMU rc0. Root adbd process status, monolithic policy loading and virtual
mountinfo checks passed too.

The ramdisk SHA256 is
`dd30a23799d91f8bbe40be264821b5e2fcd82deef35deff6d56ce0bd3ec9d9a7`;
serial SHA256 is
`e71d0fa84ff3bdc34bd07ad66ca98a6a6e2b4a2e1733e50353966ecbeda5b9ee`.
`tcp-auth-rebuild6` reproduces the entire ramdisk byte-for-byte with that same
public-key input. Default no-network `stage2-regression8` and eight offline
key/wire/stream/deadline guard tests also pass. This is not an Ace USB transport
or a firmware Fastboot return test.

All earlier authentication attempts remain failed: virtio NIC unavailable;
overly strict client CNXN version; missing printf tool; premature local poweroff
before receipt; and client mishandling of an already-closed stream. The current
client allocates fresh local stream IDs, acknowledges closure, ignores only
exact known closed-stream CLSE pairs with a bounded duplicate count, and keeps
rejecting foreign stream data and malformed packets. A guest watchdog timeout
emits FAIL and cannot turn a failed authentication/return sequence into a pass.

## Hardware module dependency findings

The private stock `modules.load.recovery` is a selection list, not a bare
insmod order: device_info precedes its Oplus dependencies, usb_boost precedes
mtu3, and ufs-mediatek-mod precedes its debug/blocktag dependencies. Resolve
`modules.dep` recursively before loading anything. USB PHY/controller/TCPC/
extcon plus UFS selected seeds have an 18-module symbol closure; this is a
lower bound for those seeds, not a verified hardware startup set.

The exact live FDT SHA256
`68c811fbaae657372d740c25ff81f03c9763eab3e897b0a7104d624ec598560b`
adds important provider requirements. USB0 at 11201000 references xsphy,
TOPCKGEN/pericfg clocks and the MT6368 VUSB regulator. Its role endpoint goes
through extcon_usb to the MT6375 charger OTG regulator, TCPC/MFD/I2C and pinctrl.
Consequently all charger modules cannot be dismissed by name. Whether a fixed
peripheral mode can avoid part of that chain needs actual driver evidence.

UFS at 112b0000 references UFS_AO/UFS_PDN/TOPCKGEN clocks, scpsys domain2,
MT6363 VEMC/VUFS12/VUFS18 regulators and two ti,syscon-reset providers; the last
maps to reset-ti-syscon.ko and was absent from the 18 seeds. This live UFS node
has no phys/phy-names/iommus/pinctrl properties, and the live tree has no separate
UFS PHY hardware node. A generic recovery-list phy-mtk-ufs entry does not prove
that module is required by this particular DT.

Several exact MT6895 clock/scpsys compatibles have no entry in modules.alias,
but matching official source has actual of_match tables and arch_initcall
registration. At OnePlusOSS commit `8baa5a377e2776402de745579cc3835d08ee1cca`,
`clk-mt6895.c` supplies TOPCKGEN/VLP_CKSYS; `clk-mt6895-peri.c` supplies
PERICFG_AO/IMP_IIC_WRAP_C/UFS_AO/UFS_PDN; `clk-mt6895-bus.c` supplies INFRACFG.
Do not interpret missing MODULE_DEVICE_TABLE exports as built-in support.
These source mappings do not prove binary/source instruction equivalence.

The missing generic helpers were fetched at that same commit into private
`provider-source/`, with URL/hash manifest. `mtk-scpsys.c` lines1258–1311 fetch
optional supplies and clocks for **all40 domains** before provider registration;
only absent-supply ENODEV is ignored, while other errors/defer abort init.
Basic/basic_lp names and subsys/subsys_lp prefixes cover all46 clock names in
the exact live scpsys node (17 basic requests/15 unique names plus31 prefix
matches), independently reproduced in `scpsys-clock-closure.json`. Thus the
global camera/display clock-provider dependency is now established from source.
The BYPASS/DISABLE flags are considered later and cannot skip these clock gets.
This does not establish a dependency on camera/panel functional drivers.

`mtk_clk_simple_probe` is in `clk-mtk.c:351`: gate registration then provider
publication, propagating errors. `mtk-spmi-pmic.c` supplies the PMIC chip-ID,
regmap and regulator-child registration paths. scpsys uses WARN_ON for some
initial power transitions, and PMIC IRQ failures may be logged before child
creation continues; a probe/provider message alone is not proof of usable
power/IRQ state. No new module/provider probe has been observed on hardware.
SPMI host source remains missing at the attempted path; preserve that404 result.

The private `actual-live.dts` matches the live DTB for these USB/UFS/provider
properties and 1830-node topology/reservations. It differs in four unrelated
camera clock-names values; it is not an exact full-tree reproduction.

## Full vendor/generic overlay and early slot refusal

`--vendor-overlay-test` keeps the original compressed vendor ramdisk as a
byte-identical prefix (928 nontrailer CPIO members) and appends the controlled
generic ramdisk. Both use legacy LZ4, without inter-ramdisk padding, following
[AOSP vendor boot ordering and compression requirements](https://source.android.com/docs/core/architecture/partitions/vendor-boot-partitions).
The actual backup boot and vendor ramdisks both have this legacy LZ4 magic.
QEMU proves this exact kernel unpacks the combined input correctly. It does
not establish physical LK/firmware behavior.

The generic archive neutralizes all original `.rc`, `.prop` and fstab paths
except the replaced controlled init.rc. The guest checks each exact comment
replacement. Before stock init, preinit hides the original module tree behind
nodev/noexec tmpfs. The host refuses unexpected original module directories or
any RAM data tree beyond the two known empty directories `/data/vendor` and
`/data`; preinit removes only those empty directories, refusing nonempty ones.
The probe checks no loaded modules, the inert recovery marker, no `/data`, and
virtual-only mounts. No persistent block device is attached to QEMU.

Before policy loading or stock init, preinit reads at most 64 KiB each of
`/proc/cmdline` and optional `/proc/bootconfig`. The shared no-libc slot parser
requires an explicit B suffix and refuses conflicting values in either source.
Missing, A, malformed and conflicting slot fixtures cannot enter stock init.
The final conflicting-slot QEMU test passes **refusal only**, not startup.
Four host tests exercise the same compiled parser including real bootconfig
syntax and conflicting duplicate/cross-source values.

Retained overlay failures established two additional requirements. With OEM
ueventd configuration disabled, `/dev/null`, random and urandom need explicit
standard permissions; otherwise adbd aborts in random_device with Permission
denied. With the original `system/build.prop`, adbd instead runs as UID2000 and
cannot read the root-only trusted key. Neutralizing the stock property files
restores the controlled secure-auth/root properties. Neither failure is treated
as a SELinux or cpuset diagnosis. Adbd runs once with kernel-log stdio and trace
output, so failures remain observable without repeated service restarts.

Final `vendor-overlay-final6` passes the full overlay, enabled policy, root
shell/adbd, wrong-key rejection, pinned-key acceptance, fresh command nonce,
RAM write/read receipt and one authenticated guest poweroff. Generic ramdisk
is 7,568,761 bytes SHA256
`2ca92cfdfdcf5557f93c9cc65835573cb0a5c7ecee6274526978992ca2ad87c3`;
combined initrd is 46,025,601 bytes SHA256
`795e3bb4b08ac876767349f3c69a419bbb4b7f385563629fed328289d51f4d6d`.
Serial SHA256 is
`041c634f2837e5f7791c4634ad7b3372d85719ee9644d71af3253ac68eba41e1`.
A rebuild with the same pinned public key reproduces preinit, generic and entire
combined initrd byte-for-byte, with identical source hashes. Default filtered
no-network regression and all 12 offline authentication/slot tests also pass.

No physical RAM diagnostic candidate has been written. Direct-root controller
support, native current-token/pstore/full-partition hash checks, actual module
startup and automatic firmware return remain required. This milestone supplies
no new physical display, touch, storage-write or iOS userspace evidence.

## Pinned module/provider planning

`diagnostics/ace-ramdiag/module_plan.py` generates an offline proposal directly
from the pinned original vendor CPIO, pinned live FDT and pinned Android Image.
It does not load modules or contact the phone. The planner validates complete
hard dependency coverage, normalized names, soft pre/post dependencies, safe
paths and graph acyclicity. It parses explicit DT binding formats for clocks,
power, resets, PHYs, buses, supplies, graph endpoints and named TCPC references.
These edges are retained separately from module symbol insertion order.

The final private `module-plan-final2` covers 66 nodes and 170 provider edges,
selecting 45 modules totaling 4,311,600 original bytes from the 270-module
archive. All 46 scpsys clock provider/argument tuples independently match the
previous source/DT closure. The report SHA256 is
`b2850e95aebfb2fa2dddfad6a6565729d5db77e6c593011319a15b318cb697c6`.
A second invocation reproduces the entire report and extracted kernel config
byte-for-byte. The exact Image's bounded embedded IKCONFIG extraction has SHA256
`7d939635d77acbaa49a3e4ab2bdbb154c0a2c5e393b8057fa11a49071b56f149`.
Eleven new graph/provider tests plus twelve prior auth/slot tests pass.

The tracked `provider_overrides.json` records exact source hashes and URLs for
missing OF aliases. MFD regulator mappings require the source cell name and
stock platform alias. These are source-table observations, not proof of module
instruction equivalence or successful probe. Root identity, fixed-clock, GICv3
and simple-bus remain explicitly unmapped to modules. An empty explicit-binding
unparsed list does not mean every possible vendor binding has been covered.

A concrete startup ordering fault was found in the symbol-only proposal:
[official extcon source](https://github.com/OnePlusOSS/android_kernel_5.10_oneplus_mt6895/blob/8baa5a377e2776402de745579cc3835d08ee1cca/drivers/misc/mediatek/extcon/extcon-mtk-usb.c#L320)
returns ENODEV when named TCPC is absent, but its probe only logs that failure
and returns zero. Later provider arrival is not assured to retry notifier
setup. `startup_preconditions.json` therefore orders TCPC before extcon and
records the required registered `/sys/class/tcpc/type_c_port0` state. The exact
TCPC driver reads `tcpc,name`; its class implementation creates a device using
that name under class `tcpc`. Their source hashes corroborate this gate.
The loader must implement and observe it; this planner does not claim to do so.

The SPMI source is available as composite `spmi-mtk-pmif-core.c` plus
`spmi-mtk-debug.c`, established by the same-revision Makefile. Preserve the
initial missing `spmi-mtk-pmif.c` path result as a failed lookup, not evidence
that the driver's source is unavailable.

Before physical use, selected module bytes still need a controlled RAM bundle,
a bounded one-pass loader, provider readiness checks, ABI checks and actual
failure handling. Inserting a module may probe enabled instances outside this
reference closure. Successful insertion or driver binding alone cannot prove
IRQ/power/role state. No new hardware result is established by this proposal.

## Executable RAM module loader

`module_bundle.py` now verifies an explicitly hash-pinned planner report against
the original pinned archive, dependency order and current planner source hashes.
It checks each module's bytes, ELF architecture/type, internal name and release
metadata before generating fixed entries and compiling `module_loader.c`.
The 45-module synthetic-identity bundle is private under
`research/ace-ramdiag-20261020/module-bundle-rebuild1`; it is not a phone image.
Its loader SHA256 is
`5cf8ca0c725e5ccc87deb9ad70700ed86505847dc026a77e77067b73f959ed74`.
An independent build reproduces all 45 module files, the generated header and
loader byte-for-byte. A kernel release check is not a full ABI proof; module
insertion uses flags zero so the kernel enforces its usual verification.

The loader requires root, a non-PID1 process, RAM root, tmpfs scratch, absent
`/data`, exact release/architecture, B suffix and expected serial. It creates an
exclusive consumed latch before preflight. All module hashes must pass before
any insertion. Each verified file is copied into a memfd, sealed against
write/shrink/grow and seal changes, and its seals rechecked. `finit_module`
receives that sealed copy with no arguments and no override flags, closing
the gap between hash verification and kernel reading. Errors stop the process;
it does not unload, retry, reboot, mount persistent storage or open block nodes.

Before a consumer, its compiled sysfs gate must resolve to a directory on real
sysfs. A monotonic 15-second deadline and poll cap bound that wait. The TCPC
class-device gate is source-derived, but actual TCPC registration has not yet
been tested. This wait bound does not bound a stalled kernel driver probe
inside `finit_module`; physical watchdog/recovery behavior still needs work.

The exact pinned Android kernel passed these diskless QEMU fixtures:

- `insert`: actual original reset-ti-syscon module inserted from the sealed
  copy, observed in `/proc/modules`; a second invocation was refused by the
  consumed latch. The same run completed secure authenticated root ADB and
  one host-issued poweroff after its RAM command receipt.
- `hash-mismatch`: corrupting the second module prevented insertion of the
  first too; no modules were loaded.
- `gate-timeout`: absent TCPC path reached the deadline without insertion.
- `syscall-error`: preloading the second module caused EEXIST after the first
  insertion. The loader stopped and retained the partial state without retry
  or unload.
- `serial-mismatch`: expected-serial disagreement stopped before insertion.

Final `module-insert-final2` ramdisk SHA256 is
`4f2995efb02ea7199a8dd130b4bcd1d07534a52edb4896dba5ecafb2f0290ff6`;
serial SHA256 is
`a108b9da76611c2fa92bf42c49b95644090064f4809b206fefb732e8aecc182d`.
The stock reset driver has no matching QEMU device. This proves kernel module
loading/guard behavior, not MT6895 reset hardware. All refusal runs preserve
their actual error evidence; their passing fixture status is not startup success.
The full vendor/auth regression also passed with its original module tree
hidden and no modules loaded. The full 45-module bundle was never executed.

Twenty-nine offline tests now pass, including SHA padding/chunk/million-byte
checks against hashlib and bundle path/identity/size/ELF guards. Provider readiness,
UDC/UFS binding and actual operations, physical recovery on loader failure,
full vendor integration and direct-root automatic readout remain open. No new
physical screen, touch, storage-write or iOS result is established here.

## FunctionFS and actual in-guest USB authentication

`--usb-ffs-test` now exercises stock adbd through actual guest USB bulk
endpoints, using the exact kernel's built-in `dummy_hcd`. It works with the
full original vendor+generic overlay, without loading MT6895 modules. This is
an emulated host/controller path, not physical Ace USB evidence.

The controlled fixture follows the kernel's
[configfs gadget sequence](https://docs.kernel.org/usb/gadget_configfs.html):
create the gadget/configuration/FunctionFS instance, associate the function,
then bind to the explicitly chosen UDC. It mounts only configfs and FunctionFS,
creates ffs.adb and no disk-backed function, and waits for stock adbd descriptor
readiness. The synthetic gadget serial and exact `dummy_udc.0` are fixed.
Physical integration must explicitly select `11201000.usb0`, the controller
named by the pinned stock recovery script, rather than selecting the first UDC.

An initial shell-poll approach allowed adbd's first FunctionFS connection to
time out before binding. The current init property trigger binds immediately
when descriptors are ready, guarded by a one-attempt property. The probe checks
actual UDC readback and USB enumeration independently; attempted is not success.
Final acceptance refuses an initial bind timeout. Earlier failed and partially
successful attempts remain retained.

For `--usb-ffs-test --tcp-auth-test`, original adbd's TCP listener is disabled.
A freestanding guest bridge owns the forwarded socket and claims the actual
dummy USB interface through USBDEVFS. It verifies dummy ancestry, synthetic
serial, VID/PID, bounded descriptors, interface/endpoints, character-device
identity and USB devnum. It never implements AUTH or shell answers, detaches a
driver, or resets USB. Actual bounded ADB frames pass between socket and USB
bulk endpoints. Host access remains restricted to a loopback port; no host
ADB server, host USB enumeration or physical phone operation occurs.

`usb-auth-final4` passes without the initial bind timeout. The kernel observed
FunctionFS BIND/ENABLE and configured USB; real bulk OUT carried two CNXN
packets, and bulk IN carried three AUTH challenges. An invalid signature was
refused and the pinned key obtained root. An 8192-byte binary readout matched
exactly, including a real 4096-byte USB WRTE frame; its SHA256 is
`dc404a613fedaeb54034514bc6505f56b933caa5250299ba7d094377a51caa46`.
After the complete RAM receipt, one authenticated poweroff command traversed
USB and guest powerdown was observed. No module was loaded; full vendor startup
neutralization, policy, root UID, no `/data` and virtual-only mounts also passed.

Generic ramdisk SHA256 is
`9cb191edfc43fe344d59b3c7eeb875bc8d4cb018702bdab389a7526e6f27062a`;
combined initrd SHA256 is
`ab0e521b7646ccaae53553b22ee1aab95489d3527a28e9a76557120d7bf9c511`;
serial SHA256 is
`d3558396dd31712a51ae7437434ab72b3cf9665a2da3be69dd5b353eb5743b13`.
Five descriptor-parser tests join the prior tests for 34 passing guards; the
original TCP mode also passes. ZLP handling exists but no explicit IN-ZLP was
observed, so this is not a full USB conformance claim. Actual physical UDC/UFS
startup, firmware return and direct-root automatic trial integration remain open.

## Reset-return coverage and runtime binding contract

The exact live tree's watchdog child contains `syscon-reboot-mode` at offset
0x24, mask0xf, with bootloader mode3. The planner now includes that node and its
parent, adding watchdog, reboot-mode and syscon-reboot-mode modules: 48 total.
The original pinned kernel config builds these as modules. Matching official
source writes the selected mode through a reboot notifier/regmap callback;
notifier registration does not prove that a later hardware write succeeds.
Actual Fastboot return remains a physical acceptance requirement.

`binding_contract.json` specifies the physical USB, UFS, watchdog and reboot
mode OF nodes, driver names and owning modules. The builder verifies exact
source hashes, literal/macro driver names, selected module metadata and pinned
FDT, then compiles expected critical property bytes into the loader. USB must
have the exact physical UDC class node `11201000.usb0`.

After insertion the loader scans real platform sysfs with bounded records and
unique OF-node matching, checks driver/module links and exact DT property bytes,
then checks any required class directory on real sysfs. Missing/unbound targets
are read-polled to a deadline; complete driver/module/property disagreement
fails immediately. The check does not bind, unbind, touch registers or create
block nodes. Platform binding still cannot prove IRQ, power, UFS operations or
firmware return. No claim is made for other buses or full hardware readiness.

This work exposed and fixed an inherited ARM64 syscall flag error. The
[ARM64 UAPI overrides](https://raw.githubusercontent.com/torvalds/linux/v5.10/arch/arm64/include/uapi/asm/fcntl.h)
define O_DIRECTORY and O_NOFOLLOW differently from asm-generic/x86. Earlier
constants instead requested O_DIRECT/O_LARGEFILE. Shared `aarch64_flags.h` now
supplies the correct flags to the loader and USB proxy. A new actual-kernel
symlink fixture gets ELOOP before insertion, closing an untested assumption in
earlier ordinary-file fixtures. No affected RAM diagnostic image was flashed.

Final `binding-insert-final3` passes actual stock-module insertion, the QEMU
PCI platform node's driver/builtin/reg/class checks, consumed-latch refusal,
secure root ADB/RAM receipt and one poweroff. Separate missing-node, wrong-driver,
wrong-module and wrong-property fixtures stop as specified and retain partial
module state. An initial UART fixture was unsuitable because PL011 uses AMBA,
not platform bus; that failure was retained. Corrected-flags USB authentication
regression also passes. Thirty-five offline tests pass.

The 48-module synthetic-identity bundle and independent rebuild reproduce all
50 module/header/loader files exactly. Loader SHA256 is
`1e986d32de49d9b0679b3ee7982da464556c4d40183495e8654ef050e12da483`;
contract SHA256 is
`520c566bfba8792bc24417c522044581f3c2498443dbd0014b640243688cf36d`.
The full bundle was compiled, never executed. Physical startup supervision must
establish reset-return support early enough for failure recovery; the current
proposal's final checks do not protect an earlier stalled probe. A physical
profile, direct-root controller, partition hash checks and automatic firmware
return are still required before deleting Android userdata.

## Return-first stages and one-child supervision

The planner now forces the dependency-closed watchdog/reboot-mode/syscon-reboot
prefix before the remaining 45 modules. Loader checks the two return-related
OF/driver/module/DT contracts immediately after that prefix and writes a
bundle-specific RAM checkpoint before continuing. A failed early check stops
before later insertion. Remaining contracts precede a distinct completion
receipt. Module insertion and binding still do not prove firmware return.

`module_supervisor.c` launches one fixed loader child. It requires fresh RAM
state and an exclusive consumed latch. It never restarts, unloads, rolls back,
reboots or touches persistent storage. Child exit0 is accepted only with the
exact regular-file completion receipt for the compiled bundle identity. That
identity binds module bytes/order, target identity, contracts, policy and source
hashes. It is a local control-flow receipt, not remote attestation.

The default full-bundle wait is 90 seconds. On expiry the supervisor sends one
SIGKILL and waits up to a five-second grace/poll cap. A reaped timed-out child
produces124; an unreaped child produces125, never success. The tested hang is
an interruptible userspace sleeper. This is not a guaranteed hardware watchdog
or a way to recover a kernel stuck inside driver probe.

Actual exact-kernel QEMU tests verify normal staged insertion/receipt acceptance,
early-binding failure blocking later insertion, preflight hash failure blocking
all insertion, timeout/reap, consumed-supervisor refusal, and rejection of exit0
with missing or incorrect receipt. Negative fault programs are confined to the
QEMU harness; production bundle compilation never includes them. The successful
case also completes secure root ADB, a RAM receipt and one authenticated host
poweroff. Direct-loader regression and all 37 offline guards pass.

The 48-module synthetic-identity bundle and its rebuild reproduce 52 files
exactly: 48 original modules, two executables and two generated headers.
Loader SHA256 is
`99927cc22f31eb165aa24c6cd4b0110e5967c5337943a97eec990873ebd3b138`;
supervisor SHA256 is
`17fe2df15d0463126a0a32ccce1b56be5fb53853723287972b5db8f2676d8860`.
The full bundle remains unexecuted. The next integration must add the actual
physical RAM profile and direct-root readout contract, including native current
record/token, complete boot/vendor hashes and guarded firmware return. Module
completion must not substitute for those checks or for usable iOS.

## Pinned direct-root RAM readout controller

`tools/ace-auto-trial.py` preserves its default `android-v1` path. A prepared
trial may explicitly select `readout_profile=ramdiag-v1` with a trial-relative
`ramdiag_contract_file` and exact `ramdiag_contract_sha256`. The host contract
format is `ACE_RAMDIAG_HOST_V1`. It binds the serial/current native token,
candidate/vendor/kernel digests, controller and validator source digests,
module bundle identity, exact guest-profile bytes and privately prepared GPT
geometry for boot_b/vendor_boot_b. Unknown profiles, unsafe paths, pin failures,
invalid/overlapping extents and incompatible Android-only options stop before
any normal reboot. No physical writer emits this profile yet.

The separate `tools/ace_ram_readout.py` library has no reboot/transport-discovery
implementation. Its reader requires the controller's fresh identity-bound ADB
lookup before each direct-root exec-out command. Each stdout/stderr/return code
and command, including partial timeout output, is retained privately. No generic
command retries are added. The RAM branch avoids su, sys.boot_completed and
userdata/AEE collection; absence of AEE is explicit, not a successful archive.
The initial actual 288-byte native record must match the current token.

A nonce-bound snapshot checks root/B-slot/secure ADB/readiness/no-data, the
exact guest profile and both bundle receipts, plus PID1 virtual mounts. The
format `ACE_RAMDIAG_GUEST_V1` contains serial, run_token, bundle_id and
kernel_sha256; it omits the enclosing image hash to avoid a circular hash.
Partition commands read complete 64MiB extents. Before accepting hashes, the
host cross-checks block rdev/sysfs/uevent identity, label and partition number,
GPT geometry, controller ancestry `112b0000.ufshci`, and 4096-byte logical
blocks. Separate boot/vendor device identities are required. None of this is
remote attestation against a compromised diagnostic kernel.

Screenshot collection is attempted immediately after RAM ADB identity returns;
headless failure is retained explicitly. Saved diagnostic pixels still cannot
establish XNU/iOS display. Native return observations retain the existing three
read limit and immediate stop for a complete different record. The existing
single reboot and exact pre-command device-not-found retry rule remain, as do
physical firmware Fastboot/product/slot/unlocked checks. Final evidence hashes
are refreshed after return-token reads append their command observations.

Actual pinned-kernel QEMU `readout-usb-overlay-final0` passes secure USB
FunctionFS auth, the 8192-byte binary stream, full vendor overlay, root/no_data,
two complete 64MiB synthetic GPT partition hash commands, and one authenticated
poweroff. The read-only USB disk is expressly refused by the production UFS
ancestry gate. It is not a phone UFS proof or a controller-native-record proof.
The earlier run exposed shell word splitting in an unquoted hash echo; quoting
preserves the required two spaces. A subsequent slow hash exposed the wire
client's five-second idle limit. Only this opt-in fixture requests bounded
90-second total/30-second idle waits; defaults stay25/5, maximum total120.
Both failed observations remain private. All65 focused offline tests pass.

Physical assembly must still supply the real device identity/key, exact module
bundle/supervisor, guest profile and host contract, correct UDC, and guarded
fresh native token/pmsg/automatic readout. It must establish readiness from real
native token, partition identity and completed module evidence. No physical RAM
candidate has been built/flashed or independently returned to firmware through
this profile. Usable iOS/display/touch/root storage remain unproven.

## Physical RAM ramdisk assembly and native startup gate

`physical_assemble.py` now assembles a private generic ramdisk offline. It
revalidates the pinned module plan, compiles the actual serial-bound 48-module
bundle/supervisor, retains the original vendor ramdisk byte prefix, and replaces
the generic init/properties with physical startup. The final generic archive
contains no QEMU probe/proxy/observer/fault programs. No enclosing boot image or
writer state is generated by this tool, and it never calls ADB or Fastboot.

The fixed init starts a one-shot startup shell before adbd. A freestanding
`native_gate.c` checks root/RAM/no-data, then reads at most289 bytes from the
actual chosen native-refusal property. It requires exactly288 bytes, the
current compiled token, magic/version/padding, stage1..7, error-127..-1 and zero
handoff. This deliberately matches the controller's normal-refusal envelope;
limiting it to pending stage5/-67 would suppress other valid failure readouts.
The complete record is saved to an exclusive RAM checkpoint. Reexecution never
replaces that checkpoint. A valid failure record remains failure evidence.

Only after this gate may the real module supervisor run once. Startup compares
both bundle receipts, then the current native property again. It requires real
ueventd-created boot/vendor aliases, exact private GPT geometry, matching
rdev/sysfs/uevent identities, distinct devices, UFS controller ancestry and
4096-byte logical blocks. It checks the entire original vendor partition hash;
the host checks the enclosing boot hash to avoid a circular embedded digest.
A final native comparison and no-data check precede diagnostic readiness.

Physical USB config mounts only configfs/FunctionFS and binds the literal
`11201000.usb0` once, gated by native/module/UFS readiness and FunctionFS ready.
No first-UDC glob or dummy controller appears. Adbd TCP is disabled and only the
existing hash-pinned host public key is included. Its source file lacked a
newline, so a private normalized copy was used; its Android RSA bytes were
verified against the existing private key. Original keys were unchanged.
Pstore is explicitly mounted and verified before startup, since merely tarring
an unmounted sysfs directory would lose the intended evidence. The pinned
kernel has built-in PSTORE/PMSG/RAM support.

`physical-build5` and independent `physical-build6` reproduce all53 compared
payload files: both ramdisks, native gate, 48modules and two module executables.
Generic SHA256 is
`ae46153531bf7268971588c25b48caefa3994132af265d5ce05ecefb1ca130ce`;
combined SHA256 is
`b8887176b7be46bd179e2e27e1d45132813de872f1c94f436e5d74fa134376ad`.
Independent extraction verified all168 entries' modes/digests, exact vendor
prefix, disabled TCP, delayed adbd and empty nonexecutable recovery marker.
The physical ramdisk/full bundle has **not been executed**.

Four actual pinned-kernel QEMU native-gate fixtures pass: pending return,
another valid normal refusal, stale token, and oversized property. These use
explicitly synthetic DT overlays. Positive cases save the actual288B property
and reject a repeat without changing it; negatives create no checkpoint. Each
also verifies an actual pstore virtual mount, secure root ADB and one host
poweroff. These prove syscall/predicate behavior, not physical native execution
or the complete physical startup script. All69 focused offline tests pass.

Read-only device preparation verified firmware Fastboot/product/B/unlocked at
2026-10-20T17:14:35Z (local October21). No ADB/screenshot was available. Original
boot/vendor backups still matched their full hashes. No partition write or
reboot occurred. Fresh native Image/preflight/boot packaging, source-bound host
contract and guarded writer integration remain before a physical RAM loop.

## Native candidate packaging and prepared RAM trial

`tools/ace-ram-candidate.py` packages a verified native image with the explicit
physical generic-ramdisk replacement. It checks the current native sources,
actual0112 linked-CI provenance, nine-case/C-entry/four-refusal reports and dump
hashes, exact embedded Android bytes, physical archive entries and source pins.
The full64MiB result is independently extracted again. The manifest binds all
retained inputs, controller/validator/packager sources and complete candidate
bytes. `prepare` additionally checks the historical verified physical readback,
its evidence hashes and absence of the new token, then emits a pinned RAM host
contract and fresh one-time-writer state. This tool never issues phone commands.

The RAM controller adds its known90s module-supervisor budget to the original
150s ADB allowance (240s total). Android retains150s. The additional wait adds no
reboot/write/read retries and relaxes no identity/native/partition gate.

The first prepared native candidate uses token `a95b5e377195d1ac`, native Image
SHA256 `cd72023f9c500c21ccf10a433f816534c0bfad8b8e88c32423b3eff94ce5a850`,
and full boot_b SHA256
`b53be40604ab70d8a08ac5c9bafde63bfc49f94c70c03846c5939f48933fad8b`.
All86 focused RAM/controller/stock-chain/native-image tests pass. A prepared
candidate and QEMU preflights do not establish a physical RAM loop or iOS boot.

The first physical RAM candidate was written once to boot_b successfully
(Fastboot sending1.389s/writing0.146s/total1.537s). One normal reboot followed.
The controller terminated with `no-adb-after-240s-no-retry`: no diagnostic ADB
returned. Both during the wait and after it, host USB discovery found no expected
serial; the final ADB/Fastboot inventories had no matching device. No native
record, partition readback, pstore or screen was obtained. The failing stage is
unknown. This is an established physical readout failure, not an iOS milestone.

The experiment remains installed; no repeated write, reboot or controller run,
slot change, userdata command or original-backup restoration occurred. Manual
return to firmware Fastboot was requested as the documented last resort because
no software USB control channel remains. Logs must be recovered before choosing
a driver/entry fix; QEMU acceptance cannot locate this physical failure.

## Bootstrap without an available console tty

After the failed physical trial, an offline audit found that the pinned Ace
live FDT requests `console=tty0` twice, while the exact refusal kernel has
`CONFIG_VT` disabled, 8250 runtime UART count0, and MT6577 UART as a module.
Old preinit required opening `/dev/console` before it could load any modules.
That creates an unavailable-console failure path before stock init/ADB.
These are captured hardware/configuration facts; the physical failure's actual
stage is still unknown because no phone logs were obtained.

`preinit.c` keeps its original standard I/O path when the console opens.
For ENODEV/ENXIO/EIO only, it uses the freshly created RAM character devices:
stdin `/dev/null`, stdout/stderr `/dev/kmsg`. Unexpected path/permission errors
still fail, as do unavailable fallback devices. All RAM-root, B-slot, policy,
native token, module, UFS and USB gates remain in place.

The fixed-kernel QEMU fixture now supports `--console-fixture absent`: tty0 with
VT disabled, plus an early boot printk channel that supplies no console tty.
The explicit old-code negative fixture powers off before stock init. The final
controlled comparison uses the exact successful full-overlay archive and only
replaces `init` with the preserved old ELF: that also powers off before stock
init. Replacing this bootstrap with the fixed ELF permits secure root USB ADB,
the binary8192B read, no-data/virtual mounts, policy and one host poweroff.
The ordinary-console USB/full-overlay regression passes too. This is a proven
bootstrap defect/fix under unavailable-console conditions, not a recovered
physical crash diagnosis.

The QEMU observation workload uses its available raw ttyAMA0 for large proc
dumps in this fixture. Redirecting those dumps to kmsg was tested and rejected:
a multi-line cat exceeds the kmsg record limit. The first attempt is retained.
Production preinit uses short kmsg messages, and the physical ramdisk contains
neither the QEMU probe nor its UART redirection.

Fresh `physical-consolefix0` and `physical-consolefix1` reproduce all53 payload
files with new token `b6cf74b8748e4e4e`. Generic SHA256 is
`0426c3cb3a4461a62697d43c0a1b98dfa44c5a366c62b6f2b3641827f586c8b4`;
combined SHA256 is
`1d22fdf19a0b4b0a7a54a8893a201cfc2e5a5f3944b3d92807993d3da6faa2fc`.
They remain offline ramdisks, not flashed boot candidates. All86 focused tests
pass. Phone inventories still had no expected ADB/Fastboot at17:37:13Z; manual
Fastboot assistance remains pending. The installed image is still the failed
`b53be406...933fad8b` experiment, with no additional write/reboot/restore.

## Console-fix boot candidate and failed-install ledger

The console-fix ramdisk now has a matching fresh-token native Image and all
nine native cases, actual C entry and four refusal preflights pass. The complete
64MiB candidate is `candidate-consolefix0/experimental-ramdiag-boot-b.img`, SHA256
`684e61c25af6f19b6153e1161d26e67ef955f1d9f63eb5db0c9bcd233e6b8184`.
Native Image SHA256 is
`c9dda82827fb49ca81da83551585742f1b8a5c8237001ec8bf2f0289cfcdfdd9`,
with token `b6cf74b8748e4e4e`. This candidate has not been written to the phone.

The preparation helper can now represent a single acknowledged failed RAM
installation after the last verified physical loop. It validates the consumed
write ledger, exact historical package/image/artifact bytes, ancestry to the
verified trial, successful flash transcript, terminal no-ADB result, and absence
of the new token. It refuses missing/ambiguous evidence, an active controller,
other partition writes, broken ancestry and reuse of the failed image/token.
Historical source pins are not reused as current build validation or permission
to replay the old image. The new candidate still requires all current source
pins and fresh firmware Fastboot identity before any new write.

Prepared state keeps `last_verified_boot_b_sha256` as actual0112 and
`previous_boot_b_sha256` as the later failed RAM experiment. It explicitly sets
`previous_install_readback_verified=false` and pins the retained historical
evidence. The failed trial remains failed. Five new focused ledger tests and
all91 focused tests pass. `phone-trial1-consolefix` and its separate one-time
writer are ready offline, with physical connection unverified; they have not
been executed. At17:52:11Z the expected device was still absent from both ADB and
Fastboot. Further physical verification requires the phone's connection to be
restored; the installed experiment remains the older `b53be406...933fad8b` image.


## Physical consolefix failure and forensic recovery (2026-10-21)

The consolefix candidate `684e61c25af6f19b6153e1161d26e67ef955f1d9f63eb5db0c9bcd233e6b8184`
was written once to boot_b. Its normal reboot was accepted, but the RAM controller
ended after 240 seconds without ADB. No RAM PID1, module, USB or partition receipt
was collected. This does not establish which stage failed. The independently
reproduced console dependency fix does not establish the physical failure cause.

After the user restored Fastboot and directed continuation in response to the
explicit diagnostic exception request, the prepared forensic image was written
once. It skips XNU, preserves native pmsg and uses the pinned Android kernel plus
original Magisk generic ramdisk. This is an experimental boot image, not a restore
of the original boot backup. The diagnostic mode is explicitly separate from the
normal automatic-trial flag; native diagnostic-readout and auto-readout are
mutually exclusive. The controller requires the explicit exception state and
source/artifact-pinned manifest before device commands.

Diagnostic ADB appeared in 26.1 seconds. Current token, root, B slot, complete
64 MiB boot_b and unchanged vendor_boot_b hashes passed. A single refreshed-token
return observation matched; one ADB reboot returned the expected phone to physical
firmware Fastboot. No return reboot retry or backup restoration occurred.
`diagnostic_only_return_verified=true` records this narrower recovery result;
`automatic_loop_verified=false` and `ios_usable=false` remain explicit.

The screenshot was saved and visually inspected: an entirely black Android
capture. It proves no XNU display or usable interface. pstore, dmesg and a complete
16,217,088-byte AEE tar were retained privately. Offline decoding checked every
entry's CRC and size in all four archived records. Exactly one HWT archive contains
the consolefix token: SHA256
`ac3169f3c5ffc68a5ea9a91b788c8c63ec8e72c5b43654334dcc066b11c91ad9`,
55 verified entries. Its raw pstore pmsg ring equals the separately collected
35,390-byte pmsg file byte for byte (SHA256
`105c3945faae74183efec5290c50dbce7b18c672499f4b38bf256cb12dfe7637`).

The isolated consolefix-token segment contains the Darwin banner, BSD initialization
through `setconf`, and successful bounded UFS capacity/GPT block0/1 completion.
The firmware watchdog snapshot PC `0xfffffe0007491a9c` resolves against the exact
linked kernel symbol list to `_cpu_idle+0x1ec`. This is a sampled idle PC, not a
CPU fault diagnosis or evidence that BSD root mounted. No later RAM Linux stage
has been established. Next diagnosis must add evidence around the native Android
handoff and earliest RAM PID1 stages; the recovered archive does not justify a
blind repeat or a guessed module/UFS fix. All raw material stays under private
`research/ace-ramdiag-20261020/forensic-consolefix0/phone-trial/analysis/`.


## Durable native Android handoff evidence (2026-10-21, offline validated)

The next native revision appends `ACEANDROID1:<token>: pending handoff` followed
by the exact 288-byte refusal envelope immediately before the Android branch.
It runs only for stage5/error-67 in normal pmsg/automatic-readout mode, after
CPU, whole-image exclusions and successful FDT copying. The codec also requires
a valid chronological pending marker for the same token and the expected
refusal envelope. It never seeds unknown RAM. Append errors do not prevent the
existing diagnostic handoff; marker absence therefore remains inconclusive.
Diagnostic-only recovery is excluded at compile time and continues to preserve
pmsg. This boundary marker proves preparation to branch, not Linux entry or PID1.

The codec was executed in host tests against stale/corrupt input and a full
wrapping ring, with guards and unchanged inputs checked. QEMU exercised the real
fallback code using an explicitly synthetic stage5/-67 fixture and pending ring,
verified the complete appended packet, then booted the unchanged pinned Android
kernel and read back its FDT envelope. Four other fallback cases still preserve
pstore. The RAM packager now requires all five cases, including that explicitly
synthetic handoff fixture. Native source pins include the new codec header.

Private `native-handofftrace0` contains Image SHA256
`450fd5a59749d8df7b2d15cc8239367975b85c1da2eb77cb2de0726ec45e5ea1`,
9 native preflights, actual first `arm_init` instruction verification and 5
fallback cases, all passing. The same linked actual0112 XNU kernel was reused;
no CI run or phone write was performed. The fresh token was absent from all
296 files in the prior forensic evidence. Early RAM PID1 tracing and a matching
physical ramdisk/full boot package remain to be prepared before a new trial.


## PID1 pmsg tracing (2026-10-21, offline validated)

PID1 now mounts only its existing virtual proc/sysfs filesystems before stdio,
reads a pinned ramdisk trace token, obtains the character major from the complete
`/sys/class/pmsg/pmsg0/dev` attribute and creates a private RAM device node with
minor zero. It strictly rejects malformed/truncated attributes. Linux pmsg uses
a dynamic character major, as implemented in the [Linux 5.10 pmsg frontend](https://raw.githubusercontent.com/torvalds/linux/v5.10/fs/pstore/pmsg.c).
No misc-device number is assumed. The optional descriptor is duplicated outside
stdio with close-on-exec, so stock init does not inherit it. Trace failures do not
change the original boot decision. Text and numeric failure output are mirrored
with `ACEPID1:<token>` prefixes while this PID1 bootstrap remains active.

The first possible trace is after virtual /dev, proc and sysfs mounts, before
stdio; earlier mount failures remain outside its coverage. Kernel device and
backend availability must be established at runtime. No persistent filesystem
is mounted to obtain the trace. The physical ramdisk manifest hashes the
`ace-ramdiag/trace-token` file, source header and rebuilt PID1.

Controlled exact-kernel/full-vendor QEMU cases under private `pid1-trace1` pass:
normal console and unavailable tty0 both produce real ramoops pmsg rings containing
the token-bound pre-stdio and second-stage-exec records. With no ramoops device,
tracing reports unavailable and the existing stock-init/adbd probe still completes.
These use a synthetic token and QEMU reserved-memory fixture, not phone evidence.
Initial `pid1-trace0` booted but its verifier used virtual GDB addresses after MMU
activation and failed to export the ring; it is retained as a failed test-driver
observation. The corrected verifier exports physical RAM via QEMU `pmemsave`.

The separate authenticated ADB/no-console/full-vendor probe also passes, and
118 focused host tests pass. Full candidate trace0 SHA256
`163bfc89c45430a1deb03322a14cfb8a4c0153f7c047ac9a48e2440d7320119a`
uses token `9838a9120670e737`, matching physical generic ramdisk SHA256
`a364e216bb73f8c52f84e5de5f92f2736b54a7f8deca6645b6fd4d87f43acbc3`.
This adds diagnostic visibility; physical RAM readout and usable iOS remain
unproven until the new candidate is actually exercised.


## Paired physical control and automation gap (2026-10-21)

The instrumented RAM trial `163bfc89...20119a` timed out after 240 seconds without
ADB. Its single write acknowledgement remains distinct from partition readback,
which was not obtained. No RAM trace receipt or failure stage was recovered.
The user restored Fastboot and explicitly required recovery automation without
routine manual intervention. A normal automatic-trial control was then prepared:
its instrumented native Image, after substituting the fresh token, is byte for
byte identical to the RAM trial's Image. The linked XNU and embedded Android are
unchanged. The ramdisk treatment is the original Magisk generic instead of the
custom RAM generic. This is a new experimental wrapper image, not a backup restore.

Control `2b17ee49...90ac58`, token `9932497624433f86`, passed nine entry preflights,
actual first C instruction and five fallback cases. The single guarded write was
accepted. Its actual diagnostic ADB returned in 76.1 seconds, current token/root/
B/full boot_b/vendor hashes passed, and one refreshed-token ADB reboot returned
firmware Fastboot. No manual action was needed during this control trial. The
screenshot was inspected and shows an Android lockscreen with USB selection.
It proves no XNU display or iOS interface. The control result narrows the remaining
automation investigation to the RAM environment/handoff differences, without
identifying an individual failed instruction.

The real control pmsg is 18,030 bytes, SHA256
`fc8e36a5709edc9cb43d59fc410bea54b358aef27d09172b48e6fb86a19e933c`.
The new `ACEANDROID1` marker and following 288-byte refusal envelope match the
actual ADB record exactly. The independent current HWT archive contains a
17,695-byte pre-reset XNU ring; adding the exact 335-byte post-reset handoff
packet reproduces the live pmsg byte for byte. They are deliberately not claimed
to be identical without that suffix. All four AEE archives passed entry CRC/size
checks (240 entries total). Neither live pmsg nor those archives contains the
prior RAM token. Missing retained data cannot distinguish RAM loss during manual
reset from an earlier failure; it is not proof that native/PID1 never ran.

Source inspection also establishes an automation design gap: `preinit.c` fatal
errors currently call `LINUX_REBOOT_CMD_POWER_OFF`. This is not proof that the
phone took that branch. Changing it to unconditional restart would risk a loop
and would not by itself fix recovery. Before another RAM hardware test, prepare
and validate a bounded automatic rescue that preserves failure evidence and
can return through the proven Android path. Keep explicit distinctions between
RAM guest success, Android rescue and iOS success. The original generic is
1,427,884 bytes versus the custom generic's 8,799,617 bytes; the instrumented
native Image is 77,594,624 bytes. These sizes support investigating an embedded
rescue generic within the existing native Image limit, but do not prove a safe
live initrd rewrite. Any implementation must validate exact source layout,
bootconfig, bounds, ordinary RAM ownership and exclusion, preserve vendor bytes,
and stop after a bounded fallback rather than repeating RAM starts.


## Bounded rescue foundations (2026-10-21, not integrated into native boot yet)

`ace/initrd_rescue.c` is an allocation-free codec for an explicitly owned ordinary
RAM extent. It validates exact SHA256 pins for vendor, original generic and rescue
generic before any input/result stores. The replacement must be disjoint and no
larger than the original generic. Vendor bytes stay unchanged. Bootconfig framing,
bounded size, little-endian size/checksum, zero padding and complete checksum are
validated; its data/footer are preserved byte for byte while alignment is adjusted.
A dry run returns the proposed layout without modifying initrd. Any refusal keeps
both input and result unchanged. This helper grants no physical RAM ownership and
does not edit FDT or reboot. Its caller must still validate bank/reservation/image/
FDT exclusion and initrd ownership before invoking it on physical addresses.

The tail checks follow the [Linux 5.10 bootconfig reader](https://raw.githubusercontent.com/torvalds/linux/v5.10/init/main.c)
and [bootconfig image tool](https://raw.githubusercontent.com/torvalds/linux/v5.10/tools/bootconfig/main.c).
The historical phone FDT `live-fdt.dtb` declares initrd `[0x66f00000,0x69509a70)`,
39,885,424 bytes. Pinned vendor plus original generic is 39,884,724 bytes, a 700-byte
difference. The difference is observed; its contents have not been dumped, so it
is not claimed to be a validated actual bootconfig. No runtime mutation is permitted
from this size inference alone.

Host tests exercise malformed/truncated/overlapping ranges, wrong hashes, corrupt
footers/checksums, 96 padding/length combinations and full before/after guards.
The actual pinned 38,456,840-byte vendor stream, 8,799,617-byte RAM generic and
1,427,884-byte original rescue generic also pass the codec. The test bootconfig is
explicitly synthetic. The ARM64 codec was cross-compiled with native-loader flags,
no undefined imports, and executed as a component fixture on the pinned Android
kernel in QEMU; its full output SHA256 agrees with the host result. This proves
codec behavior, not phone rescue or an Android boot from the replacement image.
Private evidence lives under `research/ace-ramdiag-20261021-rescue-codec/`.

`ace/pstore_rescue.c` provides a separate read-only decision and single selection
record. An exact current armed marker allows one initial RAM handoff. A complete
current-token normal handoff envelope selects rescue. One complete rescue selection
with the expected stage/error, envelope and word31 `RESCUE01` then selects stop.
Duplicates, bad order, partial records, stale token and text-only marker spoofing
refuse. The selection append is allowed only in the rescue state and cannot repeat.
It records a selection attempt, never boot success. RAM loss, authentication and
physical reset behavior are not established by this codec.

Five initrd tests and five rescue-latch tests pass. The 123-test focused suite
including initrd tests passes; the five newly added latch tests pass separately.
A read-only test on the real control's retained handoff record recognizes the
protocol state without modifying its bytes. That control used an original generic,
so this is not a physical RAM-attempt or rescue result. Native embedding, FDT end
updates, capability-gated PID1 restart and explicit controller rescue handling are
still required. The phone retains the successful automatic control image in
Fastboot. No phone write or reboot was performed for these foundations.
