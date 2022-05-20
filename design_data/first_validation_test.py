# Creates the space names matrix
m_sn = [
    "Hall", 
    "Kitchen", 
    "Living Room", 
    "Single Bedroom", 
    "Corridor",
    "Bedroom", 
    "Small Bathroom", 
    "Bathroom", 
    "Dinning Room"
    ]

# Creates the space functions matrix (0 = circulation, 1 = rooms/offices, 2 = kitchens/bathrooms, 3 = annex/balcony/garage)
m_st = [0, 2, 1, 1, 0, 1, 2, 2, 1]

# Creates the connectivity/adjacency matrix (0 = no requirement, 1 = interior door, 2 = adjacency)
m_con = [
    [0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 2, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 2, 0],
    [0, 0, 0, 0, 1, 0, 2, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 0]
    ]

# Creates the interior door size matrix (in centimeters)
m_ids = [90, 155, 200, 90, 90, 90, 90, 90, 90]

# Creates the floor dimensions matrix, defining the interval of admissible values for each flor side. The first two columns define the upper and lower bounds for the smaller side, while the last two define the upper and lower bounds for the larger side (in centimeters).
m_dim = [
    [154, 274, 423, 543],
    [188, 308, 406, 526],
    [561, 681, 630, 750],
    [168, 288, 406, 526],
    [100, 181, 319, 439],
    [268, 388, 406, 526],
    [100, 181, 147, 267],
    [147, 167, 199, 319],
    [264, 384, 464, 584]
    ]

# Creates the floor area matrix, specifying the minimum admissible area for each space (in square centimeters). This is an optional value.
m_far = [None, None, None, None, None, None, 24970, None, None]

# Creates the exterior window and exterior door size matrices. If the value is None it means that the space does not have that kind of opening.
m_ews = [None, 160, 533, 154, None, 250, None, None, 237]
m_eds = [100, None, None, None, None, None, None, None, None]

# Creates the exterior window and exterior door orientation matrices (0 = North, 1 = East, 2 = South, 3 = West)
m_ewo = [None, 0, 2, 0, None, 0, None, None, 2]
m_edo = [3, None, None, None, None, None, None, None, None]

# Creates the exterior window and exterior door vacant area matrices, that is, the rectangle in front of the opening that must be vacant. The first column specifies the size of the rectangle side touching the opening and the second column specifies its depth.
m_wa = [
    None,
    [300, 500],
    [300, 500],
    [300, 500],
    None,
    [300, 500],
    None,
    None,
    [300, 500]
    ]
m_da = [
    [100, 240], 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None
    ]

# Specifies the interior and exterior wall thickness 
t_iw = 8
t_ew = 35