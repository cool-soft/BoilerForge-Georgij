import logging

import pandas as pd
from dateutil.tz import gettz

import column_names
from heating_system.preprocess_utils import parse_datetime, float_converter
from .home_data_parser import HomeDataParser


class SoftMCSVHomeDataParser(HomeDataParser):

    def __init__(self, weather_data_timezone_name=None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("Creating instance of the service")

        self._timestamp_timezone_name = weather_data_timezone_name
        self._timestamp_parse_patterns = (
            r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hour>\d{2}):(?P<min>\d{2}).{7}",
            r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<hour>\d{1,2}):(?P<min>\d{2})"
        )
        self._ntc = 1
        self._disabled_temp_threshold = 0

    def set_timestamp_timezone_name(self, timezone_name):
        self._timestamp_timezone_name = timezone_name

    def set_timestamp_parse_patterns(self, patterns):
        self._timestamp_parse_patterns = patterns

    def set_ntc(self, ntc):
        self._ntc = ntc

    def set_disabled_temp_threshold(self, threshold):
        self._disabled_temp_threshold = threshold

    def parse_home_data(self, home_data):
        self._logger.debug("Loading data")
        boiler_df = pd.read_csv(home_data, sep=";", low_memory=False)

        self._logger.debug("Parsing data")

        boiler_df = boiler_df[boiler_df[column_names.SOFT_M_PIPE_NUMBER] == self._ntc]
        boiler_df.rename(
            columns={
                column_names.SOFT_M_TIMESTAMP: column_names.TIMESTAMP,
                column_names.SOFT_M_FORWARD_PIPE_TEMP: column_names.FORWARD_PIPE_TEMP
            },
            inplace=True
        )

        boiler_df = boiler_df[[column_names.FORWARD_PIPE_TEMP, column_names.TIMESTAMP]]
        boiler_df = boiler_df[boiler_df[column_names.FORWARD_PIPE_TEMP].notnull()]
        boiler_data_timezone = gettz(self._timestamp_timezone_name)
        boiler_df[column_names.TIMESTAMP] = boiler_df[column_names.TIMESTAMP].apply(
            lambda datetime_as_str: parse_datetime(
                datetime_as_str,
                self._timestamp_parse_patterns,
                boiler_data_timezone
            )
        )

        boiler_df[column_names.FORWARD_PIPE_TEMP] = boiler_df[column_names.FORWARD_PIPE_TEMP].apply(float_converter)
        boiler_df[column_names.FORWARD_PIPE_TEMP] = boiler_df[
            column_names.FORWARD_PIPE_TEMP].apply(
            lambda water_temp: water_temp > 100 and water_temp / 100 or water_temp
        )
        boiler_df[column_names.FORWARD_PIPE_TEMP] = boiler_df[
            boiler_df[column_names.FORWARD_PIPE_TEMP] > self._disabled_temp_threshold]

        return boiler_df
