import datetime
import logging

import pandas as pd
from dateutil.tz import gettz

import column_names
from preprocess_utils import parse_time
from .weather_data_parser import WeatherDataParser


class SoftMWeatherDataParser(WeatherDataParser):

    def __init__(self, weather_data_timezone_name=None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("Creating instance of the service")

        self._weather_data_timezone_name = weather_data_timezone_name
        self._time_parse_pattern = r"(?P<hour>\d\d):(?P<min>\d\d):(?P<sec>\d\d)"

    def set_weather_data_timezone_name(self, timezone_name):
        self._weather_data_timezone_name = timezone_name

    def parse_weather_data(self, weather_data):
        self._logger.debug("Parsing weather data")

        df = pd.read_json(weather_data)
        df.rename(
            columns={
                column_names.SOFT_M_WEATHER_TEMP: column_names.WEATHER_TEMP
            },
            inplace=True
        )

        df = self._convert_date_and_time_to_timestamp(df)
        return df

    def _convert_date_and_time_to_timestamp(self, df):
        timezone = gettz(self._weather_data_timezone_name)
        datetime_list = []
        for _, row in df.iterrows():
            time_as_str = row[column_names.SOFT_M_WEATHER_TIME]
            time = parse_time(time_as_str, self._time_parse_pattern)

            date = row[column_names.SOFT_M_WEATHER_DATE].date()

            datetime_ = datetime.datetime.combine(date, time, tzinfo=timezone)
            datetime_list.append(datetime_)

        df[column_names.TIMESTAMP] = datetime_list
        del df[column_names.SOFT_M_WEATHER_TIME]
        del df[column_names.SOFT_M_WEATHER_DATE]

        return df
