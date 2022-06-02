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
    # Declares the connectivity/adjacency evaluator variable
    con_values = []
    
    # Starts the computation by iterating through the spaces
    for i in range(len(spaces)):
        # Declares the i-space con_values
        i_con_val = []

        # Creates a controller for the j-index
        j_index = 0

        # Iterates throug the connectivity list for a given space
        for j in design_data.m_con[i]:
            if j == 0:
                i_con_val.append(0.0)
            elif j == 1:
                i_con_val.append(fcdis(spaces[i], spaces[j_index], 0))
            elif j == 2:
                i_con_val.append(fcdis(spaces[i], spaces[j_index], 0))
            else:
                sys.exit("Value out of range, review the connectivity matrix and ensure that the values are integers between 0 and 2.")
            j_index += 1
        
        con_values.append(sum(i_con_val))

    print(con_values)

    f1 = sum(con_values)

    return f1

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

def spaces_overlap(spaces, design_data):
    return 0

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