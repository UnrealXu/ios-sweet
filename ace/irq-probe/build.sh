#!/bin/sh
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
out="$repo/research/ace-irq-probe-20261019/${1:-normal}"
case "${1:-normal}" in normal) variant=;; timeout) variant=-DTEST_TIMEOUT;; exception) variant=-DTEST_BRK;; *) exit 2;; esac
mkdir -p "$out"
printf '{"status":"incomplete","reason":"build requested"}\n' > "$repo/research/ace-irq-probe-20261019/verification.json"
aarch64-linux-gnu-gcc -march=armv8-a -nostdlib -DQEMU_VIRT_ONLY $variant -c "$repo/ace/irq-probe/start.S" -o "$out/start.o"
aarch64-linux-gnu-ld -T "$repo/ace/irq-probe/linker.ld" "$out/start.o" -o "$out/probe.elf"
aarch64-linux-gnu-objcopy -O binary "$out/probe.elf" "$out/probe.Image"
aarch64-linux-gnu-objdump -d "$out/probe.elf" > "$out/disassembly.txt"
