"""
    Test the single object output files

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-19
"""

import os

from test_cases.consistencies_test import check_nodes_edges_consistency

########################################################################################################################
# [1.] Iterate over files ==============================================================================================
########################################################################################################################
concept_name = "concept_single_objects"
subfolder_names_list = ["symmetric", "non_symmetric"]

for nodes_nr in range(1, 5):

    files_output_nodes_nr_folder = os.path.join(
        "data",
        "output",
        concept_name,
        f"{concept_name}_nodes_nr_{nodes_nr}"
    )

    for sub_name in subfolder_names_list:
        sub_dir = os.path.join(files_output_nodes_nr_folder, sub_name)

        for file in os.listdir(sub_dir):
            file_name = os.fsdecode(file)
            if file_name.endswith(".txt"):

                file = open(os.path.join(sub_dir, file_name), 'r')
                lines = file.readlines()
                lines_nr = len(lines)

                lines_str = ' '.join(map(str, lines))

                for line_cnt in range(lines_nr):
                    line = lines[line_cnt]
                    if line_cnt == 0:

                        # [2.] Process the first line, get graph_id, nodes, edges and symmetry or non-symmetry ---------
                        first_line_array = line.split(";")

                        graph_str = first_line_array[0]
                        graph_idx = graph_str.split("_")[1]
                        nodes = first_line_array[1]
                        edges = first_line_array[2]
                        s_or_non_s = first_line_array[3]

                        nodes_list = nodes.replace('(', "").replace(')', "").split(", ")
                        nodes_list = [node_idx.replace(" ", "").replace(",", "") for node_idx in nodes_list]
                        nodes_list = list(map(int, nodes_list))

                        edges_list = edges.replace('[', "").replace(']', "").split(", ")
                        edges_list = [edge_idx.replace(" ", "").replace(",", "") for edge_idx in edges_list]
                        if len(edges_list) == 1 and edges_list[0] == '':
                            edges_list = []

                        if len(edges_list) > 0:
                            edges_list = list(map(int, edges_list))

                    # [3.] Check that the graph and node idx are present in the first line -----------------------------
                    # else:
                    #    if line.startswith("contains"):
                    #
                    #    elif line.startswith("is_a"):

                    # [4.] Basic consistency between nodes and edges ---------------------------------------------------
                    check_nodes_edges_consistency(lines_str, nodes_list, edges_list)

                    # [5.] Check the "symmetry" of the relations -------------------------------------------------------
                    # If there is "left_of", then there has to be "right_of" -------------------------------------------

                print("-------------------------------------------------")

