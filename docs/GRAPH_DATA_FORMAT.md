# JSON Graph Data Format v0.1

This document defines the first JSON graph data format for the project. The
format is intentionally small: it can describe an undirected weighted graph,
the query a search algorithm should run, and optional expected results for
examples or tests.

## Top-level fields

| Field | Required | Description |
| --- | --- | --- |
| `metadata` | Yes | Format and dataset metadata. |
| `nodes` | Yes | List of graph nodes. |
| `edges` | Yes | List of graph edges. |
| `query` | Yes | Search start and goal nodes, plus optional algorithm hints. |
| `constraints` | No | Optional notes about graph constraints. |
| `expected_result` | No | Optional expected path and cost for examples or tests. |

## Example

```json
{
  "metadata": {
    "format_version": "0.1",
    "name": "warehouse_route",
    "description": "Small weighted route graph for warehouse navigation",
    "directed": false
  },
  "nodes": [
    {"id": "Entrance"},
    {"id": "Aisle-1"},
    {"id": "Packing"}
  ],
  "edges": [
    {"source": "Entrance", "target": "Aisle-1", "weight": 2},
    {"source": "Aisle-1", "target": "Packing", "weight": 3}
  ],
  "query": {
    "start": "Entrance",
    "goal": "Packing",
    "algorithm": "astar",
    "heuristic": "zero"
  },
  "expected_result": {
    "path": ["Entrance", "Aisle-1", "Packing"],
    "cost": 5
  }
}
```

## Field rules

### `metadata`

`metadata` must be an object. `format_version` is required and must be `"0.1"`.
`directed` may be omitted or set to `false`. Directed graphs are not supported
by the current `Graph` implementation.

Recommended metadata fields:

- `format_version`: required string, currently `"0.1"`
- `name`: short dataset name
- `description`: short human-readable description
- `directed`: optional boolean, currently only `false` is supported

### `nodes`

`nodes` must be a list of objects. Each node must have an `id` field, and JSON
graph data v0.1 limits node IDs to strings.

```json
{"id": "A"}
```

Duplicate node IDs are invalid.

### `edges`

`edges` must be a list of objects. Each edge must include `source` and `target`
string IDs that already exist in `nodes`. `weight` is optional and defaults to
`1`.

```json
{"source": "A", "target": "B", "weight": 2.5}
```

Weights must be numbers. Negative weights are rejected by `Graph.add_edge`.
Edges are loaded as undirected edges because the current `Graph` is undirected.

### `query`

`query` must be an object with string `start` and `goal` fields. Both nodes must
exist in `nodes`.

```json
{
  "start": "A",
  "goal": "D",
  "algorithm": "astar",
  "heuristic": "zero"
}
```

`algorithm` and `heuristic` are optional hints for examples and documentation.
The loader does not dispatch algorithms.

### `constraints`

`constraints` is optional. It is reserved for simple notes such as whether
negative weights are allowed. The loader validates only the format rules
documented here and delegates edge weight validation to `Graph`.

### `expected_result`

`expected_result` is optional and can include an expected `path` and `cost`.
It is intended for examples and tests.

## Python loading API

Use `load_graph_from_json(path)` from `src.graph_io`.

```python
from src.graph import astar_with_cost
from src.graph_io import load_graph_from_json


data = load_graph_from_json("examples/graph_data/warehouse_route.json")
path, cost = astar_with_cost(
    data.graph,
    data.query["start"],
    data.query["goal"],
    lambda _node, _goal: 0,
)
```

`load_graph_from_json(path)` returns a `GraphData` dataclass with:

- `graph`: loaded `Graph`
- `metadata`: metadata object
- `query`: query object
- `constraints`: optional constraints object
- `expected_result`: optional expected result object

## Current limitations

- Node IDs are strings only.
- Graphs are undirected only.
- The loader does not run algorithms.
- The loader does not choose or build heuristic functions.
- There is no schema library dependency.
- There is no graph database, CLI, or visualization layer.
