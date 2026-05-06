# Graph Search Algorithms

This project is a small Python practice project for learning graph data
structures and search algorithms through an incremental Codex APP workflow.

## Current MVP

- Minimal undirected weighted `Graph` data structure
- Breadth-first search (`bfs`)
- Depth-first search (`dfs`)
- A* search (`astar`)
- A* search with path cost (`astar_with_cost`)
- Focused tests for graph behavior and traversal order

The implementation intentionally keeps the API small and readable. Edges are
undirected, default to weight `1`, and reject negative weights. A* can return
either a path list or a `(path, cost)` pair, and uses a caller-provided
heuristic function.

## Heuristics

`astar(graph, start, goal, heuristic)` calls `heuristic(current_node, goal_node)`
to estimate the remaining cost from each node to the goal.

- Zero heuristic always returns `0`. It is useful when nodes do not have
  coordinates or when you want A* to behave like Dijkstra's algorithm.
- Manhattan distance works well for grid maps where movement is limited to
  horizontal and vertical steps.
- Euclidean distance works well for coordinate-based maps where straight-line
  distance is a reasonable estimate.

See `docs/HEURISTICS.md` for a short learning guide.

See `docs/ALGORITHM_COMPARISON.md` for a comparison of BFS, DFS, and A*.

## A* example

```python
from src.graph import Graph, astar, astar_with_cost

graph = Graph()
graph.add_edge("A", "B", 2)
graph.add_edge("B", "D", 3)
graph.add_edge("A", "D", 10)

path = astar(graph, "A", "D", lambda node, goal: 0)
path_with_cost = astar_with_cost(graph, "A", "D", lambda node, goal: 0)

print(path)
print(path_with_cost)
```

Expected output:

```text
['A', 'B', 'D']
(['A', 'B', 'D'], 5)
```

When no path exists, `astar_with_cost` returns `([], float("inf"))`.

## Run the demo

```bash
python main.py
# or, if your shell exposes Python as python3:
python3 main.py
```

Expected output:

```text
BFS from A: ['A', 'B', 'C', 'D', 'E']
DFS from A: ['A', 'B', 'D', 'C', 'E']
A* from A to D: ['A', 'B', 'D']
A* grid path: [(0, 0), (1, 0), (2, 0), (2, 1)]
```

## Run tests

```bash
python -m pytest
# or:
pytest
```

## Project layout

```text
.
├── main.py
├── pyproject.toml
├── docs/
│   ├── ALGORITHM_COMPARISON.md
│   └── HEURISTICS.md
├── src/
│   ├── __init__.py
│   └── graph.py
└── tests/
    └── test_graph.py
```
