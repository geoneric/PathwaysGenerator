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

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current")], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current | a")], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("a")], (2, 0)
        )

    def test_serial_pathway(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(a, b)
        sequence_graph.add_sequence(b, c)

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        positions = pathway_graph_layout(pathway_graph)

        self.assertEqual(len(positions), 7)

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current")], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current | a")], (1, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("a")], (2, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("a | b")], (3, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("b")], (4, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("b | c")], (5, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("c")], (6, 0)
        )

    def test_diverging_pathways(self):
        sequence_graph = SequenceGraph()
        current = Action("current")
        a = Action("a")
        b = Action("b")
        c = Action("c")

        sequence_graph.add_sequence(current, a)
        sequence_graph.add_sequence(current, b)
        sequence_graph.add_sequence(current, c)

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        positions = pathway_graph_layout(pathway_graph)

        self.assertEqual(len(positions), 7)

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current")], (0, 0)
        )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("current | a")], (1, 1)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("a")], (2, 1)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("current | b")], (1, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("b")], (2, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("current | c")], (1, -1)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("c")], (2, -1)
        # )

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

        pathway_graph = sequence_graph_to_pathway_graph(sequence_graph)
        positions = pathway_graph_layout(pathway_graph)

        self.assertEqual(len(positions), 16)

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current")], (0, 0)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current | a")], (1, 1.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("a")], (2, 1.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("a | e")], (3, 1.5)
        )

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current | b")], (1, 0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("b")], (2, 0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("b | f")], (3, 0.5)
        )

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current | c")], (1, -0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("c")], (2, -0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("c | f")], (3, -0.5)
        )

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("current | d")], (1, -1.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("d")], (2, -1.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("d | f")], (3, -1.5)
        )

        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("f")], (4, -0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("f | e")], (5, -0.5)
        )
        npt.assert_almost_equal(
            positions[pathway_graph.conversion_by_name("e")], (6, 0.5)
        )

        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("current | b")], (1, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("b")], (2, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("current | c")], (1, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("c")], (2, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("current | d")], (1, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("d")], (2, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("b | f")], (3, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("c | f")], (3, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("d | f")], (3, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("f")], (4, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("f | e")], (5, 0)
        # )
        # npt.assert_almost_equal(
        #     positions[pathway_graph.conversion_by_name("e")], (6, 0)
        # )
