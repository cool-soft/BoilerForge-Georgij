
import datetime

from matplotlib import pyplot as plt
import numpy as np

from utils.io_utils import load_dataset, load_saved_model
from utils.metrics import relative_error
from config import DEFAULT_PREPROCESSED_HOMES_DATASETS_DIR


def create_window_sequences(temp_arr, window_size):
    sequences_count = len(temp_arr) - window_size
    sequences_arr = np.empty(shape=(sequences_count, window_size))
    for i in range(sequences_count):
        sequences_arr[i, :] = temp_arr[i:i+window_size]
    return sequences_arr


def create_sequences_with_value_delta(sequences, start_idx, end_idx, value_delta):
    sequences_count, window_size = sequences.shape
    sub_sequences_count = end_idx - start_idx
    out_arr = np.empty(shape=(sequences_count, sub_sequences_count+1, window_size))
    for sequence_n in range(sequences_count):
        out_arr[sequence_n, 0] = sequences[sequence_n, :].copy()
        for value_n, sub_sequence_n in zip(range(start_idx, end_idx), range(1, sub_sequences_count+1)):
            sequence_tmp = sequences[sequence_n].copy()
            sequence_tmp[value_n] += value_delta
            out_arr[sequence_n, sub_sequence_n, :] = sequence_tmp
    return out_arr


def calc_division(original_output, output_with_deltas, value_delta):
    sequences_count, sub_sequences_count = output_with_deltas.shape
    out_arr = np.empty(sub_sequences_count)
    for sub_sequence_n in range(sub_sequences_count):
        out_arr[sub_sequence_n] = np.average((output_with_deltas[:, sub_sequence_n] - original_output) / value_delta)
    return out_arr


def main():
    min_date = datetime.datetime(2018, 1, 1, 0, 0, 0)
    max_date = datetime.datetime(2019, 4, 1, 0, 0, 0)

    batch_size = 100000

    window_size = 5
    smooth_size = 2
    model_name = "multi_lstm_2020-09-14-21.22.12\\engelsa_37.csv"
    dataset_name = "engelsa_37.csv.pickle"

    temp_delta = 20
    start_idx = 0
    end_idx = window_size

    df = load_dataset(f"{DEFAULT_PREPROCESSED_HOMES_DATASETS_DIR}\\{dataset_name}", min_date, max_date)
    temp = df["t1"].to_numpy()

    sequences = create_window_sequences(temp, window_size)
    sequences_with_delta = create_sequences_with_value_delta(sequences, start_idx, end_idx, temp_delta)

    model = load_saved_model(
        model_name,
        "best",
        custom_objects={
            "relative_error": relative_error,
        }
    )

    sequences_count = len(sequences)
    sub_sequences_count = end_idx - start_idx + 1
    sub_sequences = sequences_with_delta.reshape((sequences_count*sub_sequences_count, 1, window_size))
    model_output = model.predict(sub_sequences, batch_size=batch_size)
    model_output = model_output.reshape((sequences_count, sub_sequences_count))

    original_output = model_output[:, 0].copy()
    output_with_delta = model_output[:, 1:].copy()
    deltas_division = calc_division(original_output, output_with_delta, temp_delta)

    x = list(range(start_idx-window_size+smooth_size+1, end_idx-window_size+smooth_size+1))

    ax = plt.axes()
    ax.set_title(f"{model_name}, {min_date} - {max_date}")
    ax.grid(True)
    ax.set_xlabel('Время, тик', fontsize=15)
    ax.set_ylabel('Отношение вх. и вых. значений', fontsize=15)

    ax.plot(x, deltas_division, color="blue")
    # ax.legend()

    plt.show()


if __name__ == '__main__':
    main()
