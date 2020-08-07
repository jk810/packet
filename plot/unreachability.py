import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path


def unreachable(data_name, n_sats, route_step, sim_time, show_plots, save_figs):
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'
    data_path = f'{results_path}' + data_name + '_data.csv'

    data = pd.read_csv(data_path)
    n_route_steps = int(sim_time/2/route_step + 1)
    n_sims = data.shape[0] / n_route_steps
    n_nodes = data['n_node'][0]
    hop_n = data['n_hop'][0]

    data_split = np.array_split(data, n_sims)   # split data by simulation

    # Plotting
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Paired.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'
    # plt.rcParams.update({'font.size': 12})

    # Percent unreachable scatter plot #
    fig1, ax1 = plt.subplots()
    for i, sim in enumerate(data_split):
        sim = sim.reset_index()
        label = 'Simulation ' + str(i + 1)
        ax1.plot(sim.index.values*route_step + sim_time/2,
                 sim['bad']/sim['total']*100, linewidth=0.5, marker='.', label=label)

    plt.xlabel('Time [mins]')
    plt.ylabel('[%]')
    plt.title('Percent Unreachable vs Time' + '\n' + str(n_nodes) + ' nodes, '
              + str(hop_n) + '-hop neighborhood')
    plt.legend()
    ax1.grid(linestyle='--')

    if save_figs:
        plt.savefig(f'{results_path}/scatter.svg')

    # Box plot (if there are multiple sims)
    if n_sims > 1:
        fig4, ax2 = plt.subplots()
        z = []
        # collect % reachability for each sim at a single time step
        for i in range(n_route_steps):
            y = data.iloc[i::n_route_steps, 3] / data.iloc[i::n_route_steps, 2] * 100
            z.append(y)

        labs = [str(i) for i in range(0, sim_time + 1, route_step)]
        ax2.boxplot(z, labels=labs)
        plt.xlabel('Time [mins]')
        plt.ylabel('[%]')
        plt.title('Percent unreachable vs Time' + '\n' + str(n_nodes) +
                  ' nodes, ' + str(hop_n) + '-hop neighborhood')
        ax2.grid(linestyle='--')

        if save_figs:
            plt.savefig(f'{results_path}/boxplot.svg')

    if show_plots:
        plt.show()


# ----------------------------------
n_hop = 4
n_con = 6
time = 1000

n_sat = 1000

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'

unreachable(data_name=data_name, n_sats=n_sat, route_step=50, sim_time=time,
            show_plots=True, save_figs=False)