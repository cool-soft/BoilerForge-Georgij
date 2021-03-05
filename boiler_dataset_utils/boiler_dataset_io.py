import pickle


def load_dataset(filepath):
    with open(filepath, "rb") as f:
        df = pickle.load(f)
    return df
