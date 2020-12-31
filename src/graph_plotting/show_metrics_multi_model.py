from utils.io_utils import load_model_metrics
from config import MODELS_DIR
import os


if __name__ == '__main__':
    # multi_model_name = "multi_lstm_2020-09-12-09.03.41"
    multi_model_name = "multi_lstm_2020-09-14-21.22.12"

    multi_model_dir = f"{MODELS_DIR}\\{multi_model_name}"
    for model_name in os.listdir(multi_model_dir):
        model_metrics = load_model_metrics(model_name, models_dir=multi_model_dir)
        model_metrics_mins = []
        for metric_name, metric_values in model_metrics.items():
            if not metric_name.startswith("val_"):
                continue
            min_value = float("inf")
            min_iter = 0
            for i, metric_value in enumerate(metric_values, start=1):
                if metric_value < min_value:
                    min_iter = i
                    min_value = metric_value
            model_metrics_mins.append(f"{metric_name}: {round(min_value, 2)} on {min_iter}")
        metrics_str = ", ".join(model_metrics_mins)
        print(f"{model_name}: {metrics_str}")
