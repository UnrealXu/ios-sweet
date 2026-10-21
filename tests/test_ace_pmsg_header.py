"""Regression checks for accepting a real, possibly colorized kernel observation."""
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('pmsg_live',Path(__file__).resolve().parents[1]/'diagnostics/ace-pmsg-header/live.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
HEADER='sig=43474244 start=288 size=288 capacity=65524 stable=1 valid=1 attempts=1'


class PmsgHeaderObservationTests(unittest.TestCase):
    def test_colored_android_tag_and_plain_output_agree(self):
        colored='\x1b[32m[ 812.111344] \x1b[33mACE_PMSG_HEADER\x1b[0m: '+HEADER+'\n'
        plain='[ 812.111344] ACE_PMSG_HEADER: '+HEADER+'\n'
        self.assertEqual(module.header_observation('',colored),module.header_observation('',plain))
        self.assertEqual(module.header_observation('',colored)['capacity'],65524)

    def test_missing_duplicate_and_old_only_observations_are_not_accepted(self):
        line='ACE_PMSG_HEADER: '+HEADER+'\n'
        for before,after in [('', ''),('',line+line),(line,line)]:
            with self.assertRaises(AssertionError):module.header_observation(before,after)
        self.assertEqual(module.header_observation(line,line+line)['size'],288)

    def test_invalid_signature_bounds_stability_and_attempts_are_refused(self):
        for old,new in [('43474244','00000000'),('start=288','start=289'),
                        ('size=288','size=65525'),('capacity=65524','capacity=65536'),
                        ('stable=1','stable=0'),('valid=1','valid=0'),
                        ('attempts=1','attempts=0'),('attempts=1','attempts=9')]:
            with self.subTest(new=new),self.assertRaises(AssertionError):
                module.header_observation('','ACE_PMSG_HEADER: '+HEADER.replace(old,new)+'\n')

    def test_new_kernel_failure_rejects_otherwise_valid_header(self):
        for diagnostic in ['Kernel panic','BUG:','CFI failure']:
            with self.subTest(diagnostic=diagnostic),self.assertRaises(AssertionError):
                module.header_observation('','ACE_PMSG_HEADER: '+HEADER+'\n'+diagnostic+'\n')


if __name__=='__main__':unittest.main()
