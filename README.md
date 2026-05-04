# Graph Search Algorithms

This project is a small Python practice project for learning graph data
structures and search algorithms through an incremental Codex APP workflow.

## Current MVP

- Minimal undirected `Graph` data structure
- Breadth-first search (`bfs`)
- Depth-first search (`dfs`)
- Focused tests for graph behavior and traversal order

The first version intentionally keeps the implementation small and readable.
A* search is planned as a later extension after the graph and basic traversal
foundation is easy to review.

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
