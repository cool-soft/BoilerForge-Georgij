import config
from metrics_utils import MetricsPlotter
from metrics_utils import load_model_metrics

if __name__ == '__main__':
    # model_name = "lstm_4_2020-06-16-19.43.24"
    # model_name = "lstm_4_2020-06-17-00.50.37"
    # model_name = "lstm_4_2020-06-17-02.23.41"
    # model_name = "dense_1_(3d)_(t_h-t_b)_2020-06-22-00.20.04"
    # model_name = "dense_gaydara_28.csv_2020-08-23-03.13.39"
    model_name = "multi_lstm_2020-09-12-09.03.41\\engelsa_37.csv"

    filepath = "{}\\{}\\{}".format(config.MODELS_DIR, model_name, config.MODEL_METRICS_FILENAME)
    model_metrics = load_model_metrics(filepath)
    metrics_plotter = MetricsPlotter()
    metrics_plotter.plot_model_metrics(model_metrics)
