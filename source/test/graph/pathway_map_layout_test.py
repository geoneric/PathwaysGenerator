import unittest

import numpy.testing as npt

from adaptation_pathways.graph.conversion import sequence_graph_to_pathway_map
from adaptation_pathways.graph.layout.pathway_map import classic_layout, default_layout
from adaptation_pathways.graph.node import Action
from adaptation_pathways.graph.sequence_graph import SequenceGraph


class PathwayMapDefaultLayoutTest(unittest.TestCase):
    def assert_equal_positions(self, positions_we_got, path, positions_we_want):
        self.assertEqual(len(path), len(positions_we_want))

        for idx, node in enumerate(path):
            self.assertEqual(positions_we_want[idx][0], node.label)
            npt.assert_almost_equal(positions_we_want[idx][1], positions_we_got[node])

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

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(a, b)
        sequence_graph.add_sequence(b, c)

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

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)

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

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)
        sequence_graph.add_sequence(a, d)
        sequence_graph.add_sequence(b, d)
        sequence_graph.add_sequence(c, d)

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

        sequence_graph.add_sequences(
            [
                (current, a),
                (a, e),
                (current, b),
                (b, f),
                (current, c),
                (c, f),
                (current, d),
                (d, f),
                (f, e),
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


class PathwayMapClassicLayoutTest(unittest.TestCase):
    def test_empty(self):
        sequence_graph = SequenceGraph()
        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        pathway_map.assign_tipping_points({})
        positions = classic_layout(pathway_map)

        self.assertEqual(len(positions), 0)

    # def test_single_period(self):
    #     sequence_graph = SequenceGraph()
    #     current = Action("current")
    #     a = Action("a")

    #     sequence_graph.add_sequence(current, a)

    #     pathway_map = sequence_graph_to_pathway_map(sequence_graph)
    #     pathway_map.assign_tipping_points({
    #         a: 10,
    #     })
    #     positions = classic_layout(pathway_map)

    #     self.assertEqual(len(positions), 4)

    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(current)], (0, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(current)], (1, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(a)], (2, 0)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 0))

    # def test_serial_pathway(self):
    #     sequence_graph = SequenceGraph()
    #     current = Action("current")
    #     a = Action("a")
    #     b = Action("b")
    #     c = Action("c")

    #     sequence_graph.add_sequence(current, a)
    #     sequence_graph.add_sequence(a, b)
    #     sequence_graph.add_sequence(b, c)

    #     pathway_map = sequence_graph_to_pathway_map(sequence_graph)
    #     positions = classic_layout(pathway_map)

    #     self.assertEqual(len(positions), 8)

    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(current)], (0, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(current)], (1, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(a)], (2, 0)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 0))
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(b)], (4, 0)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(b)], (5, 0))
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(c)], (6, 0)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(c)], (7, 0))

    # def test_diverging_pathways(self):
    #     sequence_graph = SequenceGraph()
    #     current = Action("current")
    #     a = Action("a")
    #     b = Action("b")
    #     c = Action("c")

    #     sequence_graph.add_sequence(current, a)
    #     sequence_graph.add_sequence(current, b)
    #     sequence_graph.add_sequence(current, c)

    #     pathway_map = sequence_graph_to_pathway_map(sequence_graph)
    #     positions = classic_layout(pathway_map)

    #     self.assertEqual(len(positions), 8)

    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(current)], (0, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(current)], (1, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(a)], (2, 1)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 1))
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(b)], (2, 0)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(b)], (3, 0))
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(c)], (2, -1)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(c)], (3, -1))

    # def test_use_case_01(self):
    #     sequence_graph = SequenceGraph()
    #     current = Action("current")
    #     a = Action("a")
    #     b = Action("b")
    #     c = Action("c")
    #     d = Action("d")
    #     e = Action("e")
    #     f = Action("f")

    #     sequence_graph.add_sequences(
    #         [
    #             (current, a),
    #             (a, e),
    #             (current, b),
    #             (b, f),
    #             (current, c),
    #             (c, f),
    #             (current, d),
    #             (d, f),
    #             (f, e),
    #         ]
    #     )

    #     pathway_map = sequence_graph_to_pathway_map(sequence_graph)
    #     positions = classic_layout(pathway_map)

    #     self.assertEqual(len(positions), 14)

    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(current)], (0, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(current)], (1, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(a)], (2, 1.5)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(a)], (3, 1.5)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(b)], (2, 0.5)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(b)], (3, 0.5)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(c)], (2, -0.5)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(c)], (3, -0.5)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(d)], (2, -1.5)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(d)], (3, -1.5)
    #     )

    # def test_use_case_02(self):
    #     sequence_graph = SequenceGraph()
    #     current = Action("current")
    #     a = Action("a")
    #     b = Action("b")

    #     sequence_graph.add_sequences(
    #         [
    #             (current, a),
    #             (current, b),
    #             (a, b),
    #         ]
    #     )

    #     pathway_map = sequence_graph_to_pathway_map(sequence_graph)
    #     positions = classic_layout(pathway_map)

    #     self.assertEqual(len(positions), 6)

    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(current)], (0, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_end_by_action(current)], (1, 0)
    #     )
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(a)], (2, 0)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 0))
    #     npt.assert_almost_equal(
    #         positions[pathway_map.action_begin_by_action(b)], (4, 0)
    #     )
    #     npt.assert_almost_equal(positions[pathway_map.action_end_by_action(b)], (5, 0))
