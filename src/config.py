
import datetime

TIME_STEP = datetime.timedelta(0, 0, 0, 0, 3)  # 3 minutes

DEFAULT_BOILER_T_SMOOTH_SIZE = 100

DEFAULT_START_DATE = datetime.datetime(2018, 12, 1, 0, 0, 0)
DEFAULT_END_DATE = datetime.datetime(2019, 6, 1, 0, 0, 0)

DEFAULT_MODELS_DIR = "saved_models"
DEFAULT_HISTORY_FILENAME = "history"
DEFAULT_MODEL_FILE_SUFFIX = "_model"

DEFAULT_PREPROCESSED_DATASET_FILENAME_SUFFIX = ".pickle"

DEFAULT_SRC_HOMES_DATASETS_DIR = "datasets\\src\\t_in_homes"
DEFAULT_PREPROCESSED_HOMES_DATASETS_DIR = "datasets\\preprocessed\\homes"

DEFAULT_SRC_BOILER_DATASET_PATH = "datasets\\src\\Boilers308_2.csv"
DEFAULT_PREPROCESSED_BOILER_DATASET_PATH = "datasets\\preprocessed\\boiler_t.pickle"

DEFAULT_SRC_WEATHER_DATASET_PATH = "datasets\\src\\weather_t.json"
DEFAULT_PREPROCESSED_WEATHER_DATASET_PATH = "datasets\\preprocessed\\weather_t.pickle"
DEFAULT_T_GRAPH_PATH = "datasets\\t_graph.csv"

DEFAULT_HOMES_DELTAS_PATH = "datasets\\homes_time_delta.csv"

DEFAULT_OPTIMIZED_T_TABLE_PATH = "datasets\\optimized_t_table.pickle"
DEFAULT_PREDICTED_BOILER_T_PATH = "datasets\\predicted_boiler_t.pickle"

TIMESTAMP_COLUMN_NAME = "dTimeStamp"
BOILER_COLUMN_NAME = "BOILER"

DEFAULT_HOME_T_DISPERSION_COEFFICIENT = 0.97
