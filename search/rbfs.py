"""
Recursive Best-First Search (RBFS) implementation.

ALGORITHM OVERVIEW:
------------------
RBFS is a memory-efficient alternative to A* that mimics A*'s best-first
exploration using only linear space through recursive backtracking.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Recursive call stack (implicit)
   - Successor list with f-values at each level
   - f_limit parameter passed down recursion

2. Process:
   - At each node:
     * Generate all successors with f-values
     * Sort successors by f-value
     * Expand best child recursively with f_limit
     * f_limit = min(parent's limit, 2nd-best f-value)
     * If best exceeds limit, backtrack with updated f
     * Update best's f-value based on recursion result

3. Key Mechanism:
   - Explores most promising path
   - When hits f_limit, backtracks
   - Remembers "backed up" f-values
   - Switches to next-best path if better
   - Mimics A* frontier with O(bd) memory

4. Properties:
   - Complete: Yes, with admissible heuristic
   - Optimal: Yes, with admissible heuristic
   - Time Complexity: Depends on h accuracy
   - Space Complexity: O(bd) - linear!

5. Advantages:
   - Optimal like A*
   - Memory efficient - O(bd) vs A*'s O(b^d)
   - Good for memory-limited systems
   - Can handle very deep searches

6. Disadvantages:
   - May regenerate nodes (time overhead)
   - More complex to implement than A*
   - Can thrash between paths if f-values similar
   - Best for problems where memory is constraint
"""

import sys
import logging
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state
from heuristics import face_mismatch_heuristic

logger = logging.getLogger(__name__)


def rbfs(initial_state, dimensions, max_nodes=10000):
    """
    Perform Recursive Best-First Search to find solution.
    
    Args:
        initial_state: 3D list representing initial cube state
        dimensions: tuple (x_dim, y_dim, z_dim)
    
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
    
    visited_order = []
    expanded_nodes = []
    
    h_initial = face_mismatch_heuristic(initial_state, dimensions)
    logger.info(f"RBFS: Starting with h={h_initial:.4f}, max_nodes={max_nodes}")
    
    result = _rbfs_search(
        initial_state, 0, h_initial, float('inf'), [], dimensions,
        cube, all_moves, visited_order, expanded_nodes, max_nodes
    )
    
    if result['found']:
        logger.info(f"RBFS: SOLUTION FOUND! Path length: {len(result['path'])}, Expanded: {len(expanded_nodes)}")
        return {
            'visited_order': visited_order,
            'expanded_nodes': expanded_nodes,
            'solution_path': result['path'],
            'final_state': result['state'],
            'success': True
        }
    else:
        logger.warning(f"RBFS: No solution found. Expanded {len(expanded_nodes)} nodes")
        return {
            'visited_order': visited_order,
            'expanded_nodes': expanded_nodes,
            'solution_path': [],
            'final_state': None,
            'success': False
        }


def _rbfs_search(state, g, f, f_limit, path, dimensions, cube, all_moves, 
                 visited_order, expanded_nodes, max_nodes):
    """
    Recursive helper for RBFS.
    
    Args:
        state: current state
        g: cost so far
        f: current f value
        f_limit: f-value limit
        path: current path
        dimensions: cube dimensions
        cube: Cube object
        all_moves: list of all possible moves
        visited_order: list to track visited states
        expanded_nodes: list to track expanded nodes
        max_nodes: maximum nodes to expand
    
    Returns:
        dict with 'found' flag, 'path', 'state', and 'f_min'
    """
    current_serialized = serialize_state(state, dimensions)
    
    # Check if goal
    cube.set_state(state)
    if cube.is_goal():
        return {
            'found': True,
            'path': path,
            'state': state,
            'f_min': f
        }
    
    # Mark as expanded
    if current_serialized not in expanded_nodes:
        expanded_nodes.append(current_serialized)
    
    # Check if we've exceeded max nodes
    if len(expanded_nodes) >= max_nodes:
        return {'found': False, 'f_min': float('inf')}
    
    # Generate successors
    successors = []
    for move in all_moves:
        new_state = apply_move(state, dimensions, move)
        new_serialized = serialize_state(new_state, dimensions)
        
        if new_serialized not in visited_order:
            visited_order.append(new_serialized)
        
        new_g = g + 1
        h_new = face_mismatch_heuristic(new_state, dimensions)
        f_new = new_g + h_new
        
        successors.append({
            'state': new_state,
            'move': move,
            'g': new_g,
            'f': max(f_new, f)  # Update f to be at least parent's f
        })
    
    if not successors:
        return {'found': False, 'f_min': float('inf')}
    
    # Sort successors by f value
    successors.sort(key=lambda x: x['f'])
    
    while True:
        best = successors[0]
        
        if best['f'] > f_limit:
            return {'found': False, 'f_min': best['f']}
        
        # Get alternative f value (second best)
        if len(successors) > 1:
            alternative = successors[1]['f']
        else:
            alternative = float('inf')
        
        # Recursively search best successor
        new_path = path + [best['move']]
        result = _rbfs_search(
            best['state'], best['g'], best['f'], min(f_limit, alternative),
            new_path, dimensions, cube, all_moves, visited_order, expanded_nodes, max_nodes
        )
        
        best['f'] = result['f_min']
        
        if result['found']:
            return result
        
        # Re-sort successors
        successors.sort(key=lambda x: x['f'])

