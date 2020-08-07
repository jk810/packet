from pyorbital.orbital import Orbital
import pandas as pd
import datetime
import os
from pathlib import Path

def propagate_orbits(TLE_path, days):
    num_mins = int(days*24*60)
    time_list = [datetime.datetime(2020, 1, 1, 0, 0, 0, 0) + datetime.timedelta(seconds = 60*x) for x in range(0, num_mins)]
    num = 0

    table = pd.DataFrame(time_list, columns=["Time"])
    file = open(TLE_path, "r")

    a = file.readline()
    b = file.readline()

    # Iterate over TLE file
    while a != '' and b != '':
        orb = Orbital("sat{}".format(num), line1=a, line2=b)
        pos_list = []
        for time in time_list:
            pos = orb.get_position(time, normalize=False)
            pos_list.append(pos)
        table[str(num)] = pos_list
        num += 1 

        a = file.readline()
        b = file.readline()
    file.close()

    return table


TLE_filename=r'\200.txt'

current_file_path = Path(__file__)
provision_source_path = str(current_file_path.parents[1]) + '\\'
TLE_path = provision_source_path + 'TLEs\\' + TLE_filename
results_path = provision_source_path + 'TLEs\\'
pos_table = propagate_orbits(TLE_path, .5)