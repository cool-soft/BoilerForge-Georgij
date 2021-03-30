
import numpy as np
from matplotlib import pyplot as plt


def plot_real_and_predicted(dates, real, predicted, who_temp, font_size=15):
    abs_delta = np.abs(predicted - real)

    ax = plt.axes()

    ax.set_xlabel('Дата', fontsize=font_size)
    ax.set_ylabel('Температура, град.', fontsize=font_size)

    ax.plot(dates, real, label="Реальная температура {}".format(who_temp), color="red")
    ax.plot(dates, predicted, label="Рассчитаная температура {}".format(who_temp), color="blue")
    ax.plot(dates, abs_delta, label="Разница по модулю", color="green")

    ax.grid(True)
    ax.legend()
    plt.show()


def print_min_max_mean_delta(y1, y2):
    abs_delta = np.abs(y1 - y2)
    min_delta = np.min(abs_delta)
    max_delta = np.max(abs_delta)
    # noinspection PyUnresolvedReferences
    mean_delta = np.mean(abs_delta)
    print(f"MIN: {min_delta}, MAX: {max_delta}, MEAN: {mean_delta}")
