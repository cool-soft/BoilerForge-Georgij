import numpy as np
import pandas as pd

import column_names


class HomesTempCalc:

    def __init__(self):
        self._boiler_temp_df = None
        self._home_time_delta = None
        self._model = None

    def set_boiler_df(self, boiler_temp_df):
        self._boiler_temp_df = boiler_temp_df

    def set_home_time_delta(self, time_delta):
        self._home_time_delta = time_delta

    def set_model(self, model):
        self._model = model

    def get_calculated_home_temp(self):
        boiler_temp = self._boiler_temp_df[column_names.FORWARD_PIPE_TEMP].to_numpy()
        boiler_temp = boiler_temp[:-self._home_time_delta]
        boiler_temp = boiler_temp.reshape(len(boiler_temp), 1)
        boiler_temp = boiler_temp.astype(np.float)
        predicted_temp_in_home = self._model.predict(
            boiler_temp,
            batch_size=len(boiler_temp)
        )
        boiler_temp_dates = self._boiler_temp_df[column_names.TIMESTAMP].to_list()
        predicted_temp_dates = boiler_temp_dates[self._home_time_delta:]
        predicted_temp_df = pd.DataFrame({
            column_names.TIMESTAMP: predicted_temp_dates,
            column_names.FORWARD_PIPE_TEMP: predicted_temp_in_home
        })
        return predicted_temp_df