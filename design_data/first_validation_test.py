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
m_ids = [
    [0.90], 
    [1.55], 
    [2.00], 
    [0.90], 
    [0.90], 
    [0.90], 
    [0.90], 
    [0.90], 
    [0.90]
    ]

# Creates the floor dimensions matrix, defining the interval of admissible values for each floor side. The first two columns define the upper and lower bounds for the smaller side, while the last two define the upper and lower bounds for the larger side (in centimeters).
m_dim = [
    [1.54, 2.74, 4.23, 5.43],
    [1.88, 3.08, 4.06, 5.26],
    [5.61, 6.81, 6.30, 7.50],
    [1.68, 2.88, 4.06, 5.26],
    [1.00, 1.81, 3.19, 4.39],
    [2.68, 3.88, 4.06, 5.26],
    [1.00, 1.81, 1.47, 2.67],
    [1.47, 1.67, 1.99, 3.19],
    [2.64, 3.84, 4.64, 5.84]
    ]

# Creates the floor area matrix, specifying the minimum admissible area for each space (in square centimeters). This is an optional value.
m_far = [None, None, None, None, None, None, 2.497, None, None]

# Creates the exterior window and exterior door size matrices. If the value is None it means that the space does not have that kind of opening.
m_ews = [
    None, 
    [1.60], 
    [5.33], 
    [1.54], 
    None, 
    [2.50], 
    None, 
    None, 
    [2.37]
    ]

m_eds = [
    [1.00], 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None
    ]

# Creates the exterior window and exterior door orientation matrices (0 = North, 1 = East, 2 = South, 3 = West)
m_ewo = [
    None, 
    [0], 
    [2], 
    [0], 
    None, 
    [0], 
    None, 
    None, 
    [2]
    ]

m_edo = [
    [3], 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None
    ]

# Creates the exterior window and exterior door vacant area matrices, that is, the rectangle in front of the opening that must be vacant. The first column specifies the size of the rectangle side touching the opening and the second column specifies its depth.
m_wa = [
    None,
    [3.00, 5.00],
    [3.00, 5.00],
    [3.00, 5.00],
    None,
    [3.00, 5.00],
    None,
    None,
    [3.00, 5.00]
    ]
m_da = [
    [1.00, 2.40], 
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
t_iw = 0.08
t_ew = 0.35