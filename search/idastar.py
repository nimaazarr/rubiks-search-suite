"""
Iterative Deepening A* (IDA*) implementation.

ALGORITHM OVERVIEW:
------------------
IDA* combines the memory efficiency of IDS with the heuristic guidance of A*.
It performs depth-first search with an f-cost limit that increases iteratively.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Recursive DFS with f-cost threshold
   - No explicit frontier (implicit in call stack)
   - Visited set refreshed each iteration

2. Process:
   - Initialize threshold = h(initial)
   - Each iteration:
     * Perform DFS, pruning when f(n) > threshold
     * Track minimum f-value exceeding threshold
     * If goal not found, set threshold to min_f
     * Repeat until goal found or threshold = ∞

3. Depth-First Search with Threshold:
   - For each node:
     * Calculate f(n) = g(n) + h(n)
     * If f(n) > threshold, prune and return f(n)
     * If goal, return solution
     * Recursively explore children
     * Track minimum f among pruned nodes

4. Properties:
   - Complete: Yes, with admissible heuristic
   - Optimal: Yes, with admissible heuristic
   - Time Complexity: O(b^d) but practical performance good
   - Space Complexity: O(d) - only stores path!

5. Advantages:
   - Optimal like A*
   - Memory efficient like DFS
   - Combines best of A* and IDS
   - Excellent for memory-constrained problems

6. Disadvantages:
   - Redundant node expansion
   - Slower than A* (re-explores nodes)
   - Performance sensitive to heuristic accuracy
"""

import sys
import logging
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state
from heuristics import face_mismatch_heuristic

logger = logging.getLogger(__name__)


def idastar(initial_state, dimensions, max_iterations=50):
    """
    Perform Iterative Deepening A* Search to find solution.
    
    Args:
        initial_state: 3D list representing initial cube state
        dimensions: tuple (x_dim, y_dim, z_dim)
        max_iterations: maximum number of iterations before giving up
    
    Returns:
        dict with keys:
            - visited_order: list of serialized states in order expanded
            - expanded_nodes: list of serialized states that were expanded
            - solution_path: list of moves to reach goal
            - final_state: the goal state (3D list)
            - success: True if solution found, False otherwise
    """
    from cube import Cube
    
    cube = Cube(dimensions)
    all_moves = get_all_moves(dimensions)
    
    # Check if initial state is goal
    initial_serialized = serialize_state(initial_state, dimensions)
    cube.set_state(initial_state)
    if cube.is_goal():
        return {
            'visited_order': [initial_serialized],
            'expanded_nodes': [initial_serialized],
            'solution_path': [],
            'final_state': initial_state,
            'success': True
        }
    
    # Initialize threshold with heuristic of initial state
    threshold = face_mismatch_heuristic(initial_state, dimensions)
    visited_order = []
    expanded_nodes = []
    path = []
    
    logger.info(f"IDA*: Starting with threshold={threshold:.4f}")
    
    iteration = 0
    while threshold < float('inf') and iteration < max_iterations:
        iteration += 1
        logger.info(f"IDA*: Iteration {iteration}, Threshold: {threshold:.4f}, Expanded so far: {len(expanded_nodes)}")
        
        visited = set()
        result = _ida_search(
            initial_state, 0, threshold, path, dimensions,
            cube, all_moves, visited, visited_order, expanded_nodes
        )
        
        if result['found']:
            logger.info(f"IDA*: SOLUTION FOUND! Path length: {len(result['path'])}, Expanded: {len(expanded_nodes)}")
            return {
                'visited_order': visited_order,
                'expanded_nodes': expanded_nodes,
                'solution_path': result['path'],
                'final_state': result['state'],
                'success': True
            }
        
        if result['min_threshold'] == float('inf'):
            break
        
        threshold = result['min_threshold']
    
    # No solution found
    logger.warning(f"IDA*: No solution found after {iteration} iterations. Expanded {len(expanded_nodes)} nodes")
    return {
        'visited_order': visited_order,
        'expanded_nodes': expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }


def _ida_search(state, g, threshold, path, dimensions, cube, all_moves, 
                visited, visited_order, expanded_nodes):
    """
    Recursive helper for IDA*.
    
    Returns:
        dict with 'found' flag, 'path', 'state', and 'min_threshold'
    """
    current_serialized = serialize_state(state, dimensions)
    h = face_mismatch_heuristic(state, dimensions)
    f = g + h
    
    if f > threshold:
        return {'found': False, 'min_threshold': f}
    
    # Check if goal
    cube.set_state(state)
    if cube.is_goal():
        return {
            'found': True,
            'path': path,
            'state': state,
            'min_threshold': threshold
        }
    
    if current_serialized in visited:
        return {'found': False, 'min_threshold': float('inf')}
    
    visited.add(current_serialized)
    
    # Mark as expanded
    if current_serialized not in expanded_nodes:
        expanded_nodes.append(current_serialized)
    
    min_threshold = float('inf')
    
    # Explore neighbors
    for move in all_moves:
        new_state = apply_move(state, dimensions, move)
        new_serialized = serialize_state(new_state, dimensions)
        
        if new_serialized not in visited:
            if new_serialized not in visited_order:
                visited_order.append(new_serialized)
            
            new_path = path + [move]
            result = _ida_search(
                new_state, g + 1, threshold, new_path, dimensions,
                cube, all_moves, visited, visited_order, expanded_nodes
            )
            
            if result['found']:
                return result
            
            if result['min_threshold'] < min_threshold:
                min_threshold = result['min_threshold']
    
    visited.remove(current_serialized)
    return {'found': False, 'min_threshold': min_threshold}

