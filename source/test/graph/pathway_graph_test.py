import unittest

from adaptation_pathways.graph.node import Action
from adaptation_pathways.graph.pathway_graph import PathwayGraph


class PathwayGraphTest(unittest.TestCase):
    def test_constructor(self):
        graph = PathwayGraph()

        self.assertEqual(graph.nr_nodes(), 0)

    def test_single_period(self):
        graph = PathwayGraph()
        current = Action("current")
        a = Action("a")

        graph.add_conversion(current, a)

        self.assertEqual(graph.nr_nodes(), 3)
