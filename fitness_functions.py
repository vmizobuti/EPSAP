# Implements the fitness function proposed by Rodrigues, E. et. al (2013).
#
# The function is composed of seven evaluators, each given by a different
# function in this script.
# 
# Author: Vinicius Mizobuti
# 
# Current Version: 1.0.0
# Release Date: WIP - 03/13/2022

import math

def connectivity_and_adjacency(spaces, design_data):
    """
    Computes the Connectivity/Adjacency Evaluator.
    If the Mcon matrix entry is 1 the connecitivy is calculated.
    If the Mcon matrix entry is 2 the adjacency is calculated.
    """

    return "Connectivity computed"

def spaces_overlap(individual):
    return 1

def openings_overlap(individual):
    return 1

def opening_orientation(individual):
    return 1

def floor_dimensions(individual):
    return 1

def compactness(individual):
    return 1

def overflow(individual):
    return 1