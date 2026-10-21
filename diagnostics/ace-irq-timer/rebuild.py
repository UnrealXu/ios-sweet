#!/usr/bin/env python3
"""Host-only normal Kbuild; authenticated OEM import CRCs, unchanged live config."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('register_replay', HERE.parent/'ace-read-regs/rebuild.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)
OEM = replay.CAPTURE/'arm_dsu_pmu.ko'
OEM_SHA = replay.EXPECTED[OEM]
GPL_IMPORTS = set()
NEEDED = ('module_layout', 'printk')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check-only', action='store_true')
    p.add_argument('--output', type=Path, default=ROOT/'research/ace-irq-timer-live-20261019/module')
    a = p.parse_args()
    for path, expected in replay.EXPECTED.items():
        replay.require(path.is_file() and replay.sha(path)==expected, f'Missing/changed input: {path}')
    replay.require(replay.sha(OEM)==OEM_SHA, 'OEM module hash mismatch')
    headers = replay.verify_archive(replay.CAPTURE/'kheaders.tar.xz', replay.TREE)
    scripts = replay.verify_archive(replay.PRIVATE/'scripts.tar.gz', replay.TREE/'scripts')
    versions = replay.versions(replay.elf_sections(OEM))
    replay.require(all(name in versions for name in NEEDED), 'Authentic OEM CRC missing')
    required = {name:versions[name] for name in NEEDED}
    print(f'Inputs verified: {headers} exact headers, {scripts} scripts, {len(required)} authentic imports')
    if a.check_only:
        return
    out = a.output.resolve()
    replay.require(out.is_relative_to(ROOT/'research/ace-irq-timer-live-20261019'), 'Output outside private area')
    out.mkdir(parents=True, exist_ok=False)
    for name in ('ace_irq_timer.c', 'Makefile'):
        shutil.copyfile(HERE/name, out/name)
    symvers = replay.TREE/'Module.symvers'
    original = symvers.read_bytes() if symvers.exists() else None
    try:
        # Partial build metadata reconstructed from the OEM version table;
        # export owner/class/namespace are source-derived/inferred, not a claim
        # to possess the original full Module.symvers. GPL module is retained.
        # Normal loading in the exact stock kernel is required independently.
        symvers.write_text(''.join(f'0x{crc:08x}\t{name}\tvmlinux\t{"EXPORT_SYMBOL_GPL" if name in GPL_IMPORTS else "EXPORT_SYMBOL"}\t\n'
                                   for name,crc in required.items()))
        replay.run(out,'normal-kbuild',['make','ARCH=arm64','LLVM=1','LLVM_IAS=1',
                                       'CROSS_COMPILE=aarch64-linux-gnu-',f'M={out}','V=1','modules'])
    finally:
        if original is None:
            symvers.unlink(missing_ok=True)
        else:
            symvers.write_bytes(original)
    candidate = out/'ace_irq_timer.ko'
    sections = replay.elf_sections(candidate)
    replay.require(replay.versions(sections)==required, 'Unexpected module imports/CRCs')
    replay.require(sections['.gnu.linkonce.this_module'][0][5]==1024, 'Module layout mismatch')
    replay.require(sections['.text'][0][8]==4096, 'CFI text alignment mismatch')
    for label,tool in [('elf',['llvm-readelf-18','-SWrs']),('disassembly',['llvm-objdump-18','-dr'])]:
        replay.run(out,label,tool+[str(candidate)])
    report = dict(scope='Host build only; no QEMU or phone execution implied',
                  path=str(candidate.relative_to(ROOT)),sha256=replay.sha(candidate),bytes=candidate.stat().st_size,
                  authentic_crc_source_sha256=OEM_SHA,
                  versions={name:f'0x{crc:08x}' for name,crc in required.items()},
                  source_sha256={name:replay.sha(HERE/name) for name in ['ace_irq_timer.c','Makefile','rebuild.py']},
                  symvers_restored=True,header_files_verified=headers,script_files_verified=scripts)
    (out/'build-result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
