from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import pandas as pd
import math
import time
import datetime


def reach_range(data_name, show_plots):
    start_time = time.time()

    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'

    # Get satellite distances
    distance_table = {}
    distance_file = open(results_path + 'distance.txt', 'r')
    for i, line in enumerate(distance_file):
        distance_table[i] = [float(x) for x in line.split()]
    distance_file.close()

    range_range = list(range(0, 16001, 500))
    hops_array = np.genfromtxt(results_path + 'hops.txt', dtype=int, usecols=(0,1))
    pair_dic = {str(pair[0]) + str(pair[1]): distance_table[pair[0]][pair[1]] for pair in hops_array}

    all_inrange_info = []
    for node in range(n_sat):
        in_range = []
        for i in range_range:
            in_subrange = [dist for dist in distance_table[node] if dist <= i]
            in_range.append(len(in_subrange) - 1)
        all_inrange_info.append(in_range)

    def reachable_subranges(node):
        linked = []
        for i in range_range:
            linked_in_subrange = 0

            for con in range(n_sat):
                pair_lookup = str(node) + str(con)
                
                if pair_lookup in pair_dic and pair_dic[pair_lookup] <= i:
                    linked_in_subrange += 1
            linked.append(linked_in_subrange)
        return linked


    all_pair_info = []
    for node in range(n_sat):
        pair_info = reachable_subranges(node)
        all_pair_info.append(pair_info)

    all_inrange_info = np.asarray(all_inrange_info)
    avg_inrange_info = np.mean(all_inrange_info, axis=0)

    all_pair_info = np.asarray(all_pair_info)
    avg_pair_info = np.mean(all_pair_info, axis=0)


    avg_inrange_info[0] = 1
    avg_percent_reachable_in_subranges = avg_pair_info * 100 / avg_inrange_info

    # Plotting ------------------------
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set2.colors)

    fig, ax1 = plt.subplots()

    ax1.plot(range_range, avg_percent_reachable_in_subranges, linewidth=0.5, marker='.', label='Reachable percent')

    ax1.set_ylabel('Average percent [%]')
    ax1.set_xlabel('Range [km]')
    ax1.grid(linestyle='--')
    ax1.set_axisbelow(True)
    # ax1.legend()
    ax1.set_title('Average percent reachable vs range' + '\n' + data_name)

    print(f'Runtime: {datetime.timedelta(seconds=round(time.time() - start_time))}')

    if show_plots:
        plt.show()


# ----------------------------------------------------------
n_hop = 4
n_con = 6
n_sat = 1000

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
reach_range(data_name=data_name, show_plots=True)
