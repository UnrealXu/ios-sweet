"""Explicit synthetic native DT record for QEMU syscall tests, never a phone."""
import struct
import subprocess
from pathlib import Path
TOKEN='0123456789abcdef'
SOURCE=Path(__file__).resolve().parent


def compile_gate(out, command):
    (out/'native_config.h').write_text('static const char expected_native_token[]="'+TOKEN+'";\n')
    command=command[:-3]+['-I',str(out),str(SOURCE/'native_gate.c'),'-o',str(out/'native-gate')]
    result=subprocess.run(command,capture_output=True,text=True,timeout=30)
    (out/'native-build.log').write_text(result.stdout+result.stderr)
    if result.returncode:raise ValueError('QEMU native gate compile failed')
    return (out/'native-gate').read_bytes()


def record(kind):
    words=[0]*32;words[:4]=[0x313054414e454341,1,2 if kind=='refusal' else 5,(-64 if kind=='refusal' else -67)%(1<<64)]
    raw=b'ACEFALL1'+(TOKEN if kind!='stale' else 'f'*16).encode()+bytes(8)+struct.pack('<32Q',*words)
    return raw+b'\0' if kind=='oversize' else raw


def dtb(out, command, kind):
    command=list(command)
    index=command.index('-M')+1
    command[index]+=',dumpdtb='+str(out/'qemu-base.dtb')
    result=subprocess.run(command,capture_output=True,timeout=15)
    (out/'dtb-dump.log').write_bytes(result.stdout+result.stderr)
    if result.returncode:raise ValueError('QEMU fixture DT dump failed')
    raw=record(kind)
    overlay='/dts-v1/; /plugin/; / { fragment@0 { target-path="/chosen"; __overlay__ { ace,native-refusal=['+raw.hex(' ')+']; }; }; };\n'
    (out/'native-fixture.dts').write_text(overlay)
    subprocess.run(['dtc','-@','-I','dts','-O','dtb','-o',str(out/'native-fixture.dtbo'),str(out/'native-fixture.dts')],check=True,capture_output=True)
    subprocess.run(['fdtoverlay','-i',str(out/'qemu-base.dtb'),'-o',str(out/'native-fixture.dtb'),str(out/'native-fixture.dtbo')],check=True,capture_output=True)
    return out/'native-fixture.dtb'


def check(client,out,kind):
    mounts=client.shell('cat /proc/1/mountinfo')
    (out/'native-fixture-mountinfo.txt').write_bytes(mounts)
    if not any(b' /sys/fs/pstore ' in line and b' - pstore ' in line for line in mounts.splitlines()):raise ValueError('pstore virtual mount absent')
    output=client.shell('/ace-ramdiag/native-gate; echo NATIVE_GATE_STATUS=$?')
    (out/'native-gate-first.txt').write_bytes(output)
    expected=0 if kind in ('pending','refusal') else 1
    if ('NATIVE_GATE_STATUS='+str(expected)).encode() not in output:raise ValueError('native gate unexpected first status')
    if kind in ('pending','refusal'):
        saved=client.shell('cat /tmp/ace-ramdiag-native-checked')
        (out/'native-checkpoint.bin').write_bytes(saved)
        if saved!=record(kind):raise ValueError('actual RAM native receipt mismatch')
        again=client.shell('/ace-ramdiag/native-gate; echo NATIVE_GATE_STATUS=$?')
        (out/'native-gate-second.txt').write_bytes(again)
        if b'NATIVE_GATE_STATUS=1' not in again:raise ValueError('native gate repeated checkpoint accepted')
        if client.shell('cat /tmp/ace-ramdiag-native-checked')!=saved:raise ValueError('refusal changed checkpoint')
    else:
        saved=client.shell('if [ ! -e /tmp/ace-ramdiag-native-checked ]; then echo NO_NATIVE_CHECKPOINT; fi')
        if b'NO_NATIVE_CHECKPOINT' not in saved:raise ValueError('bad native envelope created receipt')
    return dict(native_gate_fixture=kind,native_gate_syscalls_verified=True,synthetic_native_record=True)
