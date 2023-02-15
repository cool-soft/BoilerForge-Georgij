import pandas as pd
from matplotlib import pyplot as plt

import config

if __name__ == '__main__':
    allowed_homes = [
        # "engelsa_35",
        "engelsa_37",
        "gaydara_1",
        # "gaydara_22",
        # "gaydara_26",
        # "gaydara_28",
        # "gaydara_30",
        "gaydara_32",
        # "kuibysheva_10",
        # "kuibysheva_14",
        "kuibysheva_16",
        # "kuibysheva_8",
    ]

    model = pd.read_pickle(config.TEMP_CORRELATION_TABLE_PATH,)
    ax = plt.axes()
    for home_name in allowed_homes:
        new_df = model[["BOILER", home_name]].copy().sort_values("BOILER")
        boiler_array = new_df["BOILER"].to_numpy()
        home_array = new_df[home_name].to_numpy()
        ax.plot(boiler_array, home_array, label=home_name)
    ax.grid(True)
    ax.legend()
    plt.show()

