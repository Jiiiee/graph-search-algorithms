# Dijkstra Lowest-Cost Path

Dijkstra's algorithm finds the lowest-cost path from a start node to a goal node
in a graph with non-negative edge weights.

In this project, `dijkstra_with_cost(graph, start, goal)` works with the current
undirected weighted `Graph` type and returns both the path and the total cost.

## API

```python
from src.graph import Graph, dijkstra_with_cost

graph = Graph()
graph.add_edge("A", "B", 2)
graph.add_edge("B", "D", 3)
graph.add_edge("A", "D", 10)

path, cost = dijkstra_with_cost(graph, "A", "D")
```

Expected result:

```python
(["A", "B", "D"], 5)
```

## Return Rules

- If a path exists, return `(path, total_cost)`.
- If `start == goal`, return `([start], 0)`.
- If no path exists, return `([], float("inf"))`.
- If the start or goal node does not exist, raise `ValueError`.

## Weight Rules

Dijkstra requires non-negative edge weights. The current `Graph.add_edge`
method already rejects negative weights, so `dijkstra_with_cost` relies on the
same graph-level validation.

Zero-weight edges are allowed.

## Relationship To BFS And A*

BFS, Dijkstra, and A* form a useful learning sequence:

- `bfs_path` finds the shortest path by edge count and ignores weights.
- `dijkstra_with_cost` finds the lowest-cost path using real edge weights.
- `astar_with_cost` combines real edge weights with a heuristic estimate toward
  the goal.

When A* uses a zero heuristic, it has no target-direction estimate and should
return the same lowest-cost result as Dijkstra for non-negative weighted graphs.

## Current Boundaries

- Graphs are undirected.
- Edge weights must be non-negative.
- The function returns only the final path and total cost.
- It does not return visited-node counts or expansion order.
- It does not add CLI, visualization, benchmark, or graph database behavior.
