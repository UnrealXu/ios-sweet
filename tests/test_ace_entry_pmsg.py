"""Invalid experimental entry builds must fail before producing artifacts."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EntryPmsgInputTests(unittest.TestCase):
    def test_optimized_verifiers_refuse_before_creating_evidence(self):
        import os
        for script in ('verify.py', 'verify_pmsg.py'):
            for flag in ('argument', 'environment'):
                with self.subTest(script=script, optimization=flag):
                    with tempfile.TemporaryDirectory(dir=ROOT / 'research') as directory:
                        output = Path(directory) / 'must-not-exist'
                        # runpy redirects both fixed and configurable OUT before main.
                        loader = ("import runpy; from pathlib import Path; "
                                  f"n=runpy.run_path({str(ROOT / 'ace/entry' / script)!r}); "
                                  f"n['main'].__globals__['OUT']=Path({str(output)!r}); "
                                  "n['main']()")
                        command = ['python3'] + (['-O'] if flag == 'argument' else [])
                        environment = os.environ.copy()
                        if flag == 'environment':
                            environment['PYTHONOPTIMIZE'] = '1'
                        result = subprocess.run(command + ['-c', loader], cwd=ROOT,
                                                env=environment, capture_output=True,
                                                text=True, timeout=10)
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn('optimized execution is refused', result.stderr)
                        self.assertFalse(output.exists())
                        self.assertEqual(list(Path(directory).iterdir()), [])

    def test_invalid_explicit_ring_never_creates_output(self):
        cases = [('0', '128'), ('0x43000001', '128'), ('0x43000000', '12'),
                 ('0x43000000', str(0x8000000c)),
                 ('0xfffffffffffffffc', '128'), ('garbage', '128')]
        with tempfile.TemporaryDirectory(dir=ROOT / 'research') as directory:
            for index, (address, size) in enumerate(cases):
                with self.subTest(address=address, size=size):
                    output = Path(directory) / str(index)
                    result = subprocess.run([str(ROOT / 'ace/entry/build.sh'),
                                             '--output-dir', str(output),
                                             '--pmsg-ram', address, size],
                                            cwd=ROOT, capture_output=True, timeout=10)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(output.exists())

    def test_verifier_rejects_uncontrolled_fixture(self):
        cases = [('--ring-address', '0x40080000'),
                 ('--ring-address', '0x43000001'),
                 ('--ring-address', '0x44000000'),
                 ('--ring-bytes', '43'), ('--qemu-mib', '4096')]
        with tempfile.TemporaryDirectory(dir=ROOT / 'research') as directory:
            for index, arguments in enumerate(cases):
                with self.subTest(arguments=arguments):
                    output = Path(directory) / str(index)
                    result = subprocess.run(['python3', str(ROOT / 'ace/entry/verify_pmsg.py'),
                                             '--output-dir', str(output), *arguments],
                                            cwd=ROOT, capture_output=True, timeout=10)
                    self.assertEqual(result.returncode, 2)
                    self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
