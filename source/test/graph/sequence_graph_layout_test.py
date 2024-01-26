import unittest

import numpy.testing as npt

from adaptation_pathways.graph.layout.sequence_graph import default_layout
from adaptation_pathways.graph.node import Action, ActionCombination
from adaptation_pathways.graph.sequence_graph import SequenceGraph


class SequenceGraphLayoutTest(unittest.TestCase):
    def test_empty(self):
        sequence_graph = SequenceGraph()
        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), 0)

    def test_root_node(self):
        """
        current
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        actions = [current]

        sequence_graph.add_action(current)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))

    def test_single_sequence(self):
        """
        current → a
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        actions = [current, a]

        sequence_graph.add_sequence(current, a)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))
        npt.assert_almost_equal(positions[a], (1, 0))

    def test_serial_sequence(self):
        """
        current → a → b → c
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        actions = [current, a, b, c]

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(a, b)
        sequence_graph.add_sequence(b, c)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))
        npt.assert_almost_equal(positions[a], (1, 0))
        npt.assert_almost_equal(positions[b], (2, 0))
        npt.assert_almost_equal(positions[c], (3, 0))

    def test_diverging_sequence(self):
        """
                ↗ a
        current
                ↘ b
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        actions = [current, a, b]

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))
        npt.assert_almost_equal(positions[a], (1, 0.5))
        npt.assert_almost_equal(positions[b], (1, -0.5))

    def test_converging_sequence(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = Action("d")
        actions = [current, a, b, c, d]

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)
        sequence_graph.add_sequence(a, d)
        sequence_graph.add_sequence(b, d)
        sequence_graph.add_sequence(c, d)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))
        npt.assert_almost_equal(positions[a], (1, 1))
        npt.assert_almost_equal(positions[b], (1, 0))
        npt.assert_almost_equal(positions[c], (1, -1))
        npt.assert_almost_equal(positions[d], (2, 0))

    def test_use_case_01(self):
        """
        test_use_case_01
        current - a - e
        current - b - f
        current - c - f
        current - d - f
        current - f - e

        e has in-degree of two, f has in-degree of three, but since e follows f, it must be
        positioned to the right of it
        """
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = Action("d")
        e = Action("e")
        f = Action("f")
        actions = [current, a, b, c, d, e, f]

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

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))
        npt.assert_almost_equal(positions[a], (1, 1.5))
        npt.assert_almost_equal(positions[b], (1, 0.5))
        npt.assert_almost_equal(positions[c], (1, -0.5))
        npt.assert_almost_equal(positions[d], (1, -1.5))
        npt.assert_almost_equal(positions[e], (3, 0.5))
        npt.assert_almost_equal(positions[f], (2, -0.5))

    def test_action_combination_01(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", a, b)
        actions = [current, a, b, c, d]

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)
        sequence_graph.add_sequence(a, d)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))
        npt.assert_almost_equal(positions[a], (1, 1))
        npt.assert_almost_equal(positions[b], (1, 0))
        npt.assert_almost_equal(positions[c], (1, -1))
        npt.assert_almost_equal(positions[d], (2, 1))

    def test_action_combination_02(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")
        d = ActionCombination("d", a, b)
        actions = [current, a, b, c, d]

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)
        sequence_graph.add_sequence(a, d)
        sequence_graph.add_sequence(b, d)

        positions = default_layout(sequence_graph)

        self.assertEqual(len(positions), len(actions))
        self.assertTrue(all(action in positions for action in actions))
        npt.assert_almost_equal(positions[current], (0, 0))
        npt.assert_almost_equal(positions[a], (1, 1))
        npt.assert_almost_equal(positions[b], (1, 0))
        npt.assert_almost_equal(positions[c], (1, -1))
        npt.assert_almost_equal(positions[d], (2, 0.5))
