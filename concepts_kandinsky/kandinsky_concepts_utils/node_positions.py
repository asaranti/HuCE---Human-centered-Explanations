"""
    Calculate node positions
    Symmetric and non-symmetric

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-10
"""

import copy

import numpy as np


def symmetric_node_positions(image_x_left_lim: float, image_x_right_lim: float) -> dict:
    """
    Compute the symmetric node positions

    :param image_x_left_lim: Left limit of image
    :param image_x_right_lim: Right limit of image

    Return the noisy node positions for the symmetric pattern
    """

    mu, sigma = 0, 0.1

    nodes_pos_dict = {0: [1, 1], 1: [2, 1], 2: [1, 2], 3: [2, 2]}

    # Add some noise on the node positions -----------------------------------------------------------------------------
    nr_of_added_noise_values = 4  # Two nodes on the left + noise ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    noise_add_positions = np.random.normal(mu, sigma, nr_of_added_noise_values)
    print(noise_add_positions)

    nodes_with_noise_pos_dict = copy.deepcopy(nodes_pos_dict)
    # x and y coordinates of node_0 and node_2 on the left side of the image is perturbed with noise +++++++++++++++++++
    nodes_with_noise_pos_dict[0][0] = nodes_with_noise_pos_dict[0][0] + noise_add_positions[0]
    nodes_with_noise_pos_dict[0][1] = nodes_with_noise_pos_dict[0][1] + noise_add_positions[1]
    nodes_with_noise_pos_dict[2][0] = nodes_with_noise_pos_dict[2][0] + noise_add_positions[2]
    nodes_with_noise_pos_dict[2][1] = nodes_with_noise_pos_dict[2][1] + noise_add_positions[3]

    # x and y coordinates of node_1 and node_3 on the left side of the image is perturbed with noise +++++++++++++++++++
    nodes_with_noise_pos_dict[1][0] = image_x_right_lim - (nodes_with_noise_pos_dict[0][0] - image_x_left_lim)
    nodes_with_noise_pos_dict[1][1] = nodes_with_noise_pos_dict[0][1]
    nodes_with_noise_pos_dict[3][0] = image_x_right_lim - (nodes_with_noise_pos_dict[2][0] - image_x_left_lim)
    nodes_with_noise_pos_dict[3][1] = nodes_with_noise_pos_dict[2][1]

    return nodes_with_noise_pos_dict


def non_symmetric_node_positions(image_x_left_lim: float, image_x_right_lim: float) -> dict:
    """
    Compute the non_symmetric node positions

    :param image_x_left_lim: Left limit of image
    :param image_x_right_lim: Right limit of image

    Return the noisy node positions for the symmetric pattern
    """

    mu, sigma = 0, 0.1

    nodes_pos_dict = {0: [1, 1], 1: [2, 1], 2: [1, 2], 3: [2, 2]}

    ####################################################################################################################
    # [1.] Add some noise on the node positions ------------------------------------------------------------------------
    nr_of_added_noise_values = 8  # Two nodes on the left + noise ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    noise_add_positions = np.random.normal(mu, sigma, nr_of_added_noise_values)
    print(noise_add_positions)

    nodes_with_noise_pos_dict = copy.deepcopy(nodes_pos_dict)
    # x and y coordinates of node_0 and node_2 on the left side of the image is perturbed with noise +++++++++++++++++++
    nodes_with_noise_pos_dict[0][0] = nodes_with_noise_pos_dict[0][0] + noise_add_positions[0]
    nodes_with_noise_pos_dict[0][1] = nodes_with_noise_pos_dict[0][1] + noise_add_positions[1]
    nodes_with_noise_pos_dict[2][0] = nodes_with_noise_pos_dict[2][0] + noise_add_positions[2]
    nodes_with_noise_pos_dict[2][1] = nodes_with_noise_pos_dict[2][1] + noise_add_positions[3]

    # x and y coordinates of node_1 and node_3 on the left side of the image is perturbed with noise +++++++++++++++++++
    nodes_with_noise_pos_dict[1][0] = nodes_with_noise_pos_dict[1][0] + noise_add_positions[4]
    nodes_with_noise_pos_dict[1][1] = nodes_with_noise_pos_dict[1][1] + noise_add_positions[5]
    nodes_with_noise_pos_dict[3][0] = nodes_with_noise_pos_dict[3][0] + noise_add_positions[6]
    nodes_with_noise_pos_dict[3][1] = nodes_with_noise_pos_dict[3][1] + noise_add_positions[7]

    ####################################################################################################################
    # [2.] Make sure that the y axis of node 0 and 1 are different -----------------------------------------------------
    while nodes_with_noise_pos_dict[0][1] == nodes_with_noise_pos_dict[1][1]:
        noise_add_y_pos = np.random.normal(mu, sigma, 1)
        nodes_with_noise_pos_dict[1][1] = nodes_with_noise_pos_dict[1][1] + noise_add_y_pos[0]

    # Make sure that the y axis of node 2 and 3 are different ----------------------------------------------------------
    while nodes_with_noise_pos_dict[2][1] == nodes_with_noise_pos_dict[3][1]:
        noise_add_y_pos = np.random.normal(mu, sigma, 1)
        nodes_with_noise_pos_dict[3][1] = nodes_with_noise_pos_dict[3][1] + noise_add_y_pos[0]

    return nodes_with_noise_pos_dict
