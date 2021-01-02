import os

from home_temp_calc import HomesTempCalc

os.environ["path"] = (
        "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.0\\bin;"
        "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDNN\\8.0.4_for_cuda_11.0\\bin;" +
        os.environ["path"]
)

from datetime import datetime

from tensorflow.python.keras.models import load_model
import pandas as pd
from dateutil.tz import gettz
from matplotlib import pyplot as plt

import column_names
import config
from dataset_utils.dataset_io import load_dataset
from homes_time_deltas_utils.homes_deltas_io import load_homes_time_deltas
from model_utils.model_metrics import relative_error
from preprocess_utils import filter_by_timestamp_closed

if __name__ == '__main__':
    # noinspection SpellCheckingInspection
    model_name = "multi_lstm_2020-09-14-21.22.12\\engelsa_37.csv"
    iteration = "best"
    custom_model_objects = {
        "relative_error": relative_error,
    }

    # noinspection SpellCheckingInspection
    real_home_dataset_name = "engelsa_37.csv"

    start_date = datetime(2019, 2, 5, tzinfo=gettz(config.TIMEZONE))
    end_date = datetime(2019, 2, 25, tzinfo=gettz(config.TIMEZONE))

    boiler_df = load_dataset(config.BOILER_PREPROCESSED_DATASET_PATH)
    boiler_df = filter_by_timestamp_closed(boiler_df, start_date, end_date)

    homes_time_deltas = load_homes_time_deltas(config.HOMES_TIME_DELTAS_PATH)
    home_time_delta = homes_time_deltas[
        homes_time_deltas[column_names.HOME_NAME] == real_home_dataset_name
        ][column_names.TIME_DELTA].iat[0]

    real_home_dataset_path = f"{config.HOMES_PREPROCESSED_DATASETS_DIR}\\" \
                             f"{real_home_dataset_name}{config.PREPROCESSED_DATASET_FILENAME_SUFFIX}"
    real_home_dataset = load_dataset(real_home_dataset_path)
    real_home_dataset = filter_by_timestamp_closed(real_home_dataset, start_date, end_date)
    real_home_dataset = pd.DataFrame({
        column_names.TIMESTAMP: real_home_dataset[column_names.TIMESTAMP].to_list()[home_time_delta:],
        column_names.FORWARD_PIPE_TEMP: real_home_dataset[column_names.FORWARD_PIPE_TEMP].to_list()[home_time_delta:]
    })

    model_filepath = f"{config.MODELS_DIR}\\{model_name}\\{iteration}{config.MODEL_FILE_SUFFIX}"
    model = load_model(
        model_filepath,
        custom_objects=custom_model_objects
    )

    home_temp_calc = HomesTempCalc()
    home_temp_calc.set_boiler_df(boiler_df)
    home_temp_calc.set_home_time_delta(home_time_delta)
    home_temp_calc.set_model(model)
    calculated_home_dataset = home_temp_calc.get_calculated_home_temp()

    ax = plt.axes()
    ax.plot(
        real_home_dataset[column_names.TIME_DELTA].to_list(),
        real_home_dataset[column_names.FORWARD_PIPE_TEMP].to_list(),
        label=f"Реальная температура в {real_home_dataset_name}. Град."
    )
    ax.plot(
        calculated_home_dataset[column_names.TIME_DELTA].to_list(),
        calculated_home_dataset[column_names.FORWARD_PIPE_TEMP].to_list(),
        label=f"Вычисленная температура в {real_home_dataset_name}. Град."
    )

    ax.grid(True)
    ax.legend()
    plt.show()
