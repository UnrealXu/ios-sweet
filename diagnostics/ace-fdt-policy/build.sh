#!/usr/bin/env bash
# Build only; no download, sudo, phone connection or device write.
set -euo pipefail
task_root=$(cd "$(dirname "$0")/../.." && pwd)
task_out=${1:-"$task_root/research/ace-fdt-policy-build-20261020"}
if [[ -e "$task_out" ]]; then
    echo "Refusing existing output directory: $task_out" >&2
    exit 2
fi
mkdir -p "$task_out"
task_out=$(cd "$task_out" && pwd)
cd "$task_root"
aarch64-linux-gnu-gcc -std=c11 -mcpu=cortex-a55 -O2 -static -nostdlib \
    -fno-pie -no-pie -ffreestanding -fno-builtin -fno-stack-protector \
    -fno-asynchronous-unwind-tables -mgeneral-regs-only -Wall -Wextra -Werror \
    -Wl,--build-id=none,-T,diagnostics/ace-fdt-policy/linker.ld -I ace \
    diagnostics/ace-fdt-policy/start.S diagnostics/ace-fdt-policy/probe.c \
    ace/fdt.c ace/xnu_fdt.c ace/xnu_platform.c ace/xnu_cpu.c ace/xnu_handoff.c \
    -o "$task_out/ace-fdt-policy"
aarch64-linux-gnu-readelf -l "$task_out/ace-fdt-policy" > "$task_out/program-headers.txt"
aarch64-linux-gnu-objdump -d "$task_out/ace-fdt-policy" > "$task_out/disassembly.txt"
if [[ -n $(aarch64-linux-gnu-nm -u "$task_out/ace-fdt-policy") ]]; then
    echo "Unexpected runtime import" >&2
    exit 3
fi
sha256sum "$task_out/ace-fdt-policy"
