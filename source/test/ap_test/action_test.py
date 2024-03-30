import unittest

from adaptation_pathways.action import Action


class ActionTest(unittest.TestCase):
    def test_constructor_01(self):
        name = "Current situation"
        action = Action(name)

        self.assertEqual(action.name, name)
