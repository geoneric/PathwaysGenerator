import unittest

from adaptation_pathways.intervention import Intervention


class InterventionTest(unittest.TestCase):
    def test_constructor(self):
        description = "Current situation"
        tipping_point = 1100
        intervention = Intervention(description, tipping_point)

        self.assertEqual(intervention.description, description)
        self.assertEqual(intervention.tipping_point, tipping_point)
