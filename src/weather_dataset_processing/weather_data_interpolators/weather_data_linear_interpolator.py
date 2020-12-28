import logging

import pandas as pd

import column_names
import time_tick
from preprocess_utils import round_datetime
from .weather_data_interpolator import WeatherDataInterpolator


class WeatherDataLinearInterpolator(WeatherDataInterpolator):

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("Creating instance of the service")

    def interpolate_weather_data(self,
                                 weather_data: pd.DataFrame,
                                 start_datetime=None,
                                 end_datetime=None,
                                 inplace=False) -> pd.DataFrame:
        self._logger.debug("Requested weather data interpolating")

        time_tick_in_seconds = time_tick.TIME_TICK.total_seconds()

        if not inplace:
            weather_data = weather_data.copy()

        weather_data[column_names.TIMESTAMP] = weather_data[column_names.TIMESTAMP].apply(
            lambda datetime_: round_datetime(datetime_, time_tick_in_seconds)
        )
        weather_data.drop_duplicates(column_names.TIMESTAMP, inplace=True, ignore_index=True)

        if start_datetime is not None:
            start_datetime = round_datetime(start_datetime, time_tick_in_seconds)
            weather_data = self._interpolate_weather_data_start(weather_data, start_datetime)
        if end_datetime is not None:
            end_datetime = round_datetime(end_datetime, time_tick_in_seconds)
            weather_data = self._interpolate_weather_data_end(weather_data, end_datetime)
        weather_data.sort_values(by=column_names.TIMESTAMP, ignore_index=True, inplace=True)
        weather_data = self._interpolate_passes_of_weather_data(weather_data)
        weather_data.sort_values(by=column_names.TIMESTAMP, ignore_index=True, inplace=True)

        return weather_data

    def _interpolate_passes_of_weather_data(self, weather_data: pd.DataFrame):
        self._logger.debug("Interpolating passes of weather data")

        interpolated_values = []

        previous_datetime = None
        previous_t = None
        for index, row in weather_data.iterrows():

            if previous_datetime is None:
                previous_datetime = row[column_names.TIMESTAMP]
                previous_t = row[column_names.WEATHER_TEMP]
                continue

            next_datetime = row[column_names.TIMESTAMP]
            next_t = row[column_names.WEATHER_TEMP]

            datetime_delta = next_datetime - previous_datetime
            if datetime_delta > time_tick.TIME_TICK:
                number_of_passes = int(datetime_delta // time_tick.TIME_TICK) - 1
                t_step = (next_t - previous_t) / number_of_passes
                for pass_n in range(1, number_of_passes + 1):
                    interpolated_datetime = previous_datetime + (time_tick.TIME_TICK * pass_n)
                    interpolated_t = previous_t + (t_step * pass_n)
                    interpolated_values.append({
                        column_names.TIMESTAMP: interpolated_datetime,
                        column_names.WEATHER_TEMP: interpolated_t,
                    })

            previous_t = next_t
            previous_datetime = next_datetime

        weather_data = weather_data.append(
            interpolated_values,
            ignore_index=True
        )

        return weather_data

    def _interpolate_weather_data_start(self, weather_data, start_datetime):
        self._logger.debug("Interpolating start of weather data")

        first_datetime_idx = weather_data[column_names.TIMESTAMP].idxmin()
        first_row = weather_data.loc[first_datetime_idx]
        first_temp = first_row[column_names.WEATHER_TEMP]
        first_datetime = first_row[column_names.TIMESTAMP]
        if first_datetime > start_datetime:
            weather_data = weather_data.append(
                {
                    column_names.TIMESTAMP: start_datetime,
                    column_names.WEATHER_TEMP: first_temp
                },
                ignore_index=True
            )
        return weather_data

    def _interpolate_weather_data_end(self, weather_data, end_datetime):
        self._logger.debug("Interpolating end of weather data")

        last_datetime_idx = weather_data[column_names.TIMESTAMP].idxmax()
        last_row = weather_data.loc[last_datetime_idx]
        last_temp = last_row[column_names.WEATHER_TEMP]
        last_datetime = last_row[column_names.TIMESTAMP]
        if last_datetime < end_datetime:
            weather_data = weather_data.append(
                {
                    column_names.TIMESTAMP: end_datetime,
                    column_names.WEATHER_TEMP: last_temp
                },
                ignore_index=True
            )
        return weather_data
