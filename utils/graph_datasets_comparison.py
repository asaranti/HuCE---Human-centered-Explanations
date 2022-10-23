"""
    Graph datasets comparison

    :author: Anna Saranti
    :copyright: © 2022 HCI-KDD (ex-AI) group
    :date: 2022-08-04
"""

import os
import pickle

# [0.] Import the datasets ---------------------------------------------------------------------------------------------
dataset_pytorch_folder = os.path.join("data", "output", "concept_x_axis_relations")
dataset_x_axis_relations = pickle.load(open(os.path.join(dataset_pytorch_folder,
                                                         'concept_x_axis_relations.pkl'),
                                            "rb"))

dataset_pytorch_folder = os.path.join("data", "output", "concept_y_axis_relations")
dataset_y_axis_relations = pickle.load(open(os.path.join(dataset_pytorch_folder,
                                                         'concept_y_axis_relations.pkl'),
                                            "rb"))

for graph_idx in range(len(dataset_x_axis_relations)):

    graph_x = dataset_x_axis_relations[graph_idx]
    graph_y = dataset_y_axis_relations[graph_idx]

    print(graph_x.x)
    print(graph_y.x)
    print(graph_x.edge_index)
    print(graph_y.edge_index)
    print("----------------------------------------------------------------------------")
