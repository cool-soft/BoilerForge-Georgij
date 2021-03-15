import pickle
import pandas as pd


def load_heating_dataset(filepath: str) -> pd.DataFrame:
    with open(filepath, "rb") as f:
        df = pickle.load(f)
    return df
