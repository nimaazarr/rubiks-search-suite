"""
Depth-Limited Search (DLS) implementation.

ALGORITHM OVERVIEW:
------------------
DLS is DFS with a predetermined depth limit. It prevents DFS from going too
deep and potentially missing solutions in shallow branches.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Recursive call stack: Implicit depth tracking
   - Set: Visited states in current search path
   - Lists: Track visited order and expanded nodes

2. Process:
   - Recursively explore from initial state
   - At each level:
     * If depth limit reached, return failure
     * If state already visited in this path, skip
     * Check if goal state
     * Recursively explore all unvisited successors
   - Backtrack when depth limit hit or no successors

3. Properties:
   - Complete: Only if solution within depth limit
   - Optimal: No - finds first solution at or below limit
   - Time Complexity: O(b^l) where l=depth limit
   - Space Complexity: O(bl) - linear in depth limit

4. Implementation Notes:
   - Uses recursion for natural depth tracking
   - Path-checking to avoid cycles in current branch
   - Returns immediately when goal found

5. Advantages:
   - Memory efficient compared to BFS
   - Prevents infinite depth exploration
   - Good when approximate solution depth known

6. Disadvantages:
   - May miss solution if limit too low
   - Not optimal
   - Redundant exploration if limit increased
"""

import sys
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state


def dls(initial_state, dimensions, depth_limit=10):
    """
    Perform Depth-Limited Search to find solution.
    
    Args:
        initial_state: 3D list representing initial cube state
        dimensions: tuple (x_dim, y_dim, z_dim)
        depth_limit: maximum depth to search
    
    Returns:
        dict with keys:
            - visited_order: list of serialized states in order expanded
            - expanded_nodes: list of serialized states that were expanded
            - solution_path: list of moves to reach goal
            - final_state: the goal state (3D list)
            - success: True if solution found, False otherwise
    """
    from cube import Cube
    
    # Initialize
    initial_serialized = serialize_state(initial_state, dimensions)
    visited_order = []
    expanded_nodes = []
    
    # Check if initial state is goal
    cube = Cube(dimensions)
    cube.set_state(initial_state)
    if cube.is_goal():
        return {
            'visited_order': [initial_serialized],
            'expanded_nodes': [initial_serialized],
            'solution_path': [],
            'final_state': initial_state,
            'success': True
        }
    
    all_moves = get_all_moves(dimensions)
    
    # Recursive DLS
    result = _dls_recursive(
        initial_state, dimensions, depth_limit, 
        cube, all_moves, set(), visited_order, expanded_nodes, []
    )
    
    if result['success']:
        return {
            'visited_order': visited_order,
            'expanded_nodes': expanded_nodes,
            'solution_path': result['solution_path'],
            'final_state': result['final_state'],
            'success': True
        }
    else:
        return {
            'visited_order': visited_order,
            'expanded_nodes': expanded_nodes,
            'solution_path': [],
            'final_state': None,
            'success': False
        }


def _dls_recursive(state, dimensions, limit, cube, all_moves, visited, visited_order, expanded_nodes, path):
    """
    Recursive helper for DLS.
    
    Returns:
        dict with success flag and solution if found
    """
    if limit == 0:
        return {'success': False}
    
    current_serialized = serialize_state(state, dimensions)
    
    if current_serialized in visited:
        return {'success': False}
    
    visited.add(current_serialized)
    
    # Mark as expanded
    if current_serialized not in expanded_nodes:
        expanded_nodes.append(current_serialized)
    
    # Check if goal
    cube.set_state(state)
    if cube.is_goal():
        return {
            'success': True,
            'solution_path': path,
            'final_state': state
        }
    
    # Explore children
    for move in all_moves:
        new_state = apply_move(state, dimensions, move)
        new_serialized = serialize_state(new_state, dimensions)
        
        if new_serialized not in visited:
            if new_serialized not in visited_order:
                visited_order.append(new_serialized)
            
            new_path = path + [move]
            result = _dls_recursive(
                new_state, dimensions, limit - 1,
                cube, all_moves, visited, visited_order, expanded_nodes, new_path
            )
            
            if result['success']:
                return result
    
    return {'success': False}

