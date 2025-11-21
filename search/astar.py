"""
A* Search implementation.

ALGORITHM OVERVIEW:
------------------
A* is the gold standard for optimal pathfinding. It uses f(n) = g(n) + h(n)
where g(n) is actual cost from start and h(n) is estimated cost to goal.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Priority Queue (heapq): Orders by f(n) = g(n) + h(n)
   - Dictionary: Tracks best-known g(n) for each state
   - Counter: Tie-breaking for equal f-values

2. Process:
   - Initialize with start state: g=0, h=h(start), f=h
   - While queue not empty:
     * Pop state with lowest f(n)
     * If this is goal, return solution
     * For each successor:
       - Calculate g_new = g(current) + 1
       - Calculate h_new = heuristic(successor)
       - f_new = g_new + h_new
       - If g_new better than known, add to queue

3. Properties:
   - Complete: Yes, if admissible heuristic
   - Optimal: Yes, if admissible heuristic
   - Time Complexity: O(b^d) but much better with good h
   - Space Complexity: O(b^d)

4. Admissibility Requirement:
   - h(n) must never overestimate true cost
   - Our face mismatch heuristic is admissible
   - Guarantees optimal solution

5. Advantages:
   - Optimal solution guaranteed
   - Efficient with good heuristic
   - Expands far fewer nodes than BFS
   - Widely used and well-understood

6. Disadvantages:
   - Memory intensive (stores all generated nodes)
   - Performance depends on heuristic quality
   - Slower than greedy but guarantees optimality
"""

import heapq
import sys
import logging
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state
from heuristics import face_mismatch_heuristic

logger = logging.getLogger(__name__)


def astar(initial_state, dimensions, max_nodes=10000):
    """
    Perform A* Search to find solution.
    Uses f(n) = g(n) + h(n) where g is cost and h is heuristic.
    
    Args:
        initial_state: 3D list representing initial cube state
        dimensions: tuple (x_dim, y_dim, z_dim)
        max_nodes: maximum number of nodes to expand before giving up
    
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
    h_initial = face_mismatch_heuristic(initial_state, dimensions)
    g_initial = 0
    f_initial = g_initial + h_initial
    
    # Priority queue: (f, counter, g, state, path)
    counter = 0
    pq = [(f_initial, counter, g_initial, initial_state, [])]
    visited = {initial_serialized: g_initial}
    visited_order = []
    expanded_nodes = []
    
    # Check if initial state is goal
    cube = Cube(dimensions)
    cube.set_state(initial_state)
    logger.info(f"A*: Starting with h={h_initial:.4f}")
    if cube.is_goal():
        logger.info("A*: Initial state is already the goal!")
        return {
            'visited_order': [initial_serialized],
            'expanded_nodes': [initial_serialized],
            'solution_path': [],
            'final_state': initial_state,
            'success': True
        }
    
    all_moves = get_all_moves(dimensions)
    logger.info(f"A*: {len(all_moves)} possible moves per state")
    
    iteration = 0
    while pq:
        iteration += 1
        if iteration % 100 == 0:
            logger.info(f"A*: Iteration {iteration}, PQ size: {len(pq)}, Visited: {len(visited)}")
        f, _, g, current_state, path = heapq.heappop(pq)
        current_serialized = serialize_state(current_state, dimensions)
        
        # Skip if we've found a better path to this state
        if current_serialized in visited and g > visited[current_serialized]:
            continue
        
        # Mark as expanded
        if current_serialized not in expanded_nodes:
            expanded_nodes.append(current_serialized)
        
        # Check if we've exceeded max nodes
        if len(expanded_nodes) >= max_nodes:
            logger.warning(f"A*: Reached max nodes limit ({max_nodes})")
            break
        
        # Explore neighbors
        for move in all_moves:
            new_state = apply_move(current_state, dimensions, move)
            new_serialized = serialize_state(new_state, dimensions)
            new_g = g + 1  # Each move costs 1
            
            # Check if this is a better path
            if new_serialized not in visited or new_g < visited[new_serialized]:
                visited[new_serialized] = new_g
                if new_serialized not in visited_order:
                    visited_order.append(new_serialized)
                
                new_path = path + [move]
                
                # Check if goal
                cube.set_state(new_state)
                if cube.is_goal():
                    expanded_nodes.append(new_serialized)
                    logger.info(f"A*: SOLUTION FOUND! Path length: {len(new_path)}, Expanded: {len(expanded_nodes)}")
                    return {
                        'visited_order': visited_order,
                        'expanded_nodes': expanded_nodes,
                        'solution_path': new_path,
                        'final_state': new_state,
                        'success': True
                    }
                
                h_new = face_mismatch_heuristic(new_state, dimensions)
                f_new = new_g + h_new
                counter += 1
                heapq.heappush(pq, (f_new, counter, new_g, new_state, new_path))
    
    # No solution found
    logger.warning(f"A*: No solution found. Expanded {len(expanded_nodes)} nodes")
    return {
        'visited_order': visited_order,
        'expanded_nodes': expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }

