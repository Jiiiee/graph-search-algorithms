# Verification Oracle

This project uses a small verification oracle layer to check the current graph
search algorithms against an independent, mature graph library.

## Purpose

The oracle is a test-only safety layer. It helps catch regressions by comparing
the project's own results with NetworkX shortest path behavior.

NetworkX is not part of the runtime graph API. The implementation in `src/`
remains the source code being tested.

## Boundaries

- NetworkX is used only by tests.
- The existing `Graph`, BFS, DFS, `bfs_path`, `dfs_path`, A*, and
  `astar_with_cost` return values are unchanged.
- Dijkstra is verified as an additional test target through
  `dijkstra_with_cost`.
- The oracle layer does not add a CLI, visualization, benchmark, performance
  test system, or graph database integration.
- DFS path order is not treated as a NetworkX-compatible contract because this
  project returns the first path found using its current DFS neighbor order.

## Verification Rules

Tests convert the project's `Graph` into a `networkx.Graph` by copying all
nodes and undirected weighted edges.

For `astar_with_cost`, tests use a zero heuristic and compare the returned cost
with `networkx.shortest_path_length(..., weight="weight")`. The returned path is
also checked for valid endpoints and valid adjacent edges.

For `dijkstra_with_cost`, tests compare the returned cost with
`networkx.shortest_path_length(..., weight="weight")`. Tests also ask NetworkX
for a weighted shortest path, but they do not require the project's returned
path to be identical because multiple equal-cost shortest paths may exist.
Instead, the project path is checked for valid endpoints, valid adjacent edges,
and matching total cost.

For `bfs_path`, tests compare the returned path length in edges with
`networkx.shortest_path_length(...)` without weights. This avoids overfitting to
one specific path when multiple shortest paths exist.

For no-path scenarios, tests assert that project functions return their current
no-path values while NetworkX raises `NetworkXNoPath`.

Example JSON graph data is also loaded and checked where its query maps cleanly
to a NetworkX oracle rule.

## Future Candidates

Hypothesis and hypothesis-networkx may be considered later for generated graph
cases. They are intentionally not introduced in this phase.
