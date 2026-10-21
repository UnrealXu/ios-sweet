"""Execute the stackless entry marker, including rejection and wrap cases."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class EarlyEntryTests(unittest.TestCase):
    def test_patch_applies_with_ci_git_apply_not_only_posix_patch(self):
        cached=ROOT/'research/ace-ci-first-20261020/tree/xnu'
        if not cached.exists():self.skipTest('private CI source fixture unavailable')
        with tempfile.TemporaryDirectory(dir=ROOT/'research') as directory:
            d=Path(directory)
            subprocess.run(['git','init','-q',str(d)],check=True)
            for name in ('start.s','genassym.c'):
                target=d/'osfmk/arm64'/name;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((cached/'osfmk/arm64'/name).read_bytes())
            subprocess.run(['git','apply',str(ROOT/'xnu/patches/0087-ace-earliest-entry-marker.patch')],cwd=d,check=True,capture_output=True)
            self.assertIn('ACEXNU1:',(d/'osfmk/arm64/ace_early_entry.h').read_text())

    def test_qemu_actual_marker_instructions(self):
        if any(not shutil.which(x) for x in ('qemu-system-aarch64','gdb-multiarch','aarch64-linux-gnu-gcc')):
            self.skipTest('AArch64 QEMU/GDB/toolchain unavailable')
        spec=importlib.util.spec_from_file_location('early_verify',ROOT/'diagnostics/ace-early-entry/verify.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        (ROOT/'research').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT/'research') as d:
            report=module.verify(Path(d)/'matrix')
        self.assertEqual(report['cases'],19)
        self.assertFalse(report['phone_xnu_boot'])

if __name__=='__main__':unittest.main()
