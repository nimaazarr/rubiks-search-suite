"""
Cube state representation for the 3D Rubik's-cube-like puzzle.

The cube is represented as a 3D list: cube[x][y][z]
Each element is a cubie (dictionary) with 6 face colors: U, D, L, R, F, B
"""

import copy


class Cube:
    """Represents the state of the 3D cube puzzle."""
    
    def __init__(self, dimensions):
        """
        Initialize a cube with given dimensions.
        
        Args:
            dimensions: tuple (x, y, z) where each dimension is in {1,2,3,4}
        """
        self.x_dim, self.y_dim, self.z_dim = dimensions
        self.state = self._create_solved_state()
    
    def _create_solved_state(self):
        """
        Create a solved cube state where each face has a uniform color.
        
        Colors:
        - U (Up, y=max): White (W)
        - D (Down, y=0): Yellow (Y)
        - L (Left, x=0): Green (G)
        - R (Right, x=max): Blue (B)
        - F (Front, z=max): Red (R)
        - B (Back, z=0): Orange (O)
        """
        state = []
        for x in range(self.x_dim):
            x_layer = []
            for y in range(self.y_dim):
                y_layer = []
                for z in range(self.z_dim):
                    cubie = {
                        "U": "W",  # Up face
                        "D": "Y",  # Down face
                        "L": "G",  # Left face
                        "R": "B",  # Right face
                        "F": "R",  # Front face
                        "B": "O"   # Back face
                    }
                    y_layer.append(cubie)
                x_layer.append(y_layer)
            state.append(x_layer)
        return state
    
    def get_state(self):
        """Return the current state."""
        return self.state
    
    def set_state(self, state):
        """Set the cube state."""
        self.state = copy.deepcopy(state)
    
    def copy(self):
        """Return a deep copy of this cube."""
        new_cube = Cube((self.x_dim, self.y_dim, self.z_dim))
        new_cube.set_state(self.state)
        return new_cube
    
    def is_goal(self):
        """
        Check if the cube is in the solved state.
        Each of the 6 external faces must be uniform in color.
        """
        # Check Back face (z=0)
        back_color = self.state[0][0][0]["B"]
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if self.state[x][y][0]["B"] != back_color:
                    return False
        
        # Check Front face (z=max)
        front_color = self.state[0][0][self.z_dim - 1]["F"]
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if self.state[x][y][self.z_dim - 1]["F"] != front_color:
                    return False
        
        # Check Down face (y=0)
        down_color = self.state[0][0][0]["D"]
        for x in range(self.x_dim):
            for z in range(self.z_dim):
                if self.state[x][0][z]["D"] != down_color:
                    return False
        
        # Check Up face (y=max)
        up_color = self.state[0][self.y_dim - 1][0]["U"]
        for x in range(self.x_dim):
            for z in range(self.z_dim):
                if self.state[x][self.y_dim - 1][z]["U"] != up_color:
                    return False
        
        # Check Left face (x=0)
        left_color = self.state[0][0][0]["L"]
        for y in range(self.y_dim):
            for z in range(self.z_dim):
                if self.state[0][y][z]["L"] != left_color:
                    return False
        
        # Check Right face (x=max)
        right_color = self.state[self.x_dim - 1][0][0]["R"]
        for y in range(self.y_dim):
            for z in range(self.z_dim):
                if self.state[self.x_dim - 1][y][z]["R"] != right_color:
                    return False
        
        return True

