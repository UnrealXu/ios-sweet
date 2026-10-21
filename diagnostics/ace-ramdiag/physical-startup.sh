#!/system/bin/sh
# One-shot RAM guest. No persistent write, mount, retry, unload or reboot.
set -e
exec >/dev/kmsg 2>&1
trap 'echo "ACE_PHYSICAL_STARTUP: stopped; readiness remains absent"' EXIT
. /ace-ramdiag/startup.env
[ "$(id -u)" = 0 ]
[ "$(getprop ro.serialno)" = "$EXPECTED_SERIAL" ]
[ "$(getprop ro.boot.slot_suffix)" = _b ]
[ "$(getprop ro.adb.secure)" = 1 ]
[ "$(getprop service.adb.tcp.port)" = -1 ]
[ -z "$(getprop service.adb.listen_addrs)" ]
[ ! -e /data ] && [ ! -L /data ]
[ -z "$(pidof adbd)" ]
grep -q " /sys/fs/pstore .* - pstore " /proc/1/mountinfo
/ace-ramdiag/native-gate
/ace-ramdiag/module-supervisor
printf '%s\n' "$BUNDLE_ID" > /tmp/ace-expected-receipt
cmp /tmp/ace-expected-receipt /tmp/ace-ramdiag-return-checkpoint
cmp /tmp/ace-expected-receipt /tmp/ace-ramdiag-modules-complete
cmp /tmp/ace-ramdiag-native-checked /sys/firmware/devicetree/base/chosen/ace,native-refusal
# ueventd creates label aliases from the actual UFS GPT. Never invent aliases.
check_partition() {
    name=$1; expected_start=$2; expected_number=$3
    alias=/dev/block/by-name/$name
    [ -b "$alias" ]
    node=$(readlink -f "$alias");base=${node##*/}
    case "$base" in ''|*[!A-Za-z0-9._-]*) return 1;; esac
    [ "$node" = "/dev/block/$base" ]
    sys=/sys/class/block/$base
    ancestry=$(readlink -f "$sys")
    case "$ancestry" in /sys/devices/*/112b0000.ufshci/*/block/*) ;; *) return 1;; esac
    [ "${ancestry##*/}" = "$base" ]
    parent=${ancestry%/*}
    [ "$(cat "$parent/queue/logical_block_size")" = 4096 ]
    [ "$(cat "$sys/start")" = "$expected_start" ]
    [ "$(cat "$sys/size")" = 131072 ]
    [ "$(cat "$sys/partition")" = "$expected_number" ]
    grep -qx "PARTNAME=$name" "$sys/uevent"
    grep -qx 'DEVTYPE=partition' "$sys/uevent"
    grep -qx "PARTN=$expected_number" "$sys/uevent"
    grep -qx "DEVNAME=$base" "$sys/uevent"
    number=$(cat "$sys/dev")
    major=${number%:*};minor=${number#*:}
    [ "$(stat -Lc '%t:%T' "$alias")" = "$(printf '%x:%x' "$major" "$minor")" ]
    grep -qx "MAJOR=$major" "$sys/uevent"
    grep -qx "MINOR=$minor" "$sys/uevent"
    printf '%s\n' "$number" > /tmp/ace-$name.dev
}
check_partition boot_b "$BOOT_START" "$BOOT_NUMBER"
check_partition vendor_boot_b "$VENDOR_START" "$VENDOR_NUMBER"
[ "$(cat /tmp/ace-boot_b.dev)" != "$(cat /tmp/ace-vendor_boot_b.dev)" ]
# Avoid a circular enclosing-boot-image digest; host validates its full hash.
[ "$(sha256sum /dev/block/by-name/vendor_boot_b)" = "$VENDOR_SHA  /dev/block/by-name/vendor_boot_b" ]
[ -d /sys/class/udc/11201000.usb0 ]
cmp /tmp/ace-ramdiag-native-checked /sys/firmware/devicetree/base/chosen/ace,native-refusal
[ ! -e /data ] && [ ! -L /data ]
echo 'ACE_PHYSICAL_STARTUP: native/module/UFS identity gates passed; iOS unproven'
setprop sys.ace.ramdiag.ready ramdiag-v1
trap - EXIT
