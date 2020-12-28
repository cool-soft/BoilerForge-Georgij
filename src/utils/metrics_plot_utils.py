
import numpy as np
from matplotlib import pyplot as plt


def plot_model_metrics(model_name, model_metrics, font_size=11):
    grouped_metrics, standalone_metrics = group_model_metrics(model_metrics)
    metrics_count = len(grouped_metrics) + len(standalone_metrics)
    grid_size = (1, metrics_count)

    j = 0
    for metric_group in grouped_metrics:
        ax = get_ax_for_model(grid_size, 0, j, font_size, model_name)
        for metric in metric_group:
            metric_name, metric_data = metric
            plot_metric(ax, metric_data, metric_name)
        j += 1

    for metric in standalone_metrics:
        ax = get_ax_for_model(grid_size, 0, j, font_size, model_name)
        metric_name, metric_data = metric
        plot_metric(ax, metric_data, metric_name)
        j += 1

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def get_ax_for_model(grid_size, i, j, font_size, model_name):
    ax = plt.subplot2grid(grid_size, (i, j))
    ax.set_title(model_name, fontsize=font_size)
    ax.set_xlabel('iteration', fontsize=font_size)
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
