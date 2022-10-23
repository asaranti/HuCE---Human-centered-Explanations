"""
    Edges relevances utilities

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-08
"""


def define_edge_relevances(nodes_idx_list: list) -> dict:
    """
    Define the edge relevances

    :param nodes_idx_list: List of node indexes
    """

    edge_relevances_dict = {}

    ####################################################################################################################
    # [1.] Edges between left and right part of the image - without diagonals ==========================================
    ####################################################################################################################
    edge_relevances_dict[(0, 1)] = 1.0
    edge_relevances_dict[(1, 0)] = 1.0

    edge_relevances_dict[(2, 3)] = 1.0
    edge_relevances_dict[(3, 2)] = 1.0

    ####################################################################################################################
    # [2.] Diagonals relevance =========================================================================================
    ####################################################################################################################
    if nodes_idx_list == [1, 2] or nodes_idx_list == [2, 1] or nodes_idx_list == [0, 3] or nodes_idx_list == [3, 0]:
        edge_relevances_dict[(0, 3)] = 0.0
        edge_relevances_dict[(3, 0)] = 0.0

        edge_relevances_dict[(1, 2)] = 0.0
        edge_relevances_dict[(2, 1)] = 0.0
    else:
        edge_relevances_dict[(0, 3)] = 1.0
        edge_relevances_dict[(3, 0)] = 1.0

        edge_relevances_dict[(1, 2)] = 1.0
        edge_relevances_dict[(2, 1)] = 1.0

    ####################################################################################################################
    # [3.] Edges inside the left and inside the right part of the image ================================================
    ####################################################################################################################
    edge_relevances_dict[(0, 2)] = 0.0
    edge_relevances_dict[(2, 0)] = 0.0

    edge_relevances_dict[(1, 3)] = 0.0
    edge_relevances_dict[(3, 1)] = 0.0

    ####################################################################################################################
    # [4.] Return the dictionary =======================================================================================
    ####################################################################################################################
    return edge_relevances_dict
