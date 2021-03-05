
from keras import backend as K


def relative_error(y_true, y_pred):
    return K.mean(K.abs((y_pred - y_true)) / y_true)


def get_custom_loss1(l=2):
    def custom_loss1(y_true, y_pred):
        d = y_pred-y_true
        return K.mean(K.square(d)) * l * l ** K.sign(d)
    return custom_loss1
