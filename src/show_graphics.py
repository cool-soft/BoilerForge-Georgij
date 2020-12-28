
from utils.metrics_plot_utils import plot_model_metrics
from utils.io_utils import load_model_metrics

if __name__ == '__main__':
    # model_name = "lstm_4_2020-06-16-19.43.24"
    # model_name = "lstm_4_2020-06-17-00.50.37"
    # model_name = "lstm_4_2020-06-17-02.23.41"
    # model_name = "dense_1_(3d)_(t_h-t_b)_2020-06-22-00.20.04"
    # model_name = "dense_gaydara_28.csv_2020-08-23-03.13.39"
    model_name = "lstm_gaydara_28.csv_2020-08-23-04.26.47"

    model_metrics = load_model_metrics(model_name)
    plot_model_metrics(model_name, model_metrics)
