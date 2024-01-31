import unittest

import numpy.testing as npt

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination
from adaptation_pathways.graph.conversion import sequence_graph_to_pathway_map
from adaptation_pathways.graph.layout.pathway_map import classic_layout, default_layout
from adaptation_pathways.graph.node import Action as ActionNode
from adaptation_pathways.graph.sequence_graph import SequenceGraph


# pylint: disable=too-many-locals


class PathwayLayoutTestBase(unittest.TestCase):
    def assert_equal_positions(self, positions_we_got, path, positions_we_want):
        self.assertEqual(len(path), len(positions_we_want))

        for idx, node in enumerate(path):
            self.assertEqual(positions_we_want[idx][0], node.label)
            npt.assert_almost_equal(positions_we_want[idx][1], positions_we_got[node])


class PathwayMapDefaultLayoutTest(PathwayLayoutTestBase):
    def test_empty(self):
        sequence_graph = SequenceGraph()
        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        positions = default_layout(pathway_map)

        self.assertEqual(len(positions), 0)

    def test_serial_pathway(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(a_node, b_node)
        sequence_graph.add_sequence(b_node, c_node)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 1)

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 8)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 0)),
                ("a]", (3, 0)),
                ("[b", (4, 0)),
                ("b]", (5, 0)),
                ("[c", (6, 0)),
                ("c]", (7, 0)),
            ],
        )

    def test_diverging_pathways(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(current_node, b_node)
        sequence_graph.add_sequence(current_node, c_node)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 8)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 1)),
                ("a]", (3, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b", (2, 0)),
                ("b]", (3, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -1)),
                ("c]", (3, -1)),
            ],
        )

    def test_converging_pathways(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = Action("d")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(current_node, b_node)
        sequence_graph.add_sequence(current_node, c_node)
        sequence_graph.add_sequence(a_node, d_node)
        sequence_graph.add_sequence(b_node, d_node)
        sequence_graph.add_sequence(c_node, d_node)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 14)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 1)),
                ("a]", (3, 1)),
                ("[d", (4, 1)),
                ("d]", (5, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b", (2, 0)),
                ("b]", (3, 0)),
                ("[d", (4, 0)),
                ("d]", (5, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -1)),
                ("c]", (3, -1)),
                ("[d", (4, -1)),
                ("d]", (5, -1)),
            ],
        )

    def test_use_case_01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = Action("d")
        e = Action("e")
        f = Action("f")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)
        e_node = ActionNode(e)
        f_node = ActionNode(f)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (a_node, e_node),
                (current_node, b_node),
                (b_node, f_node),
                (current_node, c_node),
                (c_node, f_node),
                (current_node, d_node),
                (d_node, f_node),
                (f_node, e_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 4)

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 24)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 1.5)),
                ("a]", (3, 1.5)),
                ("[e", (4, 1.5)),
                ("e]", (5, 1.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b", (2, 0.5)),
                ("b]", (3, 0.5)),
                ("[f", (4, 0.5)),
                ("f]", (5, 0.5)),
                ("[e", (6, 0.5)),
                ("e]", (7, 0.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -0.5)),
                ("c]", (3, -0.5)),
                ("[f", (4, -0.5)),
                ("f]", (5, -0.5)),
                ("[e", (6, -0.5)),
                ("e]", (7, -0.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[3],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[d", (2, -1.5)),
                ("d]", (3, -1.5)),
                ("[f", (4, -1.5)),
                ("f]", (5, -1.5)),
                ("[e", (6, -1.5)),
                ("e]", (7, -1.5)),
            ],
        )

    def test_use_case_02(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b1 = Action("b1")
        b2 = Action("b2")
        c = Action("c")
        d = Action("d")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b1_node = ActionNode(b1)
        b2_node = ActionNode(b2)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b1_node),
                (current_node, c_node),
                (current_node, d_node),
                (b1_node, a_node),
                (b1_node, c_node),
                (b1_node, d_node),
                (c_node, b2_node),
                (b2_node, a_node),
                (c_node, a_node),
                (c_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 10)

        pathway_map.assign_tipping_points(
            {
                current: 2030,
                a: 2100,
                b1: 2040,
                c: 2050,
                d: 2100,
                b2: 2070,
            }
        )

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 32)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 1.5)),
                ("a]", (3, 1.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b1", (2, 0.5)),
                ("b1]", (3, 0.5)),
                ("[a", (4, 2.5)),
                ("a]", (5, 2.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b1", (2, 0.5)),
                ("b1]", (3, 0.5)),
                ("[c", (4, 1.5)),
                ("c]", (5, 1.5)),
                ("[b2", (6, 2)),
                ("b2]", (7, 2)),
                ("[a", (8, 2)),
                ("a]", (9, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[3],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b1", (2, 0.5)),
                ("b1]", (3, 0.5)),
                ("[c", (4, 1.5)),
                ("c]", (5, 1.5)),
                ("[a", (6, 1)),
                ("a]", (7, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[4],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b1", (2, 0.5)),
                ("b1]", (3, 0.5)),
                ("[c", (4, 1.5)),
                ("c]", (5, 1.5)),
                ("[d", (6, 0)),
                ("d]", (7, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[5],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b1", (2, 0.5)),
                ("b1]", (3, 0.5)),
                ("[d", (4, 0.5)),
                ("d]", (5, 0.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[6],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -0.5)),
                ("c]", (3, -0.5)),
                ("[b2", (4, -0.5)),
                ("b2]", (5, -0.5)),
                ("[a", (6, -1)),
                ("a]", (7, -1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[7],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -0.5)),
                ("c]", (3, -0.5)),
                ("[a", (4, -1.5)),
                ("a]", (5, -1.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[8],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -0.5)),
                ("c]", (3, -0.5)),
                ("[d", (4, -2.5)),
                ("d]", (5, -2.5)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[9],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[d", (2, -1.5)),
                ("d]", (3, -1.5)),
            ],
        )

    def test_action_combination01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, b])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b_node),
                (current_node, c_node),
                (a_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 10)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 1)),
                ("a]", (3, 1)),
                ("[d", (4, 1)),
                ("d]", (5, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b", (2, 0)),
                ("b]", (3, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -1)),
                ("c]", (3, -1)),
            ],
        )

    def test_action_combination02(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, b])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b_node),
                (current_node, c_node),
                (a_node, d_node),
                (b_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 12)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 1)),
                ("a]", (3, 1)),
                ("[d", (4, 1)),
                ("d]", (5, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b", (2, 0)),
                ("b]", (3, 0)),
                ("[d", (4, 0)),
                ("d]", (5, 0)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[c", (2, -1)),
                ("c]", (3, -1)),
            ],
        )

    def test_action_edition_01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a1 = Action("a", 1)
        b = Action("b")
        a2 = Action("a", 2)

        current_node = ActionNode(current)
        a1_node = ActionNode(a1)
        b_node = ActionNode(b)
        a2_node = ActionNode(a2)

        sequence_graph.add_sequences(
            [
                (current_node, a1_node),
                (current_node, b_node),
                (b_node, a2_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 2)

        positions = default_layout(pathway_map)
        self.assertEqual(len(positions), 7)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[a", (2, 1)),
                ("a]", (3, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (1, 0)),
                ("[b", (2, -1)),
                ("b]", (3, -1)),
                ("[a", (4, -1)),
                ("a]", (5, -1)),
            ],
        )


class PathwayMapClassicLayoutTest(PathwayLayoutTestBase):
    def test_empty(self):
        sequence_graph = SequenceGraph()
        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        pathway_map.assign_tipping_points({})
        positions = classic_layout(pathway_map)

        self.assertEqual(len(positions), 0)

    def test_single_period(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")

        current_node = ActionNode(current)
        a_node = ActionNode(a)

        sequence_graph.add_sequence(current_node, a_node)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 1)

        pathway_map.assign_tipping_points(
            {
                # current: 0, → Skipping this one is fine, default is 0
                a: 10,
            }
        )

        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 4)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (-1, 0)),
                ("current]", (0, 0)),
                ("[a", (0, 1)),
                ("a]", (10, 1)),
            ],
        )

    def test_serial_pathway(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(a_node, b_node)
        sequence_graph.add_sequence(b_node, c_node)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 1)

        pathway_map.assign_tipping_points(
            {
                current: 2030,
                a: 2040,
                b: 2050,
                c: 2060,
            }
        )

        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 8)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2027, 0)),
                ("current]", (2030, 0)),
                ("[a", (2030, 2)),
                ("a]", (2040, 2)),
                ("[b", (2040, 1)),
                ("b]", (2050, 1)),
                ("[c", (2050, -1)),
                ("c]", (2060, -1)),
            ],
        )

    def test_diverging_pathways(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)

        sequence_graph.add_sequence(current_node, a_node)
        sequence_graph.add_sequence(current_node, b_node)
        sequence_graph.add_sequence(current_node, c_node)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        pathway_map.assign_tipping_points(
            {
                current: 2030,
                a: 2040,
                b: 2050,
                c: 2060,
            }
        )

        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 8)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2027, 0)),
                ("current]", (2030, 0)),
                ("[a", (2030, 2)),
                ("a]", (2040, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2027, 0)),
                ("current]", (2030, 0)),
                ("[b", (2030, 1)),
                ("b]", (2050, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2027, 0)),
                ("current]", (2030, 0)),
                ("[c", (2030, -1)),
                ("c]", (2060, -1)),
            ],
        )

    def test_use_case_01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = Action("d")
        e = Action("e")
        f = Action("f")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)
        e_node = ActionNode(e)
        f_node = ActionNode(f)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (a_node, e_node),
                (current_node, b_node),
                (b_node, f_node),
                (current_node, c_node),
                (c_node, f_node),
                (current_node, d_node),
                (d_node, f_node),
                (f_node, e_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 4)

        pathway_map.assign_tipping_points(
            {
                current: 2030,
                a: 2040,
                b: 2050,
                c: 2060,
                d: 2070,
                f: 2080,
                e: 2090,
            }
        )

        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 24)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2024, 0)),
                ("current]", (2030, 0)),
                ("[a", (2030, 3)),
                ("a]", (2040, 3)),
                ("[e", (2040, 2)),
                ("e]", (2090, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2024, 0)),
                ("current]", (2030, 0)),
                ("[b", (2030, 1)),
                ("b]", (2050, 1)),
                ("[f", (2050, -1)),
                ("f]", (2080, -1)),
                ("[e", (2080, 2)),
                ("e]", (2090, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2024, 0)),
                ("current]", (2030, 0)),
                ("[c", (2030, -2)),
                ("c]", (2060, -2)),
                ("[f", (2060, -1)),
                ("f]", (2080, -1)),
                ("[e", (2080, 2)),
                ("e]", (2090, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[3],
            [
                ("[current", (2024, 0)),
                ("current]", (2030, 0)),
                ("[d", (2030, -3)),
                ("d]", (2070, -3)),
                ("[f", (2070, -1)),
                ("f]", (2080, -1)),
                ("[e", (2080, 2)),
                ("e]", (2090, 2)),
            ],
        )

    def test_use_case_02(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b1 = Action("b1")
        b2 = Action("b2")
        c = Action("c")
        d = Action("d")

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b1_node = ActionNode(b1)
        b2_node = ActionNode(b2)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b1_node),
                (current_node, c_node),
                (current_node, d_node),
                (b1_node, a_node),
                (b1_node, c_node),
                (b1_node, d_node),
                (c_node, b2_node),
                (b2_node, a_node),
                (c_node, a_node),
                (c_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 10)

        pathway_map.assign_tipping_points(
            {
                current: 2030,
                a: 2100,
                b1: 2040,
                c: 2050,
                d: 2100,
                b2: 2070,
            }
        )

        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 32)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[a", (2030, 3)),
                ("a]", (2100, 3)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[b1", (2030, 2)),
                ("b1]", (2040, 2)),
                ("[a", (2040, 3)),
                ("a]", (2100, 3)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[b1", (2030, 2)),
                ("b1]", (2040, 2)),
                ("[c", (2040, 1)),
                ("c]", (2050, 1)),
                ("[b2", (2050, -1)),
                ("b2]", (2070, -1)),
                ("[a", (2070, 3)),
                ("a]", (2100, 3)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[3],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[b1", (2030, 2)),
                ("b1]", (2040, 2)),
                ("[c", (2040, 1)),
                ("c]", (2050, 1)),
                ("[a", (2050, 3)),
                ("a]", (2100, 3)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[4],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[b1", (2030, 2)),
                ("b1]", (2040, 2)),
                ("[c", (2040, 1)),
                ("c]", (2050, 1)),
                ("[d", (2050, -2)),
                ("d]", (2100, -2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[5],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[b1", (2030, 2)),
                ("b1]", (2040, 2)),
                ("[d", (2040, -2)),
                ("d]", (2100, -2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[6],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[c", (2030, 1)),
                ("c]", (2050, 1)),
                ("[b2", (2050, -1)),
                ("b2]", (2070, -1)),
                ("[a", (2070, 3)),
                ("a]", (2100, 3)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[7],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[c", (2030, 1)),
                ("c]", (2050, 1)),
                ("[a", (2050, 3)),
                ("a]", (2100, 3)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[8],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[c", (2030, 1)),
                ("c]", (2050, 1)),
                ("[d", (2050, -2)),
                ("d]", (2100, -2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[9],
            [
                ("[current", (2023, 0)),
                ("current]", (2030, 0)),
                ("[d", (2030, -2)),
                ("d]", (2100, -2)),
            ],
        )

    def test_action_combination01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, b])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b_node),
                (current_node, c_node),
                (a_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        pathway_map.assign_tipping_points(
            {
                current: 2020,
                a: 2030,
                b: 2040,
                c: 2050,
                d: 2100,
            }
        )
        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 10)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[a", (2020, 2)),
                ("a]", (2030, 2)),
                ("[d", (2030, 2)),
                ("d]", (2100, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[b", (2020, 1)),
                ("b]", (2040, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[c", (2020, -1)),
                ("c]", (2050, -1)),
            ],
        )

    def test_action_combination02(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, b])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b_node),
                (current_node, c_node),
                (a_node, d_node),
                (b_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        pathway_map.assign_tipping_points(
            {
                current: 2020,
                a: 2030,
                b: 2040,
                c: 2050,
                d: 2100,
            }
        )
        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 12)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[a", (2020, 2)),
                ("a]", (2030, 2)),
                ("[d", (2030, 1)),
                ("d]", (2100, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[b", (2020, -1)),
                ("b]", (2040, -1)),
                ("[d", (2040, 1)),
                ("d]", (2100, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[c", (2020, -2)),
                ("c]", (2050, -2)),
            ],
        )

    def test_action_combination03(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, b])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b_node),
                (current_node, c_node),
                (b_node, d_node),
                (c_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        pathway_map.assign_tipping_points(
            {
                current: 2020,
                a: 2030,
                b: 2040,
                c: 2050,
                d: 2100,
            }
        )
        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 12)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[a", (2020, 2)),
                ("a]", (2030, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[b", (2020, 1)),
                ("b]", (2040, 1)),
                ("[d", (2040, 1)),
                ("d]", (2100, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[c", (2020, -1)),
                ("c]", (2050, -1)),
                ("[d", (2050, 1)),
                ("d]", (2100, 1)),
            ],
        )

    def test_action_combination04(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        e = Action("e")
        d = ActionCombination("d", [a, e])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b_node),
                (current_node, c_node),
                (a_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        pathway_map.assign_tipping_points(
            {
                current: 2020,
                a: 2030,
                b: 2040,
                c: 2050,
                d: 2100,
            }
        )
        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 10)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[a", (2020, 2)),
                ("a]", (2030, 2)),
                ("[d", (2030, 2)),
                ("d]", (2100, 2)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[b", (2020, 1)),
                ("b]", (2040, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[c", (2020, -1)),
                ("c]", (2050, -1)),
            ],
        )

    def test_action_combination05(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", [a, c])

        current_node = ActionNode(current)
        a_node = ActionNode(a)
        b_node = ActionNode(b)
        c_node = ActionNode(c)
        d_node = ActionNode(d)

        sequence_graph.add_sequences(
            [
                (current_node, a_node),
                (current_node, b_node),
                (current_node, c_node),
                (a_node, d_node),
                (c_node, d_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 3)

        pathway_map.assign_tipping_points(
            {
                current: 2020,
                a: 2030,
                b: 2040,
                c: 2050,
                d: 2100,
            }
        )
        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 12)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[a", (2020, 2)),
                ("a]", (2030, 2)),
                ("[d", (2030, 1)),
                ("d]", (2100, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[b", (2020, -1)),
                ("b]", (2040, -1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[2],
            [
                ("[current", (2012, 0)),
                ("current]", (2020, 0)),
                ("[c", (2020, -2)),
                ("c]", (2050, -2)),
                ("[d", (2050, 1)),
                ("d]", (2100, 1)),
            ],
        )

    def test_action_edition_01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a1 = Action("a", 1)
        b = Action("b")
        a2 = Action("a", 2)

        current_node = ActionNode(current)
        a1_node = ActionNode(a1)
        b_node = ActionNode(b)
        a2_node = ActionNode(a2)

        sequence_graph.add_sequences(
            [
                (current_node, a1_node),
                (current_node, b_node),
                (b_node, a2_node),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        paths = list(pathway_map.all_paths())
        self.assertEqual(len(paths), 2)

        pathway_map.assign_tipping_points(
            {
                current: 2030,
                a1: 2040,
                b: 2050,
                a2: 2060,
            }
        )
        positions = classic_layout(pathway_map)
        self.assertEqual(len(positions), 7)

        self.assert_equal_positions(
            positions,
            paths[0],
            [
                ("[current", (0, 0)),
                ("current]", (2030, 0)),
                ("[a", (2030, 1)),
                ("a]", (2040, 1)),
            ],
        )
        self.assert_equal_positions(
            positions,
            paths[1],
            [
                ("[current", (0, 0)),
                ("current]", (2030, 0)),
                ("[b", (2030, -1)),
                ("b]", (2050, -1)),
                ("[a", (2050, 1)),
                ("a]", (2060, 1)),
            ],
        )
