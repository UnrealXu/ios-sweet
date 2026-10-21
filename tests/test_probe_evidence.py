import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


class ProbeEvidenceTests(unittest.TestCase):
    def test_failed_verification_invalidates_old_success(self):
        path = Path(__file__).resolve().parents[1] / 'probe/verify.py'
        spec = importlib.util.spec_from_file_location('probe_verify_test', path)
        tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tool)
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            (output / 'verification.json').write_text('{"status":"pass"}')
            with mock.patch.object(tool, 'OUT', output), \
                 mock.patch.object(sys, 'argv', ['verify.py']), \
                 mock.patch.object(tool.shutil, 'which', return_value='/host/tool'), \
                 mock.patch.object(tool.subprocess, 'run', side_effect=RuntimeError('build failed')):
                with self.assertRaises(RuntimeError):
                    tool.main()
            self.assertNotEqual(json.loads((output / 'verification.json').read_text())['status'], 'pass')
            self.assertEqual(json.loads((output / 'verification.previous.json').read_text())['status'], 'pass')


if __name__ == '__main__':
    unittest.main()
