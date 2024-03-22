import unittest
from io import StringIO

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination
from adaptation_pathways.io import text
from adaptation_pathways.plot.colour import hex_to_rgba


class TextTest(unittest.TestCase):
    def test_empty_actions(self):
        strings = [
            """
            """,
            """
            # empty...
            """,
            """

            """,
        ]

        for string in strings:
            actions, colour_by_action = text.read_actions(
                StringIO(
                    f"""
                    {string}
                    """
                )
            )
            self.assertEqual(len(actions), 0)
            self.assertEqual(len(colour_by_action), 0)

    def test_single_action(self):
        actions, colour_by_action = text.read_actions(
            StringIO(
                """
                current
                """
            )
        )
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "current")
        self.assertEqual(len(colour_by_action), 0)

        actions, colour_by_action = text.read_actions(
            StringIO(
                """
                current #12345678
                """
            )
        )
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "current")
        self.assertEqual(len(colour_by_action), 1)
        self.assertTrue(actions[0] in colour_by_action)
        self.assertEqual(colour_by_action[actions[0]], hex_to_rgba("#12345678"))

        self.assertRaises(
            ValueError,
            text.read_actions,
            StringIO(
                """
                current
                current
                """
            ),
        )

    def test_comment(self):
        actions, colour_by_action = text.read_actions(
            StringIO(
                """
                # A comment
                current  # A comment
                # A comment
                """
            )
        )
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].name, "current")
        self.assertEqual(len(colour_by_action), 0)

    def test_action_combination(self):
        actions, colour_by_action = text.read_actions(
            StringIO(
                """
                a #12345678
                b #87654321
                c(a&b) #24688642
                """
            )
        )
        self.assertEqual(len(actions), 3)
        self.assertEqual(actions[0].name, "a")
        self.assertEqual(actions[1].name, "b")
        self.assertEqual(actions[2].name, "c")
        self.assertEqual(len(colour_by_action), 3)
        self.assertEqual(colour_by_action[actions[0]], hex_to_rgba("#12345678"))
        self.assertEqual(colour_by_action[actions[1]], hex_to_rgba("#87654321"))
        self.assertEqual(colour_by_action[actions[2]], hex_to_rgba("#24688642"))
        self.assertTrue(isinstance(actions[0], Action))
        self.assertTrue(isinstance(actions[1], Action))
        self.assertTrue(isinstance(actions[2], ActionCombination))
        self.assertEqual(actions[2].actions[0].name, "a")
        self.assertEqual(actions[2].actions[1].name, "b")

        # Order matters, actions to combine must be defined first
        self.assertRaises(
            ValueError,
            text.read_actions,
            StringIO(
                """
                c(a&b)
                a
                b
                """
            ),
        )

    def test_empty_sequences(self):
        strings = [
            """
            """,
            """
            # empty...
            """,
            """

            """,
        ]

        for string in strings:
            sequences, tipping_point_by_action = text.read_sequences(
                StringIO(
                    f"""
                    {string}
                    """
                )
            )
            self.assertEqual(len(sequences), 0)
            self.assertEqual(len(tipping_point_by_action), len(sequences))

    def test_single_sequence(self):
        strings = [
            """
            current a
            """,
            """
            current a 0
            """,
            """
            # One sequence coming up
            current a  # This is the one
            # That was the one
            """,
            """
            # One sequence coming up
            current a 0  # This is the one
            # That was the one
            """,
        ]

        for string in strings:
            sequences, tipping_point_by_action = text.read_sequences(
                StringIO(
                    f"""
                    {string}
                    """
                )
            )
            self.assertEqual(len(sequences), 1)
            self.assertEqual(sequences[0][0].name, "current")
            self.assertEqual(sequences[0][1].name, "a")

            self.assertEqual(len(tipping_point_by_action), len(sequences))
            self.assertTrue(
                all(sequence[1] in tipping_point_by_action for sequence in sequences)
            )
            self.assertEqual(tipping_point_by_action[sequences[0][1]], 0)

    def test_multiple_sequences(self):
        strings = [
            """
            current a
            a b
            b c
            """,
            """
            current a 0
            a b 0
            b c 0
            """,
        ]

        for string in strings:
            sequences, tipping_point_by_action = text.read_sequences(
                StringIO(
                    f"""
                    {string}
                    """
                )
            )
            self.assertEqual(len(sequences), 3)
            self.assertEqual(sequences[0][0].name, "current")
            self.assertEqual(sequences[0][1].name, "a")
            self.assertEqual(sequences[1][0].name, "a")
            self.assertEqual(sequences[1][1].name, "b")
            self.assertEqual(sequences[2][0].name, "b")
            self.assertEqual(sequences[2][1].name, "c")

            self.assertEqual(sequences[0][1], sequences[1][0])
            self.assertEqual(sequences[1][1], sequences[2][0])

            self.assertEqual(len(tipping_point_by_action), len(sequences))
            self.assertTrue(
                all(sequence[1] in tipping_point_by_action for sequence in sequences)
            )
            self.assertEqual(tipping_point_by_action[sequences[0][1]], 0)
            self.assertEqual(tipping_point_by_action[sequences[1][1]], 0)
            self.assertEqual(tipping_point_by_action[sequences[2][1]], 0)

    def test_multiple_editions(self):
        strings = [
            """
            current a[1]
            current a[2]
            """,
            """
            current a[1] 0
            current a[2] 0
            """,
        ]

        for string in strings:
            sequences, tipping_point_by_action = text.read_sequences(
                StringIO(
                    f"""
                    {string}
                    """
                )
            )
            self.assertEqual(len(sequences), 2)
            self.assertEqual(sequences[0][0].name, "current")
            self.assertEqual(sequences[0][1].name, "a")
            self.assertEqual(sequences[1][0].name, "current")
            self.assertEqual(sequences[1][1].name, "a")

            self.assertEqual(sequences[0][0], sequences[1][0])
            self.assertNotEqual(sequences[0][1], sequences[1][1])

            self.assertEqual(len(tipping_point_by_action), len(sequences))
            self.assertTrue(
                all(sequence[1] in tipping_point_by_action for sequence in sequences)
            )
            self.assertEqual(tipping_point_by_action[sequences[0][1]], 0)
            self.assertEqual(tipping_point_by_action[sequences[1][1]], 0)

    def test_multiple_tipping_points(self):
        sequences, tipping_point_by_action = text.read_sequences(
            StringIO(
                """
                current[1] current 2020
                current a[5] 2030
                a[5] b 2040
                b c 2050
                """
            )
        )

        self.assertEqual(len(sequences), 4)
        self.assertEqual(sequences[0][0].name, "current")
        self.assertEqual(sequences[0][1].name, "current")
        self.assertEqual(sequences[1][0].name, "current")
        self.assertEqual(sequences[1][1].name, "a")
        self.assertEqual(sequences[2][0].name, "a")
        self.assertEqual(sequences[2][1].name, "b")
        self.assertEqual(sequences[3][0].name, "b")
        self.assertEqual(sequences[3][1].name, "c")

        self.assertNotEqual(sequences[0][0], sequences[0][1])
        self.assertEqual(sequences[0][1], sequences[1][0])
        self.assertEqual(sequences[1][1], sequences[2][0])
        self.assertEqual(sequences[2][1], sequences[3][0])

        self.assertEqual(len(tipping_point_by_action), len(sequences))
        self.assertTrue(
            all(sequence[1] in tipping_point_by_action for sequence in sequences)
        )
        self.assertEqual(tipping_point_by_action[sequences[0][1]], 2020)
        self.assertEqual(tipping_point_by_action[sequences[1][1]], 2030)
        self.assertEqual(tipping_point_by_action[sequences[2][1]], 2040)
        self.assertEqual(tipping_point_by_action[sequences[3][1]], 2050)
