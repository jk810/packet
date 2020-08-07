import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# import seaborn as sns

def get_data(d):
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{d}/'

    data_path = f'{results_path}{d}_data.csv'

    data = pd.read_csv(data_path)

    return data


def unreachable(lab, route_step, sim_time):
    # names = [f'{i}sat_4hop_6con_searchmod-closest-1-way' for i in lab]
    names = [f'1000sat_4hop_6con{i}' for i in lab]

    data = []
    for d in names:
        data.append(get_data(d))

    # Plotting
    # plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set1.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'
    f, ax = plt.subplots()

    for i, l in enumerate(lab):
        sim = data[i].reset_index()
        ax.plot(sim.index.values*route_step + sim_time/2, sim['bad']/sim['total']*100,
                linewidth=0.75, marker='.', label=' '+ str(l))

    ax.grid(linestyle='--')
    ax.set_title('Unreachability')
    ax.set_xlabel('Time [minutes]')
    ax.set_ylabel('Percent unreachable [%]')

    plt.legend()
    plt.show()


# ----------------------------------
# lab = [50, 100, 250, 500, 1000, 2000]
# lab = ['', '_1-way', '_nopro', '_1-way-2000km']
# lab = ['_closest', '_closest-1-way', '_closest-nopro']
# lab = ['_searchmod', '_searchmod-1-way', '_searchmod-nopro']
# lab = ['_searchmod-closest', '_searchmod-closest-1-way', '_searchmod-closest-nopro']

# lab = ['_searchmod-1-way', '_searchmod-closest', '_searchmod-closest-1-way', ]

lab = ['', '-4000-500', '-4000-1000', '-5000-500']

unreachable(lab=lab, route_step=50, sim_time=1000)