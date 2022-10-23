"""
    All possible graphs generator

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-04
"""

import copy
import itertools
from itertools import combinations
import math
import numpy as np
import os
import random

import networkx as nx
import matplotlib.pyplot as plt

########################################################################################################################
# [0.] Create all possible graphs ======================================================================================
########################################################################################################################
max_nr_nodes = 4
all_node_ids = [0, 1, 2, 3]
nodes_pos_dict = {0: [1, 1], 1: [2, 1], 2: [1, 2], 3: [2, 2]}

mu, sigma = 0, 0.1

image_x_left_lim = 0.5
image_x_right_lim = 2.5
image_y_down_lim = 0.5
image_y_up_lim = 2.5

# Add some noise on the node positions ---------------------------------------------------------------------------------
nr_of_added_noise_values = 4    # Two nodes on the left + noise ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
noise_add_positions = np.random.normal(mu, sigma, nr_of_added_noise_values)
print(noise_add_positions)

nodes_with_noise_pos_dict = copy.deepcopy(nodes_pos_dict)
# x and y coordinates of node_0 and node_2 on the left side of the image is perturbed with noise +++++++++++++++++++++++
nodes_with_noise_pos_dict[0][0] = nodes_with_noise_pos_dict[0][0] + noise_add_positions[0]
nodes_with_noise_pos_dict[0][1] = nodes_with_noise_pos_dict[0][1] + noise_add_positions[1]
nodes_with_noise_pos_dict[2][0] = nodes_with_noise_pos_dict[2][0] + noise_add_positions[2]
nodes_with_noise_pos_dict[2][1] = nodes_with_noise_pos_dict[2][1] + noise_add_positions[3]

# x and y coordinates of node_1 and node_3 on the left side of the image is perturbed with noise +++++++++++++++++++++++
nodes_with_noise_pos_dict[1][0] = image_x_right_lim - (nodes_with_noise_pos_dict[0][0] - image_x_left_lim)
nodes_with_noise_pos_dict[1][1] = nodes_with_noise_pos_dict[0][1]
nodes_with_noise_pos_dict[3][0] = image_x_right_lim - (nodes_with_noise_pos_dict[2][0] - image_x_left_lim)
nodes_with_noise_pos_dict[3][1] = nodes_with_noise_pos_dict[2][1]

########################################################################################################################
for nodes_nr in range(2, 5):

    print(f"Create all possible graphs for node nr: {nodes_nr}")

    all_nodes_with_positions_combinations = list(itertools.combinations(all_node_ids, nodes_nr))

    positionierung = 0
    for nodes_with_positions_combinations in all_nodes_with_positions_combinations:

        print(f"Positionierung: {positionierung}")

        # nodes_idx_list = list(range(nodes_nr))
        all_graphs = []

        # [1.] All possible edges --------------------------------------------------------------------------------------
        all_edges_list = [(a, b) for idx, a in enumerate(nodes_with_positions_combinations)
                          for b in nodes_with_positions_combinations[idx + 1:]]

        all_edges_possibilities_list = sum([list(map(list, combinations(all_edges_list, i)))
                                            for i in range(len(all_edges_list) + 1)], [])

        # [2.] All possible graphs with nodes_nr of nodes --------------------------------------------------------------
        for edges_list in all_edges_possibilities_list:

            # [3.] All possible nodes ----------------------------------------------------------------------------------
            G = nx.Graph()
            for node_idx in nodes_with_positions_combinations:
                G.add_node(node_idx)

            for edge in edges_list:
                G.add_edge(edge[0], edge[1])

            all_graphs.append(G)

        print(f"Nr. of possible graphs with {nodes_nr} nodes: {len(all_graphs)}")
        nr_of_possible_graphs = int(math.pow(2, nodes_nr*(nodes_nr-1)/2))
        assert len(all_graphs) == nr_of_possible_graphs, \
            f"The number of possible graphs must be equal to: {nr_of_possible_graphs}"
        print(nr_of_possible_graphs)

        ################################################################################################################
        # [4.] Plots ===================================================================================================
        ################################################################################################################
        for graph_idx in range(len(all_graphs)):

            graph = all_graphs[graph_idx]
            print(graph.edges)

            # Plot -----------------------------------------------------------------------------------------------------
            fig = plt.figure(figsize=(12, 12))
            plt.title(f"Graph's edges: {graph.edges}", fontsize=40, fontweight="bold")
            nx.draw_networkx(
                graph,
                node_shape='o',
                pos=nodes_with_noise_pos_dict,
                with_labels=True,
            )

            # plt.show()
            plt.xlim(image_x_left_lim, image_x_right_lim)
            plt.ylim(image_y_down_lim, image_y_up_lim)
            fig.savefig(os.path.join("data", "output", "all_possible_graphs_generator",
                                     f"all_graph_topologies_nodes_nr_{nodes_nr}",
                                     f"positionierung_{positionierung}_graph_{graph_idx}.png"))
            plt.close()

        positionierung += 1

        ################################################################################################################
        # [5.] Create the pytorch structures ===========================================================================
        ################################################################################################################
        print("-------------------------------------------------------------------------------------------------------")
