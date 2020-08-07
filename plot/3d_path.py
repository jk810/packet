from shortest_paths_nx import shortest_path
import numpy as np
from pathlib import Path
import networkx as nx
import matplotlib.cm as cm
from matplotlib import colors

import plotly
import plotly.graph_objs as go
from timing import timing


@timing
def plot_path(data_name, pair, n_hop, showLN):
    current_file_path = Path(__file__)
    results_path = str(current_file_path.parents[1]) + f'/results/{data_name}/'

    # open xyz text file and extract values
    xyz = open(results_path + 'xyz.txt', 'r')
    pos = {}
    for i, line in enumerate(xyz):
        a = line.split()
        pos[str(i)] = (float(a[0]), float(a[1]), float(a[2]))
    xyz.close()

    n_nodes = len(pos)
    # Create graph object based on links and distances txt files
    G = shortest_path(results_path)

    # add degrees for nodes with 0 connections
    for i in range(n_nodes):
        if str(i) not in list(G):
            G.add_node(str(i), weight=0)

    src = pair[0]
    dst = pair[1]

    flag = False
    hops_file = open(results_path + 'hops.txt', 'r')
    for line in hops_file:
        if line.split()[0] == str(src) and line.split()[1] == str(dst):
            split1 = line.split('[')
            split2 = split1[1].split(']')
            hop_path = split2[0].split(', ')
            flag = True
            break
    hops_file.close()

    if flag is False:
        print(f'Error! There is no path between node {src} and {dst}')
        return


    # Plotting
    # Iterate over path list to get xyz coordinates
    xi = []
    yi = []
    zi = []
    for i in hop_path:
        xi.append(pos[i][0])
        yi.append(pos[i][1])
        zi.append(pos[i][2])
    path_nodes = go.Scatter3d(x=xi, y=yi, z=zi, mode='markers',
                             marker=dict(color='cyan', size=2), text=hop_path,
                             hoverinfo='text', name='Path nodes', textfont=dict(color='red'))
    path_nodes['showlegend'] = True

    # src node
    x_src = pos[str(src)][0]
    y_src = pos[str(src)][1]
    z_src = pos[str(src)][2]
    src_trace = go.Scatter3d(x=[x_src], y=[y_src], z=[z_src], mode='markers',
                             marker=dict(color='azure', size=5, line=dict(color='black', width=0.2)),
                             text=str(src), hoverinfo='text', name='Source node')
    src_trace['showlegend'] = False
    # dst node
    x_dst = pos[str(dst)][0]
    y_dst = pos[str(dst)][1]
    z_dst = pos[str(dst)][2]
    dst_trace = go.Scatter3d(x=[x_dst], y=[y_dst], z=[z_dst], mode='markers',
                             marker=dict(color='azure', size=5, line=dict(color='black', width=0.2)),
                             text=str(dst), hoverinfo='text', name='Destination node')
    dst_trace['showlegend'] = False

    # Plot nodes external to path
    xo = []
    yo = []
    zo = []
    node_list = list(range(n_nodes))
    for i in node_list:
        xo.append(pos[str(i)][0])
        yo.append(pos[str(i)][1])
        zo.append(pos[str(i)][2])
    ext_nodes = go.Scatter3d(x=xo, y=yo, z=zo, mode='markers',
                             marker=dict(color='black', size=1.3),
                             text=node_list, hoverinfo='text', name='External nodes')
    ext_nodes['showlegend'] = True

    # get link colors by hop path length
    path_colors = []
    cmap = cm.get_cmap('plasma', len(hop_path))
    for i in range(cmap.N):
        rgb = cmap(i)[:3]
        path_colors.append(colors.rgb2hex(rgb))

    # Plot path edges
    # Iterate over list of edges to get the xyz, coordinates of connected nodes
    path_traces = []
    path_links = []

    for j in range(1, len(hop_path)):
        x = [pos[hop_path[j-1]][0], pos[hop_path[j]][0], None]
        y = [pos[hop_path[j-1]][1], pos[hop_path[j]][1], None]
        z = [pos[hop_path[j-1]][2], pos[hop_path[j]][2], None]

        path_links.append([hop_path[j-1], hop_path[j]])
        path_traces.append(go.Scatter3d(x=x, y=y, z=z,
                                        mode='lines', line=dict(color=path_colors[j], width=4),
                                        name=f'Hop {j}', hoverinfo='none'))

    # Plot edges not in path
    x_ext = []
    y_ext = []
    z_ext = []

    for j in G.edges([str(i) for i in range(n_nodes)]):
        x = [pos[j[0]][0], pos[j[1]][0], None]
        y = [pos[j[0]][1], pos[j[1]][1], None]
        z = [pos[j[0]][2], pos[j[1]][2], None]
        if [j[0], j[1]] not in path_links and [j[1], j[0]] not in path_links:
            x_ext += x
            y_ext += y
            z_ext += z
    ext_edges = go.Scatter3d(x=x_ext, y=y_ext, z=z_ext, mode='lines',
                             line=dict(color='rgb(0, 0, 0)', width=0.4),
                             hoverinfo='none', name='External links')

    # Plot earth
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
    X = 6371 * np.cos(u) * np.sin(v)
    Y = 6371 * np.sin(u) * np.sin(v)
    Z = 6371 * np.cos(v)

    contours = dict(x=dict(highlight=False), y=dict(highlight=False),
                    z=dict(highlight=False))
    sphere = go.Surface(x=X, y=Y, z=Z, colorscale='Greys', showscale=False,
                        hoverinfo='none', contours=contours, reversescale=True)


    # Plotting local neighborhood of destination node
    if showLN:
        frontier_list = []
        local_n_list = []
        local_n_list_reduced = []

        # Each frontier is a dictionary of local neighborhood
        for i in range(n_hop + 1):       # includes 0-hop neighborhood
            frontier_list.append(nx.single_source_shortest_path(G, str(dst), cutoff=i))
            # get frontier keys, which are local neighborhood nodes
            local_n_list.append([str(x) for x in list(frontier_list[i].keys())])

        # Create 'reduced' list, manually add 0, 1 hop neighbor nodes
        for i in range(0, 2):
            local_n_list_reduced.append(local_n_list[i])
        # Remove lower level (-2 levels) hop nodes so each frontier only includes 'growth'
        for i in range(2, n_hop + 1):
            local_n_list_reduced.append([x for x in local_n_list[i] if
                                        x not in local_n_list[i - 2]])

        # get link colors by hop
        link_colors = []
        cmap = cm.get_cmap('GnBu', n_hop)
        for i in range(cmap.N):
            rgb = cmap(i)[:3]
            link_colors.append(colors.rgb2hex(rgb))
        link_colors.insert(0, '#000000')    # insert color for 0-hop neighborhood

        # Iterate over local nbrhood list to extract the xyz coordinates of each
        # neighborhood node
        xi = []
        yi = []
        zi = []
        for i in local_n_list[-1]:
            xi.append(pos[i][0])
            yi.append(pos[i][1])
            zi.append(pos[i][2])
        # mode='markers+text' for labels
        nbr_nodes = go.Scatter3d(x=xi, y=yi, z=zi, mode='markers',
                                marker=dict(color='red', size=2),
                                text=local_n_list[-1], hoverinfo='text', name='LN nodes')
        nbr_nodes['showlegend'] = True  


        # Plot local neighborhood edges
        # Iterate over list of edges to get the xyz, coordinates of connected nodes
        grow_edges = []
        for i, frontier in enumerate(local_n_list_reduced):
            x_grow = []
            y_grow = []
            z_grow = []
            for j in G.edges(frontier):
                x = [pos[j[0]][0], pos[j[1]][0], None]
                y = [pos[j[0]][1], pos[j[1]][1], None]
                z = [pos[j[0]][2], pos[j[1]][2], None]
                if j[0] in frontier and j[1] in frontier and nx.shortest_path_length(G, str(dst), j[0]) == i-1:
                    x_grow += x
                    y_grow += y
                    z_grow += z
            grow_edges.append(go.Scatter3d(x=x_grow, y=y_grow, z=z_grow,
                                        mode='lines', line=dict(color=link_colors[i], width=1.5),
                                        name=f'{i}-hop', hoverinfo='none'))

    # Plot layout
    noaxis = dict(showbackground=False, showgrid=False, showticklabels=False,
                  ticks='', title='', zeroline=False, showspikes=False)
    layout3d = dict(title=f'{data_name} network<br>'
                    f'Path from node {src} - {dst}: {len(hop_path)-1} hops',
                    font=dict(family='Arial'),
                    scene=dict(xaxis=noaxis, yaxis=noaxis, zaxis=noaxis))

    data = [sphere, ext_nodes, path_nodes, nbr_nodes, src_trace, dst_trace, ext_edges]
    if showLN:
        data += grow_edges
    data += path_traces
    fig = dict(data=data, layout=layout3d)

    plotly.offline.plot(fig, filename=f'{results_path}/{data_name}_{src}-{dst}_path.html')


# -------------------------------------
n_con = 6
n_hop = 4

n_sat = 10000
pair = [5000, 9000]

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
plot_path(data_name=data_name, pair=pair, n_hop=n_hop, showLN=True)
