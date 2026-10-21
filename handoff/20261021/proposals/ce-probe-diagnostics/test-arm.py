from pathlib import Path
import json,subprocess,hashlib,shutil
P=Path(__file__).resolve().parent;old=P/'arm-source';T=P/'arm-test';T.mkdir(exist_ok=False)
for n in ['start.S','link.ld']:shutil.copy2(old/n,T/n)
s=(old/'fingerprint.S').read_text().replace('ce_fingerprint_call','probe_fingerprint_call').replace('bl guarded_ce_blocks','bl native_sha_ce_probe_diag')
a=s.index('#ifdef NO_SHA_FIXTURE');b=s.index(' mov x19,#1',a)
s=s[:a]+'''#ifdef FIXTURE_EL
 cmn w0,#1
 b.eq 2f
#elif defined(FIXTURE_SHA)
 cmn w0,#3
 b.eq 2f
#else
 cbz w0,2f
#endif
'''+s[b:];(T/'fingerprint.S').write_text(s)
g=(P/'sha_ce_guard.S').read_text();oldpart,diag=g.split('native_sha_ce_probe_diag:',1)
# Controlled fixtures exercise absent/unknown capability and EL refusal.
for name,replace in [('sha-absent-FIXTURE',(' mrs x9,ID_AA64ISAR0_EL1',' mov x9,#0 /* TEST fixture */')),('sha-unknown-FIXTURE',(' mrs x9,ID_AA64ISAR0_EL1',' mov x9,#(3<<12) /* TEST fixture */')),('el2-FIXTURE',(' mrs x9,CurrentEL',' mov x9,#8 /* TEST fixture */'))]:
 body=diag.replace(*replace)
 # Any forbidden later CPACR read causes an actual ARM trap in these fixtures.
 body=body.replace(' mrs x9,CPACR_EL1',' .inst 0 /* TEST must never reach CPACR read */')
 if name.startswith('el2'):body=body.replace(' mrs x9,DAIF',' .inst 0 /* TEST must not reach DAIF read */')
 (T/(name+'.S')).write_text(oldpart+'native_sha_ce_probe_diag:'+body)
flags=['aarch64-linux-gnu-gcc','-O2','-Wall','-Wextra','-Werror','-mcpu=cortex-a55','-mgeneral-regs-only','-mstrict-align','-ffreestanding','-fno-builtin','-fno-stack-protector','-fno-pie','-nostdlib','-static','-I',str(P),'-Wl,--build-id=none,-T,'+str(T/'link.ld')]
results=[]
for n,g,macros in [('production',P/'sha_ce_guard.S',[]),('sha-absent-FIXTURE',T/'sha-absent-FIXTURE.S',['-DFIXTURE_SHA']),('sha-unknown-FIXTURE',T/'sha-unknown-FIXTURE.S',['-DFIXTURE_SHA','-DFIXTURE_UNKNOWN']),('el2-FIXTURE',T/'el2-FIXTURE.S',['-DFIXTURE_EL'])]:
 elf=T/(n+'.elf');args=flags+macros+[str(T/'start.S'),str(g),str(T/'fingerprint.S'),str(P/'test.c'),'-o',str(elf)]
 r=subprocess.run(args,capture_output=True,text=True);(T/(n+'-build.log')).write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
 binary=T/(n+'.bin');subprocess.run(['aarch64-linux-gnu-objcopy','-O','binary',str(elf),str(binary)],check=True)
 args=['qemu-system-aarch64','-M','virt,virtualization=off','-cpu','cortex-a55,cntfrq=13000000','-m','256M','-smp','1','-display','none','-serial','none','-monitor','none','-nic','none','-semihosting-config','enable=on,target=native','-kernel',str(binary)]
 r=subprocess.run(args,capture_output=True,text=True,timeout=12);log=r.stdout+r.stderr;(T/(n+'-qemu.log')).write_text(log);assert r.returncode==0 and 'PASS' in log and 'FAIL' not in log,(n,r.returncode,log)
 results.append(dict(case=n,returncode=r.returncode,log=log,qemu_argv=args,elf_sha256=hashlib.sha256(elf.read_bytes()).hexdigest()))
(P/'verification.json').write_text(json.dumps(dict(status='PASS actual EL1 production probe fields/DAIF refusal/full SIMD/sysreg fingerprint; controlled unsupported/EL fixtures',source_sha256={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['sha_ce_guard.S','probe-diag.h','test.c','test-arm.py']},results=results,legacy_probe_signature_unchanged=True,phone_io=False),indent=2)+'\n')
print('PASS four actual ARM QEMU probe profiles')
