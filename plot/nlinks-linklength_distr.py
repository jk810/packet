from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
from timing import timing


@timing
def plot_link_length(data_name, n_sat):
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'


    links = pd.read_csv(results_path + 'links_distance.txt', sep=' ', header=None)
    links.columns = ['sat', 'con', 'd']

    grouped_sat = links.groupby('sat')['d'].apply(list)
    grouped_con = links.groupby('con')['d'].apply(list)
    nodes = list(set(grouped_sat.index.tolist() + grouped_con.index.tolist()))
    nodes.sort()

    node_x = {x:[] for x in nodes}
  
    for i, row in grouped_sat.iteritems():
        for d in row:
            node_x[i].append(d)
    for j, row in grouped_con.iteritems():
        for dd in row:
            node_x[j].append(dd)

    sorted_nodes = sorted(node_x, key=lambda k: len(node_x[k]))

    mins = []
    avg = []
    maxs = []
    nums = []
    for n in sorted_nodes:
        mins.append(min(node_x[n]))
        maxs.append(max(node_x[n]))
        avg.append(sum(node_x[n]) / len(node_x[n]))
        nums.append(len(node_x[n]))
    
    # Plotting
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Set1.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'

    fig, ax = plt.subplots()
    
    ax.bar(nodes, nums, width=0.3, edgecolor='k', color='C3', linewidth=0.3, alpha=0.2)
    ax.set_ylabel('Number of links')
    ax.yaxis.label.set_color('C3')
    ax.set_xlabel('Node')
    ax.set_xticks(sorted_nodes)
    ax.set_xticklabels([str(i) for i in sorted_nodes])
    # ax.grid(linestyle=':')
    ax.set_axisbelow(True)
    ax.set_title('Node links and average length of links' + '\n' + data_name)

    ax2 = ax.twinx()
    ax2.set_ylabel('Length of link')
    ax2.scatter(nodes, maxs, linewidth=0.5, marker=10, label='max')
    ax2.scatter(nodes, avg, linewidth=0.5, marker='.', label='avg')
    ax2.scatter(nodes, mins, linewidth=0.5, marker=11, label='min')
    ax2.legend()
    plt.show()


# ----------------------------------------------------------
n_hop = 4
n_con = 6
n_sat = 100

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
plot_link_length(data_name=data_name, n_sat=n_sat)
