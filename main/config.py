import datetime

from dateutil.tz import gettz

from heating_system_utils.constants import circuits_id, column_names

BOILER_TEMP_SMOOTH_SIZE = 100

TIMEZONE = "Asia/Yekaterinburg"
START_DATETIME = datetime.datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz(TIMEZONE))
END_DATETIME = datetime.datetime(2019, 6, 1, 0, 0, 0, tzinfo=gettz(TIMEZONE))

MODELS_DIR = "storage/saved_models"
MODEL_METRICS_FILENAME = "history"
MODEL_FILE_SUFFIX = "_model"

PREPROCESSED_DATASET_FILENAME_SUFFIX = ".pickle"

HOME_DISABLED_TEMP_THRESHOLD = 0

#############################################################
#############################################################
#############################################################

HOMES_SRC_DATASETS_DIR = "storage/datasets/src/homes"
HOMES_PREPROCESSED_HEATING_CIRCUIT_DATASETS_DIR = "storage/datasets/preprocessed/homes_heating_circuit"
HOMES_PREPROCESSED_WATER_CIRCUIT_DATASETS_DIR = "storage/datasets/preprocessed/homes_water_circuit"

HOME_DATA_TIMEZONE = "Asia/Yekaterinburg"
HOME_TIMESTAMP_PATTERNS = (
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2}).{7}",
    r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<hours>\d{1,2}):(?P<minutes>\d{2})"
)
HOME_REQUIRED_CIRCUITS = (
    circuits_id.HEATING_CIRCUIT,
)
HOME_REQUIRED_COLUMNS = (
    column_names.TIMESTAMP,
    column_names.CIRCUIT_ID,
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
)
HOME_NEED_TO_FLOAT_CONVERT_COLUMNS = (
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP
)

HOME_COLUMNS_TO_INTERPOLATE = (
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP
)

#####################################################

BOILER_SRC_DATASET_PATH = "storage/datasets/src/Boilers308_2.csv"
BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH = "storage/datasets/preprocessed/boiler_heating_circuit.pickle"
BOILER_PREPROCESSED_WATER_CIRCUIT_DATASET_PATH = "storage/datasets/preprocessed/boiler_water_circuit.pickle"

BOILER_DATA_TIMEZONE = "Asia/Yekaterinburg"
BOILER_TIMESTAMP_PATTERNS = (
    r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2}).{7}",
    r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<hours>\d{1,2}):(?P<minutes>\d{2})"
)
BOILER_REQUIRED_CIRCUITS = (
    circuits_id.HEATING_CIRCUIT,
)
BOILER_REQUIRED_COLUMNS = (
    column_names.TIMESTAMP,
    column_names.CIRCUIT_ID,
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
    column_names.FORWARD_PIPE_COOLANT_VOLUME,
    column_names.BACKWARD_PIPE_COOLANT_VOLUME,
    column_names.FORWARD_PIPE_COOLANT_PRESSURE,
    column_names.BACKWARD_PIPE_COOLANT_PRESSURE
)
BOILER_NEED_TO_FLOAT_CONVERT_COLUMNS = (
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
    column_names.FORWARD_PIPE_COOLANT_VOLUME,
    column_names.BACKWARD_PIPE_COOLANT_VOLUME,
    column_names.FORWARD_PIPE_COOLANT_PRESSURE,
    column_names.BACKWARD_PIPE_COOLANT_PRESSURE
)

BOILER_COLUMNS_TO_INTERPOLATE = (
    column_names.FORWARD_PIPE_COOLANT_TEMP,
    column_names.BACKWARD_PIPE_COOLANT_TEMP,
    column_names.FORWARD_PIPE_COOLANT_VOLUME,
    column_names.BACKWARD_PIPE_COOLANT_VOLUME,
    column_names.FORWARD_PIPE_COOLANT_PRESSURE,
    column_names.BACKWARD_PIPE_COOLANT_PRESSURE
)

#############################################################
#############################################################

WEATHER_DATA_TIMEZONE = "Asia/Yekaterinburg"
WEATHER_SRC_DATASET_PATH = "storage/datasets/src/weather_data.json"
WEATHER_PREPROCESSED_DATASET_PATH = "storage/datasets/preprocessed/weather_temp.pickle"

HOMES_TIME_DELTAS_PATH = "storage/homes_time_delta.csv"
TEMP_CORRELATION_TABLE_PATH = "storage/optimized_temp_table.pickle"

TEMP_GRAPH_PATH = "storage/temp_graph.csv"

HOME_MIN_TEMP_COEFFICIENT = 0.97
PREDICTED_BOILER_TEMP_PATH = "storage/predicted_boiler_temp.pickle"

BEST_MODEL_FILENAME = "best"
