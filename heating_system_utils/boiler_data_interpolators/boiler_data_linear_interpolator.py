import logging
from datetime import timedelta

import pandas as pd

from heating_system.preprocess_utils import round_datetime
from heating_system_utils.constants import column_names
from .boiler_data_interpolator import BoilerDataInterpolator


class BoilerDataLinearInterpolator(BoilerDataInterpolator):

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug("Creating instance of the service")

        self._columns_to_interpolate = [
            column_names.FORWARD_PIPE_COOLANT_TEMP,
            column_names.BACKWARD_PIPE_COOLANT_TEMP,
            column_names.FORWARD_PIPE_COOLANT_VOLUME,
            column_names.BACKWARD_PIPE_COOLANT_VOLUME,
            column_names.FORWARD_PIPE_COOLANT_PRESSURE,
            column_names.BACKWARD_PIPE_COOLANT_PRESSURE
        ]
        self._interpolation_step = timedelta(seconds=180)

    def set_columns_to_interpolate(self, columns):
        self._columns_to_interpolate = columns

    def set_interpolation_step(self, interpolation_step):
        self._interpolation_step = interpolation_step

    def interpolate_boiler_data(
            self,
            boiler_df: pd.DataFrame,
            start_datetime=None,
            end_datetime=None,
            inplace=False
    ) -> pd.DataFrame:
        self._logger.debug("Interpolating is requested")

        if not inplace:
            boiler_df = boiler_df.copy()

        self._round_datetime(boiler_df)

        boiler_df = self._interpolate_border_datetime(boiler_df, start_datetime, end_datetime)
        boiler_df.sort_values(by=column_names.TIMESTAMP, ignore_index=True, inplace=True)
        boiler_df = self._interpolate_passes_of_datetime(boiler_df)

        self._interpolate_border_data(boiler_df)
        self._interpolate_passes_of_data(boiler_df)

        return boiler_df

    def _round_datetime(self, boiler_df):
        self._logger.debug("Rounding datetime")

        interpolations_step_in_seconds = self._interpolation_step.total_seconds()
        boiler_df[column_names.TIMESTAMP] = boiler_df[column_names.TIMESTAMP].apply(
            lambda datetime_: round_datetime(datetime_, interpolations_step_in_seconds)
        )
        boiler_df.drop_duplicates(column_names.TIMESTAMP, inplace=True, ignore_index=True)

    # noinspection PyMethodMayBeStatic
    def _interpolate_border_datetime(self, boiler_df: pd.DataFrame, start_datetime, end_datetime):
        self._logger.debug("Interpolating border datetime values")

        if start_datetime is not None:
            start_datetime = round_datetime(start_datetime, self._interpolation_step.total_seconds())
            first_datetime_idx = boiler_df[column_names.TIMESTAMP].idxmin()
            first_row = boiler_df.loc[first_datetime_idx]
            first_datetime = first_row[column_names.TIMESTAMP]
            if first_datetime > start_datetime:
                boiler_df = boiler_df.append({column_names.TIMESTAMP: start_datetime}, ignore_index=True)

        if end_datetime is not None:
            end_datetime = round_datetime(end_datetime, self._interpolation_step.total_seconds())
            last_datetime_idx = boiler_df[column_names.TIMESTAMP].idxmax()
            last_row = boiler_df.loc[last_datetime_idx]
            last_datetime = last_row[column_names.TIMESTAMP]
            if last_datetime < end_datetime:
                boiler_df = boiler_df.append({column_names.TIMESTAMP: end_datetime}, ignore_index=True)

        return boiler_df

    def _interpolate_passes_of_datetime(self, boiler_df: pd.DataFrame):
        self._logger.debug("Interpolating passes of datetime")

        inserted_datetime = []
        previous_datetime = None
        for index, row in boiler_df.iterrows():
            if previous_datetime is None:
                previous_datetime = row[column_names.TIMESTAMP]
                continue
            next_datetime = row[column_names.TIMESTAMP]

            current_datetime = previous_datetime + self._interpolation_step
            while current_datetime < next_datetime:
                inserted_datetime.append({
                    column_names.TIMESTAMP: current_datetime
                })
                current_datetime += self._interpolation_step

            previous_datetime = next_datetime

        boiler_df = boiler_df.append(inserted_datetime, ignore_index=True)
        boiler_df.sort_values(by=column_names.TIMESTAMP, ignore_index=True, inplace=True)

        return boiler_df

    def _interpolate_border_data(self, boiler_df):
        self._logger.debug("Interpolating border data values")

        first_datetime_index = boiler_df[column_names.TIMESTAMP].idxmin()
        last_datetime_index = boiler_df[column_names.TIMESTAMP].idxmax()

        for column_to_interpolate in self._columns_to_interpolate:
            first_valid_index = boiler_df[column_to_interpolate].first_valid_index()
            if first_valid_index != first_datetime_index:
                first_valid_value = boiler_df.loc[first_valid_index, column_to_interpolate]
                boiler_df.loc[first_datetime_index, column_to_interpolate] = first_valid_value

            last_valid_index = boiler_df[column_to_interpolate].last_valid_index()
            if last_valid_index != last_datetime_index:
                last_valid_value = boiler_df.loc[last_valid_index, column_to_interpolate]
                boiler_df.loc[last_datetime_index, column_to_interpolate] = last_valid_value

    def _interpolate_passes_of_data(self, boiler_df):
        self._logger.debug("Interpolating passes of data")
        for column_to_interpolate in self._columns_to_interpolate:
            boiler_df[column_to_interpolate].interpolate(inplace=True)
