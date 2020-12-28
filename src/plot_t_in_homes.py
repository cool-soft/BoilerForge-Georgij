
import datetime

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from config import (
    DEFAULT_PREPROCESSED_HOMES_DATASETS_DIR,
    DEFAULT_PREPROCESSED_WEATHER_DATASET_PATH,
    DEFAULT_PREPROCESSED_BOILER_DATASET_PATH
)
from utils.io_utils import load_dataset
from utils.preprocess_utils import average_values

if __name__ == '__main__':
    min_date = datetime.datetime(2019, 2, 1, 0, 0, 0)
    max_date = datetime.datetime(2019, 3, 1, 0, 0, 0)

    t_in_homes_smooth_size = 100
    allowed_homes = [0, 1, 2, 3]  # [0, 1, 2, 3, 4, 5, 6, 7, 9]

    dates, x = load_dataset(DEFAULT_PREPROCESSED_HOMES_DATASETS_DIR, min_date, max_date)
    _, y = load_dataset(DEFAULT_PREPROCESSED_BOILER_DATASET_PATH, min_date, max_date)
    # _, weather_t = load_dataset(dst_weather_t_file, min_date, max_date)
    # _, second_t = load_dataset(dst_second_t_file, min_date, max_date)

    register_matplotlib_converters()

    ax = plt.axes()

    # ax.plot(dates, weather_t, label="weather t")
    ax.plot(dates, y, label="real boiler t")

    x = x.T
    for i, t in enumerate(x):
        if i in allowed_homes:
            t = average_values(t, t_in_homes_smooth_size)
            ax.plot(dates, t, label="home #{}".format(i))

    ax.grid(True)
    ax.legend()
    plt.show()
