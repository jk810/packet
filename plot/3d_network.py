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
def plot_3d(data_name, center_node, n_hop, colormap):
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

    # get node degrees in sorted list
    node_and_degree = {}
    for node, val in G.degree():
        node_and_degree[node] = val
    # add degrees for nodes with 0 connections
    for i in range(n_nodes):
        if str(i) not in node_and_degree:
            node_and_degree[str(i)] = 0
            G.add_node(str(i), weight=0)

    x_center = pos[str(center_node)][0]
    y_center = pos[str(center_node)][1]
    z_center = pos[str(center_node)][2]

    frontier_list = []
    local_n_list = []
    local_n_list_reduced = []
    ext_n_list = []

    # Each frontier is a dictionary of local neighborhood
    for i in range(n_hop + 1):       # includes 0-hop neighborhood
        frontier_list.append(nx.single_source_shortest_path(G, str(center_node), cutoff=i))
        # get frontier keys, which are local neighborhood nodes
        local_n_list.append([str(x) for x in list(frontier_list[i].keys())])
    local_n_size = len(local_n_list[-1])

    # get list of external nodes
    for i in range(n_nodes):
        if str(i) not in local_n_list[-1]:
            ext_n_list.append(str(i))

    # Create 'reduced' list, manually add 0, 1 hop neighbor nodes
    for i in range(0, 2):
        local_n_list_reduced.append(local_n_list[i])
    # Remove lower level (-2 levels) hop nodes so each frontier only includes 'growth'
    for i in range(2, n_hop + 1):
        local_n_list_reduced.append([x for x in local_n_list[i] if
                                    x not in local_n_list[i - 2]])

    # Plotting
    # Iterate over local nbrhood list to extract the xyz coordinates of each neighborhood node
    xi = []
    yi = []
    zi = []
    for i in local_n_list[-1]:
        xi.append(pos[i][0])
        yi.append(pos[i][1])
        zi.append(pos[i][2])
    # mode='markers+text' for labels
    nbr_nodes = go.Scatter3d(x=xi, y=yi, z=zi, mode='markers',
                             marker=dict(color='red', size=1.7),
                             text=local_n_list[-1], hoverinfo='text')
    nbr_nodes['showlegend'] = False

    # center node
    center = go.Scatter3d(x=[x_center], y=[y_center], z=[z_center], mode='markers',
                             marker=dict(color='azure', size=4.5, line=dict(color='black', width=0.2)),
                             text=str(center_node), hoverinfo='text', name=f'Center node')
    center['showlegend'] = False

    # Plot nodes external to local neighborhood
    xo = []
    yo = []
    zo = []
    for i in ext_n_list:
        xo.append(pos[i][0])
        yo.append(pos[i][1])
        zo.append(pos[i][2])
    ext_nodes = go.Scatter3d(x=xo, y=yo, z=zo, mode='markers',
                             marker=dict(color='white', size=3,
                             line=dict(color='blue', width=0.2)),
                             text=ext_n_list, hoverinfo='text', name='External nodes')
    ext_nodes['showlegend'] = True

    # get link colors by hop path length
    link_colors = []
    cmap = cm.get_cmap(colormap, n_hop)
    for i in range(cmap.N):
        rgb = cmap(i)[:3]
        link_colors.append(colors.rgb2hex(rgb))
    link_colors.insert(0, '#000000')    # insert color for 0-hop neighborhood

    # Plot local neighborhood edges
    # Iterate over list of edges to get the xyz, coordinates of connected nodes
    grow_edges = []
    existing_links = []
    for i, frontier in enumerate(local_n_list_reduced):
        x_grow = []
        y_grow = []
        z_grow = []
        for j in G.edges(frontier):
            x = [pos[j[0]][0], pos[j[1]][0], None]
            y = [pos[j[0]][1], pos[j[1]][1], None]
            z = [pos[j[0]][2], pos[j[1]][2], None]
            if j[0] in frontier and j[1] in frontier and nx.shortest_path_length(G, str(center_node), j[0]) == i-1:
                x_grow += x
                y_grow += y
                z_grow += z
                existing_links.append([j[0], j[1]])
        grow_edges.append(go.Scatter3d(x=x_grow, y=y_grow, z=z_grow,
                                       mode='lines', line=dict(color=link_colors[i], width=1.5),
                                       name=f'{i}-hop', hoverinfo='none'))

    # Plot edges not in local neighborhood
    x_ext = []
    y_ext = []
    z_ext = []

    for j in G.edges([str(i) for i in range(n_nodes)]):
        x = [pos[j[0]][0], pos[j[1]][0], None]
        y = [pos[j[0]][1], pos[j[1]][1], None]
        z = [pos[j[0]][2], pos[j[1]][2], None]
        if [j[0], j[1]] not in existing_links and [j[1], j[0]] not in existing_links:
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

    cscale = [[0.0, "rgb(240, 240, 240)"],
              [0.111, "rgb(225, 225, 225)"],
              [0.222, "rgb(210, 210, 210)"],
              [0.333, "rgb(195, 195, 195)"],
              [0.444, "rgb(180, 180, 180)"],
              [0.555, "rgb(165, 165, 165)"],
              [0.666, "rgb(150, 150, 150)"],
              [0.777, "rgb(135, 135, 135)"],
              [0.888, "rgb(120, 120, 120)"],
              [1.0, "rgb(105, 105, 105)"]]

    contours = dict(x=dict(highlight=False), y=dict(highlight=False),
                    z=dict(highlight=False))
    sphere = go.Surface(x=X, y=Y, z=Z, colorscale=cscale, showscale=False,
                        hoverinfo='none', contours=contours, reversescale=True)
    
    # Plot layout
    noaxis = dict(showbackground=False, showgrid=False, showticklabels=False,
                  ticks='', title='', zeroline=False, showspikes=False)
    layout3d = dict(title=f'{data_name} network<br>'
                    f'Node {center_node}: {local_n_size} nodes in local neighborhood',
                    font=dict(family='Arial'),
                    scene=dict(xaxis=noaxis, yaxis=noaxis, zaxis=noaxis))

    data = [sphere, ext_nodes]#, ext_edges] #nbr_nodes, center,
    # data += grow_edges
    fig = dict(data=data, layout=layout3d)

    plotly.offline.plot(fig, filename=f'{results_path}/{data_name}_network.html')


# -------------------------------------
show_ext = True
ccc = 'jet'     # rainbow, Set1, Set2
n_con = 6
n_hop = 4

center_node = 25
n_sat = 10000

data_name = f'{n_sat}sat_{n_hop}hop_{n_con}con'
plot_3d(data_name=data_name, center_node=center_node, n_hop=n_hop, colormap=ccc)
