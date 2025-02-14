import unittest

from adaptation_pathways.action import Action
from adaptation_pathways.graph import (
    PathwayMap,
    SequenceGraph,
    sequence_graph_to_pathway_map,
    verify_tipping_points,
)
from adaptation_pathways.graph.node import Action as ActionNode
from adaptation_pathways.graph.node import ActionBegin, ActionEnd


# pylint: disable=too-many-locals


class PathwayMapTest(unittest.TestCase):
    def test_constructor(self):
        graph = PathwayMap()

        self.assertEqual(graph.nr_nodes(), 0)
        self.assertEqual(graph.nr_edges(), 0)

    def test_assign_tipping_points_empty_graph(self):
        graph = PathwayMap()
        tipping_point_by_action = {}

        # Empty collection of tipping points
        verify_tipping_points(graph, tipping_point_by_action)

        # Non-empty collection of tipping points
        action = Action("Meh")
        tipping_point_by_action[action] = 5.0

        # OK, tipping point is skipped
        verify_tipping_points(graph, tipping_point_by_action)

    def test_assign_tipping_points_non_empty_graph(self):
        graph = PathwayMap()
        action = Action("Meh")
        action_begin = ActionBegin(action)
        action_end = ActionEnd(action)

        graph.add_period(action_begin, action_end)

        tipping_point_by_action = {}

        # Non-empty collection of tipping points
        tipping_point_by_action[action] = 5.0

        verify_tipping_points(graph, tipping_point_by_action)


class VerifyTippingPointsTest(unittest.TestCase):
    def test_empty_graph(self):
        graph = PathwayMap()

        verify_tipping_points(graph, {})

    def test_single_period(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")

        current_node = ActionNode(current)
        a_node = ActionNode(a)

        sequence_graph.add_sequence(current_node, a_node)

        pathway_map = sequence_graph_to_pathway_map(sequence_graph)

        tipping_point_by_action = {
            current: 4.0,
            a: 5.0,
        }
        verify_tipping_points(pathway_map, tipping_point_by_action)

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

        tipping_point_by_action = {
            current: 2024.0,
            a: 2030.0,
            b: 2030.0,
            c: 2030.0,
            d: 2030.0,
            f: 2029.0,  # <-- can't tip this soon already
            e: 2100.0,
        }

        with self.assertRaises(ValueError):
            verify_tipping_points(pathway_map, tipping_point_by_action)

        tipping_point_by_action[f] = 2040.0  # All OK now

        verify_tipping_points(pathway_map, tipping_point_by_action)
