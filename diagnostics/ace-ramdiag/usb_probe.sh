#!/system/bin/sh
# Only binds the in-guest dummy controller. Never a physical UDC.
if [ -n "$(getprop service.adb.listen_addrs)" ] || [ "$(getprop service.adb.tcp.port)" != -1 ]; then
    echo 'ACE_RAMDIAG: FAIL USB fixture requires adbd TCP disabled'; exit 1
fi
echo 'ACE_USB_FIXTURE: adbd TCP listener disabled'
count=0
while [ "$(getprop sys.usb.ffs.ready)" != 1 ] && [ "$count" -lt 15 ]; do
    sleep 1
    count=$((count+1))
done
if [ "$(getprop sys.usb.ffs.ready)" != 1 ] || [ ! -e /dev/usb-ffs/adb/ep1 ] || [ ! -e /dev/usb-ffs/adb/ep2 ]; then
    echo 'ACE_RAMDIAG: FAIL FunctionFS descriptor readiness'; exit 1
fi
echo 'ACE_USB_FIXTURE: stock adbd FunctionFS descriptors ready'
if [ ! -d /sys/class/udc/dummy_udc.0 ]; then
    echo 'ACE_RAMDIAG: FAIL dummy UDC absent'; exit 1
fi
count=0
while [ "$(getprop sys.ace.usb.fixture.bind_attempted)" != 1 ] && [ "$count" -lt 10 ]; do
    sleep 1
    count=$((count+1))
done
if [ "$(getprop sys.ace.usb.fixture.bind_attempted)" != 1 ] || [ "$(cat /config/usb_gadget/ace/UDC)" != dummy_udc.0 ]; then
    echo 'ACE_RAMDIAG: FAIL dummy UDC bind readback'; exit 1
fi
echo 'ACE_USB_FIXTURE: bound exact dummy UDC'
count=0
found=0
while [ "$count" -lt 10 ]; do
    found=0
    for path in /sys/bus/usb/devices/*; do
        [ -f "$path/idVendor" ] && [ -f "$path/idProduct" ] && [ -f "$path/serial" ] || continue
        if [ "$(cat "$path/idVendor")" = 18d1 ] && [ "$(cat "$path/idProduct")" = d001 ] && [ "$(cat "$path/serial")" = RAMDIAG_QEMU_FIXTURE ]; then
            device=$path
            found=$((found+1))
        fi
    done
    [ "$found" = 1 ] && break
    sleep 1
    count=$((count+1))
done
if [ "$found" != 1 ]; then echo 'ACE_RAMDIAG: FAIL USB enumeration identity'; exit 1; fi
interface=$device:1.0
if [ "$(cat "$interface/bInterfaceClass")" != ff ] || [ "$(cat "$interface/bInterfaceSubClass")" != 42 ] || [ "$(cat "$interface/bInterfaceProtocol")" != 01 ]; then
    echo 'ACE_RAMDIAG: FAIL enumerated ADB interface identity'; exit 1
fi
echo "ACE_USB_FIXTURE: enumerated trusted ADB device $device"
echo ACE_USB_FIXTURE_EVIDENCE_BEGIN
cat "$device/busnum" "$device/devnum" "$device/dev" "$device/serial" "$interface/bInterfaceNumber"
for ep in "$interface"/ep_*; do
    cat "$ep/bEndpointAddress" "$ep/bmAttributes" "$ep/wMaxPacketSize"
done
echo ACE_USB_FIXTURE_EVIDENCE_END
printf '%s\n' "$device" > /tmp/ace-usb-device
echo 'ACE_USB_FIXTURE: FunctionFS + dummy host enumeration verified'
