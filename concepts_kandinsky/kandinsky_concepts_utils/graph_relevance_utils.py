"""
    Graph relevance utilities

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-09
"""

from networkx.classes.graph import Graph


def fixed_graph_relevance_distribution() -> tuple:
    """
    Define a fixed graph elements relevance distribution
    and then each time you remove one element from that,
    then the sum of the relevance of the graph will be smaller.
    """

    node_relevances_dict = {0: 0.0625, 1: 0.0625, 2: 0.15, 3: 0.15}
    edge_relevances_dict = {}

    edge_relevances_dict[(0, 1)] = 0.1
    edge_relevances_dict[(1, 0)] = 0.1

    edge_relevances_dict[(0, 2)] = 0.0375
    edge_relevances_dict[(2, 0)] = 0.0375

    edge_relevances_dict[(0, 3)] = 0.075
    edge_relevances_dict[(3, 0)] = 0.075

    edge_relevances_dict[(1, 2)] = 0.075
    edge_relevances_dict[(2, 1)] = 0.075

    edge_relevances_dict[(1, 3)] = 0.0375
    edge_relevances_dict[(3, 1)] = 0.0375

    edge_relevances_dict[(2, 3)] = 0.15
    edge_relevances_dict[(3, 2)] = 0.15

    return node_relevances_dict, edge_relevances_dict


def graph_relevance_sum_components(graph: Graph,
                                   node_relevances_dict: dict,
                                   edge_relevances_dict: dict,
                                   graph_nodes_dict_mapping: dict=None):
    """
    The graph's relevance is the sum of its components

    :param graph: The input graph
    :param node_relevances_dict: Dictionary of node relevances
    :param edge_relevances_dict: Dictionary of edge relevances
    :param graph_nodes_dict_mapping:

    :return: The sum of relevances of the nodes and edges
    """

    relevance_sum = 0

    if graph_nodes_dict_mapping is None:
        for nodes in list(graph.nodes):
            relevance_sum += node_relevances_dict[nodes]
        for edge in list(graph.edges):
            relevance_sum += edge_relevances_dict[edge]
    else:
        for nodes in list(graph.nodes):
            relevance_sum += node_relevances_dict[graph_nodes_dict_mapping[nodes]]
        for edge in list(graph.edges):
            edge_new = (graph_nodes_dict_mapping[edge[0]], graph_nodes_dict_mapping[edge[1]])
            relevance_sum += edge_relevances_dict[edge_new]

    return relevance_sum
