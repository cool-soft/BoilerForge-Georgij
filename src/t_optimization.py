
import math
import os

import numpy as np
import pandas as pd

from config import DEFAULT_OPTIMIZED_T_TABLE_PATH, DEFAULT_MODELS_DIR
from utils.metrics import relative_error
from utils.io_utils import load_saved_model


# noinspection PyShadowingNames
class TOptimizer:

    def __init__(self):
        self._smooth_size = 2
        self._window_size = 5
        self._parent_model_name = None
        self._custom_models_objects = {}

        self._t_step = 0.5
        self._min_control_t = 0
        self._max_control_t = 100

        self._submodels = {}
        self._deltas = None
        self._optimized_t_table = None
        self._control_t_pack = None

    def set_smooth_size(self, smooth_size):
        self._smooth_size = smooth_size

    def set_window_size(self, window_size):
        self._window_size = window_size

    def set_t_step(self, t_step):
        self._t_step = t_step

    def set_parent_model_name(self, parent_model_name):
        self._parent_model_name = parent_model_name

    def set_custom_models_objects(self, custom_objects):
        self._custom_models_objects = custom_objects

    def get_optimized_t_df(self):
        return self._optimized_t_table

    def start_optimization(self):
        print("Starting optimization")
        self._load_submodels()
        self._generate_control_t_pack()
        self._calc_optimized_t_table()

    def _load_submodels(self):
        print("Loading submodels")

        parent_model_dir = f"{DEFAULT_MODELS_DIR}\\{self._parent_model_name}"
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

    def _generate_control_t_pack(self):
        print("Generating available control t list")

        t_count = math.ceil((self._max_control_t-self._min_control_t)/self._t_step)
        control_t_pack = np.empty(shape=(t_count, self._window_size))
        for i in range(t_count):
            control_t_pack[i, :] = self._min_control_t + (i * self._t_step)
        self._control_t_pack = control_t_pack

    def _calc_optimized_t_table(self):
        print("Optimization is started")

        optimized_t = {}
        control_t_count = len(self._control_t_pack)
        reshaped_control_t_pack = self._control_t_pack.reshape((control_t_count, 1, self._window_size))
        for home_name, model in self._submodels.items():
            print(f"Optimization {home_name}")
            predicted_t_in_home_pack = model.predict(reshaped_control_t_pack, batch_size=control_t_count)
            optimized_t[home_name] = predicted_t_in_home_pack.reshape(control_t_count)

        boiler_t = self._control_t_pack[:, 0]
        optimized_t["BOILER"] = boiler_t
        self._optimized_t_table = pd.DataFrame(data=optimized_t)


if __name__ == '__main__':
    model_name = "multi_lstm_2020-09-14-21.22.12"
    smooth_size = 2
    window_size = 5
    custom_models_objects = {
        "relative_error": relative_error,
    }
    t_step = 0.1

    optimizer = TOptimizer()
    optimizer.set_smooth_size(smooth_size)
    optimizer.set_window_size(window_size)
    optimizer.set_parent_model_name(model_name)
    optimizer.set_custom_models_objects(custom_models_objects)
    optimizer.set_t_step(t_step)

    optimizer.start_optimization()

    optimized_t_df = optimizer.get_optimized_t_df()
    print(f"Saving optimized t table to {DEFAULT_OPTIMIZED_T_TABLE_PATH}")
    optimized_t_df.to_pickle(DEFAULT_OPTIMIZED_T_TABLE_PATH)
