import os

import numpy as np
import pandas as pd


def slice_with_window(df, window_center_index, half_window_size):
    lower_bound_inclusive = window_center_index - half_window_size
    upper_bound_exclusive = window_center_index + half_window_size + 1
    if not (0 <= lower_bound_inclusive < len(df) and 0 <= upper_bound_exclusive <= len(df)):
        raise IndexError()
    return df.iloc[lower_bound_inclusive:upper_bound_exclusive]


def get_index_of_maximum_total_acceleration(df):
    squared_total_acceleration = df['Acc_X'] ** 2 + df['Acc_Y'] ** 2 + df['Acc_Z'] ** 2
    return squared_total_acceleration.idxmax()


def get_window_around_maximum_total_acceleration(df, half_window_size):
    return slice_with_window(
        df,
        window_center_index=get_index_of_maximum_total_acceleration(df),
        half_window_size=half_window_size)


def extract_features(df):
    features = pd.DataFrame(
        index=['min', 'max', 'mean', 'var', 'skew', 'kurtosis'],
        columns=df.columns,
        dtype=np.float64)

    def order_by_column(series):
        return series[features.columns].values

    features.loc['min', :] = order_by_column(df.min())
    features.loc['max', :] = order_by_column(df.max())
    features.loc['mean', :] = order_by_column(df.mean())
    features.loc['var', :] = order_by_column(df.var(ddof=0))
    features.loc['skew', :] = order_by_column(df.skew())
    features.loc['kurtosis', :] = order_by_column(df.kurtosis())
    return features


def features2array(features):
    return np.concatenate(features.T.values)


def extract_all_features(baseDir, sensorFile, feature_extractor):
    def sensorFiles():
        for root, dirs, files in os.walk(baseDir):
            for file in files:
                if file == sensorFile:
                    yield os.path.join(root, file)

    def asDataFrame(sensorFiles_and_features):
        sensorFiles, features = zip(*sensorFiles_and_features)
        return pd.DataFrame({'sensorFile': sensorFiles, 'feature': features})

    sensorFiles_and_features = [(sensorFile, feature_extractor(sensorFile)) for sensorFile in sensorFiles()]
    return asDataFrame(sensorFiles_and_features)
