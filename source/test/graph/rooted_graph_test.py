import unittest

from adaptation_pathways.graph.rooted_graph import RootedGraph


class RootedGraphTest(unittest.TestCase):
    def test_constructor(self):
        graph = RootedGraph()

        self.assertEqual(graph.nr_nodes(), 0)
        self.assertEqual(graph.nr_edges(), 0)
