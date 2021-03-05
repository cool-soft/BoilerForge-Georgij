import math
import os

import numpy as np
import pandas as pd

import config
from model_utils.model_io import load_saved_model


class TempCorrelationTableGenerator:

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

    def set_temp_step(self, t_step):
        self._t_step = t_step

    def set_parent_model_name(self, parent_model_name):
        self._parent_model_name = parent_model_name

    def set_custom_models_objects(self, custom_objects):
        self._custom_models_objects = custom_objects

    def get_temp_correlation_table(self):
        return self._optimized_t_table

    def start_optimization(self):
        print("Starting optimization")
        self._load_submodels()
        self._generate_control_t_pack()
        self._calc_optimized_t_table()

    # noinspection SpellCheckingInspection
    def _load_submodels(self):
        print("Loading submodels")

        parent_model_dir = f"{config.MODELS_DIR}\\{self._parent_model_name}"
        submodels = {}
        for submodel_name in os.listdir(parent_model_dir):
            submodel_filepath = f"{parent_model_dir}\\{submodel_name}\\" \
                                f"{config.BEST_MODEL_FILENAME}{config.MODEL_FILE_SUFFIX}"
            model = load_saved_model(submodel_filepath, custom_objects=self._custom_models_objects)
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
