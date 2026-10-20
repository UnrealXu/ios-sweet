"""Cache invalidation and fresh-source guards for the CI acceleration path."""
from pathlib import Path
import importlib.util
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cache', ROOT / 'tools/ci-build-cache.py')
cache = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cache)


class SourceCacheTests(unittest.TestCase):
    def git(self, directory, *args):
        return subprocess.run(['git', '-C', str(directory), *args],
                              capture_output=True, check=True)

    def fixture(self, directory):
        dxb = directory / 'dxb'
        dxb.mkdir()
        self.git(dxb, 'init', '-q')
        xnu = dxb / 'xnu'
        xnu.mkdir()
        self.git(xnu, 'init', '-q')
        (xnu / 'header.h').write_text('original header\n')
        self.git(xnu, 'add', 'header.h')
        self.git(xnu, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-qm', 'pristine dependency')
        return dxb, xnu

    def test_restored_patches_and_staged_providers_are_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            dxb, xnu = self.fixture(Path(tmp))
            (xnu / 'header.h').write_text('old cached patch\n')
            (xnu / 'old-provider').mkdir()
            (xnu / 'old-provider/source.c').write_text('old source\n')
            cache.reset_sources(dxb)
            self.assertEqual((xnu / 'header.h').read_text(), 'original header\n')
            self.assertFalse((xnu / 'old-provider').exists())

    def test_generated_headers_objects_and_kernel_outputs_cannot_be_restored(self):
        for name in ['build', 'fakeroot']:
            with tempfile.TemporaryDirectory() as tmp:
                dxb, _ = self.fixture(Path(tmp))
                (dxb / name).mkdir()
                with self.assertRaisesRegex(ValueError, 'object/fakeroot'):
                    cache.reset_sources(dxb)

    def test_source_symlink_and_wrong_root_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            with self.assertRaises(ValueError):
                cache.reset_sources(directory)
            dxb, _ = self.fixture(directory)
            (dxb / 'dtrace').symlink_to(directory, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'invalid cached source'):
                cache.reset_sources(dxb)

    def test_workflow_keeps_output_out_of_caches_and_uploads_kernel_first(self):
        import yaml
        workflow = yaml.safe_load((ROOT / '.github/workflows/xnu.yml').read_text())
        steps = workflow['jobs']['build']['steps']
        for step in steps:
            if step.get('uses', '').startswith('actions/cache@'):
                for path in step['with']['path'].splitlines():
                    self.assertNotIn('fakeroot', path)
                    self.assertNotIn('dxb/build', path)
                self.assertIn('toolchain', step['with']['key'])
        names = [step.get('name') for step in steps]
        self.assertLess(names.index('Upload verified kernel immediately'),
                        names.index('Package build tree for local compiles'))
        self.assertIn('CCACHE_DISABLE=1', (ROOT / 'tools/ci-build-cache.py').read_text())

    def test_cached_mode_preserves_paths_and_uses_strict_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            env = workspace / 'github-env'
            with patch.dict(cache.os.environ, {'DXB_SHA': 'recipe', 'GITHUB_ENV': str(env)}), \
                 patch.object(cache, 'command', return_value='recipe'), \
                 patch.object(cache, 'reset_sources'), \
                 patch.object(cache.shutil, 'which', return_value='/opt/homebrew/bin/ccache'), \
                 patch.object(cache.subprocess, 'run') as run:
                cache.prepare(workspace, 'cached')
            self.assertIn('CCACHE_BASEDIR=\n', env.read_text())
            self.assertIn('CCACHE_COMPILERCHECK=content\n', env.read_text())
            self.assertEqual((workspace / '.ci-cache/ccache.conf').read_text(),
                             'compiler_check = content\nsloppiness =\nmax_size = 1G\n')
            self.assertEqual([call.args[0] for call in run.call_args_list],
                             [['ccache', '--max-size', '1G'], ['ccache', '--zero-stats']])

    def test_full_mode_disables_compiler_cache_and_does_not_restore_kdk(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            env = workspace / 'github-env'
            with patch.dict(cache.os.environ, {'DXB_SHA': 'recipe', 'GITHUB_ENV': str(env)}), \
                 patch.object(cache, 'command', return_value='recipe'), \
                 patch.object(cache, 'reset_sources'), \
                 patch.object(cache.subprocess, 'run') as run:
                cache.prepare(workspace, 'full')
            self.assertEqual(env.read_text(), 'CCACHE=\nCCACHE_DISABLE=1\n')
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
