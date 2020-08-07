import datetime
import os
from pathlib import Path
import pandas as pd

from timing import timing
from propagate import propagate
from print_txt import print_txt
from provision import provision
from route import route


@timing
def run_sim(dat, route_step, n_hop, max_con, avg_con, n_sat, perimiter_only,
            length, year):
    current_file_path = Path(__file__).resolve()
    code_source_path = str(current_file_path.parents[0])
    TLE_path = code_source_path + f'/TLE/{n_sat}.txt'

    # Create directory for sim results
    results_path = f'{code_source_path}/dial_results/{dat}'
    data_path = f'{results_path}/{dat}_data.csv'

    try:
        os.mkdir(results_path)
    except:
        pass

    print('________ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
          ' ________')
    print(data_name)

    # Propagate orbits
    pos_table = propagate(TLE_path, length, year)

    # Provision at every time step. Returns results from routing time steps
    (distable_linkdicts, all_xyz_rsteps) = provision(pos_table, route_step,
                                                     nbr_hop=n_hop,
                                                     max_conn=max_con,
                                                     avg_conn=avg_con,
                                                     length=length+1)

    # print links and distance table of last time step
    print_txt(distable_linkdicts, all_xyz_rsteps, -1, results_path)

    # # Perform routing at specified time steps
    # @timing
    # def route_sum():
    #     sim_data = []
    #     for i in range(len(distable_linkdicts)):
    #         route_data_time_i = route(n_node=n_sat, nbrhood_hop=n_hop,
    #                                   border=perimiter_only,
    #                                   linkdict=distable_linkdicts[i][1],
    #                                   distable=distable_linkdicts[i][0],
    #                                   results_path=results_path)
    #         # append routing results from a single time step
    #         sim_data.append(route_data_time_i)
    #     return sim_data
    # route_data = route_sum()
    # # Write routing results to csv
    # np_data = pd.DataFrame(route_data)    # initialize pd dataframe
    # np_data.columns = ['n_node', 'n_hop', 'total', 'bad', 'loop', 'no_path']
    # np_data.to_csv(data_path, index=False)

    return


# ---------------------------------------
# hop limit for local neighborhood
n_hop = 2
# max # of connections per satellite
max_con = 6
# average # of connections that are maintained
avg_con = 6

# time step to perform routing
route_step = 50
# boolean for using only perimeter nodes for routing
perim = False
# length of simulation in minutes
length = 1000
# start year of propagation (TLE epoch time is 1/1/2020)
year = 2030
# n_sat must match name of TLE file

sims = [5000]
for n_sat in sims:
    data_name = f'{n_sat}sat_{max_con}con'
    run_sim(dat=data_name, route_step=route_step, n_hop=n_hop, max_con=max_con,
            avg_con=avg_con, n_sat=n_sat, perimiter_only=perim, length=length,
            year=year)
