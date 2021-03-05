import column_names
from heating_system.homes_time_deltas_utils.homes_deltas_io import load_homes_time_deltas


def get_timedelta_by_home_name(home_name, filepath):
    time_deltas = load_homes_time_deltas(filepath)
    time_delta = time_deltas[time_deltas[column_names.HOME_NAME] == home_name]
    return time_delta
