import unittest

from adaptation_pathways.graph.node import Action
from adaptation_pathways.graph.sequence_graph import SequenceGraph


class SequenceGraphTest(unittest.TestCase):
    def test_constructor(self):
        graph = SequenceGraph()

        self.assertEqual(graph.nr_actions(), 0)
        self.assertEqual(graph.nr_sequences(), 0)

    def test_root_node(self):
        graph = SequenceGraph()
        current = Action("current")

        graph.add_action(current)

        self.assertEqual(graph.nr_actions(), 1)
        self.assertEqual(graph.nr_sequences(), 0)
        self.assertEqual(graph.root_node, current)
        self.assertEqual(graph.nr_from_actions(current), 0)
        self.assertEqual(graph.nr_to_actions(current), 0)
