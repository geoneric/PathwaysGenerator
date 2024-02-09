import unittest

import numpy.testing as npt

from adaptation_pathways.plot.util import distribute


class LayoutTest(unittest.TestCase):
    def test_distribute_01(self):
        values = []
        min_distance = 0.1
        distributed_values = distribute(values, min_distance)

        npt.assert_equal(distributed_values, values)

    # TODO
    # def test_distribute_02(self):
    #     values = [0.0]
    #     min_distance = 0.0
    #     distributed_values = distribute(values, min_distance)

    #     npt.assert_equal(distributed_values, values)

    # TODO
    # def test_distribute_03(self):
    #     values = [0.0, 1.0]
    #     min_distance = 0.0
    #     distributed_values = distribute(values, min_distance)

    #     npt.assert_equal(distributed_values, values)

    def test_distribute_04(self):
        values = [0.0, 1.0]
        min_distance = 1.0
        distributed_values = distribute(values, min_distance)

        npt.assert_equal(distributed_values, values)

    def test_distribute_05(self):
        values = [0.0, 1.0]
        min_distance = 2.0
        distributed_values = distribute(values, min_distance)

        npt.assert_almost_equal(distributed_values, [-0.5, 1.5])

    def test_distribute_06(self):
        values = [10.0, 12.0, 14.0]
        min_distance = 3.0
        distributed_values = distribute(values, min_distance)

        npt.assert_almost_equal(distributed_values, [9.0, 12.0, 15.0])

    def test_distribute_07(self):
        values = [14.0, 12.0, 10.0]
        min_distance = 3.0
        distributed_values = distribute(values, min_distance)

        npt.assert_almost_equal(distributed_values, [15.0, 12.0, 9.0])

    def test_distribute_08(self):
        values = [0.0, 0.0, 0.0]
        min_distance = 3.0
        distributed_values = distribute(values, min_distance)

        npt.assert_almost_equal(distributed_values, [3.0, 0.0, -3.0])
