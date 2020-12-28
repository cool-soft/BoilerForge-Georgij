
import pandas as pd

from config import DEFAULT_HOMES_DELTAS_PATH


def get_timedelta_by_home_name(home_name, path=DEFAULT_HOMES_DELTAS_PATH):
    time_deltas = load_homes_time_deltas(path)
    time_delta = time_deltas[time_deltas["home_name"] == home_name]
    return time_delta


def load_homes_time_deltas(path=DEFAULT_HOMES_DELTAS_PATH):
    time_deltas = pd.read_csv(path)
    return time_deltas
