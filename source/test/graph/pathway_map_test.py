import unittest

from adaptation_pathways.graph.conversion import sequence_graph_to_pathway_map
from adaptation_pathways.graph.node.action import Action
from adaptation_pathways.graph.node.action_begin import ActionBegin
from adaptation_pathways.graph.node.action_end import ActionEnd
from adaptation_pathways.graph.pathway_map import PathwayMap, verify_tipping_points
from adaptation_pathways.graph.sequence_graph import SequenceGraph


class PathwayMapTest(unittest.TestCase):
    def test_constructor(self):
        graph = PathwayMap()

        self.assertEqual(graph.nr_nodes(), 0)
        self.assertEqual(graph.nr_edges(), 0)

    def test_assign_tipping_points_empty_graph(self):
        graph = PathwayMap()
        tipping_points = {}

        # Empty collection of tipping points
        graph.assign_tipping_points(tipping_points)

        # Non-empty collection of tipping points
        action = Action("Meh")
        tipping_points[action] = 5

        with self.assertRaises(LookupError):
            graph.assign_tipping_points(tipping_points)

    def test_assign_tipping_points_non_empty_graph(self):
        graph = PathwayMap()
        action = Action("Meh")
        action_begin = ActionBegin(action)
        action_end = ActionEnd(action)

        graph.add_period(action_begin, action_end)

        tipping_points = {}

        # Empty collection of tipping points
        for action_end in graph.action_ends_by_action(action):
            self.assertEqual(action_end.tipping_point, 0)
        graph.assign_tipping_points(tipping_points)
        for action_end in graph.action_ends_by_action(action):
            self.assertEqual(action_end.tipping_point, 0)

        # Non-empty collection of tipping points
        tipping_points[action] = 5

        for action_end in graph.action_ends_by_action(action):
            self.assertEqual(action_end.tipping_point, 0)
        graph.assign_tipping_points(tipping_points)
        for action_end in graph.action_ends_by_action(action):
            self.assertEqual(action_end.tipping_point, 5)


class VerifyTippingPointsTest(unittest.TestCase):
    def test_empty_graph(self):
        graph = PathwayMap()

        verify_tipping_points(graph)

    def test_single_period(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")

        sequence_graph.add_sequence(current, a)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)

        with self.assertRaises(ValueError):
            verify_tipping_points(pathway_map)

        tipping_points = {a: 5}
        pathway_map.assign_tipping_points(tipping_points)
        verify_tipping_points(pathway_map)

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

        with self.assertRaises(ValueError):
            verify_tipping_points(pathway_map)

        tipping_points = {
            current: 2024,
            a: 2030,
            b: 2030,
            c: 2030,
            d: 2030,
            f: 2030,  # <-- can't tip this soon already
            e: 2100,
        }
        pathway_map.assign_tipping_points(tipping_points)

        with self.assertRaises(ValueError):
            verify_tipping_points(pathway_map)

        pathway_map.assign_tipping_points({f: 2040})  # All OK now

        verify_tipping_points(pathway_map)
