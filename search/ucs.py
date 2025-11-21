"""
Uniform-Cost Search (UCS) implementation.

ALGORITHM OVERVIEW:
------------------
UCS expands nodes in order of their path cost from the start state. It's a
variant of Dijkstra's algorithm that guarantees optimal solutions.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Priority Queue (heapq): Orders states by cumulative path cost g(n)
   - Dictionary: Maps states to their minimum known cost
   - Counter: Ensures consistent ordering for equal-cost states

2. Process:
   - Start with initial state at cost 0 in priority queue
   - Pop state with lowest cost
   - If this cost is better than previously known, expand:
     * Generate all successor states
     * Calculate new cost (current + 1 for unit step cost)
     * If new cost is better, update and add to queue
   - Continue until goal found at lowest cost

3. Properties:
   - Complete: Always finds a solution if one exists
   - Optimal: Finds lowest-cost path
   - Time Complexity: O(b^(1+⌊C*/ε⌋)) where C*=optimal cost, ε=min step cost
   - Space Complexity: O(b^(1+⌊C*/ε⌋))

4. Implementation Notes:
   - With unit costs, equivalent to BFS
   - Maintains best-known cost for each state
   - Skips states if better path already found

5. Advantages:
   - Guaranteed optimal solution
   - Works with non-uniform costs

6. Disadvantages:
   - No heuristic guidance
   - Memory intensive
"""

import heapq
import sys
sys.path.append('..')
from moves import apply_move, get_all_moves
from utils import serialize_state


def ucs(initial_state, dimensions):
    """
    Perform Uniform-Cost Search to find solution.
    All moves have cost 1, so this is equivalent to BFS but demonstrates UCS structure.
    
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
    # Priority queue: (cost, counter, state, path)
    counter = 0
    pq = [(0, counter, initial_state, [])]
    visited = {initial_serialized: 0}  # state -> min cost
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
    
    while pq:
        cost, _, current_state, path = heapq.heappop(pq)
        current_serialized = serialize_state(current_state, dimensions)
        
        # Skip if we've found a better path to this state
        if current_serialized in visited and cost > visited[current_serialized]:
            continue
        
        # Mark as expanded
        if current_serialized not in expanded_nodes:
            expanded_nodes.append(current_serialized)
        
        # Explore neighbors
        for move in all_moves:
            new_state = apply_move(current_state, dimensions, move)
            new_serialized = serialize_state(new_state, dimensions)
            new_cost = cost + 1  # Each move costs 1
            
            # Check if this is a better path
            if new_serialized not in visited or new_cost < visited[new_serialized]:
                visited[new_serialized] = new_cost
                if new_serialized not in [v for v in visited_order]:
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
                
                counter += 1
                heapq.heappush(pq, (new_cost, counter, new_state, new_path))
    
    # No solution found
    return {
        'visited_order': visited_order,
        'expanded_nodes': expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }

