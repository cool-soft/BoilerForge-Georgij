import datetime

from keras import Input, Model, Sequential
from keras.layers import (Dense, Reshape, Bidirectional, LSTM)
from config import (
    BOILER_PREPROCESSED_DATASET_PATH,
    HOMES_PREPROCESSED_DATASETS_DIR
)
from utils.dataset_utils import (
    get_between_dates,
    get_address_number_by_name,
    create_sequences_2,
    get_home_dataset_by_address_number
)
from utils.home_deltas_utils import get_timedelta_by_home_name
from utils.io_utils import load_dataset, get_model_save_name
from utils.metrics import relative_error
from utils.train_utils import train_model


# noinspection PyShadowingNames
def get_model(window_size):
    model = Sequential()
    model.add(LSTM(
        60,
        return_sequences=True,
        activation="relu",
        input_shape=(1, window_size),
        # kernel_regularizer='l2',
        # dropout=0.2,
        # recurrent_dropout=0.2
        )
    )

    model.add(LSTM(
        20,
        # return_sequences=True,
        activation="relu",
        # kernel_regularizer='l2',
        # dropout=0.2,
        # recurrent_dropout=0.2
        )
    )

    model.add(Dense(1, activation='linear'))

    model.compile(
        optimizer='adam',
        loss='mean_squared_error',
        metrics=['mae', relative_error]
    )
    return model


if __name__ == '__main__':
    window_size = 20
    address = "gaydara_28.csv"
    save_interval = 25
    epoch_count = 100000
    batch_size = 100000
    model_name = "lstm_{}".format(address)

    min_date = datetime.datetime(2018, 12, 1, 0, 0, 0)
    max_date = datetime.datetime(2019, 4, 1, 0, 0, 0)

    val_min_date = datetime.datetime(2019, 4, 1, 0, 0, 0)
    val_max_date = datetime.datetime(2019, 5, 1, 0, 0, 0)

    start_epoch = 0
    model_save_name = get_model_save_name(model_name)
    print("Model save name: {}".format(model_save_name))

    model = get_model(window_size)

    home_number = get_address_number_by_name(address)
    delta = get_timedelta_by_home_name(home_number)

    full_x = load_dataset(BOILER_PREPROCESSED_DATASET_PATH)
    full_y = load_dataset(HOMES_PREPROCESSED_DATASETS_DIR)
    full_y = get_home_dataset_by_address_number(full_y, home_number)

    _, x = get_between_dates(full_x, min_date, max_date)
    _, y = get_between_dates(full_y, min_date, max_date)
    x_seq, y_seq = create_sequences_2(x, y, window_size, delta)

    _, x_val = get_between_dates(full_x, val_min_date, val_max_date)
    _, y_val = get_between_dates(full_y, val_min_date, val_max_date)
    x_val_seq, y_val_seq = create_sequences_2(x_val, y_val, window_size, delta)

    train_model(
        model,
        x_seq,
        y_seq,
        epoch_count,
        model_save_name,
        batch_size=batch_size,
        save_step=save_interval,
        start_epoch=start_epoch,
        validation_data=(x_val_seq, y_val_seq)
    )
