import datetime

import numpy as np
import pandas as pd
from dateutil.tz import gettz

from heating_system.preprocess_utils import filter_by_timestamp_closed, average_values
from heating_system_utils.constants import column_names
from main import config


def main():
    start_datetime = datetime.datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    end_datetime = datetime.datetime(2019, 3, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    home_dataset_name = "engelsa_37.csv.pickle"
    min_lag = 1
    max_lag = 20

    boiler_df: pd.DataFrame = pd.read_pickle(config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH)
    boiler_df: pd.DataFrame = filter_by_timestamp_closed(boiler_df, start_datetime, end_datetime)

    home_df: pd.DataFrame = pd.read_pickle(f"{config.HOMES_PREPROCESSED_HEATING_CIRCUIT_DATASETS_DIR}\\{home_dataset_name}")
    home_df: pd.DataFrame = filter_by_timestamp_closed(home_df, start_datetime, end_datetime)

    boiler_df_len = len(boiler_df)
    home_df_len = len(home_df)

    assert boiler_df_len == home_df_len, \
        f"DataFrames lengths is not equal (boiler_df: {boiler_df_len}; home_df: {home_df_len})"

    boiler_forward_pipe_temp = boiler_df[column_names.FORWARD_PIPE_COOLANT_TEMP]
    boiler_forward_pipe_temp = boiler_forward_pipe_temp.iloc[1:]
    home_forward_pipe_temp = home_df[column_names.FORWARD_PIPE_COOLANT_TEMP]
    home_forward_pipe_temp = home_forward_pipe_temp.iloc[1:]

    for lag in range(min_lag, max_lag):
        boiler_forward_pipe_temp_shifted: pd.Series = boiler_forward_pipe_temp.iloc[lag:].to_numpy()
        average_values(boiler_forward_pipe_temp_shifted, 100)
        home_forward_pipe_temp_cut: pd.Series = home_forward_pipe_temp.iloc[:-lag].to_numpy()
        average_values(home_forward_pipe_temp_cut, 100)

        delta = boiler_forward_pipe_temp_shifted - home_forward_pipe_temp_cut
        print(f"Lag: {lag:3}, M: {np.mean(delta):7.5}, VAR: {np.var(delta):7.5}")


if __name__ == '__main__':
    main()
