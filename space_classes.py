# Implements all classes  and their related functions needed for the space
# allocation algorithm proposed by Rodrigues, E. et. al (2013).
# 
# Author: Vinicius Mizobuti
# 
# Current Version: 1.0.0
# Release Date: WIP - 03/13/2022

from math import sqrt
import fitness_functions as ff
from compas.geometry import Point, Polygon

class Boundary:

    def __init__(self, polygon):
        """
        Initialize a building boundary.
        A building boundary has:
        - 'geometry': the COMPAS Polygon representing the boundary;
        - 'boundary': the COMPAS Polygon representing the bounding rectangle;
        - 'width': the width of the boundary bounding rectangle;
        - 'height': the height of the boundary bounding rectangle;
        - 'position': the bottom-left vertex point coordinate (x, y);
        """
        self.geometry = polygon
        self.boundary = self.bounding_rectangle()[0]
        self.width = self.bounding_rectangle()[1]
        self.height = self.bounding_rectangle()[2]
        self.position = self.bounding_rectangle()[3]
    
    def bounding_rectangle(self):
        """
        Computes the boundary's bounding rectangle and returns the COMPAS 
        Polyline representing the rectangle, the rectangle width and the 
        rectangle height.
        """
        # Gets the points from the building boundary polygon and creates the 
        # lists to store the X and Y values of each point
        boundary_points = self.geometry.points
        x_values = []
        y_values = []

        # Iterates through the list of points storing their X and Y values in 
        # their respective lists
        for point in boundary_points:
            x_values.append(point.x)
            y_values.append(point.y)

        # Gets the maximum and minimum values for X and Y to compute the 
        # bounding rectangle  
        max_x = max(x_values)
        min_x = min(x_values)
        max_y = max(y_values)
        min_y = min(y_values)

        # Defines the lower-right corner as the rectangle position
        position = [min_x, min_y]

        # Creates the corners of the bounding rectangle
        bounding_points = [
            Point(min_x, min_y, 0), Point(max_x, min_y, 0),
            Point(max_x, max_y, 0), Point(min_x, max_y, 0),
            ]

        # Creates the bounding rectangle polygon and computes its properties
        bounding_line = Polygon(bounding_points)
        bounding_width = max_x - min_x
        bounding_height = max_y - min_y

        return bounding_line, bounding_width, bounding_height, position

class Population:

    def __init__(self, individual, size):
        """
        Initialize a population of floorplans.
        A population has:
        - 'individuals': a list of individuals;
        - 'size': the fixed size of the population based on design data;
        """
        self.individual = individual
        self.size = size
    
    def rank_individuals():
        raise NotImplementedError
    
    def compute_elite_favg():
        raise NotImplementedError
    
    def add_individual():
        raise NotImplementedError
    
    def purge():
        raise NotImplementedError

class Individual:

    def __init__(self, label, spaces):
        """
        Initialize an individual.
        An individual has:
        - 'label': the label for the individual;
        - 'spaces': the set of spaces contained by an individual;
        - 'fitness_value': the computed fitness value associated with the 
                           individual. This value is used to guarantee that a 
                           solution is reached;
        """
        self.label = label
        self.spaces = spaces
        self.fitness_value = 0.0
    
    def compute_fitness_value(self, boundaries, design_data, weights):
        """
        Computes the fitness value of the individual based on the seven
        evaluators proposed by Rodrigues, E. et al.
        """
        # Computes the Connectivity/Adjacency Evaluator
        f1 = ff.connectivity_and_adjacency(self.spaces, design_data)

        # Computes the Spaces Overlap Evaluator
        f2 = sqrt(ff.spaces_overlap(self.spaces, boundaries))

        # Computes the Openings Overlap Evaluator
        f3 = sqrt(ff.openings_overlap(self.spaces, design_data))

        # # Computes the Opening Orientation Evaluator
        # # This evaluator is currently unused, given that the create_spaces
        # # function always assumes the orientation from the matrix unless
        # # None is given.
        # f4 = sqrt(ff.opening_orientation(self.spaces, design_data))

        # Computes the Floor Dimensions Evaluator
        f5 = sqrt(ff.floor_dimensions(self.spaces, design_data))

        # Computes the Compactness Evaluator
        f6 = sqrt(ff.compactness(self.spaces, boundaries))

        # Computes the Overflow Evaluator
        f7 = sqrt(ff.overflow(self.spaces, boundaries, design_data))

        # Computes the weighted values of the evaluators
        weighted_values = [
            weights[0] * f1,
            weights[1] * f2,
            weights[2] * f3,
            weights[3] * f5,
            weights[4] * f6,
            weights[5] * f7
            ]

        # Computes the individual's fitness value
        self.fitness_value = sum(weighted_values)

        return

class Space:

    def __init__(self, label, floor, windows, doors, preferences=None):
        """
        Initialize a space.
        A space has:
        - 'label': the label for the space functionality;
        - 'floor': the floor rectangle associated with the space;
        - 'windows': the set of windows in the space;
        - 'doors': the set of doors in the space;
        - 'preferences': the user-defined topological preferences, such as 
                         adjacency to other spaces and exterior views;
        - 'geometry': the COMPAS Polygon inherited from the space floor;
        - 'position': the bottom-left vertex point coordinate (x, y)
                      inherited from the space floor;
        - 'width': the width inherited from the space floor;
        - 'height': the height inherited from the space floor;
        """
        self.label = label
        self.floor = floor
        self.windows = windows
        self.doors = doors
        self.preferences = preferences
        self.geometry = self.floor.geometry
        self.position = self.floor.position
        self.width = self.floor.width
        self.height = self.floor.height

class Window:

    def __init__(self, side, position, size, vacant_area=None):
        """
        Initialize a space window.
        A space window has two DOF and is composed of:
        - 'side': the side of the floor that the window is placed;
        - 'position': the relative position of the window on the given side;
        - 'size': the size associated with the window;
        - 'vacant_area': the area in front of the window that must not be
                         occupied by other elements. The default value is set 
                         to None, that is, no vacant area;
        """
        self.side = side
        self.position = position
        self.size = size
        self.vacant_area = vacant_area
    
class Door:

    def __init__(self, side, position, size, orientation=False):
        """
        Initialize a space door.
        A space door has two DOF and is composed of:
        - 'side': the side of the floor that the door is placed;
        - 'position': the relative position of the door on the given side;
        - 'size': the size associated with the door;
        - 'orientation': the user-defined orientation for the door opening. 
                         The default value is to open it towards the interior 
                         of the room;
        """
        self.side = side
        self.position = position
        self.size = size
        self.orientation = orientation

class Floor:

    def __init__(self, position, width, height):
        """
        Initialize a space floor.
        A space floor has four DOF and is composed of:
        - 'position': the bottom-left vertex point coordinate (x, y);
        - 'width': the floor width (constrained by user-defined limits);
        - 'height': the floor height (constrained by user-defined limits);
        - 'geometry': the COMPAS Polygon representing the floor;
        """
        self.position = position
        self.width = width
        self.height = height
        self.geometry = self.floor_geometry(self.position, 
                                            self.width, self.height)

    def floor_geometry(self, position, width, height):
        """
        Creates the floor rectangle based on its associated position, width and 
        height values.
        """
        # Computes all X and Y coordinates of the floor
        x_0 = position[0]
        x_1 = position[0] + width
        y_0 = position[1]
        y_1 = position[1] + height

        # Creates the COMPAS points for every corner of the floor
        point_0 = Point(x_0, y_0, 0)
        point_1 = Point(x_1, y_0, 0)
        point_2 = Point(x_1, y_1, 0)
        point_3 = Point(x_0, y_1, 0)

        # Creates the COMPAS Polyline given the floor coordinates
        geometry = Polygon([point_0, point_1, point_2, point_3])

        return geometry