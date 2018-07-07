import unittest as unittest
from unittest import TestCase

import pandas as pd

from falldetection.feature_extractor_workflow import FeatureExtractorWorkflow, extract_features_and_save
from falldetection.sensor import Sensor
from falldetection.sensor_files_provider import SensorFilesProvider
from falldetection.tests.test_feature_extractor import set_display_options


class FeatureExtractionTestCase(TestCase):

    def test_extract_features1(self):
        # build
        feature_extractor = FeatureExtractorWorkflow(lambda sensorFile: {
            '../../data/FallDataSet-Test/209/Testler Export/914/Test_1/340535.txt': pd.DataFrame(data=[[1.0, 1.1]],
                                                                                                 columns=['feature_0',
                                                                                                          'feature_1']),
            '../../data/FallDataSet-Test/209/Testler Export/914/Test_6/340535.txt': pd.DataFrame(data=[[2.0, 2.2]],
                                                                                                 columns=['feature_0',
                                                                                                          'feature_1']),
            '../../data/FallDataSet-Test/209/Testler Export/801/Test_1/340535.txt': pd.DataFrame(data=[[3.0, 3.3]],
                                                                                                 columns=['feature_0',
                                                                                                          'feature_1']),
            '../../data/FallDataSet-Test/209/Testler Export/801/Test_2/340535.txt': pd.DataFrame(data=[[4.0, 4.4]],
                                                                                                 columns=['feature_0',
                                                                                                          'feature_1']),
            '../../data/FallDataSet-Test/101/Testler Export/801/Test_1/340535.txt': pd.DataFrame(data=[[5.0, 5.5]],
                                                                                                 columns=['feature_0',
                                                                                                          'feature_1']),
            '../../data/FallDataSet-Test/101/Testler Export/801/Test_2/340535.txt': pd.DataFrame(data=[[6.0, 6.6]],
                                                                                                 columns=['feature_0',
                                                                                                          'feature_1']),
            '../../data/FallDataSet-Test/101/Testler Export/920/Test_1/340535.txt': pd.DataFrame(data=[[7.0, 7.7]],
                                                                                                 columns=['feature_0',
                                                                                                          'feature_1'])}[
            sensorFile])

        sensor_files = SensorFilesProvider(baseDir='../../data/FallDataSet-Test',
                                           sensor=Sensor.WAIST).provide_sensor_files()
        features_expected = pd.DataFrame(
            {'sensorFile': [
                '../../data/FallDataSet-Test/209/Testler Export/914/Test_1/340535.txt',
                '../../data/FallDataSet-Test/209/Testler Export/914/Test_6/340535.txt',
                '../../data/FallDataSet-Test/209/Testler Export/801/Test_1/340535.txt',
                '../../data/FallDataSet-Test/209/Testler Export/801/Test_2/340535.txt',
                '../../data/FallDataSet-Test/101/Testler Export/801/Test_1/340535.txt',
                '../../data/FallDataSet-Test/101/Testler Export/801/Test_2/340535.txt',
                '../../data/FallDataSet-Test/101/Testler Export/920/Test_1/340535.txt'],
                'fall': [True, True, False, False, False, False, True],
                'feature_0': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
                'feature_1': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
            })

        # execute
        features_actual = feature_extractor.extract_features(sensor_files)

        # test
        set_display_options()
        print('features_expected:\n', features_expected)
        print('features_actual:\n', features_actual)
        self.assertTrue(features_expected.equals(features_actual))


    @unittest.SkipTest
    def test_extract_features_and_save_WAIST(self):
        extract_features_and_save(
            sensor=Sensor.WAIST,
            baseDir='../../data/FallDataSet',
            sensor_files_to_exclude=['209/Testler Export/919/Test_5/340535.txt',
                                     '203/Testler Export/813/Test_1/340535.txt',
                                     '207/Testler Export/917/Test_1/340535.txt',
                                     '109/Testler Export/901/Test_6/340535.txt',
                                     '208/Testler Export/917/Test_5/340535.txt',
                                     '103/Testler Export/917/Test_5/340535.txt',
                                     '103/Testler Export/917/Test_4/340535.txt',
                                     '205/Testler Export/917/Test_5/340535.txt',
                                     '107/Testler Export/917/Test_3/340535.txt'],
            csv_file='../../data/features_waist.csv',
            autocorr_num=11,
            dft_amplitudes_num=5)

    @unittest.SkipTest
    def test_extract_features_and_save_RIGHT_THIGH(self):
        extract_features_and_save(
            sensor=Sensor.RIGHT_THIGH,
            baseDir='../../data/FallDataSet',
            sensor_files_to_exclude=['208/Testler Export/805/Test_1/340539.txt',
                                     '203/Testler Export/813/Test_1/340539.txt',
                                     '103/Testler Export/911/Test_5/340539.txt',
                                     '109/Testler Export/901/Test_6/340539.txt',
                                     '108/Testler Export/918/Test_5/340539.txt',
                                     '208/Testler Export/904/Test_6/340539.txt',
                                     '207/Testler Export/904/Test_4/340539.txt'],
            csv_file='../../data/features_right_thigh.csv',
            autocorr_num=11,
            dft_amplitudes_num=5)
