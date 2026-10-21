# Ace EL0 instruction capability probe

This is an ordinary Linux/AArch64 userspace executable, not XNU/iOS. It checks
CPU0 with `getcpu`, installs a SIGILL handler, and executes exactly one
`STLUR WZR,[X0,#16]` against its own 32-byte BSS buffer. An unsupported result
requires a positive kernel signal code and the exact test instruction's fault
address. The handler exits; it does not skip the instruction or alter a context.

Build locally (keep output under ignored research):

```sh
mkdir -p research/ace-isa-probe
aarch64-linux-gnu-gcc -nostdlib -static -no-pie -Wl,--build-id=none \
  diagnostics/ace-isa-probe/probe.S -o research/ace-isa-probe/probe
```

Run only as a normal Android shell process, with `taskset 1` and a freshly staged
private filename. Check its hash first and remove that exact staged file after
return. It uses only `getcpu`, `rt_sigaction`, stdout `write`, and `exit`. It
requires neither root nor a kernel module and does not access MMIO or partitions.
Status0 means execution + own-buffer store verified; status3 means an exact-PC
SIGILL. Status2/5/6/7 do not establish instruction support.

Actual PGKM10 result on 2026-10-19: CPU0 produced exact-PC SIGILL, exit3.
The staged file was removed; Android/Enforcing and boot ID matched before/after.
Binary SHA256: `13643257143b8ba20070f8146aa771bf2dabda8cf80cf1fa542b2d8b527093f8`.
Private captures/journal: `research/ace-xnu-pmsg-20261019/isa-phone/`.
This proves only this EL0 instruction result on CPU0, not an XNU boot or
capabilities of the other seven cores.

This probe exposed a real code-generation problem: local clang's Darwin target
kept the Apple M1 default CPU despite `-march=armv8.2-a+crypto`. Pinning the ACE
machine flags to `-mcpu=cortex-a55` removes the generated STLUR from the new
console core. Remaining code and final linked libraries still need appropriate
build and hardware validation.

`abi.c` checks the raw signal ABI against the cached actual Android kernel
UAPI declarations. The host regression compile omits the vendor tree's private
`compiler.h` implementation and sparse user-pointer annotations; the signal
structure declarations and layout remain unchanged. Initial cross-UAPI setup
was incomplete; the successful ABI compile was completed after the recorded
phone run. The exact fault-PC signal check also succeeded in that phone run.
