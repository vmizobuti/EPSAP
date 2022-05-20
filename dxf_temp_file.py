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

    # Imports boundaries from a DXF file
    filepath = os.path.join(sys.path[0], "DXF\\validation_test.dxf")
    dxf_file = DXFtoBoundaries(filepath)

    # Instantiates the building boundary
    building_boundary = Boundary(dxf_file["building"][0])

    # Instantiates the adjacent boundaries
    adjacent_boundaries = []
    for geometry in dxf_file["adjacent"]:
        adjacent_boundary = Boundary(geometry)
        adjacent_boundaries.append(adjacent_boundary)

    spaces = []
    # Instantiates the spaces given a design data
    for i in range(len(dd.m_sn)):
        name = dd.m_sn[i]
        floor = Floor((0,i), i+1, i+1)
        window = Window(dd.m_ewo[i], 0.0, 
                        dd.m_ews[i],
                        dd.m_wa[i])
        door = Door(dd.m_edo[i], 0.0,
                    dd.m_eds[i])
        
        preferences = [dd.m_con, dd.m_ids, dd.m_dim, dd.m_far, dd.m_st]
        
        space = Space(name, floor, window, door, preferences)

        spaces.append(space)
    
    
    # COMPAS View 2
    viewer = App(width=1200, height=900)

    viewer.add(building_boundary.geometry, linecolor=Color.blue())
    
    for adjacent in adjacent_boundaries:
        viewer.add(adjacent.geometry, linecolor=Color.red())
    
    for space in spaces:
        viewer.add(space.floor.geometry, linecolor=Color.black())

    viewer.show()

    return