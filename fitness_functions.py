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
import math

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
                sys.exit("Value out of range, review the connectivity matrix and ensure that the values are integers between 0 and 2.")
            
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
    r1_x = r1.floor.position[0]
    r1_y = r1.floor.position[1]
    r2_x = r2.floor.position[0]
    r2_y = r2.floor.position[1]

    # Gets the width and height for the spaces R1 and R2
    r1_w = r1.floor.width
    r1_h = r1.floor.height
    r2_w = r2.floor.width
    r2_h = r2.floor.height

    # Computes the x-coordinate distance between two spaces
    dx = max([r1_x, r2_x]) - min([r1_x, r2_x]) - r1_w - r2_w

    # Computes the y-coordinate distance between two spaces
    dy = max([r1_y, r2_y]) - min([r1_y, r2_y]) - r1_h - r2_h

    # Computes the connectivity distance based on the distance parameters
    if dx >= 0 and dy >= 0:
        con_dis = dx + dy + c
    if dx >= 0 and dy + c >= 0:
        con_dis = dx + dy + c
    if dx + c >= 0 and dy >= 0:
        con_dis = dx + dy + c
    if dx >= 0 and dy + c < 0:
        con_dis = dx
    if dx + c < 0 and dy >= 0:
        con_dis = dy
    if dx + c >= 0 and dy + c >= 0:
        con_dis = min([dx + c, dy + c]) - max([dx, dy])
    if dx + c >= 0 and dy + c < 0:
        con_dis = abs(dx)
    if dx + c < 0 and dy + c >= 0:
        con_dis = abs(dy)
    if dx + c < 0 and dy + c < 0:
        con_dis = min([abs(dx), abs(dy)])

    return con_dis

def spaces_overlap(spaces, design_data, boundaries):
    """
    Computes the Spaces Overlap Evaluator.
    """
    # Declares the spaces overlap values list to store values for all spaces
    ov_values = []
    
    # Starts the computation by iterating through the spaces j in every i
    for i in range(len(spaces)):
        # Declares the j index and the list to store connectivity values
        i_ov = []

        # Iterates through the spaces list to get its overlap values
        for j in range(len(spaces)):
            r1 = spaces[i]
            r2 = spaces[j]

            # Computes the overlap for the given spaces and adds it to the overlap values list
            overlap = rectangle_overlap(r1, r2)
            if overlap > 0:
                ov_values.append(round(overlap, 3))
    
    # # Computes the overlap between spaces and the adjacent buildings
    # for adjacent in boundaries['adjacent']:
    #     i_ov = []
    #     for i in range(len(spaces)):
    #         r1 = spaces[i]
    #         r2 = adjacent.coordinates

    evaluator = sum(ov_values)
    print(ov_values)

    return evaluator

def rectangle_overlap(r1, r2):
    """
    Computes the overlap between two spaces.
    This is used to compute any kind of overlapping for fitness purposes.
    """
    # Declares the R1 corner coordinates
    r1_x1 = r1.floor.position[0]
    r1_y1 = r1.floor.position[1]
    r1_x2 = r1_x1 + r1.floor.width
    r1_y2 = r1_y1 + r1.floor.height

    # Declares the R2 corner coordinates
    r2_x1 = r2.floor.position[0]
    r2_y1 = r2.floor.position[1]
    r2_x2 = r2_x1 + r2.floor.width
    r2_y2 = r2_y1 + r2.floor.height

    # Gets the size of the overlapping rectangle, if any exists
    dx = min([r1_x2, r2_x2]) - max([r1_x1, r2_x1])
    dy = min([r1_y2, r2_y2]) - max([r1_y1, r2_y1])

    # Declares the overlap variable
    overlap = 0.0

    # Computes the overlap area, if any exists
    if dx > 0 and dy > 0:
        overlap = dx * dy

    return overlap

def openings_overlap(spaces, design_data):
    return 0

def opening_orientation(spaces, design_data):
    return 0

def floor_dimensions(spaces, design_data):
    return 0

def compactness(spaces, design_data):
    return 0

def overflow(spaces, design_data):
    return 0