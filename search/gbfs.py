"""
Greedy Best-First Search (GBFS) implementation.

ALGORITHM OVERVIEW:
------------------
GBFS expands nodes based purely on heuristic estimate h(n) to the goal,
always choosing the node that appears closest to the goal.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Priority Queue (heapq): Orders states by heuristic value h(n)
   - Set: Tracks visited states
   - Counter: Ensures consistent ordering

2. Process:
   - Start with initial state, compute h(initial)
   - While queue not empty:
     * Pop state with lowest h value
     * Generate all successors
     * For each unvisited successor:
       - Check if goal
       - Compute h(successor)
       - Add to queue with h as priority
   - Greedily follows most promising path

3. Properties:
   - Complete: No - can get stuck in local minima
   - Optimal: No - ignores path cost
   - Time Complexity: O(b^m) worst case
   - Space Complexity: O(b^m)

4. Implementation Notes:
   - Uses only heuristic, not path cost
   - Can be very fast with good heuristic
   - May fail or explore many nodes with poor heuristic
   - Node limit prevents infinite exploration

5. Advantages:
   - Very fast when heuristic is accurate
   - Low memory for successful searches
   - Simple to implement

6. Disadvantages:
   - Not complete or optimal
   - Can be misled by heuristic
   - May explore irrelevant branches
   - No guarantee of finding solution
"""

import heapq
import sys
import logging
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state
from heuristics import face_mismatch_heuristic

logger = logging.getLogger(__name__)


def gbfs(initial_state, dimensions, max_nodes=10000):
    """
    Perform Greedy Best-First Search to find solution.
    Uses only heuristic value h(n) for priority.
    
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
    
    # Priority queue: (h, counter, state, path)
    counter = 0
    pq = [(h_initial, counter, initial_state, [])]
    visited = {initial_serialized}
    visited_order = []
    expanded_nodes = []
    
    # Check if initial state is goal
    cube = Cube(dimensions)
    cube.set_state(initial_state)
    logger.info(f"GBFS: Starting with h={h_initial:.4f}")
    if cube.is_goal():
        return {
            'visited_order': [initial_serialized],
            'expanded_nodes': [initial_serialized],
            'solution_path': [],
            'final_state': initial_state,
            'success': True
        }
    
    all_moves = get_all_moves(dimensions)
    logger.info(f"GBFS: {len(all_moves)} possible moves per state")
    
    iteration = 0
    while pq:
        iteration += 1
        if iteration % 100 == 0:
            logger.info(f"GBFS: Iteration {iteration}, PQ size: {len(pq)}, Visited: {len(visited)}")
        
        h, _, current_state, path = heapq.heappop(pq)
        current_serialized = serialize_state(current_state, dimensions)
        
        # Mark as expanded
        if current_serialized not in expanded_nodes:
            expanded_nodes.append(current_serialized)
        
        # Check if we've exceeded max nodes
        if len(expanded_nodes) >= max_nodes:
            logger.warning(f"GBFS: Reached max nodes limit ({max_nodes})")
            break
        
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
                    logger.info(f"GBFS: SOLUTION FOUND! Path length: {len(new_path)}, Expanded: {len(expanded_nodes)}")
                    return {
                        'visited_order': visited_order,
                        'expanded_nodes': expanded_nodes,
                        'solution_path': new_path,
                        'final_state': new_state,
                        'success': True
                    }
                
                h_new = face_mismatch_heuristic(new_state, dimensions)
                counter += 1
                heapq.heappush(pq, (h_new, counter, new_state, new_path))
    
    # No solution found
    logger.warning(f"GBFS: No solution found. Expanded {len(expanded_nodes)} nodes")
    return {
        'visited_order': visited_order,
        'expanded_nodes': expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }

