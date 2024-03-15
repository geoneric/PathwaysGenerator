import unittest
from io import StringIO

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination
from adaptation_pathways.io import text


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
        self.assertEqual(colour_by_action[actions[0]], "#12345678")

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
        self.assertEqual(colour_by_action[actions[0]], "#12345678")
        self.assertEqual(colour_by_action[actions[1]], "#87654321")
        self.assertEqual(colour_by_action[actions[2]], "#24688642")
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
            sequences, action_by_name_and_edition = text.read_sequences(
                StringIO(
                    f"""
                    {string}
                    """
                )
            )
            self.assertEqual(len(sequences), 0)
            self.assertEqual(len(action_by_name_and_edition), 0)

    def test_single_sequence(self):
        strings = [
            """
            current a
            """,
            """
            # One sequence coming up
            current a  # This is the one
            # That was the one
            """,
        ]

        for string in strings:
            sequences, action_by_name_and_edition = text.read_sequences(
                StringIO(
                    f"""
                    {string}
                    """
                )
            )
            self.assertEqual(len(sequences), 1)
            self.assertEqual(sequences[0][0].name, "current")
            self.assertEqual(sequences[0][1].name, "a")
            self.assertEqual(len(action_by_name_and_edition), 2)
            self.assertTrue(("current", 0) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("current", 0)].name, "current")
            self.assertTrue(("a", 0) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("a", 0)].name, "a")

    def test_multiple_sequences(self):
        strings = [
            """
            current a
            a b
            b c
            """,
        ]

        for string in strings:
            sequences, action_by_name_and_edition = text.read_sequences(
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

            self.assertEqual(len(action_by_name_and_edition), 4)
            self.assertTrue(("current", 0) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("current", 0)].name, "current")
            self.assertTrue(("a", 0) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("a", 0)].name, "a")
            self.assertTrue(("b", 0) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("b", 0)].name, "b")
            self.assertTrue(("c", 0) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("c", 0)].name, "c")

    def test_multiple_editions(self):
        strings = [
            """
            current a[1]
            current a[2]
            """,
        ]

        for string in strings:
            sequences, action_by_name_and_edition = text.read_sequences(
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

            self.assertEqual(len(action_by_name_and_edition), 3)
            self.assertTrue(("current", 0) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("current", 0)].name, "current")
            self.assertTrue(("a", 1) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("a", 1)].name, "a")
            self.assertTrue(("a", 2) in action_by_name_and_edition)
            self.assertEqual(action_by_name_and_edition[("a", 2)].name, "a")

    def test_empty_tipping_points(self):
        strings = [
            """
            """,
            """
            # empty...
            """,
            """

            """,
        ]

        action_by_name_and_edition: dict[tuple[str, int], Action] = {}

        for string in strings:
            tipping_points = text.read_tipping_points(
                StringIO(
                    f"""
                    {string}
                    """
                ),
                action_by_name_and_edition,
            )
            self.assertEqual(len(tipping_points), 0)

    def test_multiple_tipping_points(self):
        _, action_by_name_and_edition = text.read_sequences(
            StringIO(
                """
                current a[5]
                a[5] b
                b c
                """
            )
        )
        tipping_point_strings = [
            """
            current 2020
            a[5] 2030
            b 2040
            c 2050
            """,
        ]

        for string in tipping_point_strings:
            tipping_point_by_action = text.read_tipping_points(
                StringIO(
                    f"""
                    {string}
                    """
                ),
                action_by_name_and_edition,
            )
            self.assertEqual(len(tipping_point_by_action), 4)

            for name, tipping_point_we_want in [
                ("current", 2020),
                ("a", 2030),
                ("b", 2040),
                ("c", 2050),
            ]:
                _, tipping_point_we_got = next(
                    (action, tipping_point)
                    for action, tipping_point in tipping_point_by_action.items()
                    if action.name == name
                )
                self.assertEqual(tipping_point_we_got, tipping_point_we_want)

    def test_tipping_point_unknown_action(self):
        _, action_by_name_and_edition = text.read_sequences(
            StringIO(
                """
                current a[5]
                a[5] b
                b c
                """
            )
        )
        tipping_point_strings = [
            """
            current 2020
            a[4] 2030  # Unknown edition
            b 2040
            c 2050
            """,
            """
            current 2020
            æ[5] 2030  # Unknown name
            b 2040
            c 2050
            """,
        ]

        for string in tipping_point_strings:
            self.assertRaises(
                ValueError,
                text.read_tipping_points,
                StringIO(
                    f"""
                    {string}
                    """
                ),
                action_by_name_and_edition,
            )
