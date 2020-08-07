from shortest_paths_nx import shortest_path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import networkx as nx
from scipy.stats import norm
import matplotlib.cm


def stats(data_name, n_sat, show_plots, save_figs):
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'

    G = shortest_path(results_path)
    node_list = [int(x) for x in list(G.nodes)]

    avg_local_n_size_list = [-3]
    ln_min = []
    ln_max = []
    i = 1
    while True:
        local_n_size_list = []
        for j in node_list:
            # frontier is dictionary of local neighborhood
            frontier = nx.single_source_shortest_path(G, str(j), cutoff=i)
            # get frontier keys, which are local neighborhood nodes
            local_n = [int(x) for x in list(frontier.keys())]

            size_local_n = len(local_n)
            local_n_size_list.append(size_local_n)

        # calculate average size of local neighborhood (averaged over all nodes)
        avg_local_n_size = sum(local_n_size_list) / n_sat

        # Bar labels
        ln_min.append(min(local_n_size_list))
        ln_max.append(max(local_n_size_list))

        # when the network saturates, exit loop
        if avg_local_n_size == avg_local_n_size_list[-1]:
            break
        # otherwise, append avg to list
        else:
            if i == 1:
                avg_local_n_size_list[0] = avg_local_n_size
            else:
                avg_local_n_size_list.append(avg_local_n_size)
            i += 1
    # avg_percent_list = [100*x/n_sat for x in avg_local_n_size_list]
    del ln_min[-1]
    del ln_max[-1]

    # Plotting
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set1.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'
    # plt.rcParams.update({'font.size': 12})

    fig, ax = plt.subplots()
    n_hops = np.arange(1, i)
    ax.plot(n_hops, avg_local_n_size_list, marker='.', linewidth=0.5, label='Mean')
    ax.set_xlabel('Local neighborhood hop limit [# of hops]')
    ax.set_ylabel('Local neighborhood size [# of nodes]')
    ax.set_title('Local Neighborhood Size vs Hop Limit' + '\n' + data_name)
    ax.set_xticks(n_hops)
    ax.grid(linestyle='--')
    ax.scatter(n_hops, ln_max, color='C1', marker=10, label='Max')
    ax.scatter(n_hops, ln_min, color='C2', marker=11, label='Min')
    for i in range(len(ln_min)):
        ax.text(n_hops[i] + .1, ln_min[i] - 15, str(ln_min[i]), verticalalignment='center')
        ax.text(n_hops[i] + .1, ln_max[i] + 10, str(ln_max[i]), verticalalignment='center')
        ax.text(n_hops[i] + .1, avg_local_n_size_list[i], str(round(avg_local_n_size_list[i], 1)), verticalalignment='center')
    ax.legend()
    ax.fill_between(n_hops, ln_min, ln_max, color='C3', alpha=0.1)
    ax.set_axisbelow(True)

    if save_figs:
        plt.savefig(f'{results_path}/path_length.svg')
    if show_plots:
        plt.show()

# -----------------------------------------------
n_hop = 4
n_con = 6
n_sat = 1000

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
stats(data_name=data_name, n_sat=n_sat, show_plots=True, save_figs=False)
