
import datetime
import os

import pandas as pd

from config import (
    HOMES_PREPROCESSED_DATASETS_DIR,
    BOILER_PREPROCESSED_DATASET_PATH,
    PREPROCESSED_DATASET_FILENAME_SUFFIX,
    HOMES_TIME_DELTAS_PATH
)
from dataset_utils.dataset_io import load_dataset
from preprocess_utils import average_values


def get_boiler_max_idx(boiler_t):
    boiler_max_idx = 0
    for i in range(len(boiler_t)):
        if boiler_t[i] > boiler_t[boiler_max_idx]:
            boiler_max_idx = i
    return boiler_max_idx


def get_home_max_idxs(home_t, boiler_max_idx, max_delta):
    rows_count = len(home_t)
    max_idx = 0
    for i in range(boiler_max_idx+1, min(boiler_max_idx + max_delta, rows_count)):
        if home_t[i] > home_t[max_idx]:
            max_idx = i
    return max_idx


def main():
    max_delta = 40
    min_date = datetime.datetime(2019, 1, 1, 0, 0, 0)
    max_date = datetime.datetime(2019, 4, 1, 0, 0, 0)
    t_in_homes_smooth_size = 0  # 30
    boiler_t_smooth_size = 0  # 30

    boiler_df = load_dataset(BOILER_PREPROCESSED_DATASET_PATH, min_date, max_date)
    boiler_t = boiler_df["t1"].to_numpy()
    boiler_t = average_values(boiler_t, boiler_t_smooth_size)
    boiler_max_idx = get_boiler_max_idx(boiler_t)

    deltas = []
    for dataset_filename in os.listdir(HOMES_PREPROCESSED_DATASETS_DIR):
        dataset_name = dataset_filename[:-(len(PREPROCESSED_DATASET_FILENAME_SUFFIX))]

        dataset_path = f"{HOMES_PREPROCESSED_DATASETS_DIR}\\{dataset_filename}"
        df = load_dataset(dataset_path, min_date, max_date)
        t_in_home = df["t1"].to_numpy()
        t_in_home = average_values(t_in_home, t_in_homes_smooth_size)
        home_max_idx = get_home_max_idxs(t_in_home, boiler_max_idx, max_delta)
        delta = home_max_idx-boiler_max_idx

        deltas.append({"home_name": dataset_name, "time_delta": delta})
        print("{}: {}".format(dataset_name, delta))

    homes_deltas = pd.DataFrame(deltas)
    homes_deltas.to_csv(HOMES_TIME_DELTAS_PATH, index=False)


if __name__ == '__main__':
    main()
