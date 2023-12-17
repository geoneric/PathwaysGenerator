import unittest

import numpy.testing as npt

from adaptation_pathways import Action
from adaptation_pathways.graph import (
    SequenceGraph,
    pathway_graph_layout,
    sequence_graph_to_pathway_graph,
)


class PathwayGraphLayoutTest(unittest.TestCase):
    def test_empty(self):
        sequence_graph = SequenceGraph()
        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        positions = pathway_graph_layout(pathway_graph)

        self.assertEqual(len(positions), 0)

    def test_single_period(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")

        sequence_graph.add_sequence(current, a)

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        positions = pathway_graph_layout(pathway_graph)

        self.assertEqual(len(positions), 3)
        # self.assertTrue(all(action in positions for action in actions))
        # npt.assert_almost_equal(positions[current], (0, 0))

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current")], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current | a")], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("a")], (2, 0)
        )
