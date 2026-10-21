#!/usr/bin/env python3
"""Build/run a RAM-root QEMU probe of pinned stock init/adbd, never a phone image."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import secrets
import socket
import stat
import subprocess
import tempfile
import time

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).resolve().parent
VENDOR=ROOT/'research/ace-backup-20261019-wireless-v2/vendor_boot_b.img'
VENDOR_SHA='bb5a094de2f3396b9be3b20354d637092ef57d1355413b784cd863f222839670'
KERNEL=ROOT/'research/ace-stock-qemu-20261019/Image'
KERNEL_SHA='8d555ba28c880d1c1f095172bc8cfa47fa1423d01fe8400c27faa340eb2f11d0'
spec=importlib.util.spec_from_file_location('ace_cpio',ROOT/'tools/ace-recovery-diag.py')
cpio=importlib.util.module_from_spec(spec);spec.loader.exec_module(cpio)
wire_spec=importlib.util.spec_from_file_location('ace_qemu_adb_wire',SOURCE/'adb_wire.py')
wire=importlib.util.module_from_spec(wire_spec);wire_spec.loader.exec_module(wire)
bundle_spec=importlib.util.spec_from_file_location('ace_module_bundle',SOURCE/'module_bundle.py')
bundle=importlib.util.module_from_spec(bundle_spec);bundle_spec.loader.exec_module(bundle)
fixture_spec=importlib.util.spec_from_file_location("ace_readout_fixture",SOURCE/"readout_fixture.py")
fixture=importlib.util.module_from_spec(fixture_spec);fixture_spec.loader.exec_module(fixture)
native_spec=importlib.util.spec_from_file_location('ace_native_fixture',SOURCE/'native_fixture.py')
native=importlib.util.module_from_spec(native_spec);native_spec.loader.exec_module(native)

def require(ok,message):
    if not ok:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def entry(name,data,mode=stat.S_IFREG|0o755):
    return name,[1,mode,0,0,1,0,0,0,0,0,0,0,0],data

def assemble(out,observe_pid1=False,*,trusted_public_key=None,trusted_public_key_sha256=None,tcp_auth_test=False,vendor_overlay_test=False,module_test=None,usb_ffs_test=False,supervise_modules=False,native_gate_test=False,console_absent=False):
    require((trusted_public_key is None)==(trusted_public_key_sha256 is None),'key bytes and pin required together')
    if trusted_public_key is not None:wire.validate_public_key(trusted_public_key,trusted_public_key_sha256)
    require(not tcp_auth_test or trusted_public_key is not None,'TCP authentication test requires pinned key')
    sources=[*[ROOT/'ace'/n for n in ['pstore_ring.c','pstore_ring.h','pstore_trial.c','pstore_trial.h','pstore_rescue.c','pstore_rescue.h']],Path(__file__),SOURCE/'preinit.c',SOURCE/'pmsg_trace.h',SOURCE/'slot_guard.h',SOURCE/'init.rc',SOURCE/'probe.sh',
             SOURCE/'adb_wire.py',SOURCE/'readout_fixture.py',ROOT/'tools/ace_ram_readout.py',SOURCE/'module_bundle.py',SOURCE/'module_plan.py',ROOT/'tools/fdt.py',
             ROOT/'diagnostics/ace-irq-timer/qemu-start.S',ROOT/'tools/ace-recovery-diag.py']
    if module_test:
        require(module_test in ('insert','hash-mismatch','gate-timeout','syscall-error','serial-mismatch','binding-missing','binding-wrong-driver','binding-wrong-module','binding-wrong-property','symlink-refusal','supervisor-hang','supervisor-no-receipt','supervisor-wrong-receipt'),'unknown module fixture')
        require(not vendor_overlay_test,'module fixture uses filtered diskless environment; full hardware overlay remains separate')
        sources += [SOURCE/n for n in ['module_loader.c','module_supervisor.c','sha256.h','module_probe.sh','aarch64_flags.h']]
        if module_test.startswith('supervisor-'):sources.append(SOURCE/'module_fault.c')
    require(not supervise_modules or module_test is not None,'supervision requires a module fixture')
    require(not module_test or not module_test.startswith('supervisor-') or supervise_modules,'fault fixture requires supervision')
    if native_gate_test:
        sources += [SOURCE/n for n in ["native_fixture.py","native_gate.c","native_record_guard.h","aarch64_flags.h"]]
    proxy_command=None
    if usb_ffs_test:
        sources += [SOURCE/'usb-fixture.rc',SOURCE/'usb_probe.sh']
        if tcp_auth_test:sources += [SOURCE/'dummy_usb_proxy.c',SOURCE/'usb_descriptors.h',SOURCE/'aarch64_flags.h']
    for path in sources:
        copy=out/'source-snapshot'/path.relative_to(ROOT)
        copy.parent.mkdir(parents=True,exist_ok=True);copy.write_bytes(path.read_bytes())
    vendor=VENDOR.read_bytes();require(sha(vendor)==VENDOR_SHA,'vendor backup hash mismatch')
    kernel=KERNEL.read_bytes();require(sha(kernel)==KERNEL_SHA,'refusal kernel hash mismatch')
    compressed=cpio.read_vendor(vendor)['ramdisk']
    raw=subprocess.run(['lz4','-dc'],input=compressed,capture_output=True,check=True).stdout
    original=[(n,f,d) for n,f,d in cpio.read_cpio(raw) if n!='TRAILER!!!']
    members={n:(f,d) for n,f,d in original}
    require(len(members)==len(original),'duplicate vendor CPIO names')
    for n in members:
        require(not Path(n).is_absolute() and '..' not in Path(n).parts,'unsafe vendor CPIO path')
    seeds=['system/bin/init','system/bin/adbd','system/bin/sh','system/bin/toybox',
           'system/bin/toolbox','system/bin/reboot','system/bin/linker64']
    selected={};queue=list(seeds)
    with tempfile.TemporaryDirectory(prefix='ace-ramdiag-elf-') as temp:
        while queue:
            name=queue.pop(0)
            if name in selected:continue
            require(name in members,'missing dependency '+name)
            f,data=members[name];require(stat.S_ISREG(f[1]) and data[:4]==b'\x7fELF','non-ELF dependency '+name)
            path=Path(temp)/'input.elf';path.write_bytes(data)
            dynamic=subprocess.run(['readelf','-d',str(path)],capture_output=True,text=True,check=True).stdout
            needed=re.findall(r'\(NEEDED\).*?\[([^\]]+)\]',dynamic)
            for lib in needed:
                require('/' not in lib and lib not in ('.','..'),'unsafe library name')
                queue.append('system/lib64/'+lib)
            selected[name]=(f,data)
    # Use original context/policy bytes. Stock startup scripts and persistent
    # mount configuration are omitted or neutralized, including full overlays.
    for name,(f,data) in members.items():
        if '/' not in name and (name.endswith('_contexts') or name=='sepolicy'):
            selected[name]=(f,data)
    for name in ['system/etc/ld.config.txt','system/etc/selinux/plat_file_contexts']:
        selected[name]=members[name]
    for name in ['cat','id','getprop','setprop','getenforce','pidof','sleep','printf','stat','readlink','sha256sum','mkdir','ln']:
        path='system/bin/'+name;selected[path]=members[path]
    if tcp_auth_test:selected['system/bin/ifconfig']=members['system/bin/ifconfig']
    if module_test:
        for name in ['grep','insmod']:selected['system/bin/'+name]=members['system/bin/'+name]
    command=['aarch64-linux-gnu-gcc','-O2','-static','-nostdlib','-ffreestanding',
             '-fno-builtin','-fno-stack-protector','-fno-pie','-no-pie','-Wall','-Wextra','-Werror',
             '-Wl,--build-id=none,-e,_start,--strip-all',str(ROOT/'diagnostics/ace-irq-timer/qemu-start.S'),
             str(SOURCE/'preinit.c'),'-o',str(out/'preinit')]
    result=subprocess.run(command,capture_output=True,text=True)
    (out/'build.log').write_text(result.stdout+result.stderr)
    require(result.returncode==0,'preinit compile failed; see build.log')
    payload=[entry(n,d,f[1]) for n,(f,d) in sorted(selected.items())]
    payload.extend([entry('init',(out/'preinit').read_bytes()),
        entry('system/bin/ueventd',b'init',stat.S_IFLNK|0o755),
        # IsRecoveryMode tests existence only. Never include/start recovery.
        entry('system/bin/recovery',b'',stat.S_IFREG|0o644),
        entry('system/etc/init/hw/init.rc',(SOURCE/'init.rc').read_bytes(),stat.S_IFREG|0o644),
        entry('ace-ramdiag/probe.sh',(SOURCE/'probe.sh').read_bytes().replace(b'exec >/dev/console 2>&1',b'count=0\nwhile [ ! -c /dev/ttyAMA0 ] && [ "$count" -lt 10 ]; do sleep 1; count=$((count+1)); done\n[ -c /dev/ttyAMA0 ] || exit 1\nexec >/dev/ttyAMA0 2>&1') if console_absent else (SOURCE/'probe.sh').read_bytes()),
        entry('prop.default',b'ro.secure=0\nro.adb.secure=1\nro.debuggable=1\nro.build.version.sdk=31\nro.product.first_api_level=31\nro.build.type=userdebug\nservice.adb.listen_addrs=tcp:5555\n',stat.S_IFREG|0o644)])
    if observe_pid1:payload.append(entry('ace-ramdiag/observe-pid1',b'',stat.S_IFREG|0o644))
    if trusted_public_key is not None:payload.append(entry('adb_keys',trusted_public_key,stat.S_IFREG|0o600))
    if tcp_auth_test:payload.append(entry('ace-ramdiag/tcp-auth-test',b'',stat.S_IFREG|0o644))
    if usb_ffs_test:
        for index,(name,fields,data) in enumerate(payload):
            if name=='system/etc/init/hw/init.rc':payload[index]=entry(name,data+b'\nimport /ace-ramdiag/usb-fixture.rc\n',fields[1])
            if name=='prop.default':payload[index]=entry(name,data.replace(b'service.adb.listen_addrs=tcp:5555\n',b'service.adb.tcp.port=-1\n'),fields[1])
        payload += [entry('ace-ramdiag/usb-fixture.rc',(SOURCE/'usb-fixture.rc').read_bytes(),stat.S_IFREG|0o644),
                    entry('ace-ramdiag/usb-probe.sh',(SOURCE/'usb_probe.sh').read_bytes()),
                    entry('ace-ramdiag/usb-fixture',b'',stat.S_IFREG|0o400)]
        if tcp_auth_test:
            proxy_command=command[:-3]+[str(SOURCE/'dummy_usb_proxy.c'),'-o',str(out/'dummy-usb-proxy')]
            result=subprocess.run(proxy_command,capture_output=True,text=True,timeout=30)
            (out/'proxy-build.log').write_text(result.stdout+result.stderr)
            require(result.returncode==0,'USB proxy compile failed; inspect proxy-build.log')
            payload += [entry('ace-ramdiag/dummy-usb-proxy',(out/'dummy-usb-proxy').read_bytes()),
                        entry('ace-ramdiag/usb-proxy',b'',stat.S_IFREG|0o400),
                        entry('ace-ramdiag/usb-boundary.bin',bytes(range(256))*32,stat.S_IFREG|0o400)]
    if native_gate_test:
        payload.append(entry("ace-ramdiag/native-gate",native.compile_gate(out,command)))
        for index,(name,fields,data) in enumerate(payload):
            if name=='system/etc/init/hw/init.rc':
                data=data.replace(b'on early-init\n',b'on early-init\n    mkdir /sys/fs/pstore 0755 root root\n    mount pstore pstore /sys/fs/pstore\n',1)
                payload[index]=entry(name,data,fields[1])
    module_report=None
    if module_test:
        names=['reset-ti-syscon.ko']
        if module_test in ('hash-mismatch','syscall-error') or supervise_modules:names.append('reboot-mode.ko')
        release=re.findall(rb'Linux version ([0-9][^ \x00\n]{1,63}) ',kernel)
        require(len(release)==1,'kernel release banner ambiguous')
        items=[dict(module=n,data=members['lib/modules/'+n][1],gate='/sys/class/tcpc/type_c_port0' if module_test=='gate-timeout' else '/sys/devices') for n in names]
        bindings=[]
        if module_test in ('insert','binding-missing','binding-wrong-driver','binding-wrong-module','binding-wrong-property') or supervise_modules:
            bindings=[dict(dt_path='/missing-controller' if module_test=='binding-missing' else '/pcie@10000000',
                           driver='wrong-pci' if module_test=='binding-wrong-driver' else 'pci-host-generic',
                           module='reset_ti_syscon' if module_test=='binding-wrong-module' else '',class_path='/sys/bus/pci',
                           properties={'reg':'00000040100000000000000010000001' if module_test=='binding-wrong-property' else '00000040100000000000000010000000'},early=supervise_modules)]
        module_report=bundle.compile_bundle(out/'loader-bundle',items,expected_release=release[0].decode(),
                    expected_serial='RAMDIAG_WRONG_FIXTURE' if module_test=='serial-mismatch' else 'RAMDIAG_QEMU_FIXTURE',bindings=bindings,
                    return_prefix_count=1 if supervise_modules else 0,supervisor_timeout=1 if module_test=='supervisor-hang' else 30)
        loader=(out/'loader-bundle/module-loader').read_bytes()
        if module_test.startswith('supervisor-'):
            mode={'supervisor-hang':1,'supervisor-no-receipt':0,'supervisor-wrong-receipt':2}[module_test]
            (out/'fault_config.h').write_text('#define MODULE_FAULT_MODE '+str(mode)+'\n')
            fault_command=command[:-3]+['-I',str(out),str(SOURCE/'module_fault.c'),'-o',str(out/'module-fault')]
            (out/'fault-build-command.json').write_text(json.dumps(fault_command,indent=2)+'\n')
            result=subprocess.run(fault_command,capture_output=True,text=True,timeout=30)
            (out/'fault-build.log').write_text(result.stdout+result.stderr);require(result.returncode==0,'fault fixture compile failed')
            loader=(out/'module-fault').read_bytes()
        payload += [entry('ace-ramdiag/module-loader',loader),
                    entry('ace-ramdiag/module-probe.sh',(SOURCE/'module_probe.sh').read_bytes()),
                    entry('ace-ramdiag/module-fixture',module_test.encode(),stat.S_IFREG|0o400)]
        if supervise_modules:
            payload += [entry('ace-ramdiag/module-supervisor',(out/'loader-bundle/module-supervisor').read_bytes()),
                        entry('ace-ramdiag/supervisor-test',b'',stat.S_IFREG|0o400)]
        for name in names:
            data=members['lib/modules/'+name][1]
            if module_test=='hash-mismatch' and name==names[-1]:data=data[:64]+bytes([data[64]^1])+data[65:]
            if module_test=='symlink-refusal':
                payload.append(entry('ace-ramdiag/real/'+name,data,stat.S_IFREG|0o400))
                payload.append(entry('ace-ramdiag/modules/'+name,('../real/'+name).encode(),stat.S_IFLNK|0o777))
            else:payload.append(entry('ace-ramdiag/modules/'+name,data,stat.S_IFREG|0o400))
    neutralized=[]
    if vendor_overlay_test:
        require({n for n in members if n=='data' or n.startswith('data/')}=={'data','data/vendor'},'unexpected stock RAM data tree')
        require(all(stat.S_ISDIR(members[n][0][1]) for n in ['data','data/vendor']),'stock RAM data entries are not directories')
        module_dirs={str(Path(n).parent) for n in members if n.endswith('.ko')}
        require(module_dirs=={'lib/modules'},'unhandled original module directory')
        for name,(fields,data) in sorted(members.items()):
            if name=='system/etc/init/hw/init.rc':continue
            if name.endswith(('.rc','.prop')) or Path(name).name.startswith('fstab'):
                require(stat.S_ISREG(fields[1]) or stat.S_ISLNK(fields[1]),'unexpected startup config type')
                require(re.fullmatch(r'[A-Za-z0-9_./+-]+',name),'unsafe startup config path')
                neutralized.append({'path':name,'original_sha256':sha(data),'original_mode':oct(fields[1])})
                payload.append(entry(name,b'# ACE_RAMDIAG_DISABLED\n',stat.S_IFREG|0o644))
        payload.extend([entry('ace-ramdiag/vendor-overlay',b'',stat.S_IFREG|0o644),
                        entry('ace-ramdiag/neutralized-paths',('\n'.join('/'+r['path'] for r in neutralized)+'\n').encode(),stat.S_IFREG|0o644)])
    dirs={'dev','proc','sys','tmp','mnt','apex','linkerconfig'}
    for n,_,_ in payload:
        dirs.update(str(p) for p in Path(n).parents if str(p)!='.')
    payload=[entry(n,b'',stat.S_IFDIR|0o755) for n in sorted(dirs,key=lambda n:(n.count('/'),n))]+payload
    payload.append(entry('TRAILER!!!',b'',0))
    generic=cpio.write_cpio(payload)
    ramdisk=gzip.compress(generic,mtime=0)
    (out/'initramfs.cpio.gz').write_bytes(ramdisk)
    kernel_initrd='initramfs.cpio.gz';extra={}
    if vendor_overlay_test:
        require(compressed[:4]==bytes.fromhex('02214c18'),'expected stock legacy LZ4 vendor ramdisk')
        command_lz4=['lz4','-l','-9','-c']
        ramdisk=subprocess.run(command_lz4,input=generic,capture_output=True,check=True).stdout
        require(ramdisk[:4]==compressed[:4],'generic compression format differs')
        unpacked=subprocess.run(['lz4','-dc'],input=ramdisk,capture_output=True,check=True).stdout
        require(unpacked==generic,'generic LZ4 roundtrip mismatch')
        (out/'generic-ramdisk.lz4').write_bytes(ramdisk)
        combined=compressed+ramdisk
        kernel_initrd='vendor-plus-generic.initrd';(out/kernel_initrd).write_bytes(combined)
        extra=dict(compression_command=command_lz4,original_vendor_ramdisk_sha256=sha(compressed),
                   original_vendor_members=len(members),neutralized_startup_paths=neutralized,
                   original_vendor_prefix_byteidentical=combined[:len(compressed)]==compressed,
                   combined_initrd_sha256=sha(combined),combined_initrd_bytes=len(combined))
    return dict(vendor_sha256=sha(vendor),kernel_sha256=sha(kernel),ramdisk_sha256=sha(ramdisk),
                kernel_initrd_filename=kernel_initrd,vendor_overlay_test=vendor_overlay_test,module_test=module_test,module_bundle=module_report,usb_ffs_test=usb_ffs_test,usb_proxy_build_command=proxy_command,supervise_modules=supervise_modules,**extra,
                source_sha256={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sources},
                build_command=command,files={n:{'sha256':sha(d),'mode':oct(f[1]),'bytes':len(d)} for n,f,d in payload})

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    parser.add_argument('--selinux-disabled',action='store_true',help='explicit limited-policy diagnostic comparison')
    parser.add_argument('--observe-pid1',action='store_true',help='dump stalled guest PID1 proc state then power off; not an acceptance run')
    parser.add_argument('--tcp-auth-test',action='store_true',help='ephemeral keys; restricted QEMU network and loopback-only ADB wire test')
    parser.add_argument('--vendor-overlay-test',action='store_true',help='prepend exact original vendor ramdisk; neutralize startup scripts/config and hide stock modules')
    parser.add_argument('--slot-fixture',choices=['_b','_a','absent','conflict'],default='_b',help='negative values test preinit refusal only')
    parser.add_argument('--module-test',choices=['insert','hash-mismatch','gate-timeout','syscall-error','serial-mismatch','binding-missing','binding-wrong-driver','binding-wrong-module','binding-wrong-property','symlink-refusal','supervisor-hang','supervisor-no-receipt','supervisor-wrong-receipt'],help='one-pass loader/OF/supervisor fixture; no MT6895 hardware proof')
    parser.add_argument('--supervise-modules',action='store_true',help='one fixed child, deadline and exact identity receipt; no reset/retry')
    parser.add_argument('--usb-ffs-test',action='store_true',help='stock adbd FunctionFS descriptors and in-guest dummy_hcd enumeration; no physical USB')
    parser.add_argument('--readout-command-test',action='store_true',help='read-only synthetic USB GPT disk with two full64MiB hash commands; physical UFS gate must refuse')
    parser.add_argument('--native-gate-test',choices=['pending','refusal','stale','oversize'],help='explicit synthetic chosen record; actual gate syscalls/checkpoint only, never physical native proof')
    parser.add_argument('--console-fixture',choices=['normal','absent'],default='normal',help='absent selects disabled tty0 with boot printk only; not a physical-console claim')
    parser.add_argument('--expect-console-refusal',action='store_true',help='negative fixture for old preinit; no init or ADB acceptance')
    args=parser.parse_args();out=args.output.resolve()
    require(not args.expect_console_refusal or args.console_fixture=='absent' and not args.tcp_auth_test,'console refusal requires isolated absent-console fixture')
    require(not args.native_gate_test or args.tcp_auth_test,'native syscall fixture requires authenticated wire test')
    require(not args.readout_command_test or args.tcp_auth_test,'readout command fixture requires authenticated wire test')
    require(not out.exists() and out.is_relative_to(ROOT/'research'),'new private research output required')
    require(not(args.tcp_auth_test and args.observe_pid1),'observer is not an authentication acceptance run')
    require(not args.tcp_auth_test or args.slot_fixture=='_b','authentication requires positive B-slot fixture')
    out.mkdir(parents=True,mode=0o700);report={'status':'incomplete','phone_io':False,'hardware_tested':False,'ios_deployable':False,'trusted_host_key_configured':args.tcp_auth_test}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    trusted_public=None;key_pin=None
    if args.tcp_auth_test:
        trusted,trusted_public=wire.generate_key(out/'trusted.pem')
        wrong,_=wire.generate_key(out/'untrusted.pem')
        key_pin=sha(trusted_public)
        report['trusted_public_key_sha256']=key_pin
        report['qemu_auth_run_nonce']=secrets.token_hex(8)
    try:report.update(assemble(out,args.observe_pid1,trusted_public_key=trusted_public,trusted_public_key_sha256=key_pin,tcp_auth_test=args.tcp_auth_test,vendor_overlay_test=args.vendor_overlay_test,module_test=args.module_test,usb_ffs_test=args.usb_ffs_test,supervise_modules=args.supervise_modules,native_gate_test=bool(args.native_gate_test),console_absent=args.console_fixture=="absent"))
    except Exception as error:
        report.update(status='build failed',error=str(error))
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        raise
    append='console=ttyAMA0 earlycon=pl011,0x09000000 rdinit=/init nokaslr loglevel=8 panic=-1 androidboot.serialno=RAMDIAG_QEMU_FIXTURE'
    if args.slot_fixture!='absent':append+=' androidboot.slot_suffix='+('_b androidboot.slot_suffix=_a' if args.slot_fixture=='conflict' else args.slot_fixture)
    if args.selinux_disabled:append+=' selinux=0'
    if args.console_fixture=='absent':append=append.replace('console=ttyAMA0','console=tty0')+' keep_bootcon'
    command=['qemu-system-aarch64','-M','virt,gic-version=3,virtualization=off','-cpu','cortex-a55',
             '-m','2G','-smp','1','-kernel',str(KERNEL),'-initrd',str(out/report['kernel_initrd_filename']),
             '-append',append,'-no-reboot','-display','none','-monitor','none','-nic','none',
             '-serial','file:'+str(out/'serial.log')]
    if args.tcp_auth_test:
        with socket.socket() as reservation:reservation.bind(('127.0.0.1',0));port=reservation.getsockname()[1]
        # Exact kernel has no virtio-net/mmio driver. Its built-in PCI xHCI
        # and CDC Ethernet drivers can exercise a QEMU USB-network fixture.
        index=command.index('-nic');command[index:index+2]=['-netdev',f'user,id=diag,restrict=on,hostfwd=tcp:127.0.0.1:{port}-:5555','-device','qemu-xhci,id=diagxhci','-device','usb-net,netdev=diag,bus=diagxhci.0']
        report['qemu_loopback_port']=port
    if args.readout_command_test:
        disk,descriptors,hashes=fixture.disk(out)
        command+=['-drive',f'file={disk},if=none,id=readout,format=raw,readonly=on','-device','usb-storage,drive=readout,bus=diagxhci.0']
        report['synthetic_readout_disk_sha256']=sha(disk.read_bytes())
    if args.native_gate_test:command+=['-dtb',str(native.dtb(out,command,args.native_gate_test))]
    report.update(qemu_command=command,selinux_disabled_requested=args.selinux_disabled,pid1_observer_enabled=args.observe_pid1,slot_fixture=args.slot_fixture)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with (out/'host.log').open('w') as log:
        process=subprocess.Popen(command,stdout=log,stderr=log)
        positive=None
        try:
            if args.tcp_auth_test:
                deadline=time.monotonic()+(60 if args.usb_ffs_test else 35)
                while time.monotonic()<deadline and process.poll() is None:
                    if (out/'serial.log').exists():
                        current=(out/'serial.log').read_text(errors='replace')
                        if 'ACE_RAMDIAG: QEMU TCP ready' in current and (not args.usb_ffs_test or 'ACE_USB_PROXY: ready two-session USB-only bridge' in current):break
                    time.sleep(0.25)
                else:raise ValueError('QEMU TCP readiness absent; inspect serial')
                negative=wire.QemuADB(port)
                try:
                    report['untrusted_signature_rejected']=negative.authenticate(wrong) is False
                    require(report['untrusted_signature_rejected'],'untrusted signature accepted')
                finally:
                    report['negative_auth_events']=negative.events;negative.close()
                positive=wire.QemuADB(port,timeout=90,idle_timeout=30) if args.readout_command_test else wire.QemuADB(port)
                try:
                    require(positive.authenticate(trusted),'pinned trusted signature rejected')
                    report['trusted_signature_accepted']=True;report['adb_banner']=positive.banner
                    nonce=report['qemu_auth_run_nonce']
                    output=positive.shell(f"printf 'ACE_AUTHENTICATED_COMMAND_V1:{nonce}\\n'; id; getprop ro.serialno; getprop ro.adb.secure; getprop ro.boot.slot_suffix; if [ ! -e /data ]; then printf 'NO_DATA_DIRECTORY\\n'; fi")
                    (out/'authenticated-shell.txt').write_bytes(output)
                    require(b'uid=0(root)' in output and b'RAMDIAG_QEMU_FIXTURE' in output and b'NO_DATA_DIRECTORY' in output,'authenticated shell identity/root/data mismatch')
                    require(('ACE_AUTHENTICATED_COMMAND_V1:'+nonce).encode() in output,'fresh authenticated command nonce absent')
                    require(b'\n1\n_b\n' in output.replace(b'\r',b''),'authenticated secure/B-slot mismatch')
                    if args.usb_ffs_test:
                        boundary=positive.shell('cat /ace-ramdiag/usb-boundary.bin')
                        (out/'usb-authenticated-binary.bin').write_bytes(boundary)
                        require(boundary==bytes(range(256))*32,'USB authenticated binary stream mismatch')
                        report['usb_binary_stream_8192_verified']=True
                    if args.native_gate_test:report.update(native.check(positive,out,args.native_gate_test))
                    if args.readout_command_test:report.update(fixture.check(positive,out,descriptors,hashes))
                    receipt=positive.shell(f"printf '{nonce}\\n' > /tmp/ace-adb-auth.done; cat /tmp/ace-adb-auth.done")
                    require(receipt.replace(b'\r',b'')==(nonce+'\n').encode(),'authenticated RAM command receipt mismatch')
                    report['authenticated_root_shell_verified']=True
                    # The shell service is intentionally allowed to disappear
                    # during this one poweroff request. Guest watchdog failure
                    # text still makes acceptance fail; never retry the command.
                    positive.open_shell('reboot -p')
                    report['authenticated_poweroff_command_sent_once']=True
                finally:
                    report['positive_auth_events']=positive.events
            report['returncode']=process.wait(timeout=55)
        except subprocess.TimeoutExpired:report['timed_out']=True
        except Exception as error:report['runtime_error']=str(error)
        finally:
            if positive is not None:positive.close()
            if process.poll() is None:
                process.terminate()
                try:process.wait(timeout=3)
                except subprocess.TimeoutExpired:process.kill();process.wait(timeout=3)
    serial=(out/'serial.log').read_text(errors='replace')
    if args.console_fixture=='absent':
        # The fixture redirects only its QEMU probe to the available raw UART. Keep raw UART
        # unchanged; strip printk prefixes solely for existing proc parsers.
        serial=re.sub(r'^\[\s*\d+\.\d+\]\s*(?:\[\s*[^]\n]+\]\s*)?','',serial,flags=re.M)
    markers=['ACE_RAMDIAG: PID1 RAM root verified','ACE_RAMDIAG: B-slot gate verified before stock init','init second stage started!',
             'ACE_RAMDIAG: stock shell entered','uid=0(root)',
             'ACE_RAMDIAG: property readback=stage2-probe-v1','ACE_RAMDIAG: no /data directory',
             'ACE_RAMDIAG: adbd pid=','ACE_RAMDIAG: probe workload complete','reboot: Power down']
    report['markers']={m:m in serial for m in markers}
    if args.vendor_overlay_test:
        report['overlay_runtime_verified']=all(m in serial for m in ['ACE_RAMDIAG: stock module tree hidden','ACE_RAMDIAG: full vendor overlay verified'])
    report['monolithic_policy_loaded']='ACE_RAMDIAG: monolithic policy loaded; permissive diagnostic guest' in serial
    mounts=re.search(r'ACE_RAMDIAG_MOUNTS_BEGIN\r?\n(.*?)ACE_RAMDIAG_MOUNTS_END',serial,re.S)
    allowed={'rootfs','proc','sysfs','tmpfs','devpts','selinuxfs','cgroup','cgroup2'}
    if args.native_gate_test:allowed.add('pstore')
    if args.usb_ffs_test:allowed|={'configfs','functionfs'}
    mountlines=[line for line in mounts.group(1).splitlines() if re.match(r'^\d+ \d+ ',line)] if mounts else []
    report['observed_mountinfo']=mountlines
    points={line.split()[4] for line in mountlines}
    report['virtual_mounts_only']={'/','/proc','/sys','/dev'}<=points and all(' - ' in line and line.split(' - ',1)[1].split()[0] in allowed and not (line.split()[4]=='/data' or line.split()[4].startswith('/data/')) for line in mountlines)
    daemon=re.search(r'ACE_RAMDIAG_ADBD_STATUS_BEGIN\r?\n(.*?)ACE_RAMDIAG_ADBD_STATUS_END',serial,re.S)
    report['adbd_uid0_observed']=bool(daemon and re.search(r'^Uid:\s+0\s+0\s+0\s+0\s*$',daemon.group(1),re.M))
    report['serial_sha256']=sha((out/'serial.log').read_bytes())
    policy_ok=args.selinux_disabled or report['monolithic_policy_loaded']
    auth_ok=not args.tcp_auth_test or all(report.get(k) is True for k in ['untrusted_signature_rejected','trusted_signature_accepted','authenticated_root_shell_verified','authenticated_poweroff_command_sent_once'])
    auth_ok=auth_ok and (not args.readout_command_test or report.get('full_partition_command_verified') is True and report.get('synthetic_usb_disk_refused_as_ufs') is True)
    auth_ok=auth_ok and (not args.native_gate_test or report.get('native_gate_syscalls_verified') is True)
    overlay_ok=not args.vendor_overlay_test or report.get('overlay_runtime_verified') is True
    module_ok=True
    if args.module_test:
        required={'insert':['complete insertion only; hardware readiness unproven','OF binding verified /pcie@10000000 driver=pci-host-generic module=builtin','FAIL one-pass latch rc=-17'],
                  'hash-mismatch':['FAIL module SHA256 rc=-22'], 'gate-timeout':['FAIL gate deadline rc=-110'],
                  'syscall-error':['FAIL finit_module rc=-17'], 'serial-mismatch':['FAIL serial identity rc=-22'],
                  'binding-missing':['FAIL OF binding deadline rc=-110'],
                  'binding-wrong-driver':['FAIL binding driver identity rc=-22'],
                  'binding-wrong-module':['FAIL binding module identity rc=-22'],
                  'binding-wrong-property':['FAIL binding DT property bytes rc=-22'],
                  'symlink-refusal':['FAIL /ace-ramdiag/modules/reset-ti-syscon.ko rc=-40'],
                  'supervisor-hang':[], 'supervisor-no-receipt':[], 'supervisor-wrong-receipt':[]}[args.module_test]
        if args.supervise_modules and args.module_test=='insert':required=[m for m in required if not m.startswith('FAIL one-pass')]
        module_ok=all('ACE_MODULE_LOADER: '+m in serial for m in required) and ('ACE_MODULE_FIXTURE: expected result verified '+args.module_test) in serial
        if args.module_test in ('hash-mismatch','gate-timeout','serial-mismatch','symlink-refusal'):module_ok=module_ok and 'ACE_MODULE_LOADER: inserting ' not in serial
        if args.module_test=='insert':module_ok=module_ok and serial.count('ACE_MODULE_LOADER: inserting ')==(2 if args.supervise_modules else 1)
        if args.supervise_modules:
            module_ok=module_ok and serial.count('ACE_MODULE_SUPERVISOR: child started once')==1
            if args.module_test=='insert':
                checkpoint=serial.find('ACE_MODULE_LOADER: return bindings checkpoint;')
                later=serial.find('ACE_MODULE_LOADER: inserting /ace-ramdiag/modules/reboot-mode.ko')
                module_ok=module_ok and 0<=checkpoint<later and 'ACE_MODULE_SUPERVISOR: completion identity verified' in serial
            elif args.module_test=='supervisor-hang':module_ok=module_ok and 'ACE_MODULE_SUPERVISOR: timed-out child reaped; no retry' in serial and 'ACE_MODULE_SUPERVISOR: FAIL one-pass latch rc=-17' in serial and serial.count('ACE_MODULE_FAULT: child started once')==1
            elif args.module_test in ('supervisor-no-receipt','supervisor-wrong-receipt'):module_ok=module_ok and 'ACE_MODULE_SUPERVISOR: FAIL missing or wrong identity receipt rc=-22' in serial
            else:module_ok=module_ok and 'ACE_MODULE_SUPERVISOR: FAIL child failure; no retry' in serial
        report['module_fixture_verified']=module_ok
    usb_ok=not args.usb_ffs_test or all(m in serial for m in ['ACE_USB_FIXTURE: adbd TCP listener disabled','ACE_USB_FIXTURE: stock adbd FunctionFS descriptors ready','ACE_USB_FIXTURE: bound exact dummy UDC','ACE_USB_FIXTURE: FunctionFS + dummy host enumeration verified'])
    if args.usb_ffs_test:
        report['usb_initial_bind_timeout_observed']='timed out while waiting for FUNCTIONFS_BIND' in serial
        usb_ok=usb_ok and not report['usb_initial_bind_timeout_observed']
    if args.usb_ffs_test and args.tcp_auth_test:
        usb_ok=usb_ok and 'ACE_USB_PROXY: claimed synthetic identity and ADB bulk endpoints' in serial and 'ACE_USB_PROXY: ready two-session USB-only bridge' in serial and 'ACE_USB_PROXY: USB OUT CNXN' in serial and 'ACE_USB_PROXY: USB IN AUTH' in serial and report.get('usb_binary_stream_8192_verified') is True and 'ACE_USB_PROXY: FAIL' not in serial
    if args.usb_ffs_test:report['usb_enumeration_fixture_verified']=usb_ok
    report['status']=('pass RAM stage2 synthetic-disk component probe' if args.readout_command_test else 'pass diskless stage2 component probe') if not args.observe_pid1 and report.get('returncode')==0 and all(report['markers'].values()) and report['virtual_mounts_only'] and report['adbd_uid0_observed'] and policy_ok and auth_ok and overlay_ok and module_ok and usb_ok and 'ACE_RAMDIAG: FAIL' not in serial else 'failed; inspect retained serial'
    if args.slot_fixture!='_b':
        refused='ACE_RAMDIAG: FAIL B-slot gate rc=-22' in serial
        no_init='ACE_RAMDIAG: exec exact recovery init second_stage' not in serial and 'init second stage started!' not in serial
        report['slot_refusal_before_init_verified']=refused and no_init and report.get('returncode')==0 and 'reboot: Power down' in serial
        report['status']='pass preinit slot refusal only' if report['slot_refusal_before_init_verified'] else 'failed slot refusal; inspect serial'
    if args.console_fixture=='absent' and not args.expect_console_refusal:
        report['console_stdio_fallback_verified']='ACE_RAMDIAG: unavailable console; stdin null, output kmsg' in serial
        if not report['console_stdio_fallback_verified']:report['status']='failed missing console fallback evidence'
    if args.expect_console_refusal:
        report['console_unavailable_refusal_verified']=report.get('returncode')==0 and 'Warning: unable to open an initial console' in serial and 'reboot: Power down' in serial and 'init second stage started!' not in serial
        report['status']='pass expected console-unavailable refusal only' if report['console_unavailable_refusal_verified'] else 'failed console refusal fixture'
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','markers','serial_sha256']},indent=2))
    require(report['status'].startswith('pass'),'QEMU stage2 probe failed')

if __name__=='__main__':main()
