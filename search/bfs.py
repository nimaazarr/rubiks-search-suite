"""
Breadth-First Search (BFS) implementation.

ALGORITHM OVERVIEW:
------------------
BFS explores the search space level by level, guaranteeing the shortest path
to the goal. It uses a FIFO queue to maintain the frontier of unexplored states.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Queue (deque): FIFO frontier for states to explore
   - Set: Tracks visited states to avoid cycles
   - Lists: Store visited order and expanded nodes for reporting

2. Process:
   - Start with initial state in queue
   - Dequeue a state, mark as expanded
   - Generate all successor states by applying possible moves
   - For each successor:
     * Skip if already visited
     * Check if it's the goal state
     * If not goal, add to queue for later exploration
   - Continue until goal found or queue empty

3. Properties:
   - Complete: Always finds a solution if one exists
   - Optimal: Finds shortest path (with unit costs)
   - Time Complexity: O(b^d) where b=branching factor, d=depth
   - Space Complexity: O(b^d) - stores entire frontier

4. Advantages:
   - Guaranteed optimal solution
   - Systematic exploration

5. Disadvantages:
   - Memory intensive for deep search spaces
   - Explores many states even when close to goal
"""

from collections import deque
import sys
import logging
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state

logger = logging.getLogger(__name__)


def bfs(initial_state, dimensions):
    """
    Perform Breadth-First Search to find solution.
    
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
    
    # Initialize
    initial_serialized = serialize_state(initial_state, dimensions)
    queue = deque([(initial_state, [])])  # (state, path)
    visited = {initial_serialized}
    visited_order = []
    expanded_nodes = []
    
    # Check if initial state is goal
    cube = Cube(dimensions)
    cube.set_state(initial_state)
    logger.info("BFS: Checking if initial state is goal")
    if cube.is_goal():
        logger.info("BFS: Initial state is already the goal!")
        return {
            'visited_order': [initial_serialized],
            'expanded_nodes': [initial_serialized],
            'solution_path': [],
            'final_state': initial_state,
            'success': True
        }
    
    all_moves = get_all_moves(dimensions)
    logger.info(f"BFS: Starting search with {len(all_moves)} possible moves per state")
    
    iteration = 0
    while queue:
        iteration += 1
        if iteration % 100 == 0:
            logger.info(f"BFS: Iteration {iteration}, Queue size: {len(queue)}, Visited: {len(visited)}")
        current_state, path = queue.popleft()
        current_serialized = serialize_state(current_state, dimensions)
        
        # Mark as expanded
        if current_serialized not in expanded_nodes:
            expanded_nodes.append(current_serialized)
        
        # Explore neighbors
        for move in all_moves:
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
                    logger.info(f"BFS: SOLUTION FOUND! Path length: {len(new_path)}, Expanded: {len(expanded_nodes)}")
                    return {
                        'visited_order': visited_order,
                        'expanded_nodes': expanded_nodes,
                        'solution_path': new_path,
                        'final_state': new_state,
                        'success': True
                    }
                
                queue.append((new_state, new_path))
    
    # No solution found
    logger.warning(f"BFS: No solution found. Expanded {len(expanded_nodes)} nodes")
    return {
        'visited_order': visited_order,
        'expanded_nodes': expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }

