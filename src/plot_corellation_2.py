
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from column_names import TEMP_AT_BOILER_OUT
from utils.io_utils import load_optimized_t_table

if __name__ == '__main__':

    optimized_t_table = load_optimized_t_table()

    boiler_t = optimized_t_table[TEMP_AT_BOILER_OUT].to_numpy()
    del optimized_t_table[TEMP_AT_BOILER_OUT]

    register_matplotlib_converters()

    ax = plt.axes()

    for home_name in optimized_t_table.columns.values.tolist():
        ax.plot(boiler_t, optimized_t_table[home_name].to_numpy(), label=home_name)

    ax.set_xlabel('Температура бойлера, Град.')
    ax.set_ylabel('Температура на входе в дома, Град.')
    ax.set_title('Зависимость температур')

    ax.grid(True)
    ax.legend()

    plt.show()
