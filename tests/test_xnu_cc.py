import importlib.util
import os
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
from unittest import mock


class CompilerSelectionTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('clang') and shutil.which('clang++'), 'clang required')
    def test_explicit_compiler_emits_real_arm64_macho_for_c_and_cpp(self):
        path = Path(__file__).resolve().parents[1] / 'tools/xnu-cc.py'
        with mock.patch.dict(os.environ, {'XNU_CLANG': 'clang'}):
            spec = importlib.util.spec_from_file_location('xnu_cc_smoke', path)
            tool = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tool)
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            (base / 'xnu/osfmk').mkdir(parents=True)
            objects = base / 'objects'; objects.mkdir()
            for ext, kind in [('c', 'clang'), ('cpp', 'clang++')]:
                source = base / f'xnu/osfmk/compile-smoke.{ext}'
                source.write_text('int add(int a, int b) { return a + b; }\n')
                ci_source = tool.CI_DXB + f'/xnu/osfmk/compile-smoke.{ext}'
                with mock.patch.dict(os.environ, {'XNU_CC_OBJDIR': str(objects)}):
                    _, rc, error = tool.run((ci_source, (kind, ['-c', ci_source])), str(base), {'osfmk': str(base)})
                self.assertEqual(rc, 0, error)
                blob = (objects / f'osfmk__compile-smoke.{ext}.o').read_bytes()
                self.assertEqual(struct.unpack_from('<II', blob), (0xfeedfacf, 0x100000c))


if __name__ == '__main__':
    unittest.main()
