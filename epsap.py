# Implements the evolutionary program for space allocation problem 
# proposed by Rodrigues, E. et. al (2013).
# 
# Author: Vinicius Mizobuti
# 
# Current Version: 1.0.0
# Release Date: WIP - 03/13/2022

import os
import sys
import ezdxf

from compas.geometry import Point, Polyline
from compas_plotters import Plotter
from numpy.random import default_rng
from space_classes import Boundary, Population, Individual, Space, Window, Door, Floor

import design_data.first_validation_test as dd

def compute_population_size(k, elite_size, design_data):
    """
    Computes the size of the population based on the number of floor plan elements (exterior windows, exterior doors, and interior doors) multiplied by an adjustment factor k and the number of individuals on the elite group.
    """
    # Checks the validity of the parameters
    if k <= 0:
        sys.exit("Adjustment factor must be larger than zero.")
    if elite_size <= 0 or type(elite_size) != int:
        sys.exit("Size of the elite group must be an integer and larger than zero.")
    if hasattr(design_data, 'm_ews') == False:
        sys.exit("Design data is missing the number of exterior windows.")
    if hasattr(design_data, 'm_eds') == False:
        sys.exit("Design data is missing the number of exterior doors.")
    if hasattr(design_data, 'm_ids') == False:
        sys.exit("Design data is missing the number of interior doors.")

    # Gets the number of floor plan elements
    n_ew = [x for x in design_data.m_ews if x is not None]
    n_ed = [x for x in design_data.m_eds if x is not None]
    n_id = [x for x in design_data.m_ids if x is not None]
    floor_elements = len(n_ew) + len(n_ed) + len(n_id)

    # Computes the population size
    population_size = k * elite_size * floor_elements
    
    return population_size

def create_boundaries(filepath):
    """
    Imports a DXF file and transforms its polylines to boundaries according to their layers. The DXF file must contain at least one closed polyline in the layer 'building' and can contain multiple closed polylines on the layer 'adjacent'. The adjacent buildings can't have overlaps with the building boundary. 
    """
    # Reads and parses the DXF file.
    dxf_file = ezdxf.readfile(filepath)
    building = dxf_file.query('LWPOLYLINE[layer=="building"]')
    adjacent = dxf_file.query('LWPOLYLINE[layer=="adjacent"]')

    # Creates the dictionary for polyline points and output contents
    building_points = {}
    adjacent_points = {}
    dxf_contents = {'building': [], 'adjacent': []}

    # Creates the COMPAS Points for the building boundary
    for polyline in building.entities:
        # Gets the points from the DXF Polyline
        polyline_points = polyline.get_points()
        building_points[polyline] = []
        
        # Transforms the DXF Coordinates into COMPAS Points
        for point in polyline_points:
            compas_point = Point(round(point[0], 1), round(point[1], 1), 0.0)
            building_points[polyline].append(compas_point)

    # Creates the COMPAS Points for the adjacent buildings
    for polyline in adjacent.entities:
        # Gets the points from the DXF Polyline
        polyline_points = polyline.get_points()
        adjacent_points[polyline] = []
        
        # Transforms the DXF Coordinates into COMPAS Points
        for point in polyline_points:
            compas_point = Point(round(point[0], 1), round(point[1], 1), 0.0)
            adjacent_points[polyline].append(compas_point)

    # Creates the COMPAS Polylines for the building boundary
    for polyline in building_points.keys():
        # Duplicates the first point to ensure that the Polyline is closed
        building_points[polyline].append(building_points[polyline][0])
        
        # Creates the COMPAS Polyline given a list of points
        building_boundary = Boundary(Polyline(building_points[polyline]))
        
        # Adds the polyline to the "building" key in the contents dictionary
        dxf_contents['building'].append(building_boundary)
    
    # Creates the COMPAS Polylines for the adjacent buildings
    for polyline in adjacent_points.keys():
        # Duplicates the first point to ensure that the Polyline is closed
        adjacent_points[polyline].append(adjacent_points[polyline][0])
        
        # Creates the COMPAS Polyline given a list of points
        adjacent_boundary = Boundary(Polyline(adjacent_points[polyline]))
        
        # Adds the polyline to the "adjacent" key in the contents dictionary
        dxf_contents['adjacent'].append(adjacent_boundary)

    return dxf_contents

def create_spaces(design_data, boundary):
    """
    Creates a list of all spaces and its properties based on the design data.
    """    
    # Gets the list of spaces from the design data
    space_names = design_data.m_sn

    # Declares the list of spaces
    spaces = []

    # Creates a NumPy random number generator to be used on random operations
    rng = default_rng()

    # Creates the spaces based on the Space class
    for i in range(len(space_names)):
        # Creates the space label based on the space name
        label = space_names[i]

        # Defines the floor (x,y) position within the boundary's bounding box
        bounding_coordinates = boundary.coordinates
        x_coord = round(rng.uniform(low= bounding_coordinates[0],
                                    high= bounding_coordinates[2]), 2)
        y_coord = round(rng.uniform(low= bounding_coordinates[1],
                                    high= bounding_coordinates[3]), 2)

        # Defines the floor's width and height based on the design data.
        # A random coin is flipped to decide if the longest side is the
        # floor's width or height
        dimension_range = design_data.m_dim[i]
        width = 0.0
        height = 0.0

        coin_flip = rng.choice([True, False])
        if coin_flip == True:
            width = round(rng.uniform(low= dimension_range[0],
                                      high= dimension_range[1]), 2)
            height = round(rng.uniform(low= dimension_range[2],
                                       high= dimension_range[3]), 2)
        else:    
            width = round(rng.uniform(low= dimension_range[2],
                                      high= dimension_range[3]), 2)
            height = round(rng.uniform(low= dimension_range[0],
                                       high= dimension_range[1]), 2)

        # Creates the space floor based on the floor parameters
        floor = Floor((x_coord, y_coord), width, height)

        # Creates the space windows based on the windows parameters
        windows = []
        if design_data.m_ews[i] != None:
            for j in range(len(design_data.m_ews[i])):
                # Creates the window parameters
                size = design_data.m_ews[i][j]
                position = round(rng.random(), 3)
                orientation = design_data.m_ewo[i][j]

                # Creates a random orientation if none is given
                if orientation == None:
                    orientation = rng.choice([0, 1, 2, 3])
                
                # Creates the window and appends it to the windows list
                windows.append(Window(orientation, position, size))
        
        # Creates the space doors based on the doors parameters
        doors = []
        # Checks if the space has exterior doors
        # if True, create a door with the exterior parameters
        if design_data.m_eds[i] != None:
            for j in range(len(design_data.m_eds[i])):
                # Creates the door parameters
                size = design_data.m_eds[i][j]
                position = round(rng.random(), 3)
                orientation = design_data.m_edo[i][j]

                # Creates a random orientation if none is given
                if orientation == None:
                    orientation = rng.choice([0, 1, 2, 3])

                # Creates the door and appends it to the door list
                doors.append(Door(orientation, position, size))
        else:
            for j in range(len(design_data.m_ids[i])):
                # Creates the door parameters
                size = design_data.m_ids[i][j]
                position = round(rng.random(), 3)
                orientation = rng.choice([0, 1, 2, 3])

                # Creates the door and appends it to the door list
                doors.append(Door(orientation, position, size))
        
        # Creates the space based on all its parameters
        space = Space(label, floor, windows, doors)
        spaces.append(space)

    return spaces

def create_individual(label, design_data, boundary, weights):
    """
    Creates an individual by randomly allocating the spaces within the building boundary. Every individual is labeled according to its generation number and number within the generation.
    """
    # Creates the spaces to be used by every individual
    spaces = create_spaces(design_data, boundary)

    # Creates the individual based on the created spaces
    individual = Individual(label, spaces)

    # Computes the individual's initial fitness value
    individual.compute_fitness_value(design_data, weights)

    return individual

def main():

    # Imports boundaries from a DXF file
    filepath = os.path.join(sys.path[0], "DXF\\validation_test.dxf")
    boundaries = create_boundaries(filepath)

    boundary = boundaries['building'][0]

    weights = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    individual = create_individual("0.01", dd, boundary, weights)
    print(individual.fitness_value)

    # COMPAS Plotter

    plotter = Plotter()

    plotter.add(boundary.geometry, 
                linewidth=2,
                color=(1,0,0), 
                draw_points=False)

    for space in individual.spaces:
        plotter.add(space.floor.geometry,
                    linewidth=1,
                    color=(0,0,0),
                    draw_points=False)                  
    
    plotter.zoom_extents()
    plotter.show()

    return

if __name__ == '__main__':
    main()