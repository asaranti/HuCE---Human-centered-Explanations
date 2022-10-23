"""
    Nodes distances

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2021-09-29
"""

import numpy as np
import pandas as pd

from scipy.spatial import ConvexHull, distance


def distances_nodes(df: pd.DataFrame, left_nodes_list: list, right_nodes_list: list) -> np.ndarray:
    """
    Compute the distance of the nodes, the coordinates of the edge corners

    :param df: Dataframe
    :param left_nodes_list: List of indexes of nodes ("left side")
    :param right_nodes_list: List of indexes of nodes ("right side")
    :return:
    """

    # [0.] Iteration ---------------------------------------------------------------------------------------------------
    image_size = 224
    x_coordinates = df["coor_x"].tolist()
    y_coordinates = df["coor_y"].tolist()
    shapes = df["shape"].tolist()
    sizes = df["size"].tolist()

    euclidean_dist_list = []

    for node_idx in range(len(left_nodes_list)):

        left_node_index = left_nodes_list[node_idx]
        coor_x_left = x_coordinates[left_node_index]
        coor_y_left = y_coordinates[left_node_index]

        right_node_index = right_nodes_list[node_idx]
        coor_x_right = x_coordinates[right_node_index]
        coor_y_right = y_coordinates[right_node_index]

        # [2.] Distance between the nodes ------------------------------------------------------------------------------
        euclidean_dist = distance.euclidean([coor_x_left, coor_y_left], [coor_x_right, coor_y_right])
        euclidean_dist_list.append(euclidean_dist)

        ################################################################################################################
        # [3.] Depending on the shape type one can compute the the edge points -----------------------------------------
        ################################################################################################################
        # [3.1.] Compute the corner points of the object depending on its shape and size -------------------------------
        shape_left = shapes[left_node_index]
        shape_right = shapes[right_node_index]

        size_left = sizes[left_node_index]
        size_right = sizes[right_node_index]

        # Compute the nearest point of the convex hull to the center of the other --------------------------------------
        left_obj_convex_hull = compute_edge_point_on_object(shape_left, size_left, image_size, coor_x_left, coor_y_left)
        right_obj_convex_hull = compute_edge_point_on_object(shape_right, size_right, image_size,
                                                             coor_x_right, coor_y_right)

    # [5.] Gather all the egde features --------------------------------------------------------------------------------
    euclidean_dist_reshaped = np.array(euclidean_dist_list).reshape(-1, 1)

    return euclidean_dist_reshaped


def compute_edge_point_on_object(obj_shape: int, obj_size: float, image_size: int, coor_x: float, coor_y: float):
    """
    Compute the edge point on the object

    :param obj_shape: Shape type of the object
    :param obj_size: Object size in relation to the size of the image
    :param image_size: Image size
    :param coor_x: x coordinate of the center point
    :param coor_y: y coordinate of the center point
    """

    half_size = image_size * obj_size / 2

    ####################################################################################################################
    # [1.] Compute the convex hull / circumference =====================================================================
    ####################################################################################################################
    # [1.1.] CIRCLE ----------------------------------------------------------------------------------------------------
    if obj_shape == 0:

        circumference_points_nr = 100
        radius = half_size

        radians_between_each_point = 2 * np.pi / circumference_points_nr
        obj_convex_hull = []
        for p in range(0, circumference_points_nr):
            obj_convex_hull.append(
                (radius * np.cos(p * radians_between_each_point), radius * np.sin(p * radians_between_each_point)))

    # [1.2.] SQUARE ----------------------------------------------------------------------------------------------------
    if obj_shape == 1:

        point_left_down_x_1 = coor_x + half_size
        point_left_down_y_1 = coor_y + half_size

        point_left_up_x_2 = coor_x + half_size
        point_left_up_y_2 = coor_y - half_size

        point_right_up_x_3 = coor_x - half_size
        point_right_up_y_3 = coor_y - half_size

        point_right_down_x_4 = coor_x - half_size
        point_right_down_y_4 = coor_y + half_size

        points = np.array([[point_left_down_x_1, point_left_down_y_1],
                           [point_left_up_x_2, point_left_up_y_2],
                           [point_right_up_x_3, point_right_up_y_3],
                           [point_right_down_x_4, point_right_down_y_4]])

        obj_convex_hull = ConvexHull(points)

    # [1.3.] TRIANGLE --------------------------------------------------------------------------------------------------
    elif obj_shape == 2:

        point_left_down_x_1 = coor_x + half_size
        point_left_down_y_1 = coor_y + half_size

        point_up_middle_x_2 = coor_x
        point_up_middle_y_2 = coor_y - half_size

        point_right_down_x_3 = coor_x - half_size
        point_right_down_y_3 = coor_y + half_size

        points = np.array([[point_left_down_x_1, point_left_down_y_1],
                           [point_up_middle_x_2, point_up_middle_y_2],
                           [point_right_down_x_3, point_right_down_y_3]])

        obj_convex_hull = ConvexHull(points)

    else:
        assert False, "Unknown shape"

    print(obj_convex_hull)


