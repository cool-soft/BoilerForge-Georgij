import os
from datetime import datetime

import keras


def get_model_save_name(model_name):
    fit_start_time = datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    model_save_name = "{}_{}".format(model_name, fit_start_time)
    return model_save_name


def load_saved_model(model_filepath, custom_objects=None):
    from keras.engine.saving import load_model

    if custom_objects is None:
        custom_objects = {}

    model_filepath = os.path.abspath(model_filepath)
    model = load_model(model_filepath, custom_objects=custom_objects)

    return model


def get_model_save_cb(model_save_filepath, monitor="val_loss", mode="min"):
    model_save_cb = keras.callbacks.ModelCheckpoint(
        filepath=model_save_filepath,
        monitor=monitor,
        mode=mode,
        save_best_only=True
    )
    return model_save_cb
