
import datetime

from pandas.plotting import register_matplotlib_converters

from config import (
    PREPROCESSED_BOILER_DATASET_PATH,
    PREPROCESSED_HOMES_DATASETS_DIR,
    PREPROCESSED_DATASET_FILENAME_SUFFIX
)
from utils.dataset_utils import create_sequences_smooth_delta
from utils.home_deltas_utils import get_timedelta_by_home_name
from utils.io_utils import load_dataset, load_saved_model
from utils.metrics import relative_error
from utils.predict_utils import plot_real_and_predicted
from utils.preprocessing import average_values

if __name__ == '__main__':
    min_date = datetime.datetime(2019, 2, 1, 0, 0, 0)
    max_date = datetime.datetime(2019, 2, 5, 0, 0, 0)

    average_size = 0  # 100
    batch_size = 500

    address = "engelsa_37.csv_2"
    model = ("engelsa_37.csv_2", "best")

    delta = get_timedelta_by_home_name(address)
    smooth_size = 0
    window_size = 20

    model_name, epoch_number = model
    model = load_saved_model(
        model_name,
        epoch_number,
        custom_objects={
            "relative_error": relative_error,
            # "custom_loss1": get_custom_loss1()
        }
    )

    real_boiler_df = load_dataset(PREPROCESSED_BOILER_DATASET_PATH, min_date, max_date)
    real_boiler_t = real_boiler_df["t1"].to_numpy()

    real_home_df = load_dataset(f"{PREPROCESSED_HOMES_DATASETS_DIR}\\{address}{PREPROCESSED_DATASET_FILENAME_SUFFIX}", min_date, max_date)
    real_home_t = real_home_df["t1"].to_numpy()

    real_boiler_t, real_home_t = create_sequences_smooth_delta(real_boiler_t, real_home_t, window_size, delta, smooth_size)

    predicted_t = model.predict(real_boiler_t, batch_size=batch_size, verbose=1)
    predicted_t = predicted_t.reshape(len(predicted_t))
    predicted_t = average_values(predicted_t, average_size)

    register_matplotlib_converters()

    dates = real_boiler_df["dTimeStamp"]
    dates = dates[window_size+delta:-window_size]
    real_home_t = real_home_t[:-window_size]
    predicted_t = predicted_t[window_size:]
    plot_real_and_predicted(dates, real_home_t, predicted_t, who_temp=address)
