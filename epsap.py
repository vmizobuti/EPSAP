# Implements the evolutionary program for the space allocation problem 
# proposed by Rodrigues, E. et. al (2013).
# 
# Author: Vinicius Mizobuti
# 
# Current Version: 1.0.0
# Release Date: WIP - 03/13/2022

from compas.geometry import Point, Polyline
from compas.files import DXF
from spatial_classes import Boundary, Individual, Space, Window, Door, Floor


def DXFtoBoundaries(filepath):
    """
    Imports a DXF file and transforms its polylines to boundaries according to their layers. The DXF file must contain at least one closed polyline in the layer 'building' and can contain multiple closed polylines on the layer 'adjacent'. The adjacent buildings can't have overlaps with the building boundary. 
    """
    # Reads and parses the DXF file.
    dxf_file = DXF(filepath)
    dxf_contents = dxf_file.parser()

    return dxf_contents

def main():

    filepath = "C:\\Users\\vmizo\\Desktop\\testfile.dxf"

    print(DXFtoBoundaries(filepath))

    return

if __name__ == '__main__':
    main()