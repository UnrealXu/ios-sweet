"""Compile real patched XNU headers/units when the pinned local tree exists."""
import os
import pathlib
import re
import shutil
import struct
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/ci-0081/buildtree/xnu'
PATCHES = [ROOT / 'xnu/patches' / name for name in (
    '0082-separate-sweet-early-framebuffer.patch',
    '0083-ace-initial-machine-target.patch')]


@unittest.skipUnless(BASE.is_dir() and shutil.which('clang') and shutil.which('patch')
                     and shutil.which('llvm-nm'), 'pinned XNU tree and cross tools required')
class AceXnuPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.tree = pathlib.Path(cls.tmp.name)
        # Copy only affected original files, then apply the actual shipping patches.
        for patch in PATCHES:
            for name in re.findall(r'^diff --git a/(\S+) b/\S+$', patch.read_text(), re.M):
                src, dst = BASE / name, cls.tree / name
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.exists() and not dst.exists():
                    shutil.copyfile(src, dst)
        for patch in PATCHES:
            result = subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(patch)],
                                    cwd=cls.tree, capture_output=True, text=True)
            if result.returncode:
                cls.tmp.cleanup()
                raise AssertionError(result.stdout + result.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def compile(self, src, *, ace=True, extra=(), output='test.o'):
        dst = self.tree / output
        command = ['clang', '-target', 'arm64-apple-macos14.0', '-c', str(src),
                   '-I', str(self.tree / 'pexpert'), '-DARM64_BOARD_CONFIG_SWEET']
        if ace:
            command.append('-DARM64_BOARD_CONFIG_ACE')
        return subprocess.run(command + list(extra) + ['-o', str(dst)],
                              capture_output=True, text=True), dst

    def test_actual_board_header_uses_observed_timer_and_stops_at_one_cpu(self):
        src = self.tree / 'board-test.c'
        src.write_text('''#include <pexpert/arm64/ACE.h>
_Static_assert(ACE == 1 && SWEET == 1, "shared architecture selector");
_Static_assert(SWEET_VTIMER_INTID == 27, "observed Ace virtual timer");
_Static_assert(SWEET_SMP_MAX_CPUS == 1, "no unverified secondary release");
_Static_assert(SWEET_HAS_EARLY_FB == 0, "no Redmi screen address");
_Static_assert(__ARM_16K_PG__ == 1 && HAS_GIC_V3 == 1, "MMU and IRQ ABI");
int ace_board_header_verified;
''')
        result, obj = self.compile(src)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(struct.unpack_from('<II', obj.read_bytes()), (0xfeedfacf, 0x100000c))

    def test_ace_rejects_enabling_the_unverified_redmi_framebuffer(self):
        src = self.tree / 'reject-fb.c'
        src.write_text('#include <pexpert/arm64/ACE.h>\n')
        result, _ = self.compile(src, extra=['-DSWEET_HAS_EARLY_FB=1'])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Ace has no verified XNU framebuffer backend', result.stderr)

    def test_qcom_mmio_and_battery_implementations_are_absent_from_actual_objects(self):
        sources = ['bsd/dev/sweet_' + name + '.c' for name in
                   ('ufs', 'spmi', 'rpmh', 'usb', 'keys', 'touch')]
        sources.append('iokit/Kernel/arm/SweetBattery.cpp')
        for index, name in enumerate(sources):
            with self.subTest(source=name):
                result, obj = self.compile(self.tree / name, output=f'driver-{index}.o')
                self.assertEqual(result.returncode, 0, result.stderr)
                symbols = subprocess.check_output(['llvm-nm', '-g', str(obj)], text=True)
                self.assertEqual(symbols.strip(), '', symbols)

    def test_registry_matches_ace_cpu_and_excludes_unported_device_services(self):
        src = self.tree / 'iokit/KernelConfigTables.cpp'
        for ace in (False, True):
            result, obj = self.compile(src, ace=ace)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = obj.read_bytes()
            self.assertEqual(b'oneplus,ace-mt6895' in data, ace)
            self.assertEqual(b'ace,armv8-cpu' in data, ace)
            for name in (b'qcom,kryo470', b'AppleCLCD', b'SweetHIDTouch',
                         b'SweetHIDButtons', b'SweetBattery', b'AppleKeyStore'):
                self.assertEqual(name in data, not ace, name)


class AceSoftwareStaging(unittest.TestCase):
    @unittest.skipUnless(BASE.is_dir() and shutil.which('make') and shutil.which('patch'),
                         'pinned XNU template and make required')
    def test_real_provider_make_block_sets_headers_and_general_register_policy_for_ace(self):
        with tempfile.TemporaryDirectory() as directory:
            tree = pathlib.Path(directory)
            source = 'libkern/conf/Makefile.template'
            (tree / source).parent.mkdir(parents=True)
            shutil.copyfile(BASE / source, tree / source)
            subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i',
                            str(ROOT / 'xnu/patches/0086-ace-bearssl-build-flags.patch')],
                           cwd=tree, check=True, capture_output=True)
            text = (tree / source).read_text()
            start = text.index('ifneq ($(filter SWEET ACE,')
            block = text[start:text.index('\nendif', start)+len('\nendif')]
            objects = re.findall(r'^(\w+\.o)_INCFLAGS\s*=', block, re.M)
            self.assertEqual(len(objects), 18)
            objects.append('corecrypto_aes.o')
            for target in ('SWEET', 'ACE', 'VMAPPLE'):
                emit = '\n'.join('$(info '+obj+'|$('+obj+'_INCFLAGS)|$('+obj+'_CFLAGS_ADD))'
                                 for obj in objects)
                makefile = 'SRCROOT:=/source\nCURRENT_MACHINE_CONFIG:='+target+'\n'+block+'\n'+emit+'\nall:;@:\n'
                result = subprocess.check_output(['make', '-s', '-f', '-'], input=makefile, text=True)
                for row in result.splitlines():
                    obj, includes, flags = row.split('|')
                    self.assertEqual(includes, '' if target == 'VMAPPLE' or obj == 'corecrypto_aes.o' else
                                     '-I/source/libkern/crypto/sweet_bearssl/inc -I/source/libkern/crypto/sweet_bearssl/src')
                    self.assertEqual(flags, '' if target == 'VMAPPLE' else '-mgeneral-regs-only', obj)

    def test_ace_enters_shared_provider_staging_without_downloading(self):
        # Missing source / deliberately wrong SDK version must fail BEFORE any
        # network operation; unrelated boards still skip these integrations.
        with tempfile.TemporaryDirectory() as directory:
            for name in ('0019-stage-libpthread.sh', '0020-stage-bearssl.sh',
                         '0026-stage-hfs.sh'):
                for target in ('ACE', 'SWEET', 'VMAPPLE'):
                    with self.subTest(script=name, target=target):
                        env = dict(os.environ, MACHINE_CONFIG=target, MACOS_VERSION='0')
                        result = subprocess.run(['bash', str(ROOT / 'xnu/patches' / name)],
                                                cwd=directory, env=env,
                                                capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0 if target == 'VMAPPLE' else 1,
                                         result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
