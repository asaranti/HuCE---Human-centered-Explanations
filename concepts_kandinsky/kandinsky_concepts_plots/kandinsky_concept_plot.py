"""
    Kandinsky Concept plot

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-09
"""

import os

import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
import networkx as nx
from networkx.classes.graph import Graph


def plot_kandinsky_concept_zero_one(node_relevances_dict: dict,
                                    edge_relevances_dict: dict,
                                    nodes_with_noise_pos_dict: dict,
                                    graph: Graph,
                                    image_x_left_lim: float, image_x_right_lim: float,
                                    image_y_down_lim: float, image_y_up_lim: float,
                                    kandinksy_pattern_name: str, concept_name: str,
                                    graph_idx: int, nodes_nr: int, positionierung: int):
    """
    Kandinsky Concept plot

    :param node_relevances_dict: Dictionary with the node relevances
    :param edge_relevances_dict: Dictionary with edge relevances
    :param nodes_with_noise_pos_dict: Positions of nodes
    :param graph: Input graph with nodes
    :param image_x_left_lim: Left limit of the image
    :param image_x_right_lim: Right limit of the image
    :param image_y_down_lim: Down limit of the image
    :param image_y_up_lim: Upper limit of the image
    :param kandinksy_pattern_name: Kandinsky Pattern name
    :param concept_name: Concept name that will define the folder
    :param graph_idx: Index of the graph, as it is stored and presented
    :param nodes_nr: Number of nodes
    :param positionierung: Positionierung of nodes - their (x,y) coordinates
    """

    viz_style = "zero_one"

    ####################################################################################################################
    # [1.] Compute the node relevances color ===========================================================================
    ####################################################################################################################
    print(node_relevances_dict)

    blue_color_str = "#42C0FB"
    red_color_str = "#F88379"

    color_nodes_map = []
    for node_relevance_index in list(graph.nodes):

        node_relevance = node_relevances_dict[node_relevance_index]

        if node_relevance == 0.0:
            color_nodes_map.append(blue_color_str)
        elif node_relevance == 1.0:
            color_nodes_map.append(red_color_str)
        else:
            assert False, f"Invalid node relevance value: {node_relevance} - \n" \
                          f"Only 0.0 or 1.0 allowed. Your code has a BUG !!!"

    print(color_nodes_map)

    ####################################################################################################################
    # [2.] Compute the edge relevances color ===========================================================================
    ####################################################################################################################
    color_edge_map = []
    for graph_edge in list(graph.edges):

        egde_relevance = edge_relevances_dict[graph_edge]

        if egde_relevance == 0.0:
            color_edge_map.append(blue_color_str)
        elif egde_relevance == 1.0:
            color_edge_map.append(red_color_str)
        else:
            assert False, f"Invalid edge relevance value: {egde_relevance} - \n" \
                          f"Only 0.0 or 1.0 allowed. Your code has a BUG !!!"

    ####################################################################################################################
    # [3.] Plot of the graph ===========================================================================================
    ####################################################################################################################
    fig = plt.figure(figsize=(12, 12))
    plt.title(f"Graph's edges: {graph.edges}", fontsize=40, fontweight="bold")
    nx.draw_networkx(
        graph,
        node_shape='o',
        pos=nodes_with_noise_pos_dict,
        node_color=color_nodes_map,
        edge_color=color_edge_map,
        node_size=2000,
        width=10,
        with_labels=True,
    )

    plt.xlim(image_x_left_lim, image_x_right_lim)
    plt.ylim(image_y_down_lim, image_y_up_lim)

    ####################################################################################################################
    # [4.] Save to .png file ===========================================================================================
    ####################################################################################################################
    fig.savefig(os.path.join("data", "output", concept_name,
                             f"{concept_name}_nodes_nr_{nodes_nr}",
                             kandinksy_pattern_name,
                             viz_style,
                             f"positionierung_{positionierung}_{viz_style}_graph_{graph_idx}.png"))
    plt.close()


def plot_kandinsky_concept_predefined_distr(node_relevances_input_dict: dict,
                                            edge_relevances_input_dict: dict,
                                            nodes_with_noise_pos_dict: dict,
                                            graph: Graph,
                                            image_x_left_lim: float, image_x_right_lim: float,
                                            image_y_down_lim: float, image_y_up_lim: float,
                                            kandinksy_pattern_name: str, concept_name: str,
                                            graph_idx: int, nodes_nr: int, positionierung: int,
                                            graph_relevance: float,
                                            graph_nodes_dict_mapping: dict):
    """
    Kandinsky Concept plot

    :param node_relevances_input_dict: Dictionary with the node relevances
    :param edge_relevances_input_dict: Dictionary with edge relevances
    :param nodes_with_noise_pos_dict: Positions of nodes
    :param graph: Input graph with nodes
    :param image_x_left_lim: Left limit of the image
    :param image_x_right_lim: Right limit of the image
    :param image_y_down_lim: Down limit of the image
    :param image_y_up_lim: Upper limit of the image
    :param kandinksy_pattern_name: Kandinsky Pattern name
    :param concept_name: Concept name that will define the folder
    :param graph_idx: Index of the graph, as it is stored and presented
    :param nodes_nr: Number of nodes
    :param positionierung: Positionierung of nodes - their (x,y) coordinates
    :param graph_relevance: Graph's relevance
    """

    viz_style = "predefined_distr"

    ####################################################################################################################
    # [1. + 2.] Compute the node and relevances color ==================================================================
    ####################################################################################################################
    node_relevances_values_list = []
    for node in list(graph.nodes):
        if graph_nodes_dict_mapping is None:
            node_relevances_values_list.append(node_relevances_input_dict[node])
        else:
            node_relevances_values_list.append(node_relevances_input_dict[graph_nodes_dict_mapping[node]])

    edge_relevances_values_list = []
    edge_relevances_dict = {}
    for graph_edge in list(graph.edges):

        edge_new = (graph_nodes_dict_mapping[graph_edge[0]], graph_nodes_dict_mapping[graph_edge[1]])

        edge_relevances_values_list.append(edge_relevances_input_dict[edge_new])
        edge_relevances_dict[graph_edge] = round(float(edge_relevances_input_dict[edge_new]), 3)

    node_relevances_all_values_list = list(node_relevances_input_dict.values())
    edge_relevances_all_values_list = list(edge_relevances_input_dict.values())

    relevances_all_list = node_relevances_all_values_list + edge_relevances_all_values_list
    relevances_all_list = list(set(relevances_all_list))
    relevances_all_list.sort()

    ####################################################################################################################
    # [3.] Plot of the graph ===========================================================================================
    ####################################################################################################################
    fig = plt.figure(figsize=(12, 12))
    plt.title("Graph's relevance: " + "{:.5f}".format(graph_relevance), fontsize=40, fontweight="bold")

    # [3.1.] Define the colormap for the nodes and edges + range -------------------------------------------------------
    v_min = min(relevances_all_list)
    v_max = max(relevances_all_list)

    norm = plt.Normalize(v_min, v_max)
    colors_all = plt.cm.coolwarm(norm(relevances_all_list))
    colors_all_rgb = []
    for color_ in colors_all:
        colors_all_rgb.append(rgb2hex(color_))

    color_nodes_map = []
    for node_relevance in node_relevances_values_list:
        node_relevance_idx = relevances_all_list.index(node_relevance)
        color_nodes_map.append(colors_all_rgb[node_relevance_idx])

    color_edges_map = []
    for egde_relevance in edge_relevances_values_list:
        edge_relevance_idx = relevances_all_list.index(egde_relevance)
        color_edges_map.append(colors_all_rgb[edge_relevance_idx])

    # [3.2.] Actual drawing the network --------------------------------------------------------------------------------
    print(f"graph.nodes: {graph.nodes}")
    print(f"graph.edges: {graph.edges}")
    print(nodes_with_noise_pos_dict)

    nodes_with_noise_pos_dict_new = {}
    key_idx = 0
    for key in list(nodes_with_noise_pos_dict.keys()):
        value = nodes_with_noise_pos_dict[key]
        nodes_with_noise_pos_dict_new[list(graph.nodes)[key_idx]] = value
        key_idx += 1

    print(nodes_with_noise_pos_dict_new)

    nx.draw_networkx(
        graph,
        node_shape='o',
        pos=nodes_with_noise_pos_dict_new,
        node_color=color_nodes_map,
        edge_color=color_edges_map,
        node_size=2000,
        width=10,
        with_labels=True,
    )

    # [3.3.] Define node relevances around the nodes in the graph ------------------------------------------------------
    node_index = 0
    for node in list(graph.nodes):

        if node == 0 or node == 1:
            plt.text(nodes_with_noise_pos_dict_new[node][0],
                     nodes_with_noise_pos_dict_new[node][1] - 0.15,
                     s=f'{round(float(node_relevances_input_dict[graph_nodes_dict_mapping[node]]), 2)}',
                     fontsize=24,
                     bbox=dict(facecolor=color_nodes_map[node_index]),
                     horizontalalignment='center')
        else:
            plt.text(nodes_with_noise_pos_dict_new[node][0],
                     nodes_with_noise_pos_dict_new[node][1] + 0.1,
                     s=f'{round(float(node_relevances_input_dict[graph_nodes_dict_mapping[node]]), 2)}',
                     fontsize=24,
                     bbox=dict(facecolor=color_nodes_map[node_index]),
                     horizontalalignment='center')

        node_index += 1

    # [3.4.] Define the edges labels as the edge relevance values ------------------------------------------------------
    nx.draw_networkx_edge_labels(
        graph,
        pos=nodes_with_noise_pos_dict_new,
        edge_labels=edge_relevances_dict,
        font_size=24
    )

    # Colormap ---------------------------------------------------------------------------------------------------------
    sm = plt.cm.ScalarMappable(cmap=plt.cm.coolwarm, norm=plt.Normalize(vmin=v_min, vmax=v_max))
    sm.set_array([])
    cbar = plt.colorbar(sm)

    plt.xlim(image_x_left_lim, image_x_right_lim)
    plt.ylim(image_y_down_lim, image_y_up_lim)

    ####################################################################################################################
    # [4.] Save to .png file ===========================================================================================
    ####################################################################################################################
    fig.savefig(os.path.join("data", "output", concept_name,
                             f"{concept_name}_nodes_nr_{nodes_nr}",
                             kandinksy_pattern_name,
                             f"positionierung_{positionierung}_{viz_style}_graph_{graph_idx}.png"))
    plt.close()
