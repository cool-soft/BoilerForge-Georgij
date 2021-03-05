
from keras import backend as keras_backend


def relative_error(y_true, y_pred):
    return keras_backend.mean(keras_backend.abs((y_pred - y_true)) / y_true)
