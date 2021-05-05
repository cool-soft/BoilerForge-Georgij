# noinspection PyUnresolvedReferences
import init_cuda11

import logging
import os
import tempfile
import pandas as pd
from dateutil.tz import gettz

from tensorflow.python.keras.layers import LSTM
import numpy as np
from boiler.constants import column_names
from boiler.heating_obj.io.sync_heating_obj_file_loader import SyncHeatingObjFileLoader
from boiler.heating_obj.io.sync_heating_obj_pickle_reader import SyncHeatingObjPickleReader
from boiler.time_delta.io.sync_timedelta_csv_reader import SyncTimedeltaCSVReader
from boiler.time_delta.io.sync_timedelta_file_loader import SyncTimedeltaFileLoader
from boiler_softm.constants import time_tick
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import Dropout, Input

import config

MAX_TRAIN_EPOCH = 400
BATCH_SIZE = 80000

START_TIMESTAMP = pd.Timestamp(year=2018, month=12, day=1, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))
END_TIMESTAMP = pd.Timestamp(year=2019, month=4, day=1, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))
VAL_START_TIMESTAMP = pd.Timestamp(year=2019, month=4, day=1, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))
VAL_END_TIMESTAMP = pd.Timestamp(year=2019, month=5, day=1, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))


def main():
    checkpoint_filepath = f"{tempfile.gettempdir()}\\keras_checkpoint"

    timedelta_df = get_timedelta_df(config.HEATING_OBJ_TIMEDELTA_PATH)

    boiler_forward_temp = get_forward_temp(
        config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH,
        START_TIMESTAMP,
        END_TIMESTAMP
    )
    boiler_forward_temp_val = get_forward_temp(
        config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH,
        VAL_START_TIMESTAMP,
        VAL_END_TIMESTAMP
    )

    logging.debug(f"Searching homes datasets in "
                  f"{config.APARTMENT_HOUSE_PREPROCESSED_DATASETS_HEATING_CIRCUIT_DIR}")
    trained_models = {}
    for filename_with_ext in os.listdir(config.APARTMENT_HOUSE_PREPROCESSED_DATASETS_HEATING_CIRCUIT_DIR):
        dataset_name, ext = os.path.splitext(filename_with_ext)
        logging.debug(f"Processing {dataset_name}")

        filepath = os.path.join(
            config.APARTMENT_HOUSE_PREPROCESSED_DATASETS_HEATING_CIRCUIT_DIR,
            filename_with_ext
        )

        apartment_house_forward_temp = get_forward_temp(filepath, START_TIMESTAMP, END_TIMESTAMP)
        apartment_house_forward_temp_val = get_forward_temp(filepath, VAL_START_TIMESTAMP, VAL_END_TIMESTAMP)

        heating_obj_timedelta = get_timedelta_in_tick(dataset_name, timedelta_df)
        x, y = get_x_y(boiler_forward_temp, apartment_house_forward_temp, heating_obj_timedelta)
        x_val, y_val = get_x_y(boiler_forward_temp_val, apartment_house_forward_temp_val, heating_obj_timedelta)

        model = get_model()
        model_checkpoint_callback = get_model_save_cb(checkpoint_filepath)
        model.fit(
            x=x,
            y=y,
            validation_data=(x_val, y_val),
            verbose=2,
            epochs=MAX_TRAIN_EPOCH,
            callbacks=[model_checkpoint_callback],
            batch_size=BATCH_SIZE
        )
        model.load_weights(checkpoint_filepath)
        trained_models[dataset_name] = model

    corr_table: pd.DataFrame = get_corr_table_for_models(trained_models)
    corr_table.to_csv(config.TEMP_CORRELATION_TABLE_PATH+".csv", index=False, sep=";")
    corr_table.to_pickle(config.TEMP_CORRELATION_TABLE_PATH, index=False, sep=";")


def get_timedelta_df(filepath):
    logging.debug(f"Loading timedelta df from {filepath}")
    reader = SyncTimedeltaCSVReader()
    loader = SyncTimedeltaFileLoader(
        reader=reader,
        filepath=filepath
    )
    timedelta_df = loader.load_timedelta()
    return timedelta_df


def get_forward_temp(filepath, start_timestamp, end_timestamp):
    logging.debug(f"Loading forward temp {start_timestamp}:{end_timestamp} from {filepath}")

    reader = SyncHeatingObjPickleReader()
    dataset_loader = SyncHeatingObjFileLoader(
        reader=reader,
        filepath=filepath
    )
    df = dataset_loader.load_heating_obj(start_timestamp, end_timestamp)
    forward_temp = df[column_names.FORWARD_PIPE_COOLANT_TEMP].to_numpy()
    return forward_temp


def get_timedelta_in_tick(dataset_name, timedelta_df):
    logging.debug(f"Calculating timedelta in tick for {dataset_name}")

    heating_obj_timedelta = \
        timedelta_df[timedelta_df[column_names.HEATING_OBJ_ID] == dataset_name][column_names.AVG_TIMEDELTA]
    heating_obj_timedelta = heating_obj_timedelta.to_list()
    heating_obj_timedelta = heating_obj_timedelta.pop()
    heating_obj_timedelta = heating_obj_timedelta // time_tick.TIME_TICK
    heating_obj_timedelta = int(heating_obj_timedelta)

    logging.debug(f"Timedelta of {dataset_name} is {heating_obj_timedelta}")
    return heating_obj_timedelta


# def get_model():
#     model = Sequential()
#     model.add(Input(shape=(1,)))
#     model.add(Dense(units=128, activation="relu"))
#     model.add(Dropout(rate=0.2))
#     model.add(Dense(units=64, activation="relu"))
#     model.add(Dropout(rate=0.2))
#     model.add(Dense(units=32, activation="relu"))
#     model.add(Dropout(rate=0.2))
#     model.add(Dense(units=1, activation="linear"))
#     model.compile(optimizer="adam", loss="mae", metrics=["mae"])
#     return model


def get_model(window_size=1):
    model = Sequential()
    model.add(LSTM(60, return_sequences=True, activation="relu", input_shape=(1, window_size)))
    model.add(LSTM(20, activation="relu"))
    model.add(Dense(1, activation='linear'))
    model.compile(
        optimizer='adam',
        loss='mae',
        metrics=['mae']
    )
    return model


def get_model_save_cb(filepath):
    logging.debug(f"Creating model checkpoint cb {filepath}")
    return ModelCheckpoint(
        filepath=filepath,
        save_weights_only=True,
        monitor='mae',
        mode='min',
        save_best_only=True
    )


def get_x_y(boiler_value: np.array, apartment_house_value: np.array, timedelta_in_tick: int):
    boiler_value = boiler_value[:-timedelta_in_tick]
    boiler_value = boiler_value.reshape((len(boiler_value), 1, 1))
    apartment_house_value = apartment_house_value[timedelta_in_tick:]
    apartment_house_value = apartment_house_value.reshape((len(apartment_house_value), 1, 1))
    return boiler_value, apartment_house_value


def get_corr_table_for_models(trained_models):
    x = np.arange(0, 100, 0.05)
    corr_table = {column_names.CORRELATED_BOILER_TEMP: x}
    x_reshaped = x.reshape((len(x), 1, 1))
    for model_name, model in trained_models.items():
        y = model.predict(x_reshaped)
        y = y.reshape(len(y))
        corr_table[model_name] = y
    return pd.DataFrame(corr_table)


if __name__ == '__main__':
    main()
