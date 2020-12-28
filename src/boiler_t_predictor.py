
from datetime import datetime

import pandas as pd

from config import (
    DEFAULT_PREDICTED_BOILER_T_PATH,
    DEFAULT_PREPROCESSED_BOILER_DATASET_PATH,
    TIMESTAMP_COLUMN_NAME,
    BOILER_COLUMN_NAME, DEFAULT_HOME_T_DISPERSION_COEFFICIENT
)
from utils.dataset_utils import create_time_series
from utils.io_utils import (
    load_dataset,
    load_weather_dataset,
    load_optimized_t_table
)
from utils.home_deltas_utils import load_homes_time_deltas
from utils.t_graph_utils import load_t_graph
from utils.predict_utils import plot_real_and_predicted, print_min_max_mean_delta


# noinspection PyShadowingNames
class BoilerTPredictor:

    def __init__(self):
        self._window_size = 5
        self._smooth_size = 2
        self._optimized_t_table = None
        self._homes_time_deltas = None
        self._temp_graph = None
        self._home_t_dispersion_coefficient = DEFAULT_HOME_T_DISPERSION_COEFFICIENT

    def set_homes_time_deltas(self, homes_time_deltas):
        self._homes_time_deltas = homes_time_deltas

    def set_window_size(self, window_size):
        self._window_size = window_size

    def set_smooth_size(self, smooth_size):
        self._smooth_size = smooth_size

    def set_optimized_t_table(self, t_table):
        self._optimized_t_table = t_table

    def set_temp_graph(self, temp_graph):
        self._temp_graph = temp_graph

    def set_dispersion_coefficient(self, coefficient):
        self._home_t_dispersion_coefficient = coefficient

    def predict_on_weather_t_arr(self, weather_t_arr):
        print("Predicting")

        predicted_boiler_t = []
        start_t_idx = self._window_size - self._smooth_size - 1
        max_home_time_delta = self._homes_time_deltas["time_delta"].max()
        end_t_idx = len(weather_t_arr) - max_home_time_delta + smooth_size
        for t_idx in range(start_t_idx, end_t_idx, self._window_size):
            need_t_by_homes = self._get_need_t_in_homes(t_idx, weather_t_arr)
            need_boiler_t = self._calc_need_boiler_t_by_homes_t(need_t_by_homes)
            for i in range(self._window_size):
                predicted_boiler_t.append(need_boiler_t)
            print(f"Predicted {t_idx}/{end_t_idx}")

        time_series = create_time_series(min_date, max_date)
        time_series = time_series[start_t_idx:end_t_idx]
        predicted_boiler_t_df = pd.DataFrame({
            TIMESTAMP_COLUMN_NAME: time_series,
            "t1": predicted_boiler_t
        })
        return predicted_boiler_t_df

    def _get_need_t_in_homes(self, t_idx, weather_t_arr):
        need_temps = {}
        for index, row in self._homes_time_deltas.iterrows():
            home_time_delta = row["time_delta"]
            home_name = row["home_name"]

            weather_t = weather_t_arr[t_idx + home_time_delta]
            need_t = self._get_need_t_by_temp_graph(weather_t)
            need_temps[home_name] = need_t

        return need_temps

    def _get_need_t_by_temp_graph(self, weather_t):
        available_t = self._temp_graph[self._temp_graph["weather_t"] <= weather_t]
        need_t = available_t["home_t"].min() * self._home_t_dispersion_coefficient
        return need_t

    def _calc_need_boiler_t_by_homes_t(self, need_t_by_homes):
        iterator = iter(need_t_by_homes.items())
        home_name, home_need_t = next(iterator)
        need_t_condition = self._optimized_t_table[home_name] >= home_need_t
        for home_name, home_need_t in iterator:
            need_t_condition = need_t_condition & (self._optimized_t_table[home_name] >= home_need_t)

        need_boiler_t = self._optimized_t_table[need_t_condition]
        need_boiler_t = need_boiler_t[BOILER_COLUMN_NAME].min()
        return need_boiler_t


if __name__ == '__main__':
    min_date = datetime(2019, 2, 5)
    max_date = datetime(2019, 4, 30)

    window_size = 5
    smooth_size = 2

    homes_time_deltas = load_homes_time_deltas()
    optimized_t_table = load_optimized_t_table()
    temp_graph = load_t_graph()
    weather_df = load_weather_dataset(min_date, max_date)
    weather_t = weather_df["t1"].to_numpy()

    boiler_t_predictor = BoilerTPredictor()
    boiler_t_predictor.set_smooth_size(smooth_size)
    boiler_t_predictor.set_window_size(window_size)
    boiler_t_predictor.set_homes_time_deltas(homes_time_deltas)
    boiler_t_predictor.set_optimized_t_table(optimized_t_table)
    boiler_t_predictor.set_temp_graph(temp_graph)

    predicted_boiler_t_df = boiler_t_predictor.predict_on_weather_t_arr(weather_t)
    predicted_boiler_t_df.to_pickle(DEFAULT_PREDICTED_BOILER_T_PATH)

    predicted_boiler_t = predicted_boiler_t_df["t1"].to_numpy()
    dates = predicted_boiler_t_df[TIMESTAMP_COLUMN_NAME].to_list()

    real_boiler_t_dataset = load_dataset(DEFAULT_PREPROCESSED_BOILER_DATASET_PATH, min_date, max_date)
    real_boiler_t = real_boiler_t_dataset["t1"].to_numpy()
    start_t_idx = window_size - smooth_size - 1
    max_home_time_delta = homes_time_deltas["time_delta"].max()
    end_t_idx = len(real_boiler_t) - max_home_time_delta + smooth_size
    real_boiler_t = real_boiler_t[start_t_idx:end_t_idx]

    print_min_max_mean_delta(real_boiler_t, predicted_boiler_t)
    plot_real_and_predicted(
        dates,
        real_boiler_t,
        predicted_boiler_t
    )
