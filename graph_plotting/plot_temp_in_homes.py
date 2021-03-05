import datetime
import os

import matplotlib.pyplot as plt
from dateutil.tz import gettz
from pandas.plotting import register_matplotlib_converters

from heating_system import column_names
import config
from heating_system.dataset_utils.dataset_io import load_dataset
from heating_system.preprocess_utils import average_values, filter_by_timestamp_closed
from heating_system.weather_dataset_utils.weather_dataset_io import load_weather_dataset

if __name__ == '__main__':
    start_datetime = datetime.datetime(2019, 2, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    end_datetime = datetime.datetime(2019, 3, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))

    homes_in_temp_smooth_size = 100
    boiler_temp_smooth_size = 100

    # noinspection SpellCheckingInspection
    allowed_homes = [
        "engelsa_35.csv.pickle",
        "engelsa_37.csv.pickle",
        "gaydara_1.csv.pickle",
        # "gaydara_22.csv.pickle",
        # "gaydara_26.csv.pickle",
        # "gaydara_28.csv.pickle",
        # "gaydara_30.csv.pickle",
        "gaydara_32.csv.pickle",
        # "kuibysheva_10.csv.pickle",
        # "kuibysheva_14.csv.pickle",
        "kuibysheva_16.csv.pickle",
        "kuibysheva_8.csv.pickle",
    ]

    register_matplotlib_converters()
    ax = plt.axes()

    boiler_df = load_dataset(config.BOILER_PREPROCESSED_DATASET_PATH)
    boiler_df = filter_by_timestamp_closed(boiler_df, start_datetime, end_datetime)
    boiler_temp = boiler_df[column_names.FORWARD_PIPE_TEMP]
    boiler_temp = average_values(boiler_temp, boiler_temp_smooth_size)
    ax.plot(boiler_df[column_names.TIMESTAMP], boiler_temp, label="real boiler temp")

    weather_df = load_weather_dataset(config.WEATHER_PREPROCESSED_DATASET_PATH)
    weather_df = filter_by_timestamp_closed(weather_df, start_datetime, end_datetime)
    ax.plot(weather_df[column_names.TIMESTAMP], weather_df[column_names.WEATHER_TEMP], label="weather temp")

    for home_dataset_name in os.listdir(config.HOMES_PREPROCESSED_DATASETS_DIR):
        if home_dataset_name in allowed_homes:
            home_df = load_dataset(f"{config.HOMES_PREPROCESSED_DATASETS_DIR}\\{home_dataset_name}")
            home_df = filter_by_timestamp_closed(home_df, start_datetime, end_datetime)
            home_in_temp = home_df[column_names.FORWARD_PIPE_TEMP]
            home_in_temp = average_values(home_in_temp, homes_in_temp_smooth_size)
            ax.plot(home_df[column_names.TIMESTAMP], home_in_temp, label=home_dataset_name)

    ax.grid(True)
    ax.legend()
    plt.show()
