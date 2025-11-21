"""
Heuristic functions for informed search algorithms.
All heuristics must be admissible (never overestimate).
"""


def face_mismatch_heuristic(cube_state, dimensions):
    """
    Count the number of face colors that don't match the target uniform color.
    This is admissible because each move can fix at most a certain number of mismatches.
    
    For each of the 6 external faces, count how many visible cubie faces
    don't match the majority color on that face.
    
    Args:
        cube_state: 3D list representing the cube
        dimensions: tuple (x_dim, y_dim, z_dim)
    
    Returns:
        Heuristic value (number of mismatched face colors divided by a factor)
    """
    x_dim, y_dim, z_dim = dimensions
    mismatches = 0
    
    # Check Back face (z=0)
    back_colors = []
    for x in range(x_dim):
        for y in range(y_dim):
            back_colors.append(cube_state[x][y][0]["B"])
    back_target = _most_common(back_colors)
    for color in back_colors:
        if color != back_target:
            mismatches += 1
    
    # Check Front face (z=max)
    front_colors = []
    for x in range(x_dim):
        for y in range(y_dim):
            front_colors.append(cube_state[x][y][z_dim - 1]["F"])
    front_target = _most_common(front_colors)
    for color in front_colors:
        if color != front_target:
            mismatches += 1
    
    # Check Down face (y=0)
    down_colors = []
    for x in range(x_dim):
        for z in range(z_dim):
            down_colors.append(cube_state[x][0][z]["D"])
    down_target = _most_common(down_colors)
    for color in down_colors:
        if color != down_target:
            mismatches += 1
    
    # Check Up face (y=max)
    up_colors = []
    for x in range(x_dim):
        for z in range(z_dim):
            up_colors.append(cube_state[x][y_dim - 1][z]["U"])
    up_target = _most_common(up_colors)
    for color in up_colors:
        if color != up_target:
            mismatches += 1
    
    # Check Left face (x=0)
    left_colors = []
    for y in range(y_dim):
        for z in range(z_dim):
            left_colors.append(cube_state[0][y][z]["L"])
    left_target = _most_common(left_colors)
    for color in left_colors:
        if color != left_target:
            mismatches += 1
    
    # Check Right face (x=max)
    right_colors = []
    for y in range(y_dim):
        for z in range(z_dim):
            right_colors.append(cube_state[x_dim - 1][y][z]["R"])
    right_target = _most_common(right_colors)
    for color in right_colors:
        if color != right_target:
            mismatches += 1
    
    # Each move can potentially fix multiple mismatches
    # To ensure admissibility, divide by an optimistic factor
    # A single row reversal affects at most 2 * max(dimensions) cubies
    max_fix_per_move = max(x_dim, y_dim, z_dim) * 2
    
    return mismatches / max_fix_per_move


def _most_common(lst):
    """Return the most common element in a list."""
    return max(set(lst), key=lst.count)


def face_entropy_heuristic(cube_state, dimensions):
    """
    Alternative heuristic: sum of face disorder.
    For each face, count unique colors - 1.
    Admissible as each move affects limited cubies.
    
    Args:
        cube_state: 3D list representing the cube
        dimensions: tuple (x_dim, y_dim, z_dim)
    
    Returns:
        Heuristic value
    """
    x_dim, y_dim, z_dim = dimensions
    disorder = 0
    
    # Check Back face (z=0)
    back_colors = set()
    for x in range(x_dim):
        for y in range(y_dim):
            back_colors.add(cube_state[x][y][0]["B"])
    disorder += len(back_colors) - 1
    
    # Check Front face (z=max)
    front_colors = set()
    for x in range(x_dim):
        for y in range(y_dim):
            front_colors.add(cube_state[x][y][z_dim - 1]["F"])
    disorder += len(front_colors) - 1
    
    # Check Down face (y=0)
    down_colors = set()
    for x in range(x_dim):
        for z in range(z_dim):
            down_colors.add(cube_state[x][0][z]["D"])
    disorder += len(down_colors) - 1
    
    # Check Up face (y=max)
    up_colors = set()
    for x in range(x_dim):
        for z in range(z_dim):
            up_colors.add(cube_state[x][y_dim - 1][z]["U"])
    disorder += len(up_colors) - 1
    
    # Check Left face (x=0)
    left_colors = set()
    for y in range(y_dim):
        for z in range(z_dim):
            left_colors.add(cube_state[0][y][z]["L"])
    disorder += len(left_colors) - 1
    
    # Check Right face (x=max)
    right_colors = set()
    for y in range(y_dim):
        for z in range(z_dim):
            right_colors.add(cube_state[x_dim - 1][y][z]["R"])
    disorder += len(right_colors) - 1
    
    # Divide by 2 to make more admissible
    return disorder / 2.0

