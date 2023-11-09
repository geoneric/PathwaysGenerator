import unittest

from adaptation_pathways.action import Action


class InterventionTest(unittest.TestCase):
    def test_constructor(self):
        description = "Current situation"
        tipping_point = 1100
        action = Action(description, tipping_point)

        self.assertEqual(action.description, description)
        self.assertEqual(action.tipping_point, tipping_point)
