import datetime

from dateutil.tz import gettz

BOILER_TEMP_SMOOTH_SIZE = 100

TIMEZONE = "Asia/Yekaterinburg"
START_DATETIME = datetime.datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz(TIMEZONE))
END_DATETIME = datetime.datetime(2019, 6, 1, 0, 0, 0, tzinfo=gettz(TIMEZONE))

MODELS_DIR = "storage\\saved_models"
MODEL_METRICS_FILENAME = "history"
MODEL_FILE_SUFFIX = "_model"


PREPROCESSED_DATASET_FILENAME_SUFFIX = ".pickle"

NTC = 1

HOME_DISABLED_TEMP_THRESHOLD = 0
HOME_DATA_TIMEZONE = "Asia/Yekaterinburg"
HOME_TIMESTAMP_PATTERNS = (
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2}).{7}",
    r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<hours>\d{1,2}):(?P<minutes>\d{2})"
)
HOMES_SRC_DATASETS_DIR = "storage\\datasets\\src\\homes"
HOMES_PREPROCESSED_DATASETS_DIR = "storage\\datasets\\preprocessed\\homes"

BOILER_DISABLED_TEMP_THRESHOLD = 0
BOILER_DATA_TIMEZONE = "Asia/Yekaterinburg"
BOILER_SRC_DATASET_PATH = "storage\\datasets\\src\\Boilers308_2.csv"
BOILER_PREPROCESSED_DATASET_PATH = "storage\\datasets\\preprocessed\\boiler_temp.pickle"
BOILER_TIMESTAMP_PATTERNS = (
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2}).{7}",
    r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<hours>\d{1,2}):(?P<minutes>\d{2})"
)

WEATHER_DATA_TIMEZONE = "Asia/Yekaterinburg"
WEATHER_SRC_DATASET_PATH = "storage\\datasets\\src\\weather_data.json"
WEATHER_PREPROCESSED_DATASET_PATH = "storage\\datasets\\preprocessed\\weather_temp.pickle"

HOMES_DELTAS_PATH = "storage\\homes_time_delta.csv"
TEMP_CORRELATION_TABLE_PATH = "storage\\optimized_temp_table.pickle"

TEMP_GRAPH_PATH = "storage\\temp_graph.csv"
HOME_MIN_TEMP_COEFFICIENT = 0.97
PREDICTED_BOILER_TEMP_PATH = "storage\\predicted_boiler_temp.pickle"
