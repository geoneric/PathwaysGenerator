import unittest

from adaptation_pathways.graph import PathwayMap


class PathwayMapTest(unittest.TestCase):
    def test_constructor(self):
        graph = PathwayMap()

        self.assertEqual(graph.nr_nodes(), 0)
        self.assertEqual(graph.nr_edges(), 0)
