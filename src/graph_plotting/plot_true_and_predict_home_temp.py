import datetime

from pandas.plotting import register_matplotlib_converters

import column_names
import config

from dataset_utils.dataset_train_preprocessing import create_sequences_smooth_delta
from homes_time_deltas_utils.home_deltas_calculation import get_timedelta_by_home_name
from dataset_utils.dataset_io import load_dataset
from homes_time_deltas_utils.homes_deltas_io import load_homes_time_deltas
from model_utils.model_io import load_saved_model
from model_utils.model_metrics import relative_error
from predict_utils import plot_real_and_predicted
from preprocess_utils import average_values, filter_by_timestamp_closed

if __name__ == '__main__':
    min_date = datetime.datetime(2019, 2, 1, 0, 0, 0)
    max_date = datetime.datetime(2019, 2, 5, 0, 0, 0)

    average_size = 0  # 100
    batch_size = 500

    address = "engelsa_37.csv"
    model = ("engelsa_37.csv_2", "best")

    homes_time_deltas = load_homes_time_deltas(config.HOMES_TIME_DELTAS_PATH)
    delta = get_timedelta_by_home_name(address, homes_time_deltas)
    smooth_size = 0
    window_size = 20

    model_name, epoch_number = model
    model_filepath = f"{config.MODELS_DIR}\\{model_name}\\{epoch_number}{config.MODEL_FILE_SUFFIX}"
    model = load_saved_model(
        model_filepath,
        custom_objects={
            "relative_error": relative_error,
            # "custom_loss1": get_custom_loss1()
        }
    )

    real_boiler_df = load_dataset(config.BOILER_PREPROCESSED_DATASET_PATH)
    real_boiler_df = filter_by_timestamp_closed(real_boiler_df, min_date, max_date)
    real_boiler_temp = real_boiler_df[column_names.FORWARD_PIPE_TEMP].to_numpy()

    real_home_df = load_dataset(
        f"{config.HOMES_PREPROCESSED_DATASETS_DIR}\\"
        f"{address}{config.PREPROCESSED_DATASET_FILENAME_SUFFIX}"
    )
    real_home_df = filter_by_timestamp_closed(real_home_df, min_date, max_date)
    real_home_temp = real_home_df[column_names.FORWARD_PIPE_TEMP].to_numpy()

    real_boiler_temp, real_home_temp = create_sequences_smooth_delta(
        real_boiler_temp,
        real_home_temp,
        window_size,
        delta,
        smooth_size
    )

    predicted_home_temp = model.predict(real_boiler_temp, batch_size=batch_size, verbose=1)
    predicted_home_temp = predicted_home_temp.reshape(len(predicted_home_temp))
    predicted_home_temp = average_values(predicted_home_temp, average_size)

    register_matplotlib_converters()

    dates = real_boiler_df[column_names.TIMESTAMP]
    dates = dates[window_size + delta:-window_size]
    real_home_temp = real_home_temp[:-window_size]
    predicted_home_temp = predicted_home_temp[window_size:]
    plot_real_and_predicted(dates, real_home_temp, predicted_home_temp, who_temp=address)
