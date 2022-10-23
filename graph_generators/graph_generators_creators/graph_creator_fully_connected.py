"""
    Fully connected graph generator
    Open the .csv file and create a fully connected graph

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2021-09-28
"""

import os

import pandas as pd

from graph_generators.graph_generators_creators.graph_generator_fully_connected import create_fully_connected_graph


def generator_graph(kandinsky_pattern_name: str, class_name_0: str, class_name_1: str) -> tuple:
    """
    Graph generator

    :param kandinsky_pattern_name: Kandinsky Pattern name
    :param class_name_0: Name of one class (usually "counterfactual" or "false")
    :param class_name_1: Name of the opposite class (usually "true")

    :return: Dictionary where the keys are "true", "false", "counterfactual" and values are list of graph data
    """

    # [1.] Read the input data =========================================================================================
    kandisnky_class_1_path = os.path.join("data", kandinsky_pattern_name, "kandinsky_input_data", class_name_1)
    kandisnky_class_0_path = os.path.join("data", kandinsky_pattern_name, "kandinsky_input_data", class_name_0)

    files_names_class_1_list = []
    files_names_class_0_list = []

    positions_class_1_list = []
    positions_class_0_list = []

    # True -------------------------------------------------------------------------------------------------------------
    graph_class_1_data = []
    for root, dirs, class_1_files in os.walk(kandisnky_class_1_path):
        for class_1_file in class_1_files:
            if 'content' in class_1_file and class_1_file.endswith('.csv'):

                files_names_class_1_list.append(class_1_file)

                class_1_df = pd.read_csv(os.path.join(kandisnky_class_1_path, class_1_file), index_col=0)
                graph_class_1_data_sample, positions_class_1_dict = create_fully_connected_graph(class_1_df,
                                                                                                 kandisnky_class_1_path,
                                                                                                 class_1_file,
                                                                                                 class_name_1)
                positions_class_1_list.append(positions_class_1_dict)
                graph_class_1_data.append(graph_class_1_data_sample)

    # Counterfactual ---------------------------------------------------------------------------------------------------
    graph_class_0_data = []
    for root, dirs, class_0_files in os.walk(kandisnky_class_0_path):
        for class_0_file in class_0_files:
            if 'content' in class_0_file and class_0_file.endswith('.csv'):

                files_names_class_0_list.append(class_0_file)

                class_0_df = pd.read_csv(os.path.join(kandisnky_class_0_path, class_0_file), index_col=0)
                graph_class_0_data_sample, positions_class_0_dict = create_fully_connected_graph(class_0_df,
                                                                                                 kandisnky_class_0_path,
                                                                                                 class_0_file,
                                                                                                 class_name_0)
                positions_class_0_list.append(positions_class_0_dict)
                graph_class_0_data.append(graph_class_0_data_sample)

    # Return dict ------------------------------------------------------------------------------------------------------
    return {class_name_1: graph_class_1_data, class_name_0: graph_class_0_data}, \
           {class_name_1: files_names_class_1_list, class_name_0: files_names_class_0_list}, \
           {class_name_1: positions_class_1_list, class_name_0: positions_class_0_list}

