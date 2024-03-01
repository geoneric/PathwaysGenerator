import unittest

from adaptation_pathways.action import Action


class ActionTest(unittest.TestCase):
    def test_constructor_01(self):
        name = "Current situation"
        action = Action(name)

        self.assertEqual(action.name, name)
        self.assertEqual(action.edition, 0)

    def test_constructor_02(self):
        name = "Current situation"
        edition = 5
        action = Action(name, edition)

        self.assertEqual(action.name, name)
        self.assertEqual(action.edition, edition)
