from keras import backend as keras_backend


def relative_error(y_true, y_predicted):
    return keras_backend.mean(keras_backend.abs((y_predicted - y_true)) / y_true)

