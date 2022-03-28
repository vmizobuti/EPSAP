# Implements the evolutionary program for the space allocation problem 
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

    building_points = {}
    adjacent_points = {}
    dxf_contents = []

    for polyline in building.entities:
        polyline_points = polyline.get_points()
        building_points[polyline] = []
        for point in polyline_points:
            compas_point = Point(round(point[0], 1), round(point[1], 1), 0.0)
            building_points[polyline].append(compas_point)

    for polyline in adjacent.entities:
        polyline_points = polyline.get_points()
        adjacent_points[polyline] = []
        for point in polyline_points:
            compas_point = Point(round(point[0], 1), round(point[1], 1), 0.0)
            adjacent_points[polyline].append(compas_point)

    for polyline in building_points.keys():
        building_points[polyline].append(building_points[polyline][0])
        building_boundary = Polyline(building_points[polyline])
        dxf_contents.append(building_boundary)
    
    for polyline in adjacent_points.keys():
        adjacent_points[polyline].append(adjacent_points[polyline][0])
        adjacent_boundary = Polyline(adjacent_points[polyline])
        dxf_contents.append(adjacent_boundary)

    return dxf_contents

def main():

    filepath = os.path.join(sys.path[0], "DXF\\validation_test.dxf")

    dxf_file = DXFtoBoundaries(filepath)

    viewer = App(width=800, height=600, show_grid=False)

    for geometry in dxf_file:
        viewer.add(geometry)

    viewer.show()

    return

if __name__ == '__main__':
    main()