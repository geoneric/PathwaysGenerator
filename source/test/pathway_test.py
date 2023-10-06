import unittest

from adaptation_pathways.pathway import Pathway


class InterventionTest(unittest.TestCase):
    def test_constructor(self):
        pathway = Pathway()

        self.assertTrue(pathway)
