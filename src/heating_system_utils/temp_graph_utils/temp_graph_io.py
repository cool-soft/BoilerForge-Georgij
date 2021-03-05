import pandas as pd


def load_temp_graph(filepath):
    temp_graph_df = pd.read_csv(filepath)
    return temp_graph_df
