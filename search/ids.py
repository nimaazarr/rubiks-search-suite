"""
Iterative Deepening Search (IDS) implementation.

ALGORITHM OVERVIEW:
------------------
IDS combines the space efficiency of DFS with the optimality of BFS by
repeatedly performing DLS with increasing depth limits.

IMPLEMENTATION DETAILS:
----------------------
1. Data Structures:
   - Reuses DLS for each iteration
   - Accumulates visited/expanded nodes across iterations

2. Process:
   - For depth = 0, 1, 2, ... max_depth:
     * Run DLS with current depth limit
     * Accumulate visited and expanded nodes
     * If solution found, return immediately
   - Each iteration explores deeper than previous

3. Properties:
   - Complete: Yes, if solution exists within max_depth
   - Optimal: Yes, finds shallowest solution
   - Time Complexity: O(b^d) - only slightly worse than BFS
   - Space Complexity: O(bd) - linear like DFS

4. Implementation Notes:
   - Re-explores states at shallower depths
   - Overhead is acceptable because most nodes at deepest level
   - Tracks cumulative statistics across iterations

5. Advantages:
   - Optimal like BFS
   - Memory efficient like DFS
   - Best of both worlds
   - No need to know solution depth beforehand

6. Disadvantages:
   - Redundant node expansion
   - Slightly slower than BFS in practice
   - Time complexity has higher constant factor
"""

import sys
sys.path.append('..')
from search.dls import dls


def ids(initial_state, dimensions, max_depth=20):
    """
    Perform Iterative Deepening Search to find solution.
    
    Args:
        initial_state: 3D list representing initial cube state
        dimensions: tuple (x_dim, y_dim, z_dim)
        max_depth: maximum depth to search
    
    Returns:
        dict with keys:
            - visited_order: list of serialized states in order expanded
            - expanded_nodes: list of serialized states that were expanded
            - solution_path: list of moves to reach goal
            - final_state: the goal state (3D list)
            - success: True if solution found, False otherwise
    """
    all_visited_order = []
    all_expanded_nodes = []
    
    for depth in range(max_depth + 1):
        result = dls(initial_state, dimensions, depth)
        
        # Accumulate visited and expanded
        for state in result['visited_order']:
            if state not in all_visited_order:
                all_visited_order.append(state)
        
        for state in result['expanded_nodes']:
            if state not in all_expanded_nodes:
                all_expanded_nodes.append(state)
        
        if result['success']:
            return {
                'visited_order': all_visited_order,
                'expanded_nodes': all_expanded_nodes,
                'solution_path': result['solution_path'],
                'final_state': result['final_state'],
                'success': True
            }
    
    # No solution found
    return {
        'visited_order': all_visited_order,
        'expanded_nodes': all_expanded_nodes,
        'solution_path': [],
        'final_state': None,
        'success': False
    }

