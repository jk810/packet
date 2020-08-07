import numpy as np
import pandas as pd
import copy

import time
from timing import timing


@timing
def provision(pos_table, route_step, nbr_hop, max_conn, avg_conn, length):
    '''
    Performs provisioning for all nodes at every time step.
    Returns a list of all distance tables and link dictionaries at every time step
    '''
    global n_hop
    global max_con
    global avg_con

    # hop limit of local neighborhood
    n_hop = nbr_hop
    # max number of connections a satellite can make
    max_con = max_conn
    # average number of connections a satellite tries to maintain
    avg_con = avg_conn

    xyz_all_time = [[j for j in pos_table.loc[i][1:]] for i in range(len(pos_table))]

    keys = [str(i) for i in range(len(xyz_all_time[0]))]
    links = {key: [] for key in keys}

    distable_linkdicts = []

    # Generate initial distance table and links (with fully connected network)
    d_table = generate_dist_table(xyz_all_time[0])
    links = generate_links(links, d_table, xyz_all_time[0], initial=True)

    if type(length) != int:
        length = len(xyz_all_time) - 1
    elif (length) >= len(xyz_all_time):
        length = len(xyz_all_time) - 1

    # list that will hold provisioning results at desired routing time steps
    all_xyz_rsteps = []

    dt = []     # timing variable for generate_dist_table
    lt = []     # timing variable for generate_links

    # perform provisioning at every time step
    for i in range(length):
        xyz_now = xyz_all_time[i]

        sss = time.time()
        d_table = generate_dist_table(xyz_now)
        dt.append(time.time() - sss)

        ssss = time.time()
        links = generate_links(links, d_table, xyz_now, initial=False)
        lt.append(time.time() - ssss)

        # only saves provisioning results at desired time steps for routing
        if i % route_step == 0 and i >= (length-1)/2:
            distable_linkdicts.append((d_table, links))
            all_xyz_rsteps.append(xyz_all_time[i])

    print(f'       gen d time: {sum(dt)/len(dt):.3f}')
    print(f'       gen l time: {sum(lt)/len(lt):.3f}')
    return (distable_linkdicts, all_xyz_rsteps)


# generates all the links for all the satellites at a single time step
#   return: table of links
def generate_links(link, d_table, xyz_now, initial):
    '''
    generate link dictionaries for all nodes at a single time step
    '''
    global max_dist
    # max distance for a link between satellites
    max_dist = 4000
    # proactively search for a new link when distance is more than
    # max_dist - search_d
    search_d = 500
    # max range of RF finder
    rf_range = 100
    # boolean controlling whether or not to use RF reconnection
    rf = False

    # additional link; RF reconnection to guarantee reconnections
    max_con_rf = max_con + 1
    links = copy.deepcopy(link)

    # remove links that are out of range
    for sat in link:
        for con in link[sat]:
            if not check_in_range(xyz_now[int(sat)], xyz_now[int(con)]):
                links[sat].remove(con)

    links2 = copy.deepcopy(links)

    # iterate through all nodes
    for sat in links2:
        if initial:
            neighbors = list(range(len(links)))
        # else:
        #     # Build local neighborhood
        #     neighbors = []
        #     frontier = [str(sat)]
        #     for step in range(n_hop):
        #         new_frontier = []
        #         for indiv in frontier:
        #             new_frontier = new_frontier + links[indiv]
        #         frontier = list(set([i for i in new_frontier if i not in neighbors]))
        #         neighbors = neighbors + frontier
        #     # create list of nodes that are in range and outside LN
        #     in_range = []
        #     for label, value in d_table[sat].iteritems():
        #         if value < max_dist:
        #             in_range.append(str(label))
        #     in_range.remove(sat)
        #     in_range_notin_ln = list(set(in_range) - set(neighbors))

        # # iterate through all links to current node, proactively provision
        # for con in links2[sat]:
        #     if get_distance(xyz_now[int(sat)], xyz_now[int(con)]) >= max_dist - search_d:
        #         if initial:
        #             new = search_new_link(sat, links, d_table, xyz_now, max_d=max_dist-search_d, local=neighbors)
        #         else:
        #             new = search_new_link(sat, links, d_table, xyz_now, max_d=max_dist-search_d, local=in_range_notin_ln)
        #         # if a new link is found, break old connection and add new link
        #         if new != False and str(new) != sat:
        #             links[sat].remove(con)
        #             links[con].remove(sat)
        #             links2[con].remove(sat)
        #             # add new link to dictionary
        #             links[sat].append(str(new))
        #             links[str(new)].append(sat)

        # ************************************************* MODIFIED FOR DIAL
        con1 = d_table[sat] < max_dist
        filtered_d_table = d_table[con1]
        d_table_inrange = filtered_d_table[sat]
        in_range_notin_ln = list(d_table_inrange.index)
        # *************************************************

        if len(links[sat]) != 0 or initial:
            # search for new links while number of cons is < avg_con
            while len(links[sat]) < avg_con:
                if initial:
                    new = search_new_link(sat, links, d_table, xyz_now, max_d=max_dist, local=neighbors)
                else:
                    new = search_new_link(sat, links, d_table, xyz_now, max_d=max_dist, local=in_range_notin_ln)
                if new == False:
                    break
                elif str(new) != sat:
                    links[sat].append(str(new))
                    links[str(new)].append(sat)
                else:
                    break

        elif rf == True:
            for i in range(len(xyz_now)):
                node = xyz_now[i]
                if get_distance(xyz_now[int(sat)], node) <= rf_range and str(i) != sat and len(links[str(i)]) < max_con_rf:
                    links[sat].append(str(i))
                    links[str(i)].append(sat)
                    break
    return links


def search_new_link(sat, links, d_table, xyz_now, max_d, local):
    '''
    Searches for a new link in a subset of the network (or all nodes if initial).
    Returns the new connection node number, or False if no connection is found
    '''
    # Using only nodes in local subset
    d_table_subset = d_table.loc[[int(i) for i in local]]
    if int(sat) in d_table_subset.index:
        d_table_subset = d_table_subset.drop(int(sat))

    if len(d_table_subset[sat]) == 0:
        return False
    if max(d_table_subset[sat]) == 0:
        return False

    # sort nodes by distance
    scoring = d_table_subset[sat].sort_values()

    new_con = False

    for potential_link in scoring.index:
        if (check_in_range(xyz_now[int(sat)], xyz_now[int(potential_link)]) and
                len(links[str(potential_link)]) < max_con and
                str(potential_link) not in links[sat] and
                str(potential_link) != sat):
            new_con = potential_link
            break
    return new_con


def generate_dist_table(xyz_now):
    '''
    Generates distance table at a single time step
    '''
    n_sat = len(xyz_now)
    np_xyz = np.array(xyz_now)

    d_table = pd.DataFrame(index=[i for i in range(n_sat)])
    for i, pos in enumerate(np_xyz):
        d_table[str(i)] = np.sqrt(np.square(pos - np_xyz).sum(axis=1))

    return d_table


def check_in_range(pos1, pos2):
    '''
    Check if 2 nodes are within range of each other
    '''
    dist = get_distance(pos1, pos2)
    if dist > max_dist:
        return False
    else:
        return True


def get_distance(pos1, pos2):
    '''
    Calculate the distance between two satellites
    '''
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    return np.sqrt(dx**2 + dy**2 + dz**2)
