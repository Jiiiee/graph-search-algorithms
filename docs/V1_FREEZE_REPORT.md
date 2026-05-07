# v1.0 Freeze Report

## Freeze Target

The v1.0 freeze target is `v1.0-graph-search-base`.

This release freezes the current graph-search learning base: a minimal
undirected weighted graph, core traversal and path-search algorithms, JSON graph
data loading, and test-only NetworkX verification.

From v1.0 onward, `pyproject.toml` `version` is the project release version.
The planned freeze tag is `v1.0-graph-search-base`.

## Public API

The v1.0 public API is:

- `Graph`
- `Graph.add_node(node)`
- `Graph.add_edge(first, second, weight=1)`
- `Graph.nodes()`
- `Graph.neighbors(node)`
- `Graph.edge_weight(first, second)`
- `bfs(graph, start)`
- `dfs(graph, start)`
- `bfs_path(graph, start, goal)`
- `dfs_path(graph, start, goal)`
- `dijkstra_with_cost(graph, start, goal)`
- `astar(graph, start, goal, heuristic)`
- `astar_with_cost(graph, start, goal, heuristic)`
- `GraphData`
- `load_graph_from_json(path)`

Demo helper functions in `main.py` and test helper functions are not part of
the frozen public API.

## JSON v0.1 Input Format

JSON graph data format v0.1 is the frozen base input format for v1.0.

Supported fields:

- Required: `metadata`, `nodes`, `edges`, `query`
- Optional: `constraints`, `expected_result`

Current boundaries:

- `metadata.format_version` must be `"0.1"`.
- Graph data is undirected only.
- Node IDs must be strings.
- Edges must reference existing node IDs.
- Edge `weight` is optional and defaults to `1`.
- Edge weights must be numbers.
- Negative weights are rejected through `Graph.add_edge`.
- `query.start` and `query.goal` must be existing string node IDs.
- `query.algorithm` and `query.heuristic` are documentation/example hints only.
- The loader does not dispatch algorithms or build heuristic functions.

## Verification Oracle

NetworkX is used only in tests as an independent verification oracle.

Current oracle coverage:

- `astar_with_cost` weighted shortest path cost with zero heuristic
- `dijkstra_with_cost` weighted shortest path cost
- `bfs_path` unweighted shortest path edge count
- no-path behavior against `NetworkXNoPath`
- example JSON graph data where the query maps to an oracle rule

The oracle does not become runtime logic and is not part of `src`.

## Test Results

Latest v1.0 freeze validation:

```text
conda run -n graph-env python -m pytest -q
56 passed
```

## Not Supported In v1.0

- Directed graph support
- Negative weights
- CLI
- Visualization
- Benchmark or performance test system
- Graph database integration
- Hypothesis or hypothesis-networkx

## v1.1 Candidates

- Directed graph support
- JSON format evolution for coordinates, labels, node attributes, or edge attributes
- More example graph data for teaching and regression tests
- Dijkstra-specific JSON examples
- Dijkstra and A* visit counts or expansion-order statistics for teaching
- More heuristic examples
- Wider NetworkX oracle coverage
- Generated graph testing with Hypothesis or hypothesis-networkx
- Optional visualization or CLI after the base API remains stable

## Tag Plan

After this freeze report and v1.0 release hygiene are merged to `master`, create
and push:

```text
v1.0-graph-search-base
```
