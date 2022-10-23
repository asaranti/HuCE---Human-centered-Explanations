"""
    Graph visualization

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2021-10-04
"""

import os

import matplotlib.pyplot as plt
import networkx as nx
import torch_geometric


def graph_viz(graph_data: torch_geometric.data.data.Data, all_pairs_combinations: list, positions_dict: dict,
              images_path: str, image_name: str):
    """
    Graph visualization with matplotlib

    :param graph_data: Graph data
    :param all_pairs_combinations: Combinations of all graph nodes pairs
    :param positions_dict: Dictionary of positions
    :param images_path: Path of images
    :param image_name: Name of image
    :return:
    """

    graph_viz = torch_geometric.utils.to_networkx(graph_data, to_undirected=True)
    graph_viz.add_edges_from(all_pairs_combinations)

    fig = plt.figure(figsize=(12, 12))
    plt.xticks([])
    plt.yticks([])
    nx.draw_networkx(
        graph_viz,
        pos=positions_dict,
        with_labels=True,
    )
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.gca().invert_yaxis()
    plt.show()
    fig.savefig(os.path.join(images_path, image_name.replace("content", "graph").replace(".csv", "") + ".png"))
    plt.close()
