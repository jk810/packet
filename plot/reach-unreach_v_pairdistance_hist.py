from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import pandas as pd
import time
import datetime
import math


def plot_unfound_d(data_name, show_plots):
    start_time = time.time()
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'

    # Get satellite distances
    distance_table = {}
    distance_file = open(results_path + 'distance.txt', 'r')
    for i, line in enumerate(distance_file):
        distance_table[i] = [float(x) for x in line.split()]
    distance_file.close()

    n_nodes = len(distance_table)

    # get reachable pairs and the distance between the pair nodes
    # counts mirror pairs
    hops_array = np.genfromtxt(results_path + 'hops.txt', dtype=int, usecols=(0, 1))

    reachable_pairs_ds = {str(pair[0]) + str(pair[1]): distance_table[pair[0]][pair[1]] for pair in hops_array}
    reachable_d = list(reachable_pairs_ds.values())

    unreachable_d = []
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            key = str(i) + str(j)
            ukey = str(j) + str(i)
            if key not in reachable_pairs_ds:
                unreachable_d.append(distance_table[i][j])
            if ukey not in reachable_pairs_ds:
                unreachable_d.append(distance_table[j][i])
    
    reachable_df = pd.DataFrame({'reach_og': reachable_d})
    reachable_df['Existing'] = (reachable_df['reach_og'] / 1000).apply(math.floor) * 1000 + 500
    unreachable_df = pd.DataFrame({'unreach_og': unreachable_d})
    unreachable_df['None'] = (unreachable_df['unreach_og'] / 1000).apply(math.floor) * 1000 + 500

    bins = []
    for i in range(0, 16001, 1000):
        bins.append(i)

    # Plotting
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Pastel1.colors)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.hist(reachable_df['Existing'], bins, color='C1', edgecolor='black', alpha=0.9, linewidth=0.5, label='Reachable pairs')
    ax2.hist(unreachable_df['None'], bins, color='C0', edgecolor='black', alpha=0.9, linewidth=0.5, label='Unreachable pairs')

    ax1.set_ylabel('Count')
    ax2.set_ylabel('Count')
    ax1.set_xlabel('Distance between nodes [km]')
    ax2.set_xlabel('Distance between nodes [km]')
    ax1.grid(linestyle='--')
    ax2.grid(linestyle='--')
    ax1.set_axisbelow(True)
    ax2.set_axisbelow(True)
    ax1.legend()
    ax2.legend()
    ax1.set_title('Distance histograms of Reachable and Unreachable node pairs' + '\n' + data_name)

    print(f'Runtime: {datetime.timedelta(seconds=round(time.time() - start_time))}')

    if show_plots:
        plt.show()


# ----------------------------------------------------------
n_hop = 4
n_con = 6
n_sat = 1000

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
plot_unfound_d(data_name=data_name, show_plots=True)
