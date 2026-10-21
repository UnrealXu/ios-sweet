#!/system/bin/sh
# QEMU-only observation workload; any attached disk is a synthetic fixture.
exec >/dev/console 2>&1
echo 'ACE_RAMDIAG: stock shell entered'
if [ -f /ace-ramdiag/module-fixture ]; then
    /system/bin/sh /ace-ramdiag/module-probe.sh || exit 1
fi
if [ -f /ace-ramdiag/usb-fixture ]; then
    /system/bin/sh /ace-ramdiag/usb-probe.sh || exit 1
fi
id
echo "ACE_RAMDIAG: serial=$(getprop ro.serialno) secure=$(getprop ro.adb.secure)"
setprop sys.ace.ramdiag.ready stage2-probe-v1
echo "ACE_RAMDIAG: property readback=$(getprop sys.ace.ramdiag.ready)"
if [ -f /ace-ramdiag/vendor-overlay ]; then
    overlay_ok=1
    while IFS= read -r path; do
        if [ "$(cat "$path")" != '# ACE_RAMDIAG_DISABLED' ]; then
            echo "ACE_RAMDIAG: FAIL startup config not neutralized: $path"
            overlay_ok=0
        fi
    done < /ace-ramdiag/neutralized-paths
    if [ -e /lib/modules/modules.load ] || [ -n "$(cat /proc/modules)" ] || [ -s /system/bin/recovery ] || [ -x /system/bin/recovery ]; then
        echo 'ACE_RAMDIAG: FAIL stock modules or recovery still active'
        overlay_ok=0
    fi
    if [ "$overlay_ok" = 1 ]; then echo 'ACE_RAMDIAG: full vendor overlay verified'; fi
fi
echo ACE_RAMDIAG_MOUNTS_BEGIN
cat /proc/1/mountinfo
echo ACE_RAMDIAG_MOUNTS_END
if [ -e /data ]; then
    echo 'ACE_RAMDIAG: FAIL unexpected /data'
else
    echo 'ACE_RAMDIAG: no /data directory'
fi
count=0
while [ "$count" -lt 10 ]; do
    daemon=$(pidof adbd)
    if [ -n "$daemon" ]; then
        echo "ACE_RAMDIAG: adbd pid=$daemon state=$(getprop init.svc.adbd)"
        echo ACE_RAMDIAG_ADBD_STATUS_BEGIN
        cat /proc/$daemon/status
        echo ACE_RAMDIAG_ADBD_STATUS_END
        break
    fi
    sleep 1
    count=$((count+1))
done
if [ -f /ace-ramdiag/vendor-overlay ] && [ -z "$(pidof adbd)" ]; then
    echo "ACE_RAMDIAG_DEBUG: init.svc.adbd=$(getprop init.svc.adbd)"
fi
echo 'ACE_RAMDIAG: probe workload complete'
if [ -f /ace-ramdiag/tcp-auth-test ]; then
    ifconfig lo up
    if ifconfig eth0 10.0.2.15 netmask 255.255.255.0 up || ifconfig usb0 10.0.2.15 netmask 255.255.255.0 up; then
        echo 'ACE_RAMDIAG: QEMU TCP ready'
    else
        echo 'ACE_RAMDIAG: FAIL QEMU network configuration'
    fi
    if [ -f /ace-ramdiag/usb-proxy ]; then
        /ace-ramdiag/dummy-usb-proxy &
    fi
    cat /proc/net/dev
    count=0
    while [ ! -f /tmp/ace-adb-auth.done ] && [ "$count" -lt 35 ]; do
        sleep 1
        count=$((count+1))
    done
    if [ -f /tmp/ace-adb-auth.done ]; then
        echo 'ACE_RAMDIAG: authenticated host command completed'
        # The authenticated host first reads back its nonce, then sends a
        # single poweroff command. Do not race that receipt with local reboot.
        count=0
        while [ "$count" -lt 15 ]; do
            sleep 1
            count=$((count+1))
        done
        echo 'ACE_RAMDIAG: FAIL authenticated host poweroff absent'
    else
        echo 'ACE_RAMDIAG: FAIL authenticated host command absent'
    fi
fi
reboot -p
