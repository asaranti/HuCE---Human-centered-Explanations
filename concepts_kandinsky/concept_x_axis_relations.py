"""
    Concept for symmetric and non-symmetric x axis relations

    :author: Anna Saranti
    :copyright: © 2022 HCI-KDD (ex-AI) group
    :date: 2022-02-10
"""

import copy
import itertools
from itertools import combinations
import os
import pickle

import networkx as nx
import numpy as np
from sklearn import preprocessing
import torch
from torch_geometric.data import Data

from concepts_kandinsky.kandinsky_concepts_plots.kandinsky_concept_plot import plot_kandinsky_concept_zero_one, \
    plot_kandinsky_concept_predefined_distr
from concepts_kandinsky.kandinsky_concepts_utils.edges_relevances_utils import define_edge_relevances
from concepts_kandinsky.kandinsky_concepts_utils.graph_relevance_utils import fixed_graph_relevance_distribution, \
    graph_relevance_sum_components
from concepts_kandinsky.kandinsky_concepts_utils.utilities_files import cleanup_files_output, zip_generated_files
from concepts_kandinsky.kandinsky_concepts_utils.node_positions import symmetric_node_positions, \
    non_symmetric_node_positions


########################################################################################################################
# [0.] x-axis relation =================================================================================================
########################################################################################################################
def x_axis_relations(all_node_ids: list, nodes_shapes: list, nodes_colors: list,
                     nodes_with_noise_pos_dict: dict,
                     node_relevances_fixed_dict: dict, edge_relevances_fixed_dict: dict,
                     image_x_left_lim: float, image_x_right_lim: float,
                     image_y_down_lim: float, image_y_up_lim: float,
                     kandinksy_pattern_name: str, concept_name: str,
                     graph_idx_over_all: int):
    """
    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################
    """

    new_line_or_not = ""

    label_encoder_shapes = preprocessing.LabelEncoder()
    label_encoder_shapes.fit(nodes_shapes)
    label_encoder_colors = preprocessing.LabelEncoder()
    label_encoder_colors.fit(nodes_colors)
    node_features_nr = 4

    graphs_all = {}
    relevance_sum_all = {}
    relevance_graph_components_all = {}

    ####################################################################################################################
    for nodes_nr in range(1, 5):

        # Delete the files in a folder ---------------------------------------------------------------------------------
        cleanup_files_output(kandinksy_pattern_name, concept_name, nodes_nr)

        print(f"Create all possible graphs for node nr: {nodes_nr}")

        all_nodes_with_positions_combinations = list(itertools.combinations(all_node_ids, nodes_nr))

        positionierung = 0
        for nodes_with_positions_combinations in all_nodes_with_positions_combinations:

            if len(nodes_with_positions_combinations) == 1:
                continue

            print(f"Positionierung: {positionierung}")

            # nodes_idx_list = list(range(nodes_nr))
            all_graphs = []

            # [1.] All possible edges ----------------------------------------------------------------------------------
            all_edges_list = [(a, b) for idx, a in enumerate(nodes_with_positions_combinations)
                              for b in nodes_with_positions_combinations[idx + 1:]]

            all_edges_possibilities_list = sum([list(map(list, combinations(all_edges_list, i)))
                                                for i in range(len(all_edges_list) + 1)], [])

            # [2.] All possible graphs with nodes_nr of nodes ----------------------------------------------------------
            for edges_list in all_edges_possibilities_list:

                # [3.] All possible nodes ------------------------------------------------------------------------------
                G = nx.Graph()
                for node_index in nodes_with_positions_combinations:
                    G.add_node(node_index)

                for edge in edges_list:
                    G.add_edge(edge[0], edge[1])

                all_graphs.append(G)

            print(f"Nr. of single graphs with {nodes_nr} nodes: {len(all_graphs)}")

            for graph_idx in range(len(all_graphs)):

                graph = all_graphs[graph_idx]

                print(f"Graph: {graph_idx}")
                print(f"Nodes: {graph.nodes}")
                print(f"Edges: {graph.edges}")

                nodes_relevances = {}
                edges_relevances = {}

                graph_nodes_dict_mapping = dict(zip(list(graph.nodes), list(range(len(graph.nodes)))))
                print(f"graph_nodes_dict_mapping: {graph_nodes_dict_mapping}")

                nodes_attributes = np.empty([0, node_features_nr])

                ########################################################################################################
                # [4.] Create file output ==============================================================================
                ########################################################################################################
                graph_edges_list = list(graph.edges)

                # [4.1.] Gather data information for each graph's object -----------------------------------------------
                sub_concept_str = ""
                graph_node_indexes_list = copy.deepcopy(list(graph.nodes))
                print(list(graph.nodes))

                for node_idx in list(graph.nodes):

                    # [4.2.] Rest of nodes to compute the relation -----------------------------------------------------
                    rest_of_nodes_indexes_list = copy.deepcopy(graph_node_indexes_list)
                    rest_of_nodes_indexes_list.remove(node_idx)

                    # [4.3.] Create the string of the subconcept -------------------------------------------------------
                    x_coor_8_float_digits = "{:.5f}".format(nodes_with_noise_pos_dict[node_idx][0])
                    y_coor_8_float_digits = "{:.5f}".format(nodes_with_noise_pos_dict[node_idx][1])

                    sub_concept_str += new_line_or_not + \
                                       f"contains(graph_{graph_idx_over_all}, object_{graph_idx_over_all}_{node_idx}), "

                    # [4.4.] Left-of and right-of ----------------------------------------------------------------------
                    for rest_node_idx in rest_of_nodes_indexes_list:

                        if (node_idx, rest_node_idx) in graph_edges_list or \
                                (rest_node_idx, node_idx) in graph_edges_list:

                            # [4.4.1.] Define edge relevance -----------------------------------------------------------
                            edge_relevance_fixed = edge_relevances_fixed_dict[(node_idx, rest_node_idx)]
                            if nodes_with_noise_pos_dict[node_idx][0] < nodes_with_noise_pos_dict[rest_node_idx][0]:
                                sub_concept_str += f"left_of(object_{graph_idx_over_all}_{node_idx}, " \
                                                   f"object_{graph_idx_over_all}_{rest_node_idx}), " \
                                                   + new_line_or_not
                            elif nodes_with_noise_pos_dict[node_idx][0] > nodes_with_noise_pos_dict[rest_node_idx][0]:
                                sub_concept_str += f"right_of(object_{graph_idx_over_all}_{node_idx}, " \
                                                   f"object_{graph_idx_over_all}_{rest_node_idx}), " \
                                                   + new_line_or_not

                    # [4.5.] Add the shapes, coordinates, color, relevances --------------------------------------------
                    sub_concept_str += f"is_a(object_{graph_idx_over_all}_{node_idx}, {nodes_shapes[node_idx]}), " \
                                       + new_line_or_not
                    sub_concept_str += f"has_coordinates(object_{graph_idx_over_all}_{node_idx}, " + \
                                       x_coor_8_float_digits + ", " + \
                                       y_coor_8_float_digits + "), " + new_line_or_not
                    sub_concept_str += f"has_color(object_{graph_idx_over_all}_{node_idx}, " + \
                                       f"{nodes_colors[node_idx]}), " + new_line_or_not

                    # [4.6.] Node characteristics ----------------------------------------------------------------------
                    node_shape_enc = label_encoder_shapes.transform(np.array([nodes_shapes[node_idx]]))[0]
                    node_color_enc = label_encoder_colors.transform(np.array([nodes_colors[node_idx]]))[0]
                    nodes_attributes_row = [node_shape_enc, node_color_enc,
                                            nodes_with_noise_pos_dict[node_idx][0],
                                            nodes_with_noise_pos_dict[node_idx][1]]
                    nodes_attributes = np.vstack((nodes_attributes, nodes_attributes_row))
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                relevance_sum = graph_relevance_sum_components(graph,
                                                               node_relevances_fixed_dict,
                                                               edge_relevances_fixed_dict)
                sub_concept_str += new_line_or_not + f"has_relevance(graph_{graph_idx_over_all}, " + \
                                   "{:.5f}".format(relevance_sum) + "), " + new_line_or_not

                # [4.7.] Add up the strings ----------------------------------------------------------------------------
                cncpt_name_str = ""
                if kandinksy_pattern_name == "symmetric":
                    cncpt_name_str = "symmetry"
                else:
                    cncpt_name_str = "non-symmetry"

                graph_data = f'graph_{graph_idx_over_all}; ' + \
                             str(nodes_with_positions_combinations) + "; " + \
                             str(graph_edges_list) + "; " + \
                             cncpt_name_str + '; ' + new_line_or_not + new_line_or_not + \
                             sub_concept_str
                print(graph_data)

                # [4.8.] Write graph output ----------------------------------------------------------------------------
                f = open(os.path.join("data", "output", concept_name,
                                      f"{concept_name}_nodes_nr_{nodes_nr}",
                                      kandinksy_pattern_name,
                                      f"positionierung_{positionierung}_graph_{graph_idx_over_all}.txt"), 'w')
                f.writelines(graph_data)
                f.close()

                ########################################################################################################
                # [5.] Plots ===========================================================================================
                ########################################################################################################
                """
                plot_kandinsky_concept_predefined_distr(
                    node_relevances_fixed_dict, edge_relevances_fixed_dict, nodes_with_noise_pos_dict, graph,
                    image_x_left_lim, image_x_right_lim, image_y_down_lim, image_y_up_lim,
                    kandinksy_pattern_name, concept_name,
                    graph_idx_over_all, nodes_nr, positionierung,
                    relevance_sum,
                    None
                )
                """

                ########################################################################################################
                # [6.] Graph dataset ===================================================================================
                ########################################################################################################

                # [6.1.] "nodes_attributes" already computed in [4.6.] -------------------------------------------------

                # [6.2.] Edge Idx --------------------------------------------------------------------------------------
                edges_left_indexes = []
                edges_right_indexes = []

                for edge_tuple in graph.edges:
                    edges_left_indexes.append(graph_nodes_dict_mapping[edge_tuple[0]])
                    edges_right_indexes.append(graph_nodes_dict_mapping[edge_tuple[1]])

                edge_idx_np = np.array([edges_left_indexes, edges_right_indexes])
                edge_idx = torch.tensor(edge_idx_np, dtype=torch.long)

                # [6.3.] Graph label -----------------------------------------------------------------------------------
                if kandinksy_pattern_name == "symmetric":
                    label = 1
                elif kandinksy_pattern_name == "non_symmetric":
                    label = 0
                else:
                    print("The concept should be either symmetric or non-symmetric")

                # [6.4.] Graph -----------------------------------------------------------------------------------------
                print("-----------------------------------------------------------------------------------------------")
                print(f"Graph: {graph_idx_over_all}")
                print(nodes_attributes)
                print(edge_idx)
                print(label)

                graph_torch = Data(
                    x=torch.tensor(nodes_attributes, dtype=torch.float32),
                    edge_index=edge_idx,
                    edge_attr=None,
                    y=torch.tensor([label]),
                    pos=None,
                    node_labels=np.array(graph.nodes),
                    node_feature_labels=["shape", "color", "coordinate_x", "coordinate_y"],
                    graph_id=f"graph_id_{concept_name}_{graph_idx_over_all}_0"
                )

                print(graph_torch)

                graphs_all[f"graph_{graph_idx_over_all}"] = graph_torch
                relevance_sum_all[f"graph_{graph_idx_over_all}"] = relevance_sum

                node_index_current = 0
                for nodes in list(graph.nodes):
                    nodes_relevances[node_index_current] = node_relevances_fixed_dict[nodes]
                    node_index_current += 1
                edge_index_current = 0
                for edge in list(graph.edges):
                    edges_relevances[edge_index_current] = edge_relevances_fixed_dict[edge]
                    edge_index_current += 1

                relevance_graph_components_all[f"graph_{graph_idx_over_all}"] = \
                    {"nodes_relevances": nodes_relevances,
                     "edges_relevances": edges_relevances}

                print("===============================================================================================")

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                graph_idx_over_all += 1

            positionierung += 1

    return graph_idx_over_all, graphs_all, relevance_sum_all, relevance_graph_components_all

########################################################################################################################
# [0.] Create all possible graphs ======================================================================================
########################################################################################################################
max_nr_nodes = 4
all_node_ids = [0, 1, 2, 3]
nodes_pos_dict = {0: [1, 1], 1: [2, 1], 2: [1, 2], 3: [2, 2]}
nodes_shapes = ["triangle", "triangle", "circle", "circle"]
nodes_colors = ["0, 0, 255", "0, 0, 255", "255, 255, 0", "255, 255, 0"]

mu, sigma = 0, 0.1

image_x_left_lim = 0.5
image_x_right_lim = 2.5
image_y_down_lim = 0.5
image_y_up_lim = 2.5

node_relevances_fixed_dict, edge_relevances_fixed_dict = fixed_graph_relevance_distribution()

graph_idx_over_all = 30

concept_name = "concept_x_axis_relations"

########################################################################################################################
# [1.] Symmetric =======================================================================================================
########################################################################################################################
kandinksy_pattern_name = "symmetric"
nodes_with_noise_pos_symmetric_dict = symmetric_node_positions(image_x_left_lim, image_x_right_lim)

graph_idx_over_all, graphs_all_symmetric, relevance_sum_all_symmetric, relevance_graph_components_all_symmetric = \
    x_axis_relations(all_node_ids,
                     nodes_shapes,
                     nodes_colors,
                     nodes_with_noise_pos_symmetric_dict,
                     node_relevances_fixed_dict,
                     edge_relevances_fixed_dict,
                     image_x_left_lim, image_x_right_lim,
                     image_y_down_lim, image_y_up_lim,
                     kandinksy_pattern_name,
                     concept_name,
                     graph_idx_over_all
                     )

########################################################################################################################
# [2.] Non-Symmetric ===================================================================================================
########################################################################################################################
kandinksy_pattern_name = "non_symmetric"
nodes_with_noise_pos_non_symmetric_dict = non_symmetric_node_positions(image_x_left_lim, image_x_right_lim)

graph_idx_over_all, graphs_all_non_symmetric, relevance_sum_all_non_symmetric, \
    relevance_graph_components_all_non_symmetric = x_axis_relations(
    all_node_ids,
    nodes_shapes,
    nodes_colors,
    nodes_with_noise_pos_non_symmetric_dict,
    node_relevances_fixed_dict,
    edge_relevances_fixed_dict,
    image_x_left_lim, image_x_right_lim,
    image_y_down_lim,
    image_y_up_lim,
    kandinksy_pattern_name,
    concept_name,
    graph_idx_over_all
)

print(f"=============================> LAST GRAPH ID: {graph_idx_over_all}")

########################################################################################################################
# [3.] Zip the files in the end ========================================================================================
########################################################################################################################
zip_generated_files(concept_name)

########################################################################################################################
# [4.] Graph dataset ===================================================================================================
########################################################################################################################
graphs_all = graphs_all_symmetric
graphs_all.update(graphs_all_non_symmetric)
print(graphs_all)

relevance_sum_all = relevance_sum_all_symmetric
relevance_sum_all.update(relevance_sum_all_non_symmetric)
print(relevance_sum_all)

relevance_graph_components_all = relevance_graph_components_all_symmetric
relevance_graph_components_all.update(relevance_graph_components_all_non_symmetric)
print(relevance_graph_components_all)

node_positions_all = {"symmetric": nodes_with_noise_pos_symmetric_dict,
                      "non_symmetric": nodes_with_noise_pos_non_symmetric_dict}

dataset_pytorch_folder = os.path.join("data", "output", "concept_x_axis_relations")
with open(os.path.join(dataset_pytorch_folder, 'concept_x_axis_relevances_sums.pkl'), 'wb') as f:
    pickle.dump(graphs_all, f)
with open(os.path.join(dataset_pytorch_folder, 'relevance_sums.pkl'), 'wb') as f:
    pickle.dump(relevance_sum_all, f)
with open(os.path.join(dataset_pytorch_folder, 'relevance_graph_components_all.pkl'), 'wb') as f:
    pickle.dump(relevance_graph_components_all, f)
with open(os.path.join(dataset_pytorch_folder, 'node_positions_all.pkl'), 'wb') as f:
    pickle.dump(node_positions_all, f)

