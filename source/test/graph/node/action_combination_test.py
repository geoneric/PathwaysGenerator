import unittest

from adaptation_pathways.graph.node import Action, ActionCombination


class ActionCombinationTest(unittest.TestCase):
    def test_order_is_maintained(self):
        a = Action("a")
        b = Action("b")

        c = ActionCombination("c", a, b)

        self.assertEqual(str(c), "c")
        self.assertEqual(c.actions, [a, b])

        c = ActionCombination("c", b, a)

        self.assertEqual(str(c), "c")
        self.assertEqual(c.actions, [b, a])

    def test_duplicates_are_removed(self):
        a = Action("a")

        with self.assertRaises(ValueError):
            ActionCombination("b", a, a)
