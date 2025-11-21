"""
Move operations for the 3D cube puzzle.

Only allowed move: Rotate an ENTIRE row of cubies along x, y, or z axis.
Movement is a CIRCULAR REVERSAL: A-B-C-D becomes D-C-B-A
Also updates cubie orientations based on rotation axis.
"""

import copy


def apply_move(cube_state, dimensions, move):
    """
    Apply a move to the cube state and return the new state.
    
    Args:
        cube_state: 3D list representing the cube
        dimensions: tuple (x_dim, y_dim, z_dim)
        move: tuple (axis, index) where axis is 'x', 'y', or 'z'
    
    Returns:
        new_state: deep copy of cube_state with move applied
    """
    new_state = copy.deepcopy(cube_state)
    axis, index = move
    x_dim, y_dim, z_dim = dimensions
    
    if axis == 'x':
        # Row along x-axis: all cubies with x=index
        # Other coordinates (y, z) vary
        row = []
        for y in range(y_dim):
            for z in range(z_dim):
                row.append((index, y, z))
        
        # Extract cubies and their positions
        cubies = [new_state[x][y][z] for x, y, z in row]
        
        # Reverse the row (circular reversal)
        cubies_reversed = cubies[::-1]
        
        # Rotate each cubie's orientation for x-axis rotation
        cubies_rotated = [_rotate_cubie_x(cubie) for cubie in cubies_reversed]
        
        # Place back
        for i, (x, y, z) in enumerate(row):
            new_state[x][y][z] = cubies_rotated[i]
    
    elif axis == 'y':
        # Row along y-axis: all cubies with y=index
        # Other coordinates (x, z) vary
        row = []
        for x in range(x_dim):
            for z in range(z_dim):
                row.append((x, index, z))
        
        # Extract cubies
        cubies = [new_state[x][y][z] for x, y, z in row]
        
        # Reverse the row
        cubies_reversed = cubies[::-1]
        
        # Rotate each cubie's orientation for y-axis rotation
        cubies_rotated = [_rotate_cubie_y(cubie) for cubie in cubies_reversed]
        
        # Place back
        for i, (x, y, z) in enumerate(row):
            new_state[x][y][z] = cubies_rotated[i]
    
    elif axis == 'z':
        # Row along z-axis: all cubies with z=index
        # Other coordinates (x, y) vary
        row = []
        for x in range(x_dim):
            for y in range(y_dim):
                row.append((x, y, index))
        
        # Extract cubies
        cubies = [new_state[x][y][z] for x, y, z in row]
        
        # Reverse the row
        cubies_reversed = cubies[::-1]
        
        # Rotate each cubie's orientation for z-axis rotation
        cubies_rotated = [_rotate_cubie_z(cubie) for cubie in cubies_reversed]
        
        # Place back
        for i, (x, y, z) in enumerate(row):
            new_state[x][y][z] = cubies_rotated[i]
    
    return new_state


def _rotate_cubie_x(cubie):
    """
    Rotate a cubie's face colors for rotation around x-axis.
    When rotating around x-axis (reversal along x), the faces change:
    U -> F -> D -> B -> U (cycle)
    L and R stay the same
    """
    rotated = copy.deepcopy(cubie)
    rotated["U"] = cubie["B"]
    rotated["F"] = cubie["U"]
    rotated["D"] = cubie["F"]
    rotated["B"] = cubie["D"]
    # L and R unchanged
    return rotated


def _rotate_cubie_y(cubie):
    """
    Rotate a cubie's face colors for rotation around y-axis.
    When rotating around y-axis (reversal along y), the faces change:
    F -> L -> B -> R -> F (cycle)
    U and D stay the same
    """
    rotated = copy.deepcopy(cubie)
    rotated["F"] = cubie["R"]
    rotated["L"] = cubie["F"]
    rotated["B"] = cubie["L"]
    rotated["R"] = cubie["B"]
    # U and D unchanged
    return rotated


def _rotate_cubie_z(cubie):
    """
    Rotate a cubie's face colors for rotation around z-axis.
    When rotating around z-axis (reversal along z), the faces change:
    U -> L -> D -> R -> U (cycle)
    F and B stay the same
    """
    rotated = copy.deepcopy(cubie)
    rotated["U"] = cubie["R"]
    rotated["L"] = cubie["U"]
    rotated["D"] = cubie["L"]
    rotated["R"] = cubie["D"]
    # F and B unchanged
    return rotated


def get_all_moves(dimensions):
    """
    Get all possible moves for a cube with given dimensions.
    
    Returns:
        List of moves, each as tuple (axis, index)
    """
    x_dim, y_dim, z_dim = dimensions
    moves = []
    
    # X-axis moves
    for i in range(x_dim):
        moves.append(('x', i))
    
    # Y-axis moves
    for i in range(y_dim):
        moves.append(('y', i))
    
    # Z-axis moves
    for i in range(z_dim):
        moves.append(('z', i))
    
    return moves

