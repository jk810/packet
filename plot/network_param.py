import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


def param(n_sats, route_step, show_plots, save_figs):
    current_file_path = Path(__file__)

    con_range = [x for x in range(3, 7)]
    hop_range = [y for y in range(3, 7)]
    results = [[], [], [], []]

    # Plotting
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set1.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'
    fig, ax = plt.subplots()
    markers = ['.', '^', 'x', '+']

    for hop in hop_range:
        for con in con_range:
            data_name = f'{n_sats}sat_{hop}hop_{con}con'
            data_path = str(current_file_path.parents[1]) + f'/results/{data_name}/{data_name}_data.csv'

            data = pd.read_csv(data_path)
            last_points = data.tail(5)
        
            per_unreach = last_points['bad'].mean() / last_points['total'].mean() * 100
            results[hop - 3].append(per_unreach)

        ax.plot(con_range, results[hop - 3], linewidth=0.5, marker=markers[hop - 3], label=f'{hop} hop LN')


    plt.xlabel('Max connections per node')
    plt.ylabel('Unreachability [%]')
    plt.title('Percent unreachable vs Max cons per node' + '\n' + f'{n_sats}-node network')
    ax.set_xticks(con_range)
    ax.set_axisbelow(True)
    plt.legend()
    ax.grid(linestyle='--')

    # if save_figs:
    #     plt.savefig(f'{results_path}/scatter.svg')
    if show_plots:
        plt.show()


# ------------------------------------
n_sat = 1000
year = 2030

param(n_sats=n_sat, route_step=40, show_plots=True, save_figs=False)
