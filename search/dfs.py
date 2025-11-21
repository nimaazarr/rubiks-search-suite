"""
Depth-First Search (DFS) implementation.

ALGORITHM OVERVIEW:
------------------
DFS explores the search space by going as deep as possible along each branch
before backtracking. It uses a LIFO stack to maintain the frontier.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Stack (list): LIFO frontier for depth-first exploration
   - Set: Tracks visited states to avoid cycles
   - Depth tracking: Prevents infinite loops with max_depth limit

2. Process:
   - Start with initial state on stack with depth 0
   - Pop a state, mark as expanded
   - If depth limit not reached:
     * Generate all successor states
     * For each unvisited successor:
       - Check if goal
       - Push to stack with incremented depth
   - Continue until goal found or stack empty

3. Properties:
   - Complete: Only with depth limit
   - Optimal: No - finds first solution, not necessarily shortest
   - Time Complexity: O(b^m) where m=maximum depth
   - Space Complexity: O(bm) - only stores path from root

4. Advantages:
   - Memory efficient
   - Fast when solution is deep in tree

5. Disadvantages:
   - May find suboptimal solutions
   - Can get stuck in deep branches
   - Requires depth limit to guarantee termination
"""

import sys
import logging
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state

logger = logging.getLogger(__name__)


def dfs(initial_state, dimensions, max_depth=20):
    """
    Perform Depth-First Search to find solution.
    
    Args:
        initial_state: 3D list representing initial cube state
        dimensions: tuple (x_dim, y_dim, z_dim)
        max_depth: maximum depth to search (to prevent infinite loops)
    
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
    stack = [(initial_state, [], 0)]  # (state, path, depth)
    visited = {initial_serialized}
    visited_order = []
    expanded_nodes = []
    
    # Check if initial state is goal
    cube = Cube(dimensions)
    cube.set_state(initial_state)
    logger.info(f"DFS: Starting with max_depth={max_depth}")
    if cube.is_goal():
        return {
            'visited_order': [initial_serialized],
            'expanded_nodes': [initial_serialized],
            'solution_path': [],
            'final_state': initial_state,
            'success': True
        }
    
    all_moves = get_all_moves(dimensions)
    logger.info(f"DFS: {len(all_moves)} possible moves per state")
    
    iteration = 0
    while stack:
        iteration += 1
        if iteration % 1000 == 0:
            logger.info(f"DFS: Iteration {iteration}, Stack size: {len(stack)}, Visited: {len(visited)}")
        
        current_state, path, depth = stack.pop()
        current_serialized = serialize_state(current_state, dimensions)
        
        # Mark as expanded
        if current_serialized not in expanded_nodes:
            expanded_nodes.append(current_serialized)
        
        # Check depth limit
        if depth >= max_depth:
            continue
        
        # Explore neighbors (in reverse order for DFS)
        for move in reversed(all_moves):
            new_state = apply_move(current_state, dimensions, move)
            new_serialized = serialize_state(new_state, dimensions)
            
            if new_serialized not in visited:
                visited.add(new_serialized)
                visited_order.append(new_serialized)
                new_path = path + [move]
                
                # Check if goal
                cube.set_state(new_state)
                if cube.is_goal():
                    expanded_nodes.append(new_serialized)
                    return {
                        'visited_order': visited_order,
                        'expanded_nodes': expanded_nodes,
                        'solution_path': new_path,
                        'final_state': new_state,
                        'success': True
                    }
                
                stack.append((new_state, new_path, depth + 1))
    
    # No solution found
    return {
        'visited_order': visited_order,
        'expanded_nodes': expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }

