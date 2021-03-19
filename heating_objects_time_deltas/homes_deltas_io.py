import pandas as pd


def load_homes_time_deltas(filepath):
    time_deltas = pd.read_csv(filepath)
    return time_deltas
