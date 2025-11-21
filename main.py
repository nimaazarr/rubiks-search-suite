"""
Main script to run all search algorithms on a scrambled cube.
"""

import time
import logging
from cube import Cube
from moves import apply_move
from utils import serialize_state
from search.bfs import bfs
from search.dfs import dfs
from search.ucs import ucs
from search.dls import dls
from search.ids import ids
from search.gbfs import gbfs
from search.astar import astar
from search.wastar import wastar
from search.idastar import idastar
from search.rbfs import rbfs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('solver.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)


def create_scrambled_cube(dimensions, moves_list):
    """
    Create a scrambled cube by applying a series of moves to the solved state.
    
    Args:
        dimensions: tuple (x_dim, y_dim, z_dim)
        moves_list: list of moves to apply
    
    Returns:
        scrambled cube state
    """
    cube = Cube(dimensions)
    state = cube.get_state()
    
    for move in moves_list:
        state = apply_move(state, dimensions, move)
    
    return state


def format_move(move):
    """Format a move as a string."""
    axis, index = move
    return f"({axis},{index})"


def print_results(algorithm_name, result, execution_time):
    """Print results for a single algorithm."""
    print(f"\n{'='*80}")
    print(f"ALGORITHM: {algorithm_name}")
    print(f"{'='*80}")
    print(f"Success: {result['success']}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    print(f"Number of Expanded Nodes: {len(result['expanded_nodes'])}")
    print(f"Number of Visited States: {len(result['visited_order'])}")
    
    if result['success']:
        print(f"Solution Path Length: {len(result['solution_path'])}")
        print(f"Solution Path: {' -> '.join([format_move(m) for m in result['solution_path']])}")
    else:
        print("No solution found.")
    
    print(f"\nFirst 5 Expanded Nodes:")
    for i, state in enumerate(result['expanded_nodes'][:5]):
        print(f"  {i+1}. {state[:50]}...")
    
    if len(result['expanded_nodes']) > 5:
        print(f"  ... and {len(result['expanded_nodes']) - 5} more")


def write_report(results, dimensions, initial_state, scramble_moves):
    """Write comprehensive report to file."""
    with open('report.txt', 'w') as f:
        f.write("="*80 + "\n")
        f.write("RUBIK'S CUBE PUZZLE SOLVER - COMPREHENSIVE REPORT\n")
        f.write("="*80 + "\n\n")
        
        # Problem setup
        f.write("PROBLEM SETUP\n")
        f.write("-"*80 + "\n")
        f.write(f"Cube Dimensions: {dimensions[0]} x {dimensions[1]} x {dimensions[2]}\n")
        f.write(f"Scramble Moves Applied: {len(scramble_moves)}\n")
        f.write(f"Scramble Sequence: {' -> '.join([format_move(m) for m in scramble_moves])}\n")
        f.write(f"Initial State (serialized): {serialize_state(initial_state, dimensions)[:100]}...\n\n")
        
        # Summary table
        f.write("ALGORITHM PERFORMANCE SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Algorithm':<20} {'Success':<10} {'Expanded':<12} {'Path Len':<12} {'Time (s)':<12}\n")
        f.write("-"*80 + "\n")
        
        for name, result, exec_time in results:
            success = "Yes" if result['success'] else "No"
            expanded = len(result['expanded_nodes'])
            path_len = len(result['solution_path']) if result['success'] else "N/A"
            f.write(f"{name:<20} {success:<10} {expanded:<12} {str(path_len):<12} {exec_time:<12.4f}\n")
        
        f.write("\n\n")
        
        # Detailed results for each algorithm
        f.write("DETAILED ALGORITHM RESULTS\n")
        f.write("="*80 + "\n\n")
        
        for name, result, exec_time in results:
            f.write(f"\n{name}\n")
            f.write("-"*80 + "\n")
            f.write(f"Success: {result['success']}\n")
            f.write(f"Execution Time: {exec_time:.4f} seconds\n")
            f.write(f"Expanded Nodes: {len(result['expanded_nodes'])}\n")
            f.write(f"Visited States: {len(result['visited_order'])}\n")
            
            if result['success']:
                f.write(f"Solution Path Length: {len(result['solution_path'])}\n")
                f.write(f"Solution Path: {' -> '.join([format_move(m) for m in result['solution_path']])}\n")
            else:
                f.write("No solution found within search limits.\n")
            
            f.write(f"\nExpanded Nodes (first 10):\n")
            for i, state in enumerate(result['expanded_nodes'][:10]):
                f.write(f"  {i+1}. {state}\n")
            
            if len(result['expanded_nodes']) > 10:
                f.write(f"  ... and {len(result['expanded_nodes']) - 10} more\n")
            
            f.write("\n")
        
        # Heuristic analysis
        f.write("\n" + "="*80 + "\n")
        f.write("HEURISTIC ANALYSIS\n")
        f.write("="*80 + "\n\n")
        
        f.write("Heuristic Function: Face Mismatch Heuristic\n")
        f.write("-"*80 + "\n")
        f.write("Description: Counts the number of face colors that don't match the\n")
        f.write("target uniform color for each of the 6 external faces, divided by\n")
        f.write("an optimistic factor (max affected cubies per move).\n\n")
        
        f.write("Admissibility: This heuristic is admissible because:\n")
        f.write("  1. Each move can affect at most 2 * max(dimensions) cubies\n")
        f.write("  2. We divide the total mismatches by this maximum\n")
        f.write("  3. This ensures we never overestimate the cost to goal\n\n")
        
        f.write("Consistency: For any state n and successor n':\n")
        f.write("  h(n) <= cost(n,n') + h(n')\n")
        f.write("  Since cost(n,n') = 1 for all moves, and each move can reduce\n")
        f.write("  mismatches by at most a bounded amount, the heuristic is consistent.\n\n")
        
        # Comparison
        f.write("\n" + "="*80 + "\n")
        f.write("ALGORITHM COMPARISON\n")
        f.write("="*80 + "\n\n")
        
        f.write("Blind Search Algorithms:\n")
        f.write("-"*80 + "\n")
        f.write("BFS: Complete and optimal, but explores many states\n")
        f.write("DFS: Incomplete (with depth limit), may find suboptimal solutions\n")
        f.write("UCS: Complete and optimal, equivalent to BFS with unit costs\n")
        f.write("DLS: Complete up to depth limit, not optimal\n")
        f.write("IDS: Complete and optimal, combines benefits of BFS and DFS\n\n")
        
        f.write("Informed Search Algorithms:\n")
        f.write("-"*80 + "\n")
        f.write("GBFS: Not complete or optimal, but can be fast with good heuristic\n")
        f.write("A*: Complete and optimal with admissible heuristic\n")
        f.write("Weighted A*: Trades optimality for speed (W > 1)\n")
        f.write("IDA*: Complete and optimal, memory efficient\n")
        f.write("RBFS: Complete and optimal, memory efficient with bounded space\n\n")
        
        f.write("\nConclusion:\n")
        f.write("-"*80 + "\n")
        f.write("For this puzzle, informed search algorithms (A*, IDA*, RBFS) typically\n")
        f.write("outperform blind search by using the heuristic to guide exploration.\n")
        f.write("A* is usually fastest but uses more memory, while IDA* and RBFS trade\n")
        f.write("time for space efficiency.\n")


def main():
    """Main function to run all algorithms."""
    logger.info("="*80)
    logger.info("Starting Rubik's Cube Puzzle Solver")
    logger.info("="*80)
    
    print("Rubik's Cube Puzzle Solver")
    print("="*80)
    
    # Define cube dimensions
    dimensions = (2, 2, 2)  # 2x2x2 cube for reasonable search time
    logger.info(f"Cube Dimensions: {dimensions[0]} x {dimensions[1]} x {dimensions[2]}")
    print(f"\nCube Dimensions: {dimensions[0]} x {dimensions[1]} x {dimensions[2]}")
    
    # Create a scrambled cube with a few moves
    # For demonstration, use a simple scramble that's solvable
    # Using fewer moves to keep search space manageable
    scramble_moves = [
        ('x', 0),
        ('y', 1)
    ]
    
    logger.info(f"Applying {len(scramble_moves)} scramble moves: {scramble_moves}")
    print(f"Applying {len(scramble_moves)} scramble moves: {scramble_moves}")
    initial_state = create_scrambled_cube(dimensions, scramble_moves)
    logger.info(f"Initial state created")
    print(f"Initial state created (serialized preview): {serialize_state(initial_state, dimensions)[:50]}...")
    
    # Define algorithms to test
    # Note: Using reasonable depth limits to ensure algorithms complete in reasonable time
    algorithms = [
        ("BFS", lambda: bfs(initial_state, dimensions)),
        ("DFS", lambda: dfs(initial_state, dimensions, max_depth=6)),
        ("UCS", lambda: ucs(initial_state, dimensions)),
        ("DLS", lambda: dls(initial_state, dimensions, depth_limit=5)),
        ("IDS", lambda: ids(initial_state, dimensions, max_depth=6)),
        ("GBFS", lambda: gbfs(initial_state, dimensions)),
        ("A*", lambda: astar(initial_state, dimensions)),
        ("Weighted A*", lambda: wastar(initial_state, dimensions, weight=2.0)),
        ("IDA*", lambda: idastar(initial_state, dimensions)),
        ("RBFS", lambda: rbfs(initial_state, dimensions))
    ]
    
    results = []
    
    # Run each algorithm
    for name, algo_func in algorithms:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running {name}...")
        logger.info(f"{'='*60}")
        print(f"\n\nRunning {name}...")
        start_time = time.time()
        
        try:
            result = algo_func()
            end_time = time.time()
            execution_time = end_time - start_time
            
            logger.info(f"{name} completed in {execution_time:.4f} seconds")
            logger.info(f"{name} - Success: {result['success']}, Expanded: {len(result['expanded_nodes'])}, Path Length: {len(result['solution_path']) if result['success'] else 'N/A'}")
            
            print_results(name, result, execution_time)
            results.append((name, result, execution_time))
            
        except Exception as e:
            logger.error(f"Error running {name}: {str(e)}")
            print(f"Error running {name}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Write comprehensive report
    print("\n\n" + "="*80)
    print("Writing comprehensive report to report.txt...")
    write_report(results, dimensions, initial_state, scramble_moves)
    print("Report written successfully!")
    print("="*80)


if __name__ == "__main__":
    main()

