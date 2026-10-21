import importlib.util
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import fdt

spec = importlib.util.spec_from_file_location('ace_dt_audit', Path(__file__).resolve().parents[1] / 'tools/ace-dt-audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def u32(*v):
    return struct.pack('>%dI' % len(v), *v)


def fixture(extra_cpu=False):
    """Synthetic DTB with a 4-cell GIC provider and dynamic carve-out."""
    names, body = bytearray(), bytearray()
    def begin(name):
        body.extend(u32(1) + name.encode() + b'\0')
        body.extend(b'\0' * (-len(body) % 4))
    def prop(name, value):
        off = len(names)
        names.extend(name.encode() + b'\0')
        body.extend(u32(3, len(value), off) + value)
        body.extend(b'\0' * (-len(body) % 4))
    def end():
        body.extend(u32(2))
    begin(''); prop('#address-cells', u32(2)); prop('#size-cells', u32(2))
    prop('interrupt-parent', u32(1))
    begin('gic'); prop('compatible', b'arm,gic-v3\0'); prop('phandle', u32(1))
    prop('#interrupt-cells', u32(4)); prop('reg', u32(0, 0xc000000, 0, 0x40000, 0, 0xc040000, 0, 0x200000)); end()
    begin('timer'); prop('compatible', b'arm,armv8-timer\0')
    prop('interrupts', u32(1, 13, 4, 0, 1, 14, 4, 0, 1, 11, 4, 0, 1, 10, 4, 0))
    prop('clock-frequency', u32(13000000)); end()
    begin('ufs'); prop('compatible', b'jedec,ufs-2.0\0')
    prop('interrupts', u32(0, 137, 4, 0)); prop('reg', u32(0, 0x112b0000, 0, 0x2300)); end()
    begin('psci'); prop('compatible', b'arm,psci-1.0\0'); prop('method', b'smc\0'); end()
    begin('cpus'); prop('#address-cells', u32(1)); prop('#size-cells', u32(0))
    for n in range(2 if extra_cpu else 1):
        begin('cpu@' + str(n)); prop('device_type', b'cpu\0'); prop('reg', u32(n << 8)); end()
    end()
    begin('reserved-memory'); prop('#address-cells', u32(2)); prop('#size-cells', u32(2))
    begin('dynamic'); prop('size', u32(0, 0x100000)); prop('no-map', b''); end(); end()
    end(); body.extend(u32(9))
    st, ss = 56, 56 + len(body)
    return u32(0xd00dfeed, ss + len(names), st, ss, 40, 17, 16, 0, len(names), len(body)) + b'\0' * 16 + body + names


class DeviceTreeTests(unittest.TestCase):
    def test_four_cell_gic_spi_ppi_and_cpu_reg(self):
        report = audit.audit(fixture())
        self.assertEqual([x['intid'] for x in report['timers'][0]['interrupts']], [29, 30, 27, 26])
        self.assertEqual(report['ufs'][0]['interrupts'][0]['intid'], 169)
        self.assertEqual(report['cpus'][0]['reg'], [{'address': 0, 'size': 0}])
        self.assertFalse(report['hardware_execution_verified'])

    def test_dynamic_reservation_not_invented_as_address(self):
        record = audit.audit(fixture())['reserved_memory'][0]
        self.assertTrue(record['dynamic'])
        self.assertTrue(record['no_map'])
        self.assertNotIn('reg', record)

    def test_truncation_and_block_bounds(self):
        for size in (0, 39, 60, len(fixture()) - 1):
            with self.subTest(size=size), self.assertRaises(fdt.FDTError):
                fdt.parse(fixture()[:size])
        broken = bytearray(fixture())
        struct.pack_into('>I', broken, 12, len(broken) - 1)
        with self.assertRaises(fdt.FDTError):
            fdt.parse(broken)

    def test_bad_provider_length_and_missing_parent(self):
        tree = fdt.parse(fixture()); timer = tree.by_path('/timer')
        timer.props['interrupts'] = u32(1, 11, 4)
        with self.assertRaises(fdt.FDTError):
            fdt.interrupts(tree, timer)
        timer.props['interrupt-parent'] = u32(999)
        with self.assertRaises(fdt.FDTError):
            fdt.interrupts(tree, timer)

    def test_extended_interrupts_and_ppi_bounds(self):
        tree = fdt.parse(fixture()); timer = tree.by_path('/timer')
        del timer.props['interrupts']
        timer.props['interrupts-extended'] = u32(1, 1, 11, 4, 0)
        self.assertEqual(fdt.interrupts(tree, timer)[0]['intid'], 27)
        timer.props['interrupts-extended'] = u32(1, 1, 16, 4, 0)
        with self.assertRaises(fdt.FDTError):
            fdt.interrupts(tree, timer)
        timer.props['interrupts-extended'] = u32(1, 0, 987, 4, 0)
        self.assertEqual(fdt.interrupts(tree, timer)[0]['intid'], 1019)
        for invalid in (988, 0xffffffff):
            timer.props['interrupts-extended'] = u32(1, 0, invalid, 4, 0)
            with self.assertRaises(fdt.FDTError):
                fdt.interrupts(tree, timer)

    def test_implicit_parent_controller(self):
        tree = fdt.parse(fixture())
        del tree.root.props['interrupt-parent']
        controller = tree.by_path('/gic')
        controller.props['interrupt-controller'] = b''
        child = fdt.Node('child', controller, {'interrupts': u32(0, 137, 4, 0)})
        controller.children.append(child)
        self.assertEqual(fdt.interrupts(tree, child)[0]['intid'], 169)

    def test_physical_controller_precedes_root_default(self):
        tree = fdt.parse(fixture())
        nested = fdt.Node('nested', tree.root, {'interrupt-controller': b'',
                         '#interrupt-cells': u32(4), 'phandle': u32(2),
                         'compatible': b'arm,gic-v3\0'})
        tree.root.children.append(nested)
        child = fdt.Node('child', nested, {'interrupts': u32(0, 137, 4, 0)})
        nested.children.append(child)
        self.assertEqual(fdt.interrupts(tree, child)[0]['provider'], '/nested')

    def test_profile_mismatch_is_explicit(self):
        report = audit.audit(fixture())
        profile = {'gic': {'distributor': 0xc000000, 'redistributor': 0xc040000},
                   'timer': {'frequency': 13000000, 'virtual_intid': 27},
                   'psci_conduit': 'smc', 'cpu_affinities': [0]}
        self.assertEqual(audit.check_profile(report, profile), [])
        profile['timer']['virtual_intid'] = 19
        self.assertIn('virtual timer interrupt differs from Ace profile', audit.check_profile(report, profile))


if __name__ == '__main__':
    unittest.main()
