import pandas as pd
from dateutil.tz import gettz

#############################################################

DEFAULT_TIMEZONE = "Asia/Yekaterinburg"
SHARED_START_TIMESTAMP = pd.Timestamp(year=2018, month=12, day=1, hour=0, minute=0, tz=gettz(DEFAULT_TIMEZONE))
SHARED_END_TIMESTAMP = pd.Timestamp(year=2019, month=6, day=1, hour=0, minute=0, tz=gettz(DEFAULT_TIMEZONE))

#############################################################

STORAGE_PATH = "../shared_storage"
PREPROCESSED_DATASETS_PATH = f"{STORAGE_PATH}/datasets/preprocessed"
SRC_DATASETS_PATH = f"{STORAGE_PATH}/datasets/src"

#############################################################

APARTMENT_HOUSE_SRC_DATASETS_DIR = f"{SRC_DATASETS_PATH}/apartment_house"
APARTMENT_HOUSE_PREPROCESSED_DATASETS_HEATING_CIRCUIT_DIR = \
    f"{PREPROCESSED_DATASETS_PATH}/apartment_house_heating_circuit"
APARTMENT_HOUSE_PREPROCESSED_DATASETS_HOT_WATER_CIRCUIT_DIR = \
    f"{PREPROCESSED_DATASETS_PATH}/apartment_house_hot_water_circuit"

APARTMENT_HOUSE_DATA_TIMEZONE = DEFAULT_TIMEZONE

#####################################################

BOILER_SRC_DATASET_PATH = f"{SRC_DATASETS_PATH}/Boilers308_2.csv"
BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH = \
    f"{PREPROCESSED_DATASETS_PATH}/boiler_heating_circuit.pickle"
BOILER_PREPROCESSED_WATER_CIRCUIT_DATASET_PATH = \
    f"{PREPROCESSED_DATASETS_PATH}/boiler_water_circuit.pickle"

BOILER_DATA_TIMEZONE = DEFAULT_TIMEZONE

#############################################################

WEATHER_DATA_TIMEZONE = DEFAULT_TIMEZONE
WEATHER_SRC_DATASET_PATH = f"{SRC_DATASETS_PATH}/weather.json"
WEATHER_PREPROCESSED_DATASET_PATH = f"{PREPROCESSED_DATASETS_PATH}/weather.pickle"

HEATING_OBJ_TIMEDELTA_PATH = f"{STORAGE_PATH}/heating_obj_time_delta.csv"
TEMP_CORRELATION_TABLE_PATH = f"{STORAGE_PATH}/temp_correlation_table.pickle"

TEMP_GRAPH_PATH = f"{STORAGE_PATH}/temp_graph.csv"
