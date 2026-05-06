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
├── src/
│   ├── __init__.py
│   └── graph.py
└── tests/
    └── test_graph.py
```
