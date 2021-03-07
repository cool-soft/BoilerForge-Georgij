import pickle
import pandas as pd


def load_dataset(filepath) -> pd.DataFrame:
    with open(filepath, "rb") as f:
        df = pickle.load(f)
    return df
