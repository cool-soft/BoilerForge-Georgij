
import os

import pandas as pd

from config import (
    SRC_WEATHER_DATASET_PATH,
    PREPROCESSED_WEATHER_DATASET_PATH,
    START_DATE,
    END_DATE
)

from utils.preprocess_utils import (
    round_datetime,
    interpolate_t,
    remove_duplicates_by_timestamp,
    round_timestamp,
    convert_date_and_time_to_timestamp,
    rename_column
)


def process_weather_t(src_weather_path, dst_weather_file, min_date, max_date):
    min_date = round_datetime(min_date)
    max_date = round_datetime(max_date)

    with open(os.path.abspath(src_weather_path), "r") as f:
        df = pd.read_json(f)

    df = convert_date_and_time_to_timestamp(df)
    df = round_timestamp(df)
    df = rename_column(df, "temp", "t1")
    df = interpolate_t(df, min_date, max_date)
    df = remove_duplicates_by_timestamp(df)

    df.to_pickle(dst_weather_file)


if __name__ == '__main__':
    process_weather_t(
        SRC_WEATHER_DATASET_PATH,
        PREPROCESSED_WEATHER_DATASET_PATH,
        START_DATE,
        END_DATE
    )
