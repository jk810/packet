import os


def print_txt(distable_linkdicts, all_xyz_rsteps, step, results_path):
    '''
    Record simulation results from each routing time step to .txt files.
    This function will remove existing results in the directory.
    Writes distance.txt, xyz.txt, links.txt, and links_distance.txt
    '''

    links = [i[1] for i in distable_linkdicts]
    mylinks = links[step]
    try:
        os.remove(results_path + f'/links_{step}.txt')
    except:
        pass
    try:
        os.remove(results_path + f'/distance_{step}.txt')
    except:
        pass
    try:
        os.remove(results_path + f'/links_distance_{step}.txt')
    except:
        pass
    try:
        os.remove(results_path + f'/xyz_{step}.txt')
    except:
        pass

    my_positions = all_xyz_rsteps[step]
    my_distances = distable_linkdicts[step][0]

    file = open(results_path + f'/distance_{step}.txt', 'w')

    for i, column in my_distances.iteritems():
        k = list(column)
        for j in range(len(k)):
            if j == 0:
                file.write(str(k[j]))
            elif j == len(k) - 1:
                file.write(' ' + str(k[j]) + '\n')
            else:
                file.write(' ' + str(k[j]))
    file.close()

    # Write file with xyz position of every satellite at specified time
    file = open(results_path + f'/xyz_{step}.txt', 'w')
    for num in range(len(my_positions)):
        pos = my_positions[num]
        x = str(pos[0])
        y = str(pos[1])
        z = str(pos[2])
        file.write(x + ' ' + y + ' ' + z + '\n')
    file.close()

    file1 = open(results_path + f'/links_{step}.txt', 'w')
    file2 = open(results_path + f'/links_distance_{step}.txt', 'w')
    set_check = set()
    for sat in mylinks:
        for conn in mylinks[sat]:
            if (sat, conn) not in set_check and (conn, sat) not in set_check:
                file1.write(sat + ' ' + conn + '\n')
                file2.write(sat + ' ' + conn + ' ' + str(my_distances[sat][int(conn)]) + '\n')
                set_check.add((sat, conn))
                set_check.add((conn, sat))
    file1.close()
    file2.close()
