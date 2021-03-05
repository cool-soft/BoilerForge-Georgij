import os

import config
from heating_system.metrics_utils.metrics_io import save_model_metrics


# noinspection PyShadowingNames
from heating_system.model_utils.model_io import get_model_save_cb


def train_model(
        model,
        x,
        y,
        x_val,
        y_val,
        epoch_count,
        batch_size,
        model_dir,
        verbose_mode=2
):

    model_dir = os.path.abspath(model_dir)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_save_filename = f"{model_dir}\\{config.MODEL_FILE_SUFFIX}"
    model_save_cb = get_model_save_cb(model_save_filename)

    model_metrics_history = model.fit(
        x=x,
        y=y,
        epochs=epoch_count,
        verbose=verbose_mode,
        batch_size=batch_size,
        validation_data=(x_val, y_val),
        callbacks=[model_save_cb]
    )

    metrics_filepath = "{}\\{}{}".format(
        model_dir, config.BEST_MODEL_FILENAME, config.MODEL_METRICS_FILENAME
    )
    save_model_metrics(model_metrics_history.history, metrics_filepath)


