from pyorbital.orbital import Orbital
import pandas as pd
import datetime
from timing import timing


@timing
def propagate(TLE_path, length, year):
    '''
    Reads TLE file, propagates satellites based on sim length and epoch year
    Returns a position table of every node at every time step
    '''

    time_list = [datetime.datetime(year, 1, 1, 0, 0, 0, 0) +
                 datetime.timedelta(seconds=60*x) for x in range(length + 3)]
    node_num = 0

    table = pd.DataFrame(time_list, columns=["Time"])
    file = open(TLE_path, "r")

    # corrected = open(r"C:\Users\JK31434\Desktop\Packet\code_source\TLEs\correct_TLEs.txt",'w')

    a = file.readline()
    b = file.readline()

    # Iterate over TLE file
    while a != '' and b != '':
        # try:
        orb = Orbital("sat{}".format(node_num), line1=a, line2=b)
        pos_list = []
        for time in time_list:
            pos = orb.get_position(time, normalize=False)
            pos_list.append(pos[0])     # pos[1] has xyz velocity
        table[str(node_num)] = pos_list
        node_num += 1

            # corrected.write(a)
            # corrected.write(b)
        # except:
        #     pass

        a = file.readline()
        b = file.readline()
    file.close()

    return table
