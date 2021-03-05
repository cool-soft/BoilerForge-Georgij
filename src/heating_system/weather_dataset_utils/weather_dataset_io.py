import pickle


def load_weather_dataset(filepath):
    with open(filepath, "rb") as f:
        weather_df = pickle.load(f)
    return weather_df
