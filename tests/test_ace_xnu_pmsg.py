"""Exercise the shipping XNU pmsg source, with explicit host-only adapters."""
import ctypes as c
import os
import pathlib
import random
import re
import shutil
import shlex
import struct
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/ci-0081/buildtree/xnu'
PATCHES = [ROOT / 'xnu/patches' / name for name in (
    '0082-separate-sweet-early-framebuffer.patch',
    '0083-ace-initial-machine-target.patch',
    '0084-ace-pmsg-serial-console.patch')]
SIZE, CAP, MAGIC = 65536, 65524, 0x43474244


class Console(c.Structure):
    _fields_ = [('zone', c.c_void_p), ('bytes', c.c_size_t), ('busy', c.c_uint32)]


class Input(c.Structure):
    _fields_ = [(n, c.c_uint64) for n in (
        'ram_base', 'ram_bytes', 'pmsg_base', 'pmsg_bytes', 'sctlr', 'current_el')]
    _fields_ += [(n, c.c_uint32) for n in (
        'revision', 'version', 'bootarg_present', 'enabled', 'lookup_ok', 'compat_ok',
        'reg_length', 'ecc_size', 'type_signature', 'ecc_length', 'type_length', 'map_ok')]


class Stats(c.Structure):
    _fields_ = [('maps', c.c_uint32), ('registrations', c.c_uint32),
                ('completions', c.c_uint32), ('map_base', c.c_uint64), ('map_bytes', c.c_uint64)]


@unittest.skipUnless(BASE.is_dir() and shutil.which('clang') and shutil.which('patch'),
                     'pinned XNU tree and compiler required')
class AceXnuPmsg(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.tree = pathlib.Path(cls.tmp.name)
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
        text = (cls.tree / 'pexpert/arm/pe_serial.c').read_text()
        start = text.index('#if defined(ARM64_BOARD_CONFIG_ACE)\n/* Explicit opt-in')
        end = text.index('#endif /* ARM64_BOARD_CONFIG_ACE */', start)
        frontend = text[start:end] + '#endif\n'
        boot = (BASE / 'pexpert/pexpert/arm64/boot.h').read_text()
        video = re.search(r'struct Boot_Video \{.*?\n\};', boot, re.S).group()
        args = re.search(r'typedef struct boot_args \{.*?\n\} boot_args;', boot, re.S).group()
        declarations = ('#define BOOT_LINE_LENGTH 608\n' + video +
                        '\ntypedef struct Boot_Video Boot_Video;\n' + args +
                        '\n_Static_assert(sizeof(boot_args) == 736, "XNU BootArgs ABI");\n')
        fixture = (ROOT / 'tests/fixtures/ace_pmsg_frontend.c').read_text()
        fixture = fixture.replace('/* INSERT_ACE_BOOT_ARGS */', declarations)
        fixture = fixture.replace('/* INSERT_ACE_FRONTEND */', frontend)
        host = cls.tree / 'frontend.c'; host.write_text(fixture)
        cls.core = cls.tree / 'pexpert/arm/pe_ace_pmsg.c'
        cls.flags = ['clang', '-std=c11', '-O2', '-DARM64_BOARD_CONFIG_ACE',
                     '-I', str(cls.tree / 'pexpert')]
        libpath = cls.tree / 'console.so'
        result = subprocess.run(cls.flags + ['-shared', '-fPIC', str(cls.core), str(host),
                                             '-o', str(libpath)], capture_output=True, text=True)
        if result.returncode:
            cls.tmp.cleanup()
            raise AssertionError(result.stderr)
        cls.lib = c.CDLL(str(libpath))
        cls.lib.ace_pmsg_console_bind.argtypes = [c.POINTER(Console), c.c_void_p, c.c_size_t]
        cls.lib.ace_pmsg_console_bind.restype = c.c_int
        cls.lib.ace_pmsg_console_putc.argtypes = [c.POINTER(Console), c.c_uint8]
        cls.lib.ace_pmsg_console_putc.restype = c.c_int
        cls.lib.test_probe.argtypes = [c.POINTER(Input), c.c_void_p, c.POINTER(Stats)]
        cls.lib.test_send.argtypes = [c.c_uint8]
        cls.lib.test_ready.restype = c.c_uint
        cls.lib.test_busy.argtypes = [c.c_uint]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def zone(self, text=b''):
        zone = (c.c_ubyte * SIZE)()
        struct.pack_into('<III', zone, 0, MAGIC, len(text), len(text))
        zone[12:12 + len(text)] = text
        return zone

    def read(self, zone):
        _, start, size = struct.unpack_from('<III', zone)
        data = bytes(zone)[12:]
        return data[:size] if size < CAP else data[start:] + data[:start]

    def config(self):
        # Synthetic host policy only: this is not an authorized phone RAM window.
        return Input(0x140000000, 0x40000000, 0x48160000, SIZE, 5, 4,
                     2, 2, 1, 1, 1, 1, 16, 0, 0, 4, 4, 1)

    def probe(self, config, zone):
        stats = Stats()
        self.lib.test_probe(c.byref(config), zone, c.byref(stats))
        return stats

    def test_bind_preserves_existing_record_and_append_wraps_exactly(self):
        previous = b'previous Android boot\n'
        zone = self.zone(previous); console = Console(); before = bytes(zone)
        self.assertEqual(self.lib.ace_pmsg_console_bind(c.byref(console), zone, SIZE), 0)
        self.assertEqual(bytes(zone), before)
        text = bytes(range(256)) * 260
        for byte in text:
            self.assertEqual(self.lib.ace_pmsg_console_putc(c.byref(console), byte), 0)
        self.assertEqual(self.read(zone), (previous + text)[-CAP:])
        self.assertEqual(console.busy, 0)

    def test_malformed_bind_and_numeric_or_alias_arguments_do_not_write(self):
        for header in [(0, 0, 0), (MAGIC, CAP, CAP), (MAGIC, 0, CAP + 1),
                       (MAGIC, 3, 4), (MAGIC, 5, 4)]:
            with self.subTest(header=header):
                zone = self.zone(); struct.pack_into('<III', zone, 0, *header)
                console = Console(); before = bytes(zone)
                self.assertLess(self.lib.ace_pmsg_console_bind(c.byref(console), zone, SIZE), 0)
                self.assertEqual(bytes(zone), before)
                self.assertEqual(bytes(console), bytes(Console()))
        zone = self.zone(); console = Console(); before = bytes(zone)
        for pointer, size in [(zone, SIZE - 1), (zone, SIZE + 1),
                              (c.c_void_p(c.addressof(zone) + 1), SIZE),
                              (c.c_void_p((1 << 64) - 4), SIZE), (None, SIZE)]:
            self.assertEqual(self.lib.ace_pmsg_console_bind(c.byref(console), pointer, size), -1)
        aliased = c.cast(zone, c.POINTER(Console))
        self.assertEqual(self.lib.ace_pmsg_console_bind(aliased, zone, SIZE), -6)
        self.assertEqual(bytes(zone), before)

    def test_corrupt_after_bind_and_busy_writer_fail_without_data_changes(self):
        zone = self.zone(b'old'); console = Console()
        self.assertEqual(self.lib.ace_pmsg_console_bind(c.byref(console), zone, SIZE), 0)
        console.busy = 1; before = bytes(zone)
        self.assertEqual(self.lib.ace_pmsg_console_putc(c.byref(console), 65), -4)
        self.assertEqual(bytes(zone), before)
        console.busy = 0
        struct.pack_into('<I', zone, 0, 0); before = bytes(zone)
        self.assertEqual(self.lib.ace_pmsg_console_putc(c.byref(console), 65), -2)
        self.assertEqual(bytes(zone), before)
        self.assertEqual(console.busy, 0)
        self.assertEqual(self.lib.ace_pmsg_console_putc(c.byref(Console()), 65), -5)
        self.assertEqual(self.lib.ace_pmsg_console_putc(None, 65), -1)

    def test_bounded_header_mutations_use_independent_ring_model(self):
        rng = random.Random(6895)
        for _ in range(400):
            zone = self.zone()
            start, size = rng.randrange(CAP + 10), rng.randrange(CAP + 10)
            if rng.randrange(3) == 0:
                size = CAP; start = rng.randrange(CAP)
            elif rng.randrange(3) == 0:
                size = start = rng.randrange(CAP)
            struct.pack_into('<III', zone, 0, MAGIC, start, size)
            console = Console(); before = bytes(zone)
            rc = self.lib.ace_pmsg_console_bind(c.byref(console), zone, SIZE)
            valid = start < CAP and size <= CAP and (size == CAP or start == size)
            self.assertEqual(rc == 0, valid)
            self.assertEqual(bytes(zone), before)
            if valid:
                old = self.read(zone)
                self.assertEqual(self.lib.ace_pmsg_console_putc(c.byref(console), 0xa5), 0)
                self.assertEqual(self.read(zone), (old + b'\xa5')[-CAP:])

    def test_actual_core_with_asan_ubsan_and_guard_pages(self):
        exe = self.tree / 'sanitize'
        result = subprocess.run(self.flags + ['-O1', '-fsanitize=address,undefined',
                                '-fno-omit-frame-pointer', str(self.core),
                                str(ROOT / 'tests/fixtures/ace_pmsg_sanitize.c'), '-o', str(exe)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([str(exe)], capture_output=True, text=True, timeout=20,
                                env=dict(os.environ, ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',
                                         UBSAN_OPTIONS='halt_on_error=1'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(shutil.which('llvm-objdump') and shutil.which('llvm-nm'),
                         'LLVM object tools required')
    def test_actual_machine_flags_pin_a55_and_emit_no_stlur_or_runtime_atomics(self):
        make = (self.tree / 'makedefs/MakeInc.def').read_text()
        flags = shlex.split(re.search(r'^MACHINE_FLAGS_ARM64_ACE = (.*)$', make, re.M).group(1))
        command = ['clang', '-target', 'arm64-apple-macos14.0', *flags,
                   '-ffreestanding', '-mkernel', '-fno-stack-protector', '-O2',
                   '-I', str(self.tree / 'pexpert'), '-c', str(self.core)]
        options = subprocess.run(command + ['-###'], capture_output=True, text=True)
        self.assertEqual(options.returncode, 0, options.stderr)
        self.assertIn('"-target-cpu" "cortex-a55"', options.stderr)
        obj = self.tree / 'arm64-core.o'
        result = subprocess.run(command + ['-o', str(obj)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(struct.unpack_from('<II', obj.read_bytes()), (0xfeedfacf, 0x100000c))
        disasm = subprocess.check_output(['llvm-objdump', '-d', '--mattr=+lse,+rcpc-immo',
                                         str(obj)], text=True)
        self.assertNotIn('stlur', disasm)
        self.assertIn('stlr', disasm)
        self.assertEqual(subprocess.check_output(['llvm-nm', '-u', str(obj)], text=True).strip(), '')

    def test_frontend_wrong_policy_never_maps_or_writes(self):
        bad = [('ram_bytes', 0), ('ram_base', (1 << 64) - 16),
               ('ram_base', 0x48160000), ('revision', 1), ('version', 1),
               ('bootarg_present', 0), ('enabled', 0), ('enabled', 2),
               ('lookup_ok', 0), ('compat_ok', 0), ('current_el', 8),
               ('sctlr', 1 << 25), ('pmsg_base', 0x48164000),
               ('pmsg_bytes', SIZE + 16384), ('reg_length', 8),
               ('ecc_size', 4), ('type_signature', 1), ('ecc_length', 8), ('type_length', 0)]
        for key, value in bad:
            with self.subTest(field=key, value=value):
                config = self.config(); setattr(config, key, value)
                zone = self.zone(b'preserved'); before = bytes(zone)
                stats = self.probe(config, zone)
                self.assertEqual(stats.maps, 0)
                self.assertEqual(stats.registrations, 0)
                self.assertEqual(stats.completions, 0)
                self.assertEqual(bytes(zone), before)

    def test_frontend_map_or_header_failure_keeps_record_unmodified(self):
        for mode in ('map', 'header', 'state'):
            with self.subTest(mode=mode):
                config = self.config(); zone = self.zone(b'preserved')
                if mode == 'map': config.map_ok = 0
                if mode == 'header': struct.pack_into('<I', zone, 0, 0)
                if mode == 'state': struct.pack_into('<I', zone, 4, 1)
                before = bytes(zone); stats = self.probe(config, zone)
                self.assertEqual(stats.maps, 1)
                self.assertEqual(stats.registrations, 0)
                self.assertEqual(stats.completions, 0)
                self.assertEqual(bytes(zone), before)

    def test_frontend_valid_mapping_publishes_marker_and_drops_recursion(self):
        zone = self.zone(b'preserved\n'); stats = self.probe(self.config(), zone)
        marker = b'ACEXNU pmsg serial ready\n'
        self.assertEqual((stats.maps, stats.registrations), (1, 1))
        self.assertEqual((stats.map_base, stats.map_bytes), (0x48160000, SIZE))
        self.assertEqual(stats.completions, len(marker))
        self.assertEqual(self.read(zone), b'preserved\n' + marker)
        self.assertEqual(self.lib.test_ready(), 1)
        self.lib.test_send(65)
        before = bytes(zone)
        self.lib.test_busy(1)
        self.assertEqual(self.lib.test_ready(), 1)
        self.lib.test_send(66)
        self.assertEqual(bytes(zone), before)
        self.lib.test_busy(0)
        self.lib.test_send(67)
        self.assertTrue(self.read(zone).endswith(b'AC'))


class AndroidProbeAbi(unittest.TestCase):
    @unittest.skipUnless(shutil.which('aarch64-linux-gnu-gcc'), 'cross GCC required')
    def test_raw_signal_layout_against_actual_cached_android_uapi(self):
        kernel = ROOT / 'research/ace-kbuild-path-20261019/android12-5.10'
        if not (kernel / 'arch/arm64/include/uapi/asm/signal.h').exists():
            self.skipTest('actual Android kernel headers absent')
        include = ['arch/arm64/include/uapi', 'arch/arm64/include/generated/uapi',
                   'include/uapi', 'include']
        with tempfile.TemporaryDirectory() as directory:
            obj = pathlib.Path(directory) / 'signal-abi.o'
            cmd = ['aarch64-linux-gnu-gcc', '-ffreestanding', '-D__EXPORTED_HEADERS__',
                   '-D__user=', '-D__LINUX_COMPILER_H']
            for name in include:
                cmd += ['-I', str(kernel / name)]
            result = subprocess.run(cmd + ['-c', str(ROOT / 'diagnostics/ace-isa-probe/abi.c'),
                                          '-o', str(obj)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = obj.read_bytes()
            self.assertEqual(data[:6], b'\x7fELF\x02\x01')
            self.assertEqual(struct.unpack_from('<H', data, 18)[0], 183)


if __name__ == '__main__':
    unittest.main()
