from shortest_paths_nx import shortest_path
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def plot_range(data_name, hop_limit, range_limit, show_plots):

    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'

    # Get satellite distances
    distance_table = {}
    distance_file = open(results_path + 'distance.txt', 'r')
    for i, line in enumerate(distance_file):
        distance_table[i] = [float(x) for x in line.split()]
    distance_file.close()

    n_nodes = len(distance_table)
    G = shortest_path(results_path)

    # get node degrees in sorted list
    node_and_degree = {}
    for node, val in G.degree():
        node_and_degree[node] = val
    # add degrees for nodes with 0 connections
    for i in range(n_nodes):
        if str(i) not in node_and_degree:
            G.add_node(str(i), weight=0)
            # node_and_degree[str(i)] = 0

    range_range = list(range(0, range_limit + 1, 200))

    def percent_in_LN_range(node, hop_n):
        p_in_LN_range = []
        in_range = []
        for i in range_range:
            # get satellites within various ranges
            in_subrange = {j: dist for j, dist in enumerate(distance_table[node]) if dist <= i}

            # get local neighborhood nodes for n_hop limit
            frontier_list = nx.single_source_shortest_path(G, str(node), cutoff=hop_n)
            # get frontier keys, which are local neighborhood nodes
            frontier_keys = [int(x) for x in list(frontier_list.keys())]

            # get satellites that are in the LN AND within the range
            in_LN_subrange = [x for x in frontier_keys if x in in_subrange]

            p_in_LN_range.append(len(in_LN_subrange) / len(in_subrange) * 100)
            in_range.append(len(in_subrange))

        return p_in_LN_range, in_range

    results = []
    avg_results = []
    pir = []

    for h in range(hop_limit + 1):
        for node in range(n_nodes):
            rrr, pirrr = percent_in_LN_range(node, h)
            results.append(rrr)
            if h == 0:  # only need to to in_range count once
                pir.append(pirrr)
        np_results = np.asarray(results)
        avg_results.append(np.mean(np_results, axis=0))
    np_pir = np.asarray(pir)
    avg_np_pir = np.mean(np_pir, axis=0)

    # Plotting
    #
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set2.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'

    fig, ax = plt.subplots()

    for i, curve in enumerate(avg_results):
        ax.plot(range_range, curve, linewidth=0.5, marker='.',
                label=f'{i}-hop local neighborhood')
    plt.xlabel('Range [km]')
    plt.ylabel('[Average %]')
    plt.title('Average percent nodes in LN and in range vs Range'
              + '\n' + data_name)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='--')
    # ax.grid(which='minor', linestyle=':')
    ax.set_axisbelow(True)

    blank = [0]*len(range_range)
    ax.scatter(range_range, blank, c='r', marker=11, label='Average nodes in range')

    plt.legend()
    # axx = ax.twinx()
    # axx.set_ylabel('Average nodes in range')
    # axx.yaxis.label.set_color('red')
    # axx.tick_params(axis='y', labelcolor='red')
    # axx.scatter(range_range, avg_np_pir, marker='x', color='r')

    for i in range(len(range_range)):
        ax.text(range_range[i], blank[i] + 1, str(round(avg_np_pir[i], 1)))

    if show_plots:
        plt.show()


# -------------------------------------
n_hop = 4
n_con = 6

hop_limit = 4
range_limit = 5000
n_sat = 1000

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
plot_range(data_name=data_name, hop_limit=hop_limit, range_limit=range_limit,
           show_plots=True)
