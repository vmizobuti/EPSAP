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
from compas.colors import Color
from compas_view2.app import App
from spatial_classes import Boundary, Individual, Space, Window, Door, Floor


def DXFtoBoundaries(filepath):
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
        building_boundary = Polyline(building_points[polyline])
        
        # Adds the polyline to the "building" key in the contents dictionary
        dxf_contents['building'].append(building_boundary)
    
    # Creates the COMPAS Polylines for the adjacent buildings
    for polyline in adjacent_points.keys():
        # Duplicates the first point to ensure that the Polyline is closed
        adjacent_points[polyline].append(adjacent_points[polyline][0])
        
        # Creates the COMPAS Polyline given a list of points
        adjacent_boundary = Polyline(adjacent_points[polyline])
        
        # Adds the polyline to the "adjacent" key in the contents dictionary
        dxf_contents['adjacent'].append(adjacent_boundary)

    return dxf_contents

def main():

    filepath = os.path.join(sys.path[0], "DXF\\validation_test.dxf")

    dxf_file = DXFtoBoundaries(filepath)

    viewer = App(width=1200, height=900)

    for geometry in dxf_file["building"]:
        viewer.add(geometry, linecolor=Color.blue())
    
    for geometry in dxf_file["adjacent"]:
        viewer.add(geometry, linecolor=Color.red())

    viewer.show()

    return

if __name__ == '__main__':
    main()