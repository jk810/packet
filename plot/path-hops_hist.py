from shortest_paths_nx import shortest_path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import networkx as nx
from scipy.stats import norm
import matplotlib.cm
from timing import timing


@timing
def stats(data_name, n_sat, show_plots):
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'
    hops_path = results_path + 'hops.txt'

    G = shortest_path(results_path)

    path_length = []
    pairs = []
    hops_file = open(hops_path, 'r')
    for line in hops_file:
        path_length.append(int(line.split()[2]))
        pairs.append(line.split()[0:2])
    hops_file.close()

    test = 0
    for pair in pairs:
        test += nx.shortest_path_length(G, pair[0], pair[1])
    nx_avg_path_length = test / len(pairs)


    # Plotting
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Paired.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'

    # Path length distribution #
    fig, ax = plt.subplots()

    # histogram
    bins = np.arange(min(path_length), max(path_length) + 2) - 0.5
    ax.hist(path_length, bins, color='C0', rwidth=0.7, edgecolor='black', linewidth=0.5, alpha=0.8)
    ax.set_ylabel('Number of connections')
    ax.grid(linestyle=':')
    ax.set_axisbelow(True)

    # gaussian fit
    ax2 = ax.twinx()
    ax2.set_ylabel('Probability distribution')
    ax2.yaxis.label.set_color('C9')

    x = np.arange(min(path_length), max(path_length) + .1, .1)
    (mu, sigma) = norm.fit(path_length)
    # scale = len(path_length)
    y = norm.pdf(x, mu, sigma)
    ax2.set_ylim(bottom=0, top=max(y)*1.2)
    ax2.plot(x, y, 'C9--')
    s = r'$\mu = $' + f'{mu:.3f}' + '\n' + r'$\sigma = $' + f'{sigma:.3f}'
    s2 = 'NetworkX routing:' + '\n' + r'$\mu = $' + f'{nx_avg_path_length:.3f}'
    ax2.text(.95, .85, s, transform=ax.transAxes, va='baseline', ha='right',
             bbox=dict(facecolor='C0', alpha=0.7))
    ax2.text(.95, .78, s2, transform=ax.transAxes, va='top', ha='right',
             bbox=dict(facecolor='C2', alpha=0.7))
    ax2.tick_params(axis='y', labelcolor='C9')

    plt.xticks(range(min(path_length), max(path_length) + 1))
    ax.set_xlabel('Number of hops')
    plt.title(f'Path length distribution: {data_name}')
    fig.tight_layout()  # otherwise right y-label is clipped

    if show_plots:
        plt.show()

# -----------------------------------------------
n_hop = 4
n_con = 6
n_sat = 500

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
stats(data_name=data_name, n_sat=n_sat, show_plots=True)
