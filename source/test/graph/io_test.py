import unittest
from io import StringIO

from adaptation_pathways.graph.io import read_sequences


class ReadSequencesTest(unittest.TestCase):
    def test_empty(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 0)
        self.assertEqual(sequence_graph.nr_sequences(), 0)

        sequence_graph = read_sequences(
            StringIO(
                """


                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 0)
        self.assertEqual(sequence_graph.nr_sequences(), 0)

    def test_single_sequence(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                current a
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 2)
        self.assertEqual(sequence_graph.nr_sequences(), 1)

        root_node = sequence_graph.root_node
        self.assertEqual(str(root_node), "current")

        a = sequence_graph.to_nodes(root_node)[0]
        self.assertEqual(str(a), "a")

    def test_comment(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                # A comment
                current a  # A comment
                # A comment
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 2)
        self.assertEqual(sequence_graph.nr_sequences(), 1)

        root_node = sequence_graph.root_node
        self.assertEqual(str(root_node), "current")

        a = sequence_graph.to_nodes(root_node)[0]
        self.assertEqual(str(a), "a")

    def test_serial_sequence(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                current a
                a b
                b c
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 4)
        self.assertEqual(sequence_graph.nr_sequences(), 3)

        root_node = sequence_graph.root_node
        self.assertEqual(str(root_node), "current")

        a = sequence_graph.to_nodes(root_node)[0]
        self.assertEqual(str(a), "a")

        b = sequence_graph.to_nodes(a)[0]
        self.assertEqual(str(b), "b")

        c = sequence_graph.to_nodes(b)[0]
        self.assertEqual(str(c), "c")

    def test_diverging_sequence(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                current a
                current b
                current c
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 4)
        self.assertEqual(sequence_graph.nr_sequences(), 3)

        root_node = sequence_graph.root_node
        self.assertEqual(str(root_node), "current")

        a = sequence_graph.to_nodes(root_node)[0]
        self.assertEqual(str(a), "a")

        b = sequence_graph.to_nodes(root_node)[1]
        self.assertEqual(str(b), "b")

        c = sequence_graph.to_nodes(root_node)[2]
        self.assertEqual(str(c), "c")

    def test_converging_sequence(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                current a
                current b
                current c
                a d
                b d
                c d
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 5)
        self.assertEqual(sequence_graph.nr_sequences(), 6)

        root_node = sequence_graph.root_node
        self.assertEqual(str(root_node), "current")

        a = sequence_graph.to_nodes(root_node)[0]
        self.assertEqual(str(a), "a")

        b = sequence_graph.to_nodes(root_node)[1]
        self.assertEqual(str(b), "b")

        c = sequence_graph.to_nodes(root_node)[2]
        self.assertEqual(str(c), "c")

        d = sequence_graph.to_nodes(a)[0]
        self.assertEqual(str(d), "d")

        d = sequence_graph.to_nodes(b)[0]
        self.assertEqual(str(d), "d")

        d = sequence_graph.to_nodes(c)[0]
        self.assertEqual(str(d), "d")

    def test_use_case_01(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                current a
                a e
                current b
                b f
                current c
                c f
                current d
                d f
                f e
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 7)
        self.assertEqual(sequence_graph.nr_sequences(), 9)

        root_node = sequence_graph.root_node
        self.assertEqual(str(root_node), "current")

        a = sequence_graph.to_nodes(root_node)[0]
        self.assertEqual(str(a), "a")

        b = sequence_graph.to_nodes(root_node)[1]
        self.assertEqual(str(b), "b")

        c = sequence_graph.to_nodes(root_node)[2]
        self.assertEqual(str(c), "c")

        d = sequence_graph.to_nodes(root_node)[3]
        self.assertEqual(str(d), "d")

        e = sequence_graph.to_nodes(a)[0]
        self.assertEqual(str(e), "e")

        f = sequence_graph.to_nodes(b)[0]
        self.assertEqual(str(f), "f")

        f = sequence_graph.to_nodes(c)[0]
        self.assertEqual(str(f), "f")

        f = sequence_graph.to_nodes(d)[0]
        self.assertEqual(str(f), "f")

        e = sequence_graph.to_nodes(f)[0]
        self.assertEqual(str(e), "e")

    def test_error(self):
        with self.assertRaises(ValueError):
            read_sequences(
                StringIO(
                    """
                    current
                    """
                )
            )
        with self.assertRaises(ValueError):
            read_sequences(
                StringIO(
                    """
                    current a b
                    """
                )
            )

    def test_action_combination(self):
        sequence_graph = read_sequences(
            StringIO(
                """
                current a
                current b
                a       c(a & b)  # c is a combination of a and c
                b       c         # This is the same action combination c
                """
            )
        )

        self.assertEqual(sequence_graph.nr_actions(), 4)
        self.assertEqual(sequence_graph.nr_sequences(), 4)

        root_node = sequence_graph.root_node
        self.assertEqual(str(root_node), "current")

        a = sequence_graph.to_nodes(root_node)[0]
        self.assertEqual(str(a), "a")

        b = sequence_graph.to_nodes(root_node)[1]
        self.assertEqual(str(b), "b")

        c = sequence_graph.to_nodes(a)[0]
        self.assertEqual(str(c), "c")
        self.assertEqual(c.actions[0], a)
        self.assertEqual(c.actions[1], b)

        c = sequence_graph.to_nodes(b)[0]
        self.assertEqual(str(c), "c")
        self.assertEqual(c.actions[0], a)
        self.assertEqual(c.actions[1], b)

    def test_action_combination_different_order(self):
        with self.assertRaises(ValueError):
            read_sequences(
                StringIO(
                    """
                    current a
                    current b
                    b       c         # c is a normal action
                    a       c(a & b)  # c is a combination of a and b ...
                    """
                )
            )


class ReadTippingPointsTest(unittest.TestCase):
    pass
