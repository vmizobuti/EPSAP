# Implements the fitness function proposed by Rodrigues, E. et. al (2013).
#
# The function is composed of seven evaluators, each given by a different
# function in this script.
# 
# Author: Vinicius Mizobuti
# 
# Current Version: 1.0.0
# Release Date: WIP - 03/13/2022

import sys

from shapely.geometry import Polygon as ShpPolygon
from compas.geometry import offset_polygon

def connectivity_and_adjacency(spaces, design_data):
    """
    Computes the Connectivity/Adjacency Evaluator.
    If the Mcon matrix entry is 1 the connectivity is calculated.
    If the Mcon matrix entry is 2 the adjacency is calculated.
    If the Mcon matrix entry is 0 the returning value is zero.
    """
    # Declares the connectivity values list to store values for all spaces
    con_values = []
    
    # Starts the computation by iterating through the spaces j in every i
    for i in range(len(spaces)):
        # Declares the j index and the list to store connectivity values
        j = 0
        i_con = []

        # Computes the c-value based on the size of the space interior doors 
        # and the wall thickness
        c = design_data.t_iw + \
            max([sum(design_data.m_ids[i]), sum(design_data.m_ids[j])])

        # Iterates throug the connectivity list for a given space
        for value in design_data.m_con[i]:
            if value == 0:
                i_con.append(0.0)
            elif value == 1:
                i_con.append(fcdis(spaces[i], spaces[j], c))
            elif value == 2:
                i_con.append(0.1 * fcdis(spaces[i], spaces[j], 0))
            # Aborts the program if the Mcon has any value out of range
            else:
                sys.exit("Value out of range, review the connectivity matrix \
                    and ensure that the values are integers between 0 and 2.")
            
            # Moves to the next space in the list
            j += 1
        
        # Sums all the connectivity values for the space i
        con_values.append(sum(i_con))

    # Sums all the connectivity values for the individual
    evaluator = sum(con_values)

    return evaluator

def fcdis(r1, r2, c):
    """
    Computes the connectivity distance between two spaces.
    This is used to compute the Connectivity/Adjacency evaluator.
    """
    # Declares the connectivity distance variable
    con_dis = 0.0

    # Gets the X and Y coordinates for the spaces R1 and R2
    r1_x = r1.position[0]
    r1_y = r1.position[1]
    r2_x = r2.position[0]
    r2_y = r2.position[1]

    # Gets the width and height for the spaces R1 and R2
    r1_w = r1.width
    r1_h = r1.height
    r2_w = r2.width
    r2_h = r2.height

    # Computes the x-coordinate distance between two spaces
    dx = max([r1_x, r2_x]) - min([r1_x, r2_x]) - r1_w - r2_w

    # Computes the y-coordinate distance between two spaces
    dy = max([r1_y, r2_y]) - min([r1_y, r2_y]) - r1_h - r2_h

    # Computes the connectivity distance based on the distance parameters
    if dx >= 0 and dy >= 0:
        con_dis = dx + dy + c
    elif dx >= 0 and dy + c >= 0:
        con_dis = dx + dy + c
    elif dx + c >= 0 and dy >= 0:
        con_dis = dx + dy + c
    elif dx >= 0 and dy + c < 0:
        con_dis = dx
    elif dx + c < 0 and dy >= 0:
        con_dis = dy
    elif dx + c >= 0 and dy + c >= 0:
        con_dis = min([dx + c, dy + c]) - max([dx, dy])
    elif dx + c >= 0 and dy + c < 0:
        con_dis = abs(dx)
    elif dx + c < 0 and dy + c >= 0:
        con_dis = abs(dy)
    elif dx + c < 0 and dy + c < 0:
        con_dis = min([abs(dx), abs(dy)])

    return con_dis

def spaces_overlap(spaces, boundaries):
    """
    Computes the Spaces Overlap Evaluator.
    It attributes a penalty value based on the overlapping area among floors
    and between floors and the adjacent buildings.
    """
    # Declares the spaces overlap values list to store values for all spaces
    ov_values = []
    
    # Starts the computation by iterating through the spaces j in every i
    for i in range(len(spaces)):
        # Declares the j index and the list to store connectivity values
        i_ov = []

        # Iterates through the spaces list to get its overlap values
        for j in range(len(spaces)):
            # Checks if the spaces i and j being evaluated area not the same
            if j == i:
                continue

            # Transforms the spaces in Shapely Polygons to compute the boolean
            # intersection of the spaces
            shp_r1 = ShpPolygon(spaces[i].geometry.points)
            shp_r2 = ShpPolygon(spaces[j].geometry.points)

            # Computes the area of the intersection and adds to the list
            intersection = shp_r1.intersection(shp_r2)
            if intersection.area > 0:
                ov_values.append(round(intersection.area, 3))
        
    # Computes the overlap between spaces and the adjacent buildings
    for adjacent in boundaries['adjacent']:
        # Transforms the adjacent boundary in a Shapely Polygon
        shp_ra = ShpPolygon(adjacent.geometry.points)

        # Computes the overlap between the adjacent and every i space in spaces
        for i in range(len(spaces)):
            # Transforms the space in a Shapely Polygon
            ri = spaces[i]
            shp_ri = ShpPolygon(ri.geometry.points)

            # Computes the area of the intersection and adds to the list
            intersection = shp_ra.intersection(shp_ri)
            if intersection.area > 0:
                ov_values.append(round(intersection.area, 3))

    # Sums all the overlap values for the individual
    evaluator = sum(ov_values)

    return evaluator

def openings_overlap(spaces, design_data):
    return 0

def floor_dimensions(spaces, design_data):
    """
    Computes the Floor Dimensions Evaluator.
    It is a modified version from the one originally proposed by the authors.
    Given that no space is created beyond the dimensions matrix values, this
    evaluator only creates penalties if the floor has an area inferior to the
    specified minimum area.
    """
    # Declares the list to store the amount of spaces that are underdimensioned
    missing_areas = []
    
    # Iterates over all spaces to see if they have an associated minimum floor
    # area in the design data
    for i in range(len(spaces)):
        if design_data.m_far[i] is not None:
            # Gets the area of the space in the current individual
            space_area = spaces[i].geometry.area

            # If the area of the space is below the minimum required, add it
            # to the missing areas list
            if design_data.m_far[i] > space_area:
                missing_areas.append(design_data.m_far[i] - space_area)
        else:
            # If the space don't have an associated minimum floor area, add
            # zero to the list for proper computation
            missing_areas.append(0.0)

    # Computes the floor dimensions evaluator value based on the obtained 
    # parameters
    evaluator = sum(missing_areas)

    return evaluator

def compactness(spaces, boundaries):
    """
    Computes the Compactness Evaluator.
    It attributes a penalty value based on the empty area inside the building
    boundary. That is, the less empty area inside the boundary, the more
    compact is an individual.
    """
    # Declares the area of the building boundary
    boundary_area = round(boundaries['building'][0].geometry.area, 3)

    # Converts the building boundary to a Shapely Polygon
    building = ShpPolygon(boundaries['building'][0].geometry.points)

    # Computes the overlap between every space and the building boundary
    ov_building = []

    for i in range(len(spaces)):
        # Converts the space floor to a Shapely Polygon
        ri = ShpPolygon(spaces[i].geometry.points)

        # Computes the area of the intersection and adds to the list
        intersection = building.intersection(ri)
        if intersection.area > 0:
            ov_building.append(round(intersection.area, 3))
    
    # Computes the overlap between every space to decrease it from the 
    # compactness value
    ov_spaces = []

    for i in range(len(spaces)):
        for j in range(len(spaces)):
            # Checks if the spaces i and j being evaluated area not the same
            if j == i:
                continue
            
            # Converts the space floor to a Shapely Polygon
            ri = ShpPolygon(spaces[i].geometry.points)
            rj = ShpPolygon(spaces[j].geometry.points)

            # Computes the intersection and evaluates if it intersects with the
            # building boundary as well
            intersection = ri.intersection(rj)
            building_overlap = building.intersection(intersection)

            # Adds the value to the list if it is greater than zero
            if building_overlap.area > 0:
                ov_spaces.append(round(intersection.area, 3))
    
    # Prunes the duplicate values in the spaces list (that is due to the nature
    # of the iteration among floors)
    ov_spaces = list(set(ov_spaces))

    # Computes the compactness evaluator value based on the obtained parameters
    evaluator = boundary_area - sum(ov_building) - sum(ov_spaces)
    print(evaluator)

    return evaluator

def overflow(spaces, boundaries, design_data):
    """
    Computes the Overflow Evaluator.
    It attributes a penalty value based on any space that is partially or
    totally outside the shrinked building boundary, that is, the boundary
    deflated according to the exterior and interior wall thickness (creating a
    boundary based on the core line of the walls).
    """
    # Creates the deflated building boundary by offseting it according to the
    # exterior and interior wall thickness
    offset_distance = design_data.t_ew - (0.5 * design_data.t_iw)
    building = offset_polygon(
        boundaries['building'][0].geometry.points, offset_distance
        )
    deflated_boundary = ShpPolygon(building)

    # Computes the sum of all space areas for evaluation
    space_area = sum([
        round(spaces[i].geometry.area, 3) for i in range(len(spaces))
        ])

    # Computes the overlaps between the spaces and the building boundary
    ov_building = []

    for i in range(len(spaces)):
        # Converts the space floor to a Shapely Polygon
        ri = ShpPolygon(spaces[i].geometry.points)

        # Computes the area of the intersection and adds to the list
        intersection = deflated_boundary.intersection(ri)
        if intersection.area > 0:
            ov_building.append(round(intersection.area, 3))

    # Computes the overflow evaluator value based on the obtained parameters
    evaluator = space_area - sum(ov_building)

    return evaluator