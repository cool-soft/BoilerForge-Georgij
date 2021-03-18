import datetime

import numpy as np
import pandas as pd
from dateutil.tz import gettz
import matplotlib.pyplot as plt

from heating_system.preprocess_utils import filter_by_timestamp_closed, average_values
from heating_system_utils.constants import column_names
from main import config


class LagFinder:

    def __init__(self):
        self._min_lag = 1
        self._max_lag = 20
        self._extrema_area_size = 10
        self._contact_check_radius_front = 5
        self._contact_check_radius_back = 1

    def set_min_lag(self, lag: int):
        self._min_lag = lag

    def set_max_lag(self, lag: int):
        self._max_lag = lag

    def set_extrema_area_size(self, area_size: int):
        self._extrema_area_size = area_size

    def set_contact_check_radius_front(self, radius):
        self._contact_check_radius_front = radius

    def set_contact_check_radius_back(self, radius):
        self._contact_check_radius_back = radius

    def find_lag(self, x_arr, y_arr):
        x_min_extrema_arr, x_max_extrema_arr = self._find_extrema(x_arr)
        y_min_extrema_arr, y_max_extrema_arr = self._find_extrema(y_arr)

        x_max_extrema_arr = self._filter_extrema(x_max_extrema_arr, x_arr)
        y_max_extrema_arr = self._filter_extrema(y_max_extrema_arr, y_arr)

        target_lag = None
        min_avg_contact_length = float("inf")
        max_contact_count = 0

        for lag in range(self._min_lag, self._max_lag+1):

            contact_count = 0
            contact_length_sum = 0
            for x_extrema_index in x_max_extrema_arr:
                contact_length = self._find_contact_length(x_extrema_index+lag, y_max_extrema_arr)
                if not contact_length == float("inf"):
                    contact_length_sum += contact_length
                    contact_count += 1

            if contact_count > max_contact_count:
                avg_contact_length = contact_length_sum / contact_count
                min_avg_contact_length = avg_contact_length
                max_contact_count = contact_count
                target_lag = lag

            elif contact_count > 0 and contact_count == max_contact_count:
                avg_contact_length = contact_length_sum / contact_count
                if min_avg_contact_length > avg_contact_length:
                    min_avg_contact_length = min_avg_contact_length
                    target_lag = lag

        return target_lag

    def _find_contact_length(self, x_extrema_index, y_extrema_arr):
        min_y_extrema = x_extrema_index - self._contact_check_radius_back
        max_y_extrema = x_extrema_index + self._contact_check_radius_front

        min_contact_length = float("inf")
        for y_extrema_index in y_extrema_arr:
            if min_y_extrema <= y_extrema_index <= max_y_extrema:
                contact_length = y_extrema_index - x_extrema_index
                if abs(contact_length) < abs(min_contact_length):
                    min_contact_length = contact_length

        return min_contact_length

    # noinspection PyMethodMayBeStatic
    def _find_extrema(self, arr):
        min_extrema = []
        max_extrema = []
        for i in range(1, len(arr)-1):
            if arr[i] > arr[i-1] and arr[i] > arr[i+1]:
                max_extrema.append(i)
            if arr[i] < arr[i-1] and arr[i] < arr[i+1]:
                min_extrema.append(i)
        return min_extrema, max_extrema

    def _filter_extrema(self, extrema_arr, arr, check_max=True):
        filtered_extrema_arr = []
        for extrema_index in extrema_arr:
            if self._check_extrema_index_in_area(extrema_index, arr, check_max):
                filtered_extrema_arr.append(extrema_index)
        return filtered_extrema_arr

    def _check_extrema_index_in_area(self, index_to_check, arr, check_max=True):
        start_index = max(index_to_check-self._extrema_area_size, 0)
        for i in range(start_index, index_to_check):
            if check_max and arr[i] >= arr[index_to_check]:
                return False
            if not check_max and arr[i] <= arr[index_to_check]:
                return False

        arr_len = len(arr)
        end_index = min(index_to_check+self._extrema_area_size, arr_len)
        for i in range(index_to_check+1, end_index):
            if check_max and arr[i] > arr[index_to_check]:
                return False
            if not check_max and arr[i] < arr[index_to_check]:
                return False

        return True


def main():
    start_datetime = datetime.datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    end_datetime = datetime.datetime(2019, 4, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    # home_dataset_name = "engelsa_35.csv.pickle"
    home_dataset_name = "engelsa_37.csv.pickle"
    # home_dataset_name = "gaydara_22.csv.pickle"
    min_lag = 2
    max_lag = 20

    boiler_df: pd.DataFrame = pd.read_pickle(config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH)
    boiler_df: pd.DataFrame = filter_by_timestamp_closed(boiler_df, start_datetime, end_datetime)

    home_df: pd.DataFrame = pd.read_pickle(
        f"{config.HOMES_PREPROCESSED_HEATING_CIRCUIT_DATASETS_DIR}\\{home_dataset_name}"
    )
    home_df: pd.DataFrame = filter_by_timestamp_closed(home_df, start_datetime, end_datetime)

    boiler_df_len = len(boiler_df)
    home_df_len = len(home_df)
    assert boiler_df_len == home_df_len, \
        f"DataFrames lengths is not equal (boiler_df: {boiler_df_len}; home_df: {home_df_len})"

    instance = LagFinder()
    instance.set_min_lag(min_lag)
    instance.set_max_lag(max_lag)
    instance.set_extrema_area_size(10)
    lag = instance.find_lag(
        boiler_df[column_names.FORWARD_PIPE_COOLANT_TEMP].to_numpy(),
        home_df[column_names.FORWARD_PIPE_COOLANT_TEMP].to_numpy()
    )
    print(lag)


def main2():
    instance = LagFinder()
    instance.set_extrema_area_size(3)
    arr = [1, 5, 4, 2, 1, 2, 6, 7, 1, 8, 1, 6, 5, 9]
    print(instance._find_extrema(arr))


def main3():
    start_datetime = datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    end_datetime = datetime.datetime(2019, 3, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    home_dataset_name = "engelsa_37.csv.pickle"

    min_lag = 2
    max_lag = 20

    boiler_df: pd.DataFrame = pd.read_pickle(config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH)
    boiler_df: pd.DataFrame = filter_by_timestamp_closed(boiler_df, start_datetime, end_datetime)

    home_df: pd.DataFrame = pd.read_pickle(
        f"{config.HOMES_PREPROCESSED_HEATING_CIRCUIT_DATASETS_DIR}\\{home_dataset_name}"
    )
    home_df: pd.DataFrame = filter_by_timestamp_closed(home_df, start_datetime, end_datetime)

    boiler_df_len = len(boiler_df)
    home_df_len = len(home_df)
    assert boiler_df_len == home_df_len, \
        f"DataFrames lengths is not equal (boiler_df: {boiler_df_len}; home_df: {home_df_len})"

    instance = LagFinder()
    instance.set_min_lag(min_lag)
    instance.set_max_lag(max_lag)
    instance.set_extrema_area_size(10)

    boiler_temp = boiler_df[column_names.FORWARD_PIPE_COOLANT_TEMP].to_numpy()
    home_temp = home_df[column_names.FORWARD_PIPE_COOLANT_TEMP].to_numpy()
    datetime_ = boiler_df[column_names.TIMESTAMP].to_list()

    # noinspection PyProtectedMember
    # _, boiler_max_extrema = instance._find_extrema(boiler_temp)
    # noinspection PyProtectedMember
    # _, home_max_extrema = instance._find_extrema(home_temp)

    plt.plot(datetime_, boiler_temp, label="boiler_temp")
    plt.plot(datetime_, home_temp, label="home_temp")

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
    # main2()
    # main3()
