import pickle


def load_temp_correlation_table(path):
    with open(path, "rb") as f:
        df = pickle.load(f)
    return df
