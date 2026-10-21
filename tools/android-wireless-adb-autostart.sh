#!/system/bin/sh
# Magisk late_start service: restore Android's paired TLS wireless debugging.
# One bounded attempt per boot; no adbd restart, auth change, or TCP legacy mode.
umask 077
state_dir=/data/adb/ace-wireless-debugging
mkdir -p "$state_dir" || exit 1
[ -e "$state_dir/disable" ] && exit 0
status_file="$state_dir/status.txt"
write_status() {
    {
        printf 'state=%s\n' "$1"
        printf 'boot_id='
        /system/bin/cat /proc/sys/kernel/random/boot_id
        printf 'wireless_setting=%s\n' "${enabled:-not-read}"
        printf 'tls_port=%s\n' "${port:-not-read}"
    } > "$status_file"
}
# late_start is nonblocking. Wait for framework/settings and the user's Wi-Fi.
count=0
while [ "$(/system/bin/getprop sys.boot_completed)" != 1 ]; do
    [ -e "$state_dir/disable" ] && exit 0
    count=$((count + 1))
    if [ "$count" -ge 120 ]; then write_status boot-timeout; exit 1; fi
    /system/bin/sleep 2
done
count=0
while [ "$count" -lt 90 ]; do
    [ -e "$state_dir/disable" ] && exit 0
    if /system/bin/ip addr show wlan0 2>/dev/null | /system/bin/grep -q 'scope global'; then
        enabled=$(/system/bin/timeout 10 /system/bin/settings get global adb_wifi_enabled)
        if [ "$enabled" != 1 ]; then
            /system/bin/timeout 10 /system/bin/settings put global adb_wifi_enabled 1
        fi
        port=$(/system/bin/getprop service.adb.tls.port)
        case "$port" in ''|*[!0-9]*) ;; *)
            if [ "$port" -gt 0 ] && [ "$port" -lt 65536 ]; then
                enabled=$(/system/bin/timeout 10 /system/bin/settings get global adb_wifi_enabled)
                if [ "$enabled" = 1 ]; then write_status tls-ready; exit 0; fi
            fi
        esac
    fi
    count=$((count + 1))
    /system/bin/sleep 2
done
write_status wifi-or-tls-timeout
exit 1
