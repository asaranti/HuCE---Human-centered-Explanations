"""
    Graph Generators Runner

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-06
"""

from graph_generators.graph_generators_creators.graph_creator_all_possible_graphs import \
    generator_all_possible_graphs_graph

########################################################################################################################
# [1.] Graphs dataset for classification ===============================================================================
########################################################################################################################
kandinsky_pattern_name = "OneRedKPattern"
class_name_0 = "counterfactual"         # Class 0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class_name_1 = "true"                   # Class 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

num_classes = 2

data_dict, data_files_names_dict, positions_dict = generator_all_possible_graphs_graph(
    kandinsky_pattern_name,
    class_name_0,
    class_name_1
)
