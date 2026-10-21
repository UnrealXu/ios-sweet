#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd)
out="$repo/research/ace-offline/probe"
mkdir -p "$out"
cc=${CROSS_COMPILE:-aarch64-linux-gnu-}
flags=(-march=armv8-a -ffreestanding -fpie -fno-stack-protector -fno-builtin -fno-asynchronous-unwind-tables -mgeneral-regs-only -O2 -Wall -Wextra -Werror)
"${cc}gcc" "${flags[@]}" -c "$repo/probe/start.S" -o "$out/start.o"
"${cc}gcc" "${flags[@]}" -c "$repo/probe/probe.c" -o "$out/probe.o"
"${cc}ld" -T "$repo/probe/linker.ld" --emit-relocs -Map="$out/probe.map" -o "$out/probe.elf" "$out/start.o" "$out/probe.o"
"${cc}objcopy" -O binary --gap-fill=0 --pad-to="$("${cc}nm" "$out/probe.elf" | awk '$3=="image_end" {print "0x"$1}')" "$out/probe.elf" "$out/probe.Image"
"${cc}readelf" -rW "$out/probe.elf" > "$out/relocations.txt"
if grep -Eq 'R_AARCH64_ABS|R_AARCH64_GLOB_DAT|R_AARCH64_JUMP_SLOT' "$out/relocations.txt"; then
    echo 'Unexpected absolute/dynamic relocation' >&2; exit 1
fi
if [[ -n $("${cc}nm" -u "$out/probe.elf") ]]; then
    echo 'Undefined symbol' >&2; exit 1
fi
"${cc}objdump" -d "$out/probe.elf" > "$out/disassembly.txt"
python3 - "$out/probe.Image" <<'PY'
import pathlib, struct, sys
p = pathlib.Path(sys.argv[1]); b = p.read_bytes()
assert b[56:60] == b'ARM\x64'
assert struct.unpack_from('<Q', b, 8)[0] == 0x80000
assert struct.unpack_from('<Q', b, 16)[0] == len(b)
print(f'Built {p}: {len(b)} bytes, valid ARM64 Image header')
PY
