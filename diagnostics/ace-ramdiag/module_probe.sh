#!/system/bin/sh
# Diskless QEMU fixtures only. The stock driver has no matching device there.
fixture=$(cat /ace-ramdiag/module-fixture)
echo "ACE_MODULE_FIXTURE: begin $fixture"
if [ "$fixture" = syscall-error ]; then
    # Establish EEXIST on the SECOND entry, after first insertion succeeds.
    if ! insmod /ace-ramdiag/modules/reboot-mode.ko; then
        echo 'ACE_RAMDIAG: FAIL fixture preload'; exit 1
    fi
fi
runner=/ace-ramdiag/module-loader
if [ -f /ace-ramdiag/supervisor-test ]; then runner=/ace-ramdiag/module-supervisor; fi
$runner
result=$?
echo "ACE_MODULE_FIXTURE: loader rc=$result"
case "$fixture" in
    insert)
        [ "$result" = 0 ] && grep -q '^reset_ti_syscon ' /proc/modules || {
            echo 'ACE_RAMDIAG: FAIL module insertion fixture'; exit 1;
        }
        if [ -f /ace-ramdiag/supervisor-test ]; then
            [ -f /tmp/ace-ramdiag-return-checkpoint ] && grep -q '^reboot_mode ' /proc/modules || {
                echo 'ACE_RAMDIAG: FAIL staged insertion checkpoint'; exit 1;
            }
        fi
        $runner
        [ "$?" = 1 ] || { echo 'ACE_RAMDIAG: FAIL consumed loader restarted'; exit 1; }
        ;;
    syscall-error)
        [ "$result" = 1 ] && grep -q '^reset_ti_syscon ' /proc/modules && grep -q '^reboot_mode ' /proc/modules || {
            echo 'ACE_RAMDIAG: FAIL syscall refusal fixture'; exit 1;
        }
        ;;
    binding-missing|binding-wrong-driver|binding-wrong-module|binding-wrong-property)
        [ "$result" = 1 ] && grep -q '^reset_ti_syscon ' /proc/modules || {
            echo 'ACE_RAMDIAG: FAIL OF binding refusal fixture'; exit 1;
        }
        if [ -f /ace-ramdiag/supervisor-test ]; then
            if grep -q '^reboot_mode ' /proc/modules || [ -e /tmp/ace-ramdiag-return-checkpoint ]; then
                echo 'ACE_RAMDIAG: FAIL later insertion after early binding refusal'; exit 1
            fi
        fi
        ;;
    supervisor-hang|supervisor-no-receipt|supervisor-wrong-receipt)
        expected=1
        [ "$fixture" = supervisor-hang ] && expected=124
        [ "$result" = "$expected" ] && [ -z "$(cat /proc/modules)" ] || {
            echo 'ACE_RAMDIAG: FAIL supervisor refusal fixture'; exit 1;
        }
        if [ "$fixture" = supervisor-hang ]; then
            $runner
            [ "$?" = 1 ] || { echo 'ACE_RAMDIAG: FAIL consumed supervisor accepted'; exit 1; }
        fi
        ;;
    hash-mismatch|gate-timeout|serial-mismatch|symlink-refusal)
        [ "$result" = 1 ] && [ -z "$(cat /proc/modules)" ] || {
            echo 'ACE_RAMDIAG: FAIL pre-insertion refusal fixture'; exit 1;
        }
        ;;
    *) echo 'ACE_RAMDIAG: FAIL unknown module fixture'; exit 1 ;;
esac
echo ACE_MODULE_FIXTURE_MODULES_BEGIN
cat /proc/modules
echo ACE_MODULE_FIXTURE_MODULES_END
echo "ACE_MODULE_FIXTURE: expected result verified $fixture"
