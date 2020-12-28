import datetime

from dateutil.tz import gettz

BOILER_TEMP_SMOOTH_SIZE = 100

START_DATE = datetime.datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz("Asia/Yekaterinburg"))
END_DATE = datetime.datetime(2019, 6, 1, 0, 0, 0, tzinfo=gettz("Asia/Yekaterinburg"))

MODELS_DIR = "saved_models"
HISTORY_FILENAME = "history"
MODEL_FILE_SUFFIX = "_model"

WEATHER_DATA_TIMEZONE = "Asia/Yekaterinburg"

PREPROCESSED_DATASET_FILENAME_SUFFIX = ".pickle"

SRC_HOMES_DATASETS_DIR = "storage\\datasets\\src\\t_in_homes"
PREPROCESSED_HOMES_DATASETS_DIR = "storage\\datasets\\preprocessed\\homes"

SRC_BOILER_DATASET_PATH = "storage\\datasets\\src\\Boilers308_2.csv"
PREPROCESSED_BOILER_DATASET_PATH = "storage\\datasets\\preprocessed\\boiler_t.pickle"

SRC_WEATHER_DATASET_PATH = "storage\\datasets\\src\\weather_t.json"
PREPROCESSED_WEATHER_DATASET_PATH = "storage\\datasets\\preprocessed\\weather_t.pickle"

HOMES_DELTAS_PATH = "storage\\datasets\\homes_time_delta.csv"
TEMP_CORRELATION_TABLE_PATH = "storage\\datasets\\optimized_t_table.pickle"

TEMP_GRAPH_PATH = "storage\\datasets\\t_graph.csv"
HOME_MIN_TEMP_COEFFICIENT = 0.97
PREDICTED_BOILER_TEMP_PATH = "storage\\datasets\\predicted_boiler_t.pickle"
