import pandas as pd
from heating_objects_time_deltas.constants import column_names


def get_timedelta_by_home_name(home_name, filepath):
    time_deltas = pd.read_csv(filepath)
    time_delta = time_deltas[time_deltas[column_names.HOME_NAME] == home_name]
    return time_delta
