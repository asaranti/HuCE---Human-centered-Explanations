"""
    Geometric relations utilities

    :author: Anna Saranti
    :copyright: © 2021 HCI-KDD (ex-AI) group
    :date: 2022-02-08
"""

from shapely import geometry
from shapely.geometry import LineString, Point, Polygon


def point_contained_alignment_triangles(image_x_left_lim: float, image_x_right_lim: float,
                                        image_y_down_lim: float, image_y_up_lim: float,
                                        center_obj_x_coor: float, center_obj_y_coor: float,
                                        obj_contained_x_coor: float, obj_contained_y_coor: float) -> str:
    """
    Point contained in the alignment triangles of the image.

    :param image_x_left_lim: Left limit of the x coordinate in image
    :param image_x_right_lim: Right limit of the x coordinate in image
    :param image_y_down_lim: Down limit of the y coordinate in image
    :param image_y_up_lim: Up limit of the y coordinate in image
    :param center_obj_x_coor: The x coordinate of the center object
    :param center_obj_y_coor: The y coordinate of the center object
    :param obj_contained_x_coor: Object's x coordinate to search in which triangle is contained
    :param obj_contained_y_coor: Object's y coordinate to search in which triangle is contained

    :return: The subconcept string
    """

    ####################################################################################################################
    # [0.] Center of objects the same ==================================================================================
    ####################################################################################################################
    if center_obj_x_coor == obj_contained_x_coor and image_y_down_lim == image_y_up_lim:
        return "center"

    ####################################################################################################################
    # [1.] Define the image edge points ================================================================================
    ####################################################################################################################
    middle_right_coors = (image_x_right_lim, center_obj_y_coor)
    top_right_coors = (image_x_right_lim, image_y_up_lim)
    top_middle_coors = (center_obj_x_coor, image_y_up_lim)
    top_left_coors = (image_x_left_lim, image_y_up_lim)
    middle_left_coors = (image_x_left_lim, center_obj_y_coor)
    bottom_left_coors = (image_x_left_lim, image_y_down_lim)
    bottom_middle_coors = (center_obj_x_coor, image_y_down_lim)
    bottom_right_coors = (image_x_right_lim, image_y_down_lim)

    # Coordinates of the center object point ---------------------------------------------------------------------------
    center_obj_coors = (center_obj_x_coor, center_obj_y_coor)

    ####################################################################################################################
    # [2.] Define the triangles by which you split the image and their corresponding subconcepts =======================
    ####################################################################################################################
    polygon_1 = Polygon([center_obj_coors, top_right_coors, top_middle_coors])
    polygon_2 = Polygon([center_obj_coors, middle_right_coors, top_right_coors])
    polygon_3 = Polygon([center_obj_coors, bottom_right_coors, middle_right_coors])
    polygon_4 = Polygon([center_obj_coors, bottom_middle_coors, bottom_right_coors])
    polygon_5 = Polygon([center_obj_coors, bottom_left_coors, bottom_middle_coors])
    polygon_6 = Polygon([center_obj_coors, middle_left_coors, bottom_left_coors])
    polygon_7 = Polygon([center_obj_coors, top_left_coors, middle_left_coors])
    polygon_8 = Polygon([center_obj_coors, top_middle_coors, top_left_coors])

    polygon_1_subconcept = "top_middle_top_right"           #
    polygon_2_subconcept = "middle_right_top_right"         #
    polygon_3_subconcept = "middle_right_bottom_right"      #
    polygon_4_subconcept = "bottom_middle_bottom_right"     #
    polygon_5_subconcept = "bottom_middle_bottom_left"      #
    polygon_6_subconcept = "middle_left_bottom_left"        #
    polygon_7_subconcept = "middle_left_top_left"           #
    polygon_8_subconcept = "top_middle_top_left"            #

    ####################################################################################################################
    # [3.] Compute in which polygon the object is contained and return the corresponding subconcept string =============
    ####################################################################################################################
    obj_contained_coors = Point(obj_contained_x_coor, obj_contained_y_coor)

    # [3.1.] Object exactly on the line of the image's rectangle edge objects ------------------------------------------
    top_right_line = LineString([center_obj_coors, top_right_coors])
    top_middle_line = LineString([center_obj_coors, top_middle_coors])
    top_left_line = LineString([center_obj_coors, top_left_coors])
    middle_left_line = LineString([center_obj_coors, middle_left_coors])
    bottom_left_line = LineString([center_obj_coors, bottom_left_coors])
    bottom_middle_line = LineString([center_obj_coors, bottom_middle_coors])
    bottom_right_line = LineString([center_obj_coors, bottom_right_coors])
    middle_right_line = LineString([center_obj_coors, middle_right_coors])

    top_right_top_middle_line = LineString([top_right_coors, top_middle_coors])
    top_middle_top_left_line = LineString([top_middle_coors, top_left_coors])
    top_left_middle_left_line = LineString([top_left_coors, middle_left_coors])
    middle_left_bottom_left_line = LineString([middle_left_coors, bottom_left_coors])
    bottom_left_bottom_middle_line = LineString([bottom_left_coors, bottom_middle_coors])
    bottom_middle_bottom_right_line = LineString([bottom_middle_coors, bottom_right_coors])
    bottom_right_middle_right_line = LineString([bottom_right_coors, middle_right_coors])
    middle_right_top_right_line = LineString([middle_right_coors, top_right_coors])

    if top_right_line.covers(obj_contained_coors):
        return "top_right"
    elif top_middle_line.covers(obj_contained_coors):
        return "top_middle"
    elif top_left_line.covers(obj_contained_coors):
        return "top_left"
    elif middle_left_line.covers(obj_contained_coors):
        return "middle_left"
    elif bottom_left_line.covers(obj_contained_coors):
        return "bottom_left"
    elif bottom_middle_line.covers(obj_contained_coors):
        return "bottom_middle"
    elif bottom_right_line.covers(obj_contained_coors):
        return "bottom_right"
    elif middle_right_line.covers(obj_contained_coors):
        return "middle_right"
    # [3.2.] Object exactly on the line of the image's rectangle edge lines --------------------------------------------
    elif top_right_top_middle_line.contains(obj_contained_coors):
        return polygon_1_subconcept
    elif top_middle_top_left_line.contains(obj_contained_coors):
        return polygon_8_subconcept
    elif top_left_middle_left_line.contains(obj_contained_coors):
        return polygon_7_subconcept
    elif middle_left_bottom_left_line.contains(obj_contained_coors):
        return polygon_6_subconcept
    elif bottom_left_bottom_middle_line.contains(obj_contained_coors):
        return polygon_5_subconcept
    elif bottom_middle_bottom_right_line.contains(obj_contained_coors):
        return polygon_4_subconcept
    elif bottom_right_middle_right_line.contains(obj_contained_coors):
        return polygon_3_subconcept
    elif middle_right_top_right_line.contains(obj_contained_coors):
        return polygon_2_subconcept
    # [3.3.] Object contained inside the polygon -----------------------------------------------------------------------
    elif polygon_1.contains(obj_contained_coors):
        return polygon_1_subconcept
    elif polygon_2.contains(obj_contained_coors):
        return polygon_2_subconcept
    elif polygon_3.contains(obj_contained_coors):
        return polygon_3_subconcept
    elif polygon_4.contains(obj_contained_coors):
        return polygon_4_subconcept
    elif polygon_5.contains(obj_contained_coors):
        return polygon_5_subconcept
    elif polygon_6.contains(obj_contained_coors):
        return polygon_6_subconcept
    elif polygon_7.contains(obj_contained_coors):
        return polygon_7_subconcept
    elif polygon_8.contains(obj_contained_coors):
        return polygon_8_subconcept
    else:
        assert False, f"The object with coordinates: {obj_contained_coors}\n" \
                      f"is not contained in any of the triangles\n" \
                      f"of the image with the imaginary center {center_obj_coors}.\n" \
                      f"There is a BUG in your code !!!"
