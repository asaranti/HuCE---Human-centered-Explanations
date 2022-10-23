"""
    Test the consistency of the generated files

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-19
"""

all_possible_relations = ["left_of", "right_of", "down_of", "up_of",
                          "top_left", "top_middle", "top_right",
                          "middle_left", "middle_right"
                          "bottom_left", "bottom_middle", "bottom_right",
                          "top_middle_top_right",
                          "middle_right_top_right",
                          "middle_right_bottom_right",
                          "bottom_middle_bottom_right",
                          "bottom_middle_bottom_left",
                          "middle_left_bottom_left",
                          "middle_left_top_left",
                          "top_middle_top_left"]


def check_nodes_edges_consistency(input_file_content: str, nodes_indexes_list: list, edge_indexes_list: list):
    """
    Check the nodes and edges consistency.
    [1.] The egdes' nodes indexes (if any) must be contained in the node indexes
    [2.] No edges <-- means --> no relation
    [3.] Only elements that have an edge between them, can have a relation

    :param input_file_content: The whole input file content
    :param nodes_indexes_list: List of node indexes
    :param edge_indexes_list: List of edge tuples and indexes
    """

    # [1.] The egdes' nodes indexes (if any) must be contained in the node indexes -------------------------------------
    if len(edge_indexes_list) > 0:
        print("NODE INDEX CHECK TODO")

    # No edges <-- means --> no relation -------------------------------------------------------------------------------
    if len(edge_indexes_list) == 0:
        for relation_str in all_possible_relations:
            assert relation_str not in input_file_content, f"No edge means no relation. " \
                                                           f"The relation {relation_str} should not be in the file."

    # [3.] Only elements that have an edge between them, can have a relation -------------------------------------------


