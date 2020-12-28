
import os

import keras

from utils.io_utils import save_history
from config import DEFAULT_MODELS_DIR, DEFAULT_MODEL_FILE_SUFFIX


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
        models_dir=DEFAULT_MODELS_DIR,
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

    save_history(history.history, model_name, models_dir=models_dir)


def get_model_save_cb(model_save_dir, save_step):

    if not save_step:
        model_save_filename = f"{model_save_dir}\\best{DEFAULT_MODEL_FILE_SUFFIX}"
        model_save_cb = keras.callbacks.ModelCheckpoint(
            filepath=model_save_filename,
            monitor='val_loss',
            mode='min',
            save_best_only=True
        )
    else:
        model_save_filename = f"{model_save_dir}\\{{}}{DEFAULT_MODEL_FILE_SUFFIX}"
        model_save_cb = keras.callbacks.ModelCheckpoint(
            filepath=model_save_filename,
            monitor='val_loss',
            mode='min',
            period=save_step
        )

    return model_save_cb
