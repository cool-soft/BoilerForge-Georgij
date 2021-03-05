import json


def load_model_metrics(filepath):
    with open(filepath, "r") as f:
        model_metrics = json.load(f)
    return model_metrics


def save_model_metrics(metrics_history, filepath):
    with open(filepath, "w") as f:
        json.dump(metrics_history, f, indent=4)
