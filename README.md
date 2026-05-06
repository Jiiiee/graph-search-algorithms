# Graph Search Algorithms

This project is a small Python practice project for learning graph data
structures and search algorithms through an incremental Codex APP workflow.

## Current MVP

- Minimal undirected weighted `Graph` data structure
- Breadth-first search (`bfs`)
- Depth-first search (`dfs`)
- A* search (`astar`)
- Focused tests for graph behavior and traversal order

The implementation intentionally keeps the API small and readable. Edges are
undirected, default to weight `1`, and reject negative weights. A* returns the
path as a list of nodes and uses a caller-provided heuristic function.

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

## A* example

```python
from src.graph import Graph, astar

graph = Graph()
graph.add_edge("A", "B", 1)
graph.add_edge("B", "D", 1)
graph.add_edge("A", "D", 5)

path = astar(graph, "A", "D", lambda node, goal: 0)
print(path)
```

Expected output:

```text
['A', 'B', 'D']
```

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
│   └── HEURISTICS.md
├── src/
│   ├── __init__.py
│   └── graph.py
└── tests/
    └── test_graph.py
```
