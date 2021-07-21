import os

import numpy as np
import pandas as pd
from boiler.constants import column_names
from boiler.constants.column_names import TIMESTAMP
from dateutil.tz import gettz

import config
from predict_utils import plot_real_and_predicted
from train_corr_table_model import get_forward_temp, get_timedelta_in_tick, get_x_y, get_timedelta_df, get_times

START_TIMESTAMP = pd.Timestamp(year=2021, month=4, day=12, hour=22, minute=30, tz=gettz(config.DEFAULT_TIMEZONE))
END_TIMESTAMP = pd.Timestamp(year=2021, month=4, day=26, hour=1, minute=36, tz=gettz(config.DEFAULT_TIMEZONE))


def calc_coolant_temp_for_object(temp_correlation_df, obj_id: str, boiler_temp: float) -> float:
    temps = temp_correlation_df[
        temp_correlation_df[column_names.CORRELATED_BOILER_TEMP] <= boiler_temp
        ]
    forward_pipe_temp = temps[obj_id].max()
    return forward_pipe_temp


def plot_house_difference(house: str = "17_.pickle"):
    correlation_df = pd.read_pickle(os.path.join("../", config.TEMP_CORRELATION_TABLE_PATH))

    timedelta_df = get_timedelta_df(os.path.join("../", config.HEATING_OBJ_TIMEDELTA_PATH))

    boiler_forward_temp = get_forward_temp(
        os.path.join("../", config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH),
        START_TIMESTAMP,
        END_TIMESTAMP
    )

    dataset_name, ext = os.path.splitext(house)
    filepath = os.path.join(
        os.path.join("../", config.APARTMENT_HOUSE_PREPROCESSED_DATASETS_HEATING_CIRCUIT_DIR),
        house
    )
    apartment_house_forward_temp = get_forward_temp(filepath, START_TIMESTAMP, END_TIMESTAMP)
    heating_obj_timedelta = get_timedelta_in_tick(dataset_name, timedelta_df)
    boiler_value, apartment_house_value = get_x_y(boiler_forward_temp, apartment_house_forward_temp,
                                                  heating_obj_timedelta)
    dates = get_times(
        os.path.join("../", config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH),
        START_TIMESTAMP,
        END_TIMESTAMP
    )

    predicted: list = []

    for boiler_temp in boiler_forward_temp:
        apartment_house_temp = calc_coolant_temp_for_object(
            temp_correlation_df=correlation_df,
            obj_id=dataset_name,
            boiler_temp=boiler_temp
        )
        predicted.append(apartment_house_temp)

    plot_real_and_predicted(
        dates=dates,
        real=apartment_house_value,
        predicted=predicted,
        who_temp="C"
    )


def main():
    plot_house_difference()


if __name__ == '__main__':
    main()
