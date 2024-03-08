import unittest

import adaptation_pathways as ap


class PackageTest(unittest.TestCase):
    def test_version_attribute(self):
        self.assertTrue(hasattr(ap, "__version__"))
        self.assertTrue(isinstance(ap.__version__, str))
