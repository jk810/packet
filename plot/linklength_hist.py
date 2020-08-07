from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime

def plot_link_length(data_name, show_plots):
    start_time = time.time()
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'

    # Get satellite distances
    distance_table = {}
    distance_file = open(results_path + 'distance.txt', 'r')
    for i, line in enumerate(distance_file):
        distance_table[i] = [float(x) for x in line.split()]
    distance_file.close()

    # get link distances
    link_d = np.genfromtxt(results_path + 'links_distance.txt', usecols=2)
    
    link_d_df = pd.DataFrame({'d': link_d})
    avg_d = link_d_df['d'].mean()
    max_d = link_d_df['d'].max()
    link_d_df['d_floor'] = (link_d_df['d'] / 100).astype(int) * 100 + 50

    bins = []
    for i in range(0, 4001, 200):
        bins.append(i)

    # Plotting
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Paired.colors)
    plt.rcParams['font.sans-serif'] = 'Arial'

    fig, ax = plt.subplots()
    ax.hist(link_d_df['d_floor'], bins, edgecolor='black', alpha=0.8, linewidth=0.5)

    ax.set_ylabel('Count')
    ax.set_xlabel('Length of link [km]')
    ax.grid(linestyle=':')
    ax.set_axisbelow(True)
    ax.set_title('Link length histogram at t=1000' + '\n' + data_name)
    plt.xticks(bins)

    s = r'$\mu = $' + f'{avg_d:.1f} km'
    ax.text(.1, .9, s, transform=ax.transAxes, bbox=dict(facecolor='C1', alpha=0.5))

    print(f'Runtime: {datetime.timedelta(seconds=round(time.time() - start_time))}')

    if show_plots:
        plt.show()


# ----------------------------------------------------------
n_hop = 4
n_con = 6
n_sat = 1000

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
plot_link_length(data_name=data_name, show_plots=True)
