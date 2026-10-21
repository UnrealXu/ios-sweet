"""Focused host boundary checks; actual interrupt delivery uses QEMU verifier."""
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IrqProbeHostTests(unittest.TestCase):
    def test_optimized_verifier_refuses_without_changing_evidence(self):
        report = ROOT / 'research/ace-irq-probe-20261019/verification.json'
        before = report.read_bytes() if report.exists() else None
        for arguments, setting in [(['-O'], None), ([], '1')]:
            environment = os.environ.copy()
            if setting:
                environment['PYTHONOPTIMIZE'] = setting
            result = subprocess.run(['python3', *arguments,
                                     str(ROOT / 'ace/irq-probe/verify.py')],
                                    capture_output=True, text=True, env=environment,
                                    timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Optimized verification is refused', result.stderr)
            self.assertEqual(report.read_bytes() if report.exists() else None, before)

    def test_unknown_variant_refuses_without_changing_evidence(self):
        report = ROOT / 'research/ace-irq-probe-20261019/verification.json'
        before = report.read_bytes() if report.exists() else None
        result = subprocess.run([str(ROOT / 'ace/irq-probe/build.sh'), 'unknown'],
                                capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report.read_bytes() if report.exists() else None, before)


if __name__ == '__main__':
    unittest.main()
