"""Offline module/provider planning guards; no target module execution."""
import importlib.util
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ace_module_plan', ROOT / 'diagnostics/ace-ramdiag/module_plan.py')
plan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plan)


class DependencyPlanTests(unittest.TestCase):
    def test_return_stage_must_precede_consumers_and_be_dependency_closed(self):
        d = plan.Dependencies(['a.ko', 'b.ko', 'z.ko'], 'a.ko:b.ko\nb.ko:\nz.ko:', '')
        self.assertEqual(d.ordered(['a', 'z'], first=['z']), ['z.ko', 'b.ko', 'a.ko'])
        with self.assertRaisesRegex(ValueError, 'later stage'):
            d.ordered(['a', 'z'], first=['a'])
        with self.assertRaisesRegex(ValueError, 'outside closure'):
            d.ordered(['a'], first=['z'])

    def test_transitive_symbol_pre_and_post_order(self):
        d = plan.Dependencies(['consumer.ko', 'hard.ko', 'pre.ko', 'post.ko'],
                              '/lib/modules/consumer.ko: /lib/modules/hard.ko\nhard.ko:\npre.ko:\npost.ko:\n',
                              'softdep consumer pre:\u00a0pre.ko post:post.ko\n')
        result = d.ordered(['consumer'])
        self.assertEqual(set(result), {'consumer.ko', 'hard.ko', 'pre.ko', 'post.ko'})
        self.assertLess(result.index('hard.ko'), result.index('consumer.ko'))
        self.assertLess(result.index('pre.ko'), result.index('consumer.ko'))
        self.assertLess(result.index('consumer.ko'), result.index('post.ko'))

    def test_missing_ambiguous_and_unsafe_modules_refused(self):
        for files, hard, soft in [(['a.ko'], '', ''),
                                  (['a.ko'], 'a.ko: missing.ko', ''),
                                  (['a-b.ko', 'a_b.ko'], '', ''),
                                  (['a.ko'], 'a.ko:\na.ko:', ''),
                                  (['a.ko'], 'a.ko: ../a.ko', ''),
                                  (['a.ko'], 'a.ko:', 'softdep a pre:missing'),
                                  (['a.ko'], 'a.ko:', 'softdep a missing')]:
            with self.subTest(files=files, hard=hard, soft=soft), self.assertRaises(ValueError):
                plan.Dependencies(files, hard, soft)

    def test_cycles_refused_including_post_constraints(self):
        d = plan.Dependencies(['a.ko', 'b.ko'], 'a.ko:b.ko\nb.ko:a.ko', '')
        with self.assertRaisesRegex(ValueError, 'cycle'):
            d.ordered(['a'])
        d = plan.Dependencies(['a.ko', 'b.ko'], 'a.ko:b.ko\nb.ko:', 'softdep a post:b')
        with self.assertRaisesRegex(ValueError, 'cycle'):
            d.ordered(['a'])

    def test_repeated_order_does_not_mutate_hard_graph(self):
        d = plan.Dependencies(['a.ko', 'b.ko'], 'a.ko:b.ko\nb.ko:', '')
        self.assertEqual(d.ordered(['a']), ['b.ko', 'a.ko'])
        self.assertEqual(d.ordered(['a']), ['b.ko', 'a.ko'])
        self.assertEqual(d.hard['a.ko'], {'b.ko'})

    def test_source_order_constraints_are_checked_not_assumed_readiness(self):
        d = plan.Dependencies(['a.ko', 'b.ko'], 'a.ko:\nb.ko:', '')
        self.assertEqual(d.ordered(['a', 'b'], before=[('b', 'a')]), ['b.ko', 'a.ko'])
        with self.assertRaisesRegex(ValueError, 'outside closure'):
            d.ordered(['a'], before=[('b', 'a')])
        with self.assertRaisesRegex(ValueError, 'cycle'):
            d.ordered(['a', 'b'], before=[('b', 'a'), ('a', 'b')])


def cells(*values):
    return struct.pack('>' + 'I' * len(values), *values)


def node(parent, name, **props):
    child = plan.fdt.Node(name, parent, props)
    if parent is not None:
        parent.children.append(child)
    return child


class ProviderPlanTests(unittest.TestCase):
    def fixture(self):
        root = node(None, '')
        clock = node(root, 'clk', phandle=cells(1), **{'#clock-cells': cells(1)})
        consumer = node(root, 'usb', clocks=cells(1, 7), compatible=b'mediatek,mtu3\0')
        return plan.fdt.Tree(root, [], 0), clock, consumer

    def test_variable_specs_and_parent_edges(self):
        tree, clock, consumer = self.fixture()
        nodes, edges, _ = plan.provider_closure(tree, ['/usb'])
        self.assertEqual(set(nodes), {'/', '/usb', '/clk'})
        self.assertIn(dict(consumer='/usb', property='clocks', provider='/clk', args=[7]), edges)

    def test_unknown_or_truncated_reference_is_not_ignored(self):
        for value in [cells(1), cells(2, 7)]:
            tree, _, consumer = self.fixture()
            consumer.props['clocks'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                plan.provider_closure(tree, ['/usb'])

    def test_graph_endpoint_cycles_are_finite(self):
        tree, _, consumer = self.fixture()
        p = node(consumer, 'port')
        a = node(p, 'endpoint@0', phandle=cells(2), **{'remote-endpoint': cells(3)})
        p = node(tree.root, 'peer')
        node(p, 'endpoint@0', phandle=cells(3), **{'remote-endpoint': cells(2)})
        nodes, edges, _ = plan.provider_closure(tree, ['/usb'])
        self.assertIn('/peer/endpoint@0', nodes)
        self.assertEqual(len([r for r in edges if r['property'] == 'remote-endpoint']), 2)
        self.assertIn(a.path, nodes)

    def test_named_tcpc_requires_unique_target(self):
        tree, _, consumer = self.fixture()
        consumer.props['tcpc'] = b'type_c_port0\0'
        with self.assertRaisesRegex(ValueError, 'named tcpc'):
            plan.provider_closure(tree, ['/usb'])
        target = node(tree.root, 'tcpc', **{'tcpc,name': b'type_c_port0\0'})
        nodes, edges, _ = plan.provider_closure(tree, ['/usb'])
        self.assertIn(target.path, nodes)
        self.assertIn(dict(consumer='/usb', property='tcpc name -> tcpc,name', provider='/tcpc', args=['type_c_port0']), edges)
        node(tree.root, 'duplicate', **{'tcpc,name': b'type_c_port0\0'})
        with self.assertRaisesRegex(ValueError, 'named tcpc'):
            plan.provider_closure(tree, ['/usb'])

    def test_mfd_child_mapping_requires_exact_platform_alias(self):
        root = node(None, '', compatible=b'mediatek,mt6363\0')
        dep = plan.Dependencies(['mt6363-regulator.ko'], 'mt6363-regulator.ko:', '')
        source = dict(module='mt6363-regulator.ko', compatible=['mediatek,mt6363'], source='mfd.c', sha256='0' * 64, platform_cell='mt6363-regulator')
        with self.assertRaisesRegex(ValueError, 'platform alias'):
            plan.match_modules({'/': root}, dep, '', [source])
        matches = plan.match_modules({'/': root}, dep, 'alias platform:mt6363-regulator mt6363_regulator', [source])
        self.assertEqual(matches['/']['modules'], ['mt6363-regulator.ko'])

    def test_alias_and_source_matches_remain_distinct_evidence(self):
        tree, _, consumer = self.fixture()
        dep = plan.Dependencies(['mtu3.ko'], 'mtu3.ko:', '')
        matches = plan.match_modules({'/usb': consumer}, dep, 'alias of:N*T*Cmediatek,mtu3C* mtu3', [])
        self.assertEqual(matches['/usb']['modules'], [])
        # The C* variant expects trailing C data; supply a second compatible.
        consumer.props['compatible'] = b'mediatek,mtu3\0mediatek,mt6895-mtu3\0'
        self.assertEqual(plan.match_modules({'/usb': consumer}, dep, 'alias of:N*T*Cmediatek,mtu3C* mtu3', [])['/usb']['modules'], ['mtu3.ko'])
        source = dict(module='mtu3.ko', compatible=['mediatek,mtu3'], source='drivers/usb.c', sha256='0' * 64)
        evidence = plan.match_modules({'/usb': consumer}, dep, '', [source])['/usb']['evidence']
        self.assertEqual(evidence[0]['kind'], 'matching official source table only')


if __name__ == '__main__':
    unittest.main()
