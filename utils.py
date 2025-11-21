"""
Utility functions for state serialization and hashing.
"""


def serialize_state(cube_state, dimensions):
    """
    Serialize cube state to a string for hashing and comparison.
    
    Args:
        cube_state: 3D list representing the cube
        dimensions: tuple (x_dim, y_dim, z_dim)
    
    Returns:
        String representation of the state
    """
    x_dim, y_dim, z_dim = dimensions
    parts = []
    
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                cubie = cube_state[x][y][z]
                # Serialize each cubie's 6 faces in fixed order
                cubie_str = f"{cubie['U']}{cubie['D']}{cubie['L']}{cubie['R']}{cubie['F']}{cubie['B']}"
                parts.append(cubie_str)
    
    return "|".join(parts)


def deserialize_state(state_str, dimensions):
    """
    Deserialize a state string back to cube state.
    
    Args:
        state_str: String representation of the state
        dimensions: tuple (x_dim, y_dim, z_dim)
    
    Returns:
        3D list representing the cube
    """
    x_dim, y_dim, z_dim = dimensions
    parts = state_str.split("|")
    
    cube_state = []
    idx = 0
    
    for x in range(x_dim):
        x_layer = []
        for y in range(y_dim):
            y_layer = []
            for z in range(z_dim):
                cubie_str = parts[idx]
                cubie = {
                    "U": cubie_str[0],
                    "D": cubie_str[1],
                    "L": cubie_str[2],
                    "R": cubie_str[3],
                    "F": cubie_str[4],
                    "B": cubie_str[5]
                }
                y_layer.append(cubie)
                idx += 1
            x_layer.append(y_layer)
        cube_state.append(x_layer)
    
    return cube_state

