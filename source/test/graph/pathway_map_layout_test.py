import unittest

import numpy.testing as npt

from adaptation_pathways.graph.conversion import sequence_graph_to_pathway_map
from adaptation_pathways.graph.layout.pathway_map import default_layout
from adaptation_pathways.graph.node import Action
from adaptation_pathways.graph.sequence_graph import SequenceGraph


class PathwayMapLayoutTest(unittest.TestCase):
    def test_empty(self):
        sequence_graph = SequenceGraph()
        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        positions = default_layout(pathway_map)

        self.assertEqual(len(positions), 0)

    def test_single_period(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")

        sequence_graph.add_sequence(current, a)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        positions = default_layout(pathway_map)

        self.assertEqual(len(positions), 4)

        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(current)], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(current)], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(a)], (2, 0)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 0))

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
        positions = default_layout(pathway_map)

        self.assertEqual(len(positions), 8)

        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(current)], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(current)], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(a)], (2, 0)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 0))
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(b)], (4, 0)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(b)], (5, 0))
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(c)], (6, 0)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(c)], (7, 0))

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
        positions = default_layout(pathway_map)

        self.assertEqual(len(positions), 8)

        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(current)], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(current)], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(a)], (2, 1)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 1))
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(b)], (2, 0)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(b)], (3, 0))
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(c)], (2, -1)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(c)], (3, -1))

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
        positions = default_layout(pathway_map)

        self.assertEqual(len(positions), 14)

        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(current)], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(current)], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(a)], (2, 1.5)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(a)], (3, 1.5)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(b)], (2, 0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(b)], (3, 0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(c)], (2, -0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(c)], (3, -0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(d)], (2, -1.5)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(d)], (3, -1.5)
        )

    def test_use_case_02(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")

        sequence_graph.add_sequences(
            [
                (current, a),
                (current, b),
                (a, b),
            ]
        )

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        positions = default_layout(pathway_map)

        self.assertEqual(len(positions), 6)

        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(current)], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_end_by_action(current)], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(a)], (2, 0)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(a)], (3, 0))
        npt.assert_almost_equal(
            positions[pathway_map.action_begin_by_action(b)], (4, 0)
        )
        npt.assert_almost_equal(positions[pathway_map.action_end_by_action(b)], (5, 0))
