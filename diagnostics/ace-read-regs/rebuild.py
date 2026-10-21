#!/usr/bin/env python3
"""Host-only normal Kbuild replay from hash-bound private inputs. No downloads."""
import argparse
import hashlib
import json
import pathlib
import shutil
import struct
import subprocess
import tarfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIVATE = ROOT / 'research/ace-kbuild-path-20261019'
CAPTURE = ROOT / 'research/ace-live-20261019-wireless'
TREE = PRIVATE / 'android12-5.10'
EXPECTED = {
    CAPTURE / 'kheaders.tar.xz': 'e65e44a2ff42b6d3a1bbb9c34b768ee00be27fb88a65f31c5baed3b008b9bd05',
    CAPTURE / 'arm_dsu_pmu.ko': 'e4f929eaeaa6db5451d310fdee8e96d0791cb2331e9d971e4f5af7be54564a7b',
    ROOT / 'research/ace-offline/stock-kernel.config': '7d939635d77acbaa49a3e4ab2bdbb154c0a2c5e393b8057fa11a49071b56f149',
    PRIVATE / 'scripts.tar.gz': '299f91d26699f91290e70e257e6a5b1b62486482ee0f3b23b1c907b587bb1276',
    # Official root Makefile plus only the obsolete zero-init acknowledgement
    # flag removal. Actual -ftrivial-auto-var-init=zero remains enabled.
    TREE / 'Makefile': '84f83b1f302fcbf784d51eed0d5486ca37df91683d9e027f7e3450f886763dc1',
    TREE / 'arch/arm64/Makefile': '605a51c53ec8b065d69b4aeb37e91b372012778e517523e0cf2a4beffdf94fff',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_archive(archive, destination):
    """Compare regular source/header members; never follow/extract tar links."""
    count = 0
    with tarfile.open(archive) as tar:
        for member in tar:
            parts = pathlib.PurePosixPath(member.name)
            require(not parts.is_absolute() and '..' not in parts.parts,
                    f'Unsafe archive member: {member.name}')
            if member.isfile():
                target = destination / parts
                require(target.is_file() and target.read_bytes() == tar.extractfile(member).read(),
                        f'Source/header mismatch: {target}')
                count += 1
    return count


def elf_sections(path):
    """Small read-only ELF64-LE parser; no vendor binary editing or copying."""
    data = path.read_bytes()
    require(data[:6] == b'\x7fELF\x02\x01', 'Expected little-endian ELF64')
    require(struct.unpack_from('<H', data, 18)[0] == 183, 'Expected AArch64 ELF')
    offset = struct.unpack_from('<Q', data, 40)[0]
    stride, count, names_index = struct.unpack_from('<HHH', data, 58)
    require(stride == 64, 'Unsupported section header format')
    entries = [struct.unpack_from('<IIQQQQIIQQ', data, offset + i * stride)
               for i in range(count)]
    names_entry = entries[names_index]
    names = data[names_entry[4]:names_entry[4] + names_entry[5]]
    result = {}
    for entry in entries:
        name = names[entry[0]:].split(b'\0', 1)[0].decode()
        result[name] = (entry, data[entry[4]:entry[4] + entry[5]])
    return result


def versions(sections):
    data = sections['__versions'][1]
    require(len(data) % 64 == 0, 'Unexpected modversion record size')
    result = {}
    for i in range(0, len(data), 64):
        value = struct.unpack_from('<Q', data, i)[0]
        name = data[i + 8:i + 64].split(b'\0', 1)[0].decode()
        require(value <= 0xffffffff and name not in result, 'Invalid CRC record')
        result[name] = value
    return result


def run(output, label, command):
    (output / (label + '-command.json')).write_text(json.dumps(command, indent=2) + '\n')
    result = subprocess.run(command, cwd=TREE, capture_output=True, text=True)
    (output / (label + '.log')).write_text(result.stdout + result.stderr)
    require(result.returncode == 0, f'{label} exit {result.returncode}; see {output}/{label}.log')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true', help='Verify private inputs without building')
    args = parser.parse_args()
    for path, expected in EXPECTED.items():
        require(path.is_file() and sha(path) == expected, f'Missing/changed input: {path}')
    headers = verify_archive(CAPTURE / 'kheaders.tar.xz', TREE)
    scripts = verify_archive(PRIVATE / 'scripts.tar.gz', TREE / 'scripts')
    print(f'Input checks pass: {headers} exact headers, {scripts} official script source files')
    if args.check_only:
        return

    # Existing prepared tree is required. This does not run Kconfig or rewrite
    # captured generated headers. No vmlinux/driver/kernel build is requested.
    output = PRIVATE / 'module-rebuilt'
    output.mkdir(exist_ok=True)
    for name in ('ace_read_regs.c', 'Makefile'):
        shutil.copyfile(HERE / name, output / name)
    stock = versions(elf_sections(CAPTURE / 'arm_dsu_pmu.ko'))
    needed = ('module_layout', 'printk')
    require(all(name in stock for name in needed), 'Missing authentic OEM import CRC')
    # CRCs are recovered facts. Owner/class/namespace initially infer official
    # same-family EXPORT_SYMBOL declarations; exact-stock QEMU and device load
    # validated this narrow pair. This is not an original full Module.symvers.
    (TREE / 'Module.symvers').write_text(''.join(
        f'0x{stock[name]:08x}\t{name}\tvmlinux\tEXPORT_SYMBOL\t\n' for name in needed))

    run(output, 'fixdep', ['make', '-f', 'scripts/Makefile.build', 'obj=scripts/basic',
                         'srctree=.', 'HOSTCC=gcc', 'HOSTCFLAGS=-O2', 'V=1'])
    includes = ['-I./arch/arm64/include', '-I./arch/arm64/include/generated',
                '-I./include', '-I./arch/arm64/include/uapi',
                '-I./arch/arm64/include/generated/uapi', '-I./include/uapi',
                '-I./include/generated/uapi']
    resource = subprocess.check_output(['clang', '-print-resource-dir'], text=True).strip()
    cpp = ['--target=aarch64-linux-gnu', '-march=armv8-a', '-mgeneral-regs-only',
           '-nostdinc', '-isystem', resource + '/include', '-D__KERNEL__',
           '-include', './include/linux/kconfig.h'] + includes
    common = ['make', '-f', 'scripts/Makefile.build', 'srctree=.', 'ARCH=arm64',
              'SRCARCH=arm64', 'HOSTCC=gcc', 'HOSTCFLAGS=-O2', 'CC=clang',
              'NM=llvm-nm-18', 'V=1', 'KBUILD_CPPFLAGS=' + ' '.join(cpp),
              'KBUILD_CFLAGS=-O2 -fno-pic']
    run(output, 'host-modpost', common + ['obj=scripts/mod'])
    run(output, 'module-linker-script', common + ['obj=scripts', 'CPP=clang -E', 'scripts/module.lds'])
    run(output, 'normal-kbuild', ['make', 'ARCH=arm64', 'LLVM=1', 'LLVM_IAS=1',
                                 'CROSS_COMPILE=aarch64-linux-gnu-', f'M={output}', 'V=1', 'modules'])
    candidate = output / 'ace_read_regs.ko'
    sections = elf_sections(candidate)
    actual_versions = versions(sections)
    require(actual_versions == {name: stock[name] for name in needed}, 'Unexpected/missing versions')
    require(sections['.gnu.linkonce.this_module'][0][5] == 1024, 'Unexpected struct module size')
    require(sections['.text'][0][8] == 4096, 'CFI .text alignment mismatch')
    for label, tool in [('elf', ['llvm-readelf-18', '-SWrs']),
                        ('disassembly', ['llvm-objdump-18', '-dr'])]:
        run(output, label, tool + [str(candidate)])
    report = {'scope': 'New host candidate; independently revalidate before execution',
              'path': str(candidate), 'sha256': sha(candidate), 'bytes': candidate.stat().st_size,
              'versions': {name: f'0x{value:08x}' for name, value in actual_versions.items()},
              'validated_original_preserved': str(PRIVATE / 'module/ace_read_regs.ko')}
    (output / 'rebuild-result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
