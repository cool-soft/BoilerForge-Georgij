import pickle

from config import (
    WEATHER_PREPROCESSED_DATASET_PATH,
    START_DATETIME,
    END_DATETIME
)
from preprocess_utils import filter_by_timestamp_closed


def load_weather_dataset(
    min_date=START_DATETIME,
    max_date=END_DATETIME,
    path=WEATHER_PREPROCESSED_DATASET_PATH
):
    weather_df = load_dataset(path, min_date, max_date)
    return weather_df


def load_dataset(path, start_date, end_date):
    df = load_dataframe(path)
    df = filter_by_timestamp_closed(df, start_date, end_date)
    return df


def load_dataframe(path):
    with open(path, "rb") as f:
        df = pickle.load(f)
    return df

