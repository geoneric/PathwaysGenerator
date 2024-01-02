import unittest

from adaptation_pathways.graph.node import Action
from adaptation_pathways.graph.pathway_graph import PathwayGraph


class PathwayGraphTest(unittest.TestCase):
    def test_constructor(self):
        graph = PathwayGraph()

        self.assertEqual(graph.nr_conversions(), 0)

    def test_single_period(self):
        graph = PathwayGraph()
        current = Action("current")
        a = Action("a")

        graph.set_pathway(current, a)

        self.assertEqual(graph.nr_conversions(), 2)
