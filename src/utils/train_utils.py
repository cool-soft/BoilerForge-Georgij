
import os

import keras

import config
from metrics_utils.metrics_io import save_model_metrics
from config import MODELS_DIR, MODEL_FILE_SUFFIX


# noinspection PyShadowingNames
def train_model(
        model,
        x,
        y,
        x_val,
        y_val,
        epoch_count,
        batch_size,
        model_name,
        models_dir=MODELS_DIR,
        save_step=0,
        verbose_mode=2
):

    model_save_dir = f"{models_dir}\\{model_name}"
    model_save_dir = os.path.abspath(model_save_dir)
    if not os.path.exists(model_save_dir):
        os.makedirs(model_save_dir)

    model_save_cb = get_model_save_cb(model_save_dir, save_step)

    history = model.fit(
        x=x,
        y=y,
        epochs=epoch_count,
        verbose=verbose_mode,
        batch_size=batch_size,
        validation_data=(x_val, y_val),
        callbacks=[model_save_cb]
    )

    model_dir = "{}\\{}".format(models_dir, model_name)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    filepath = "{}\\{}".format(models_dir, config.MODEL_METRICS_FILENAME)
    save_model_metrics(history.history, filepath)


def get_model_save_cb(model_save_dir, save_step):

    if not save_step:
        model_save_filename = f"{model_save_dir}\\best{MODEL_FILE_SUFFIX}"
        model_save_cb = keras.callbacks.ModelCheckpoint(
            filepath=model_save_filename,
            monitor='val_loss',
            mode='min',
            save_best_only=True
        )
    else:
        model_save_filename = f"{model_save_dir}\\{{}}{MODEL_FILE_SUFFIX}"
        model_save_cb = keras.callbacks.ModelCheckpoint(
            filepath=model_save_filename,
            monitor='val_loss',
            mode='min',
            period=save_step
        )

    return model_save_cb
