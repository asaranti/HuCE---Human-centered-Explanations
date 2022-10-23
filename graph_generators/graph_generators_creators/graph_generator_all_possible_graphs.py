"""
    Create the fully connected graph with all the features
    and their corresponding encodings for further processing
    from a GNN

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2021-10-04
"""

from itertools import combinations
import numpy as np
import pandas as pd
from sklearn import preprocessing

import torch
import torch_geometric
from torch_geometric.data import Data
from utils.nodes_distances import distances_nodes

from plots.graph_visualization import graph_viz


def create_all_possible_graphs(data_df: pd.DataFrame, images_path: str, image_name: str, class_str: str) -> \
        tuple:
    """
    Create a fully connected graph with all features and encodings

    :param data_df: Dataframe of data
    :param images_path: Path of images
    :param image_name: Image name
    :param class_str: Class string description
    :return: Graph data
    """

    ####################################################################################################################
    # [1.] Create the fully connected graph ============================================================================
    ####################################################################################################################

    # [1.1.] Nodes features --------------------------------------------------------------------------------------------
    # TODO: Label Encoder is "primitive", it needs to be updated to something more orthogonal for both cases ~~~~~~~~~~~
    color_label_encoder = preprocessing.LabelEncoder()
    color_label_encoder.fit(["(255, 0, 0)", "(255, 255, 0)", "(0, 0, 255)"])
    color_encoded = color_label_encoder.transform(data_df["color"].tolist())
    data_df["color"] = color_encoded

    shape_label_encoder = preprocessing.LabelEncoder()
    shape_label_encoder.fit(["CIRCLE", "SQUARE", "TRIANGLE"])
    shape_encoded = shape_label_encoder.transform(data_df["shape"].tolist())
    data_df["shape"] = shape_encoded

    position_list = data_df["position"].tolist()
    coor_x_list = []
    coor_y_list = []
    positions_dict = {}
    row_cnt = 0
    for centroid in position_list:
        coordinates_array = centroid.replace("(", "").replace(")", "").split(",")
        coor_x = float(coordinates_array[0])
        coor_y = float(coordinates_array[1])
        coor_x_list.append(coor_x)
        coor_y_list.append(coor_y)

        positions_dict[row_cnt] = np.array([coor_x, coor_y])
        row_cnt += 1

    data_df["coor_x"] = coor_x_list
    data_df["coor_y"] = coor_y_list

    data_df.drop(['position'], axis=1, inplace=True)

    # [1.2.] Edge indexes and attributes -------------------------------------------------------------------------------
    edge_index, edge_attr = compute_edge_indexes_and_features(data_df)

    # [1.3.] Graph definition, visualization and image save ------------------------------------------------------------
    if class_str == "true":
        class_label = 1
    elif class_str == "counterfactual" or class_str == "false":
        class_label = 0
    else:
        assert False, "Class must be either true, counterfactual or false. Instead it is: " + str(class_str)

    # [1.4.] Drop the coordinates to allow more generalization ---------------------------------------------------------
    # data_df.drop(["coor_x"], axis=1, inplace=True)
    # data_df.drop(["coor_y"], axis=1, inplace=True)

    df_values_matrix = data_df.values
    nodes_features = torch.tensor(df_values_matrix, dtype=torch.float)

    # column_names = data_df.columns.values.tolist()
    # print(f"Column names: {column_names}")

    graph_data = Data(x=nodes_features,
                      edge_index=edge_index,
                      edge_attr=edge_attr,
                      y=torch.tensor([class_label],
                                     dtype=torch.long))

    # [2.] Visualization -----------------------------------------------------------------------------------------------
    # graph_viz(graph_data, all_pairs_combinations, positions_dict, images_path, image_name)

    # [3.] Return graph data -------------------------------------------------------------------------------------------
    return graph_data, positions_dict


def compute_edge_indexes_and_features(data_df: pd.DataFrame):
    """
    Compute the edge features

    :param data_df: Dataframe containing the nodes information

    :return: The tuple containing the edge_index (pairs of nodes connected with an edge) and edge_attr (edge attributes)
    """

    # [1.] Edge connectivity -------------------------------------------------------------------------------------------
    rows_nr = data_df.shape[0]
    nodes_nr_list = range(0, rows_nr)

    if rows_nr > 1:
        all_pairs_combinations = list(combinations(nodes_nr_list, 2))
        left_nodes_list, right_nodes_list = zip(*all_pairs_combinations)

        edge_index = torch.tensor(np.array([left_nodes_list, right_nodes_list]), dtype=torch.long)

        # [2.] Distances of nodes --------------------------------------------------------------------------------------
        edge_distances = distances_nodes(data_df, left_nodes_list, right_nodes_list)

    else:
        edge_index = torch.tensor(np.array([[], []]), dtype=torch.long)
        edge_distances = np.empty([0, 1])

    return edge_index, edge_attr
