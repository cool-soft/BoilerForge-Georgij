import logging

import pandas as pd
from dateutil.tz import gettz

from heating_system.preprocess_utils import parse_datetime, float_converter
from heating_system_utils.constants import column_names, soft_m_column_names, circuits_id, soft_m_circuits_id
from .boiler_data_parser import BoilerDataParser


class SoftMCSVBoilerDataParser(BoilerDataParser):

    def __init__(self, weather_data_timezone_name=None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("Creating instance of the service")

        self._timestamp_timezone_name = weather_data_timezone_name
        self._timestamp_parse_patterns = (
            r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hour>\d{2}):(?P<min>\d{2}).{7}",
            r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<hour>\d{1,2}):(?P<min>\d{2})"
        )

        self._need_circuits = (circuits_id.HEATING_CIRCUIT, circuits_id.WATER_CIRCUIT)

        self._need_to_float_convert_columns = (
            column_names.FORWARD_PIPE_COOLANT_TEMP,
            column_names.BACKWARD_PIPE_COOLANT_TEMP,
            column_names.FORWARD_PIPE_COOLANT_VOLUME,
            column_names.BACKWARD_PIPE_COOLANT_VOLUME,
            column_names.FORWARD_PIPE_COOLANT_PRESSURE,
            column_names.BACKWARD_PIPE_COOLANT_PRESSURE
        )

        self._circuits_equal_id = {
            soft_m_circuits_id.WATER_CIRCUIT: circuits_id.WATER_CIRCUIT,
            soft_m_circuits_id.HEATING_CIRCUIT: circuits_id.HEATING_CIRCUIT
        }

        self._columns_equal_names = {
            soft_m_column_names.TIMESTAMP: column_names.TIMESTAMP,
            soft_m_column_names.CIRCUIT_ID: column_names.CIRCUIT_ID,
            soft_m_column_names.FORWARD_PIPE_COOLANT_TEMP: column_names.FORWARD_PIPE_COOLANT_TEMP,
            soft_m_column_names.BACKWARD_PIPE_COOLANT_TEMP: column_names.BACKWARD_PIPE_COOLANT_TEMP,
            soft_m_column_names.FORWARD_PIPE_COOLANT_VOLUME: column_names.FORWARD_PIPE_COOLANT_VOLUME,
            soft_m_column_names.BACKWARD_PIPE_COOLANT_VOLUME: column_names.BACKWARD_PIPE_COOLANT_VOLUME,
            soft_m_column_names.FORWARD_PIPE_COOLANT_PRESSURE: column_names.FORWARD_PIPE_COOLANT_PRESSURE,
            soft_m_column_names.BACKWARD_PIPE_COOLANT_PRESSURE: column_names.BACKWARD_PIPE_COOLANT_PRESSURE
        }

        self._water_temp_columns = (
            column_names.FORWARD_PIPE_COOLANT_TEMP,
            column_names.BACKWARD_PIPE_COOLANT_TEMP
        )

    def set_timestamp_timezone_name(self, timezone_name):
        self._timestamp_timezone_name = timezone_name

    def set_timestamp_parse_patterns(self, patterns):
        self._timestamp_parse_patterns = patterns

    def set_need_circuits(self, need_circuits):
        self._need_circuits = need_circuits

    def parse_boiler_data(self, boiler_data):
        self._logger.debug("Loading data")
        boiler_df = pd.read_csv(boiler_data, sep=";", low_memory=False)

        self._logger.debug("Parsing data")

        boiler_df.rename(columns=self._columns_equal_names, inplace=True)
        boiler_df = self._exclude_unused_columns(boiler_df)
        self._rename_circuits(boiler_df)
        boiler_df = self._exclude_unused_circuits(boiler_df)
        self._parse_datetime(boiler_df)
        self._convert_values_to_float_right(boiler_df)
        self._divide_incorrect_hot_water_temp(boiler_df)

        return boiler_df

    # noinspection PyMethodMayBeStatic
    def _exclude_unused_columns(self, boiler_df):
        self._logger.debug("Excluding unused columns")

        boiler_df = boiler_df[[
            column_names.TIMESTAMP,
            column_names.CIRCUIT_ID,
            column_names.FORWARD_PIPE_COOLANT_TEMP,
            column_names.BACKWARD_PIPE_COOLANT_TEMP,
            column_names.FORWARD_PIPE_COOLANT_VOLUME,
            column_names.BACKWARD_PIPE_COOLANT_VOLUME,
            column_names.FORWARD_PIPE_COOLANT_PRESSURE,
            column_names.BACKWARD_PIPE_COOLANT_PRESSURE
        ]]
        return boiler_df

    # noinspection PyMethodMayBeStatic
    def _rename_circuits(self, boiler_df):
        self._logger.debug("Renaming circuits")

        boiler_df[column_names.CIRCUIT_ID] = boiler_df[column_names.CIRCUIT_ID].apply(
            lambda soft_m_circuit: self._circuits_equal_id.get(soft_m_circuit, soft_m_circuit)
        )

    def _exclude_unused_circuits(self, boiler_df):
        self._logger.debug("Excluding unused circuits")

        boiler_df = boiler_df[boiler_df[column_names.CIRCUIT_ID].isin(self._need_circuits)]
        return boiler_df

    def _parse_datetime(self, boiler_df: pd.DataFrame):
        self._logger.debug("Parsing datetime")

        boiler_data_timezone = gettz(self._timestamp_timezone_name)
        boiler_df[column_names.TIMESTAMP] = boiler_df[column_names.TIMESTAMP].apply(
            parse_datetime, args=(self._timestamp_parse_patterns, boiler_data_timezone)
        )

    # noinspection PyMethodMayBeStatic
    def _convert_values_to_float_right(self, boiler_df):
        self._logger.debug("Converting values to float")

        for column_name in self._need_to_float_convert_columns:
            boiler_df[column_name] = boiler_df[column_name].apply(float_converter)

    # noinspection PyMethodMayBeStatic
    def _divide_incorrect_hot_water_temp(self, boiler_df):
        self._logger.debug("Dividing incorrect water temp")

        for column_name in self._water_temp_columns:
            boiler_df[column_name] = boiler_df[column_name].apply(
                lambda water_temp: water_temp > 120 and water_temp / 100 or water_temp
            )
