"""
Weighted A* Search implementation.

ALGORITHM OVERVIEW:
------------------
Weighted A* modifies A* by using f(n) = g(n) + W*h(n) where W > 1.
This trades optimality for speed by being more greedy with heuristic guidance.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Same as A*: Priority Queue, g-cost dictionary
   - Weight parameter W (typically 1 < W < 5)

2. Process:
   - Identical to A* but with weighted f-value:
     * f(n) = g(n) + W*h(n)
     * Higher W means more greedy behavior
     * W=1 reduces to standard A*
   - Expands nodes with lower weighted f-values first

3. Properties:
   - Complete: Yes
   - Optimal: No - solution cost ≤ W * optimal
   - Time Complexity: Better than A* in practice
   - Space Complexity: O(b^d)

4. Solution Quality:
   - Bounded suboptimality: cost ≤ W * optimal_cost
   - W=2.0 means solution at most twice optimal cost
   - Trade-off: higher W = faster but worse solution

5. Advantages:
   - Faster than A* (expands fewer nodes)
   - Still has bounded suboptimality
   - Good for problems where near-optimal suffices
   - Tunable speed vs quality trade-off

6. Disadvantages:
   - Not optimal
   - Solution quality depends on W
   - May still explore many nodes if h is poor
"""

import heapq
import sys
import logging
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state
from heuristics import face_mismatch_heuristic

logger = logging.getLogger(__name__)


def wastar(initial_state, dimensions, weight=2.0, max_nodes=10000):
    """
    Perform Weighted A* Search to find solution.
    Uses f(n) = g(n) + W*h(n) where W is the weight parameter.
    
    Args:
        initial_state: 3D list representing initial cube state
        dimensions: tuple (x_dim, y_dim, z_dim)
        weight: weight for heuristic (typically between 1 and 5)
    
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
    f_initial = g_initial + weight * h_initial
    
    # Priority queue: (f, counter, g, state, path)
    counter = 0
    pq = [(f_initial, counter, g_initial, initial_state, [])]
    visited = {initial_serialized: g_initial}
    visited_order = []
    expanded_nodes = []
    
    # Check if initial state is goal
    cube = Cube(dimensions)
    cube.set_state(initial_state)
    logger.info(f"Weighted A* (W={weight}): Starting with f={f_initial:.4f}")
    if cube.is_goal():
        return {
            'visited_order': [initial_serialized],
            'expanded_nodes': [initial_serialized],
            'solution_path': [],
            'final_state': initial_state,
            'success': True
        }
    
    all_moves = get_all_moves(dimensions)
    logger.info(f"Weighted A*: {len(all_moves)} possible moves per state")
    
    iteration = 0
    while pq:
        iteration += 1
        if iteration % 100 == 0:
            logger.info(f"Weighted A*: Iteration {iteration}, PQ size: {len(pq)}, Visited: {len(visited)}")
        
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
            logger.warning(f"Weighted A*: Reached max nodes limit ({max_nodes})")
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
                    logger.info(f"Weighted A*: SOLUTION FOUND! Path length: {len(new_path)}, Expanded: {len(expanded_nodes)}")
                    return {
                        'visited_order': visited_order,
                        'expanded_nodes': expanded_nodes,
                        'solution_path': new_path,
                        'final_state': new_state,
                        'success': True
                    }
                
                h_new = face_mismatch_heuristic(new_state, dimensions)
                f_new = new_g + weight * h_new
                counter += 1
                heapq.heappush(pq, (f_new, counter, new_g, new_state, new_path))
    
    # No solution found
    logger.warning(f"Weighted A*: No solution found. Expanded {len(expanded_nodes)} nodes")
    return {
        'visited_order': visited_order,
        'expanded_nodes': expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }

