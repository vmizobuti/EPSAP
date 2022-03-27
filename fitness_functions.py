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

# Implements the evaluator for connectivity and adjacency given an individual I
def connectivity_and_adjacency(individual):
    

    return 0

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

# Implements the fitness function for the individual I and its list of weights
# for each evaluator. The fitness function is given by:
# f(I) = c1*f1(I) + sum(ci*sqrt(fi(I))) for i = 2 to 7
def fitness_function(individual, weights):
    # Calculates all the evaluators and stores their values in a list
    f1 = connectivity_and_adjacency(individual)
    f2 = math.sqrt(spaces_overlap(individual))
    f3 = math.sqrt(openings_overlap(individual))
    f4 = math.sqrt(opening_orientation(individual))
    f5 = math.sqrt(floor_dimensions(individual))
    f6 = math.sqrt(compactness(individual))
    f7 = math.sqrt(overflow(individual))
    evaluators = [f1, f2, f3, f4, f5, f6, f7]

    # Computes the weighted values for each evaluator
    weighted_evaluators = [c * f for  c, f in zip(weights, evaluators)]

    # Computes the fitness value for the individual I
    individual_fitness = sum(weighted_evaluators)

    return individual_fitness     

def main():
    print(fitness_function(0, [1, 1, 1, 1, 1, 1, 1]))

if __name__ == '__main__':
    main()