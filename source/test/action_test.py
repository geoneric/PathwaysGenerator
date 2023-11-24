import unittest

from adaptation_pathways.action import Action


class ActionTest(unittest.TestCase):
    def test_constructor(self):
        label = "Current situation"
        action = Action(label)

        self.assertEqual(action.label, label)
