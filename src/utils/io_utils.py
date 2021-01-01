
import json
import pickle
from datetime import datetime

from config import (
    MODELS_DIR,
    MODEL_FILE_SUFFIX,
    WEATHER_PREPROCESSED_DATASET_PATH,
    START_DATETIME,
    END_DATETIME,
    TEMP_CORRELATION_TABLE_PATH
)
from preprocess_utils import filter_by_timestamp_closed


def load_weather_dataset(
    min_date=START_DATETIME,
    max_date=END_DATETIME,
    path=WEATHER_PREPROCESSED_DATASET_PATH
):
    weather_df = load_dataset(path, min_date, max_date)
    return weather_df


def load_optimized_t_table(path=TEMP_CORRELATION_TABLE_PATH):
    df = load_dataframe(path)
    return df


def load_dataset(path, start_date, end_date):
    df = load_dataframe(path)
    df = filter_by_timestamp_closed(df, start_date, end_date)
    return df


def load_dataframe(path):
    with open(path, "rb") as f:
        df = pickle.load(f)
    return df


def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def get_model_save_name(model_name):
    fit_start_time = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    model_save_name = "{}_{}".format(model_name, fit_start_time)
    return model_save_name


def load_saved_model(model_name, iteration, custom_objects=None, models_dir=MODELS_DIR, file_suffix=MODEL_FILE_SUFFIX):
    from keras.engine.saving import load_model

    if custom_objects is None:
        custom_objects = {}
    model_path = "{}\\{}\\{}{}".format(models_dir, model_name, iteration, file_suffix)
    model = load_model(model_path, custom_objects=custom_objects)
    return model


