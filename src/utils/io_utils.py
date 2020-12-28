
import json
import os
import pickle
from datetime import datetime

from config import (
    DEFAULT_MODELS_DIR,
    DEFAULT_HISTORY_FILENAME,
    DEFAULT_MODEL_FILE_SUFFIX,
    DEFAULT_PREPROCESSED_WEATHER_DATASET_PATH,
    DEFAULT_START_DATE,
    DEFAULT_END_DATE,
    DEFAULT_OPTIMIZED_T_TABLE_PATH
)
from utils.preprocess_utils import filter_by_timestamp


def load_weather_dataset(
    min_date=DEFAULT_START_DATE,
    max_date=DEFAULT_END_DATE,
    path=DEFAULT_PREPROCESSED_WEATHER_DATASET_PATH
):
    weather_df = load_dataset(path, min_date, max_date)
    return weather_df


def load_optimized_t_table(path=DEFAULT_OPTIMIZED_T_TABLE_PATH):
    df = load_dataframe(path)
    return df


def load_dataset(path, start_date, end_date):
    df = load_dataframe(path)
    df = filter_by_timestamp(df, start_date, end_date)
    return df


def load_dataframe(path):
    with open(path, "rb") as f:
        df = pickle.load(f)
    return df


def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def save_history(history, model_name, models_dir=DEFAULT_MODELS_DIR, filename=DEFAULT_HISTORY_FILENAME):
    model_dir = os.path.abspath("{}\\{}".format(models_dir, model_name))
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    filename = "{}\\{}".format(model_dir, filename)
    with open(filename, "w") as f:
        json.dump(history, f, indent=4)


def get_model_save_name(model_name):
    fit_start_time = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    model_save_name = "{}_{}".format(model_name, fit_start_time)
    return model_save_name


def load_saved_model(model_name, iteration, custom_objects=None, models_dir=DEFAULT_MODELS_DIR, file_suffix=DEFAULT_MODEL_FILE_SUFFIX):
    from keras.engine.saving import load_model

    if custom_objects is None:
        custom_objects = {}
    model_path = "{}\\{}\\{}{}".format(models_dir, model_name, iteration, file_suffix)
    model = load_model(model_path, custom_objects=custom_objects)
    return model


def load_model_metrics(model_name, models_dir=DEFAULT_MODELS_DIR, history_filename=DEFAULT_HISTORY_FILENAME):
    file_path = "{}\\{}\\{}".format(models_dir, model_name, history_filename)
    model_metrics = load_json(file_path)
    return model_metrics
