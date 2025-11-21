# Rubik's Cube Puzzle Solver - Search Algorithms Suite

A comprehensive implementation and comparison of **10 classical search algorithms** applied to a 3D Rubik's-cube-like puzzle with row-reversal move mechanics.

## 🎯 Project Overview

This project implements a generalized Rubik's cube puzzle solver with dimensions x × y × z (where x, y, z ∈ {1,2,3,4}) and compares the performance of both blind (uninformed) and informed search algorithms.

### Key Features
- ✅ **10 Search Algorithms**: BFS, DFS, UCS, DLS, IDS, GBFS, A*, Weighted A*, IDA*, RBFS
- ✅ **Custom Move Mechanics**: Row reversal with cubie orientation updates
- ✅ **Admissible Heuristic**: Face mismatch heuristic with formal proofs
- ✅ **Comprehensive Logging**: Track every state expansion and visit
- ✅ **Detailed Analysis**: Performance comparison with statistical reports
- ✅ **Full Documentation**: Algorithm explanations and implementation details

## 📊 Quick Results

On a 2×2×2 cube scrambled with 2 moves:

| Algorithm | Nodes Expanded | Time | Optimal? |
|-----------|----------------|------|----------|
| **RBFS** | **20** 🏆 | 0.014s | ✅ |
| **IDA*** | 25 | 0.047s | ✅ |
| **Weighted A*** | 29 | **0.013s** ⚡ | ✅ |
| **A*** | 30 | 0.015s | ✅ |
| BFS | 116 | 0.114s | ✅ |
| DFS | 200 | 0.043s | ❌ (suboptimal) |
| GBFS | 10,000 | 10.4s | ❌ (failed) |

**Key Finding**: Informed search algorithms achieved **75-97% reduction** in node expansions compared to blind search!

## 🏗️ Project Structure

```
rubiks-search-suite/
├── cube.py              # State representation & goal checking
├── moves.py             # Row reversal mechanics & orientation updates
├── utils.py             # Serialization & hashing utilities
├── heuristics.py        # Admissible heuristic functions
├── search/              # Algorithm implementations
│   ├── bfs.py          # Breadth-First Search
│   ├── dfs.py          # Depth-First Search
│   ├── ucs.py          # Uniform-Cost Search
│   ├── dls.py          # Depth-Limited Search
│   ├── ids.py          # Iterative Deepening Search
│   ├── gbfs.py         # Greedy Best-First Search
│   ├── astar.py        # A* Search
│   ├── wastar.py       # Weighted A* Search
│   ├── idastar.py      # Iterative Deepening A*
│   └── rbfs.py         # Recursive Best-First Search
├── main.py              # Main runner for all algorithms
├── report.txt           # Detailed experimental results
├── RESULTS.md           # Comprehensive analysis & insights
└── README.md            # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- No external dependencies required (uses only standard library)

### Installation

```bash
git clone https://github.com/yourusername/rubiks-search-suite.git
cd rubiks-search-suite
```

### Running the Solver

```bash
python3 main.py
```

This will:
1. Create a scrambled 2×2×2 cube
2. Run all 10 search algorithms
3. Display progress with logging
4. Generate `report.txt` with detailed results
5. Output performance statistics

### Customizing the Puzzle

Edit `main.py` to change:

```python
# Cube dimensions (1-4 for each dimension)
dimensions = (3, 3, 3)  # 3x3x3 cube

# Scramble moves
scramble_moves = [
    ('x', 0),
    ('y', 1),
    ('z', 2)
]
```

## 📋 Problem Definition

### State Representation

Each cubie stores colors for all 6 faces:

```python
cubie = {
    "U": color,  # Up (White)
    "D": color,  # Down (Yellow)
    "L": color,  # Left (Green)
    "R": color,  # Right (Blue)
    "F": color,  # Front (Red)
    "B": color   # Back (Orange)
}
```

### Move Mechanics

**Only allowed move**: Rotate an entire row along x, y, or z axis

- Movement is a **circular reversal**: `A-B-C-D → D-C-B-A`
- Cubie orientations update based on rotation axis
- Example: `('x', 0)` reverses row at x=0

### Goal State

Each of the 6 external faces must be uniform in color.

## 🧮 Algorithm Implementations

### Blind Search (Uninformed)

1. **BFS**: Level-by-level exploration, guarantees shortest path
2. **DFS**: Depth-first with depth limit, memory efficient
3. **UCS**: Cost-based expansion, optimal with any costs
4. **DLS**: DFS with predetermined depth limit
5. **IDS**: Iteratively increasing depth limits, optimal + memory efficient

### Informed Search (Heuristic-Guided)

6. **GBFS**: Pure heuristic, fast but not optimal
7. **A***: f(n) = g(n) + h(n), optimal with admissible h
8. **Weighted A***: f(n) = g(n) + W×h(n), trades optimality for speed
9. **IDA***: Iterative deepening with f-cost threshold, memory efficient
10. **RBFS**: Recursive best-first with linear memory, optimal

See [RESULTS.md](RESULTS.md) for detailed algorithm analysis.

## 🎓 Heuristic Function

### Face Mismatch Heuristic

```python
h(state) = total_face_mismatches / max_fixes_per_move

where:
- total_face_mismatches = count of non-matching face colors
- max_fixes_per_move = 2 × max(x_dim, y_dim, z_dim)
```

### Properties

- **Admissible**: Never overestimates (h(n) ≤ h*(n))
- **Consistent**: h(n) ≤ cost(n,n') + h(n')
- **Effective**: Enables 75-97% reduction in node expansions

**Proof of Admissibility**: Each move affects at most 2×max_dimension cubies, so dividing total mismatches by this gives a lower bound on required moves.

## 📈 Performance Analysis

### Node Expansion Comparison

```
Blind Search:
  BFS: ████████████░░░░░░░░░░ 116 nodes
  UCS: ████████████░░░░░░░░░░ 116 nodes
  DLS: ████████████████████░░ 492 nodes
  IDS: █████████████████████░ 619 nodes

Informed Search:
  A*:  ███░░░░░░░░░░░░░░░░░░░ 30 nodes (74% reduction!)
  WA*: ███░░░░░░░░░░░░░░░░░░░ 29 nodes
  IDA*:██░░░░░░░░░░░░░░░░░░░░ 25 nodes
  RBFS:██░░░░░░░░░░░░░░░░░░░░ 20 nodes (83% reduction!)
```

### Key Insights

1. **RBFS is most efficient** (20 nodes) - optimal + memory efficient
2. **A* is most practical** (30 nodes) - fast + simple + optimal
3. **GBFS failed** (10,000 nodes) - proves heuristic alone insufficient
4. **Informed >> Blind** - 4-6× fewer node expansions

## 🔬 Experimental Results

Full experimental details in:
- **[report.txt](report.txt)**: Raw data and statistics
- **[RESULTS.md](RESULTS.md)**: Comprehensive analysis and insights

### Test Configuration
- **Cube**: 2×2×2 (8 cubies)
- **Scramble**: 2 moves
- **Optimal Solution**: 4 moves
- **Total Possible Moves**: 6 per state

## 📚 Documentation

Each algorithm file includes detailed documentation:
- Algorithm overview and theory
- Implementation details
- Data structures used
- Time/space complexity
- Advantages and disadvantages
- Use case recommendations

## 🎯 Use Cases & Recommendations

| Scenario | Recommended Algorithm |
|----------|---------------------|
| Need optimal, have memory | **A*** |
| Need optimal, limited memory | **RBFS** or **IDA*** |
| Memory very constrained | **IDA*** |
| Speed critical, near-optimal OK | **Weighted A*** |
| No heuristic available | **IDS** |
| Just need any solution | **DFS** |

## 🧪 Testing & Reproducibility

All results are deterministic and reproducible:
```bash
# Run with same initial state
python3 main.py

# Check output consistency
diff report.txt expected_report.txt
```

## 📖 References

- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
- Korf, R. E. (1985). Depth-first iterative-deepening: An optimal admissible tree search
- Korf, R. E. (1993). Linear-space best-first search

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional heuristics
- Larger cube dimensions
- Visualization tools
- Performance optimizations
- More test cases

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Created as a comprehensive demonstration of classical search algorithms applied to combinatorial puzzles.

## 🙏 Acknowledgments

- Inspired by classic AI textbook problems
- Implements foundational algorithms from AI research
- Educational resource for understanding search strategies

---

**For detailed analysis and insights, see [RESULTS.md](RESULTS.md)**

*Last updated: November 2025*
