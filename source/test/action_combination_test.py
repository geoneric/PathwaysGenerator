import unittest

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination


class ActionCombinationTest(unittest.TestCase):
    def test_order_is_maintained(self):
        a = Action("a")
        b = Action("b")

        c = ActionCombination("c", [a, b])

        self.assertEqual(c.name, "c")
        self.assertEqual(c.actions, [a, b])

        c = ActionCombination("c", [b, a])

        self.assertEqual(c.name, "c")
        self.assertEqual(c.actions, [b, a])

    def test_duplicates_are_removed(self):
        a = Action("a")

        with self.assertRaises(ValueError):
            ActionCombination("b", [a, a])
