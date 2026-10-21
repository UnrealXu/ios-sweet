"""Boundary tests for actual log interpretation; never access ADB."""
import importlib.util
import os
from pathlib import Path
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('irq_live',ROOT/'diagnostics/ace-irq-timer/live.py')
live=importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)


def fixture():
    # A13MHz counter can give equal adjacent reads on a fast CPU.
    return '\n'.join(f'ACE_IRQ_TIMER\x1b[0m: el=1 mpidr={0x81000000+(cpu<<8):x} daif=0 freq=13000000 first={100+cpu*100} last={100+cpu*100} ctl=1 sre=7 gctl=8400 pmr=f0 group=1 bpr=3' for cpu in range(8))


class IrqTimerLogTests(unittest.TestCase):
    def test_same_tick_is_valid_but_progresses_across_cpus(self):
        samples=live.observations('',fixture())
        self.assertEqual(len(samples),8)
        self.assertEqual(samples[0]['first'],samples[0]['last'])

    def test_bad_or_incomplete_capture_is_rejected(self):
        for bad in [fixture().replace('last=100 ','last=99 '),
                    fixture().replace('mpidr=81000100','mpidr=81000000'),
                    fixture().replace('freq=13000000','freq=62500000'),
                    fixture().replace('sre=7','sre=0'),
                    fixture().replace(' bpr=3',' group=1'),
                    '\n'.join(fixture().splitlines()[:-1]),
                    fixture()+'\nBUG: fixture',
                    fixture().replace('first=200 last=200','first=100 last=100')]:
            with self.subTest(bad=bad[:90]),self.assertRaises((AssertionError,ValueError)):
                live.observations('',bad)

    def test_stale_capture_is_rejected(self):
        with self.assertRaises(AssertionError):
            live.observations(fixture(),fixture())

    def test_optimized_mode_refuses_before_device_or_output(self):
        for script in ['live.py','qemu.py']:
            result=subprocess.run(['python3','-O',str(ROOT/'diagnostics/ace-irq-timer'/script)],
                                  capture_output=True,text=True,timeout=10)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('without optimization',result.stderr)


if __name__=='__main__': unittest.main()
