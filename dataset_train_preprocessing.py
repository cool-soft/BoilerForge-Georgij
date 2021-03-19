
import numpy as np
from main.config import TIME_TICK


def create_sequences(x, y, window_size, delta=0):
    sequences_count = len(x) - window_size - delta
    addresses_count = len(x[0])

    input_seq = np.empty(shape=(sequences_count, window_size, addresses_count))
    output_seq = np.empty(shape=(sequences_count,))
    for i in range(sequences_count):
        input_seq[i] = x[i + delta:i + window_size + delta]
        output_seq[i] = y[i]

    return input_seq, output_seq


def create_sequences_2(x, y, window_size, delta, reshape=True):
    sequences_count = len(x) - window_size - delta

    input_seq = np.empty(shape=(sequences_count, window_size))
    output_seq = np.empty(shape=(sequences_count, ))
    for i in range(sequences_count):
        input_seq[i] = x[i:i+window_size]
        output_seq[i] = y[i+window_size+delta]

    if reshape:
        input_seq = input_seq.reshape((sequences_count, 1, window_size))

    return input_seq, output_seq


def create_sequences_smooth_delta(boiler_t, home_t, window_size, delta, smooth_size):
    sequences_count = len(boiler_t) - window_size - delta

    boiler_t_seq = np.empty(shape=(sequences_count, window_size))
    for i in range(sequences_count):
        boiler_t_seq[i] = boiler_t[i:i + window_size]
    boiler_t_seq = boiler_t_seq.reshape((sequences_count, 1, window_size))

    home_t_seq = np.empty(shape=(sequences_count,))
    for i in range(sequences_count):
        home_t_seq[i] = home_t[i + window_size - smooth_size + delta]

    return boiler_t_seq, home_t_seq


def normalize_arrays(*datasets):
    max_val = -float("inf")
    min_val = float("inf")

    for dataset in datasets:
        min_val = min(min_val, np.min(dataset))
        max_val = max(max_val, np.max(dataset))

    normalized_datasets = []
    for dataset in datasets:
        dataset = dataset.copy()
        dataset -= min_val
        dataset /= max_val - min_val
        normalized_datasets.append(dataset)

    if len(normalized_datasets) == 1:
        return normalized_datasets[0]

    return normalized_datasets


def create_time_series(min_date, max_date, time_step=TIME_TICK):
    date = min_date
    time_series = []
    while date <= max_date:
        time_series.append(date)
        date += time_step
    return time_series
