import matplotlib.pyplot as plt


def plot_heating_system_node_data(x_data, y_datas,
                                  x_label="Дата",
                                  y_label="Температура, град.",
                                  data_labels=["Температура {}"],
                                  colors=["red", "green", "blue", "yellow"],
                                  who_temp="\u00B0C",
                                  font_size=15,
                                  title=""):
    plt.gcf().canvas.manager.set_window_title(title)

    ax = plt.axes()
    ax.set_title(title)

    ax.set_xlabel(x_label, fontsize=font_size)
    ax.set_ylabel(y_label, fontsize=font_size)

    for i in range(0, len(y_datas)):
        ax.plot(x_data, y_datas[i], label=data_labels[i].format(who_temp), color=colors[i])

    ax.grid(True)
    ax.legend()
    plt.show()
