
import os
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from column_names import SOFT_M_TIMESTAMP
from config import (
    MODELS_DIR,
    PREDICTED_BOILER_TEMP_PATH,
    HOMES_DELTAS_PATH,
    WEATHER_PREPROCESSED_DATASET_PATH
)
from homes_time_deltas_utils.homes_deltas_io import load_homes_time_deltas
from model_utils.model_io import load_saved_model
from model_utils.model_metrics import relative_error
from preprocess_utils import filter_by_timestamp_closed
from temp_graph_utils.temp_graph_calculation import calc_need_t_in_home
from time_tick import TIME_TICK
from dataset_utils.dataset_train_preprocessing import create_time_series

# noinspection PyShadowingNames
from weather_dataset_utils.weather_dataset_io import load_weather_dataset


class HomesTCalc:

    def __init__(self):
        self._smooth_size = 2
        self._window_size = 5
        self._parent_model_name = None
        self._predicted_boiler_t_path = PREDICTED_BOILER_TEMP_PATH
        self._home_time_deltas_path = HOMES_DELTAS_PATH
        self._custom_models_objects = {}

        self._homes_time_deltas = None
        self._calculated_t_in_homes_df = None
        self._predicted_boiler_t_df = None
        self._boiler_t_seq = None

    def set_smooth_size(self, smooth_size):
        self._smooth_size = smooth_size

    def set_window_size(self, window_size):
        self._window_size = window_size

    def set_parent_model_name(self, parent_model_name):
        self._parent_model_name = parent_model_name

    def set_custom_models_objects(self, custom_objects):
        self._custom_models_objects = custom_objects

    def get_calculated_t_in_homes_df(self):
        return self._calculated_t_in_homes_df

    def start_calculation(self):
        print("Calculation starting")

        self._load_predicted_boiler_t_df()
        self._load_submodels()
        self._create_boiler_t_sequences()

        self._calculate()

    def _load_submodels(self):
        print("Loading submodels")

        parent_model_dir = f"{MODELS_DIR}\\{self._parent_model_name}"
        submodels = {}
        for submodel_name in os.listdir(parent_model_dir):
            model = load_saved_model(
                submodel_name,
                "best",
                custom_objects=self._custom_models_objects,
                models_dir=parent_model_dir
            )
            submodels[submodel_name] = model
        self._submodels = submodels

    def _load_predicted_boiler_t_df(self):
        with open(self._predicted_boiler_t_path, "rb") as f:
            self._predicted_boiler_t_df = pickle.load(f)

    def _calculate(self):
        calculated_t_dict = {}
        for model_name, model in self._submodels.items():
            predicted_t = model.predict(self._boiler_t_seq, batch_size=len(self._boiler_t_seq))
            predicted_t = predicted_t.reshape(len(predicted_t))
            calculated_t_dict[model_name] = predicted_t
        self._calculated_t_in_homes_df = pd.DataFrame(calculated_t_dict)

    def _create_boiler_t_sequences(self):
        boiler_t = self._predicted_boiler_t_df["t1"].to_numpy()
        sequences_count = int(len(boiler_t) / self._window_size)
        boiler_t_seq = np.empty(shape=(sequences_count * self._window_size, self._window_size))
        for i in range(0, sequences_count * self._window_size, self._window_size):
            for j in range(self._window_size):
                boiler_t_seq[i+j] = boiler_t[i:i + self._window_size]
        self._boiler_t_seq = boiler_t_seq.reshape((sequences_count * self._window_size, 1, self._window_size))


if __name__ == '__main__':
    model_name = "multi_lstm_2020-09-14-21.22.12"
    smooth_size = 2
    window_size = 5
    custom_models_objects = {
        "relative_error": relative_error,
    }

    boiler_start_date = datetime(2019, 2, 5)
    boiler_end_date = datetime(2019, 2, 25)

    start_idx_delta = window_size - smooth_size - 1

    home_t_calc = HomesTCalc()
    home_t_calc.set_smooth_size(smooth_size)
    home_t_calc.set_window_size(window_size)
    home_t_calc.set_parent_model_name(model_name)
    home_t_calc.set_custom_models_objects(custom_models_objects)

    home_t_calc.start_calculation()

    calculated_t_df = home_t_calc.get_calculated_t_in_homes_df()

    homes_time_deltas = load_homes_time_deltas()
    dates = create_time_series(boiler_start_date, boiler_end_date)

    ax = plt.axes()

    for idx, row in homes_time_deltas.iterrows():
        home_name = row["home_name"]
        time_delta = row["time_delta"]

        home_t = calculated_t_df[home_name].to_numpy()
        additional_dates = create_time_series(boiler_end_date + TIME_TICK, boiler_end_date + (TIME_TICK * time_delta))
        home_dates = dates[time_delta + start_idx_delta:] + additional_dates
        home_dates = home_dates[:len(home_t)]

        ax.plot(home_dates, home_t, label=home_name)

    weather_start_date = boiler_start_date + ((homes_time_deltas["time_delta"].min() + start_idx_delta) * TIME_TICK)
    weather_end_date = boiler_end_date + ((homes_time_deltas["time_delta"].max() + smooth_size) * TIME_TICK)
    weather_df = load_weather_dataset(WEATHER_PREPROCESSED_DATASET_PATH)
    weather_df = filter_by_timestamp_closed(weather_df, weather_start_date, weather_end_date)
    weather_t = weather_df["t1"].to_numpy()
    # TODO: this
    need_t = calc_need_t_in_home(weather_t)

    ax.plot(
        weather_df[SOFT_M_TIMESTAMP],
        need_t,
        label="Требования температурного графика",
        linestyle="-",
        color="red"
    )

    ax.grid(True)
    ax.legend()
    plt.show()
