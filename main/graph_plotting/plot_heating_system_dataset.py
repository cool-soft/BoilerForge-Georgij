import datetime

import matplotlib.pyplot as plt
from dateutil.tz import gettz
from pandas.plotting import register_matplotlib_converters

from main import config
from heating_system_utils.constants import column_names
from heating_system.preprocess_utils import average_values, filter_by_timestamp_closed
from heating_system_utils.boiler_dataset_io import load_dataset

if __name__ == '__main__':
    start_datetime = datetime.datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    end_datetime = datetime.datetime(2019, 3, 1, 0, 0, 0, tzinfo=gettz(config.TIMEZONE))
    # dataset_path = config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH
    dataset_path = f"{config.HOMES_PREPROCESSED_HEATING_CIRCUIT_DATASETS_DIR}\\engelsa_37.csv.pickle"

    register_matplotlib_converters()
    ax = plt.axes()

    columns_to_plot = (
        column_names.FORWARD_PIPE_COOLANT_TEMP,
        # column_names.BACKWARD_PIPE_COOLANT_TEMP,
        # column_names.FORWARD_PIPE_COOLANT_VOLUME,
        # column_names.BACKWARD_PIPE_COOLANT_VOLUME,
        # column_names.FORWARD_PIPE_COOLANT_PRESSURE,
        # column_names.BACKWARD_PIPE_COOLANT_PRESSURE
    )

    loaded_dataset = load_dataset(dataset_path)
    loaded_dataset = filter_by_timestamp_closed(loaded_dataset, start_datetime, end_datetime)

    for column_name in columns_to_plot:
        data_to_plot = loaded_dataset[column_name]
        # data_to_plot = average_values(data_to_plot, 100)
        ax.plot(loaded_dataset[column_names.TIMESTAMP], data_to_plot, label=column_name)

    ax.grid(True)
    ax.legend()
    plt.show()
