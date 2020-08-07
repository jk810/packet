import datetime
import os
from pathlib import Path

from timing import timing
from propagate import propagate
from batch_print_txt import print_txt
from provision import provision


@timing
def run_sim(dat, route_step, n_hop, max_con, avg_con, n_sat, perimiter_only,
            length, year):
    current_file_path = Path(__file__).resolve()
    code_source_path = str(current_file_path.parents[0])
    TLE_path = code_source_path + f'/TLEs/{n_sat}.txt'

    # Create directory for sim results
    results_path = f'{code_source_path}/results/{dat}'

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

    # print links and distance table for each routing time step
    for i in range(len(distable_linkdicts)):
        print_txt(distable_linkdicts, all_xyz_rsteps, i, results_path)

    return


# ---------------------------------------
# hop limit for local neighborhood
n_hop = 4
# max # of connections per satellite
max_con = 6
# average # of connections that are maintained
avg_con = 4

# time step to perform routing
route_step = 50
# boolean for using only perimeter nodes for routing
perim = False
# length of simulation in minutes
length = 1000
# start year of propagation (TLE epoch time is 1/1/2020)
year = 2030
# n_sat must match name of TLE file

sims = [1000]
for n_sat in sims:
    data_name = f'{n_sat}sat_{n_hop}hop_{max_con}con'
    run_sim(dat=data_name, route_step=route_step, n_hop=n_hop, max_con=max_con,
            avg_con=avg_con, n_sat=n_sat, perimiter_only=perim, length=length,
            year=year)
