from unittest import TestCase

import pandas as pd

from falldetection.feature_extraction import *


class FeatureExtractionTestCase(TestCase):

    def test_slice_with_window1(self):
        df = pd.DataFrame({'Acc_X': [1.0, 2.0, 3.0, 4.0, 5.0]})
        df_sliced = slice_with_window(df, window_center_index=2, half_window_size=2)
        self.assertTrue(df.equals(df_sliced))

    def test_slice_with_window2(self):
        df = pd.DataFrame({'Acc_X': [1.0, 2.0, 3.0, 4.0, 5.0]})
        df_sliced_actual = slice_with_window(df, window_center_index=2, half_window_size=1)
        df_sliced_expected = pd.DataFrame({'Acc_X': [2.0, 3.0, 4.0]}, index=[1, 2, 3])
        self.assertTrue(df_sliced_expected.equals(df_sliced_actual))

    def test_slice_with_window3(self):
        df = pd.DataFrame({'Acc_X': [1.0, 2.0, 3.0, 4.0, 5.0]})
        with self.assertRaises(IndexError):
            slice_with_window(df, window_center_index=2, half_window_size=3)

    def test_get_index_of_maximum_total_acceleration1(self):
        df = pd.DataFrame(
            {'Acc_X': [1.0, 2.0, 30.0, 4.0, 5.0],
             'Acc_Y': [1.0, 2.0, 40.0, 4.0, 5.0],
             'Acc_Z': [1.0, 2.0, 50.0, 4.0, 5.0]})
        index = get_index_of_maximum_total_acceleration(df)
        self.assertEquals(index, 2)

    def test_get_index_of_maximum_total_acceleration2(self):
        df = pd.DataFrame(
            {'Acc_X': [1.0, 20.0, 3.0, 4.0, 5.0],
             'Acc_Y': [1.0, 30.0, 4.0, 4.0, 5.0],
             'Acc_Z': [1.0, 40.0, 5.0, 4.0, 5.0]},
            index=list('abcde'))
        index = get_index_of_maximum_total_acceleration(df)
        self.assertEquals(index, 'b')

    def test_get_window_around_maximum_total_acceleration(self):
        df = pd.DataFrame(
            {'Acc_X': [1.0, 20.0, 3.0, 4.0, 5.0],
             'Acc_Y': [1.0, 30.0, 4.0, 4.0, 5.0],
             'Acc_Z': [1.0, 40.0, 5.0, 4.0, 5.0]})
        df_sliced_actual = get_window_around_maximum_total_acceleration(df, half_window_size=1)
        df_sliced_expected = pd.DataFrame(
            {'Acc_X': [1.0, 20.0, 3.0],
             'Acc_Y': [1.0, 30.0, 4.0],
             'Acc_Z': [1.0, 40.0, 5.0]})
        self.assertTrue(df_sliced_expected.equals(df_sliced_actual))
