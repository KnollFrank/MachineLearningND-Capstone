import pandas as pd

from falldetection.fall_predicate import isFall
from falldetection.feature_extractor import FeatureExtractor
from falldetection.sensor_files_provider import SensorFilesProvider


class FeatureExtractorWorkflow:

    def __init__(self, feature_extractor):
        self.feature_extractor = feature_extractor

    def extract_features(self, sensorFiles):
        return pd.concat(self.__create_dataFrames(sensorFiles), ignore_index=True, axis='index')

    def __create_dataFrames(self, sensorFiles):
        return [self.__create_dataFrame(sensorFile) for sensorFile in sensorFiles]

    def __create_dataFrame(self, sensorFile):
        return pd.concat((self.sensorFile_and_fall_df(sensorFile), self.feature_extractor(sensorFile)), axis='columns')

    def sensorFile_and_fall_df(self, sensorFile):
        return pd.DataFrame(data={'sensorFile': [sensorFile], 'fall': isFall(sensorFile)})


def extract_features_and_save(sensor, baseDir, sensor_files_to_exclude, csv_file, autocorr_num, dft_amplitudes_num):
    sensor_files = SensorFilesProvider(baseDir, sensor, sensor_files_to_exclude).provide_sensor_files()
    feature_extractor = FeatureExtractor(autocorr_num=autocorr_num, dft_amplitudes_num=dft_amplitudes_num)
    features = FeatureExtractorWorkflow(feature_extractor.extract_features).extract_features(sensor_files)
    features.to_csv(csv_file)

# TODO: als Benchmark zusätzlich zu den im proposal definierten noch einen Schwellwert-Algorithmus z.B. für die totale Beschleunigung implementieren oder besser einen machine learning Algorithmus (z.B. SVM), der nur die totale Beschleunigung verwendet.
# TODO: PCA aus Interesse anwenden, um herauszufinden, welche Features am wichtigsten sind.
# TODO: teste neuronales Netz, das ohne die Features auskommt, sondern direkt mit den Rohdaten (Time Series) arbeitet.
