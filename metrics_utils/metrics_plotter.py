import numpy as np
from matplotlib import pyplot as plt


# noinspection SpellCheckingInspection
class MetricsPlotter:

    def __init__(self):
        self._label_font_size = 11
        self._ylabel = 'Значение метрики'
        self._xlabel = 'Итерация'

    def set_xlabel(self, xlabel):
        self._xlabel = xlabel

    def set_ylabel(self, ylabel):
        self._ylabel = ylabel

    def set_label_font_size(self, font_size):
        self._label_font_size = font_size

    def plot_model_metrics(self, model_metrics):
        grouped_metrics, standalone_metrics = group_model_metrics(model_metrics)
        metrics_count = len(grouped_metrics) + len(standalone_metrics)
        grid_size = (1, metrics_count)

        row_number = 0
        column_number = 0
        for metric_group in grouped_metrics:
            ax = self._get_ax_for_model(grid_size, row_number, column_number)
            for metric in metric_group:
                metric_name, metric_data = metric
                plot_metric(ax, metric_data, metric_name)
            column_number += 1

        for metric in standalone_metrics:
            ax = self._get_ax_for_model(grid_size, row_number, column_number)
            metric_name, metric_data = metric
            plot_metric(ax, metric_data, metric_name)
            column_number += 1

        plt.subplots_adjust(hspace=0.5)
        plt.show()

    def _get_ax_for_model(self, grid_size, i, j):
        ax = plt.subplot2grid(grid_size, (i, j))
        ax.set_ylabel(self._ylabel, fontsize=self._label_font_size)
        ax.set_xlabel(self._xlabel, fontsize=self._label_font_size)
        ax.grid(True)
        return ax


def group_model_metrics(model_metrics):
    train_metrics = {}
    validation_metrics = {}
    for metric_name, metric_data in model_metrics.items():
        if metric_name.startswith("val_"):
            validation_metrics[metric_name] = metric_data
        else:
            train_metrics[metric_name] = metric_data

    metrics_groups = []
    standalone_metrics = []
    for metric_name, metric_data in train_metrics.items():
        metric_group = []
        val_metric_name = "val_{}".format(metric_name)
        if val_metric_name in validation_metrics:
            metric_group.append([metric_name, metric_data])
            metric_group.append([val_metric_name, validation_metrics[val_metric_name]])
            del validation_metrics[val_metric_name]
        else:
            standalone_metrics.append([metric_name, metric_data])
        if metric_group:
            metrics_groups.append(metric_group)

    for metric_name, metric_data in validation_metrics.items():
        standalone_metrics.append([metric_name, metric_data])

    return metrics_groups, standalone_metrics


def plot_metric(ax, metric_data, metric_name):
    x = np.arange(1, len(metric_data) + 1)
    ax.plot(x, metric_data, label=metric_name)
    ax.legend()
