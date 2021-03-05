
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

import config
from heating_system import column_names
from model_utils.simple_model_utils.simple_model_io import load_temp_correlation_table

if __name__ == '__main__':

    temp_correlation_table = load_temp_correlation_table(config.TEMP_CORRELATION_TABLE_PATH)

    boiler_temp = temp_correlation_table[column_names.BOILER_OUT_TEMP].to_numpy()
    homes_temps = temp_correlation_table.copy()
    del homes_temps[column_names.BOILER_OUT_TEMP]

    register_matplotlib_converters()
    ax = plt.axes()
    for home_name in homes_temps.columns.values.tolist():
        home_temp = homes_temps[home_name].to_numpy()
        ax.plot(boiler_temp, home_temp, label=home_name)

    ax.set_xlabel('Температура бойлера, Град.')
    ax.set_ylabel('Температура на входе в дома, Град.')
    ax.set_title('Зависимость температур')

    ax.grid(True)
    ax.legend()

    plt.show()
