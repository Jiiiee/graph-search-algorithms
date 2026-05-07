import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from src.graph import Graph


@dataclass(frozen=True)
class GraphData:
    """Graph data loaded from a JSON graph data file."""

    graph: Graph
    metadata: Dict[str, Any]
    query: Dict[str, Any]
    constraints: Optional[Dict[str, Any]] = None
    expected_result: Optional[Dict[str, Any]] = None


def load_graph_from_json(path: Union[str, Path]) -> GraphData:
    """Load a Graph and query metadata from a JSON graph data file."""

    with Path(path).open(encoding="utf-8") as file:
        raw_data = json.load(file)

    if not isinstance(raw_data, dict):
        raise ValueError("Graph data file must contain a JSON object")

    metadata = _required_mapping(raw_data, "metadata")
    if metadata.get("format_version") != "0.1":
        raise ValueError("Unsupported graph data format version")
    if metadata.get("directed", False) is not False:
        raise ValueError("Only undirected graph data is supported")

    node_items = _required_list(raw_data, "nodes")
    edge_items = _required_list(raw_data, "edges")
    query = _required_mapping(raw_data, "query")
    constraints = _optional_mapping(raw_data, "constraints")
    expected_result = _optional_mapping(raw_data, "expected_result")

    graph = Graph()
    node_ids = _load_nodes(graph, node_items)
    _load_edges(graph, edge_items, node_ids)
    _validate_query(query, node_ids)

    return GraphData(
        graph=graph,
        metadata=metadata,
        query=query,
        constraints=constraints,
        expected_result=expected_result,
    )


def _load_nodes(graph: Graph, node_items: List[Any]) -> Set[str]:
    node_ids: Set[str] = set()

    for index, node_item in enumerate(node_items):
        if not isinstance(node_item, dict):
            raise ValueError(f"Node at index {index} must be an object")

        node_id = node_item.get("id")
        if not isinstance(node_id, str):
            raise ValueError(f"Node id at index {index} must be a string")
        if node_id in node_ids:
            raise ValueError(f"Duplicate node id: {node_id!r}")

        node_ids.add(node_id)
        graph.add_node(node_id)

    return node_ids


def _load_edges(graph: Graph, edge_items: List[Any], node_ids: Set[str]) -> None:
    for index, edge_item in enumerate(edge_items):
        if not isinstance(edge_item, dict):
            raise ValueError(f"Edge at index {index} must be an object")

        source = edge_item.get("source")
        target = edge_item.get("target")
        if not isinstance(source, str):
            raise ValueError(f"Edge source at index {index} must be a string")
        if not isinstance(target, str):
            raise ValueError(f"Edge target at index {index} must be a string")
        if source not in node_ids:
            raise ValueError(f"Edge source does not exist: {source!r}")
        if target not in node_ids:
            raise ValueError(f"Edge target does not exist: {target!r}")

        weight = edge_item.get("weight", 1)
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise ValueError(f"Edge weight at index {index} must be a number")

        graph.add_edge(source, target, weight)


def _validate_query(query: Dict[str, Any], node_ids: Set[str]) -> None:
    start = query.get("start")
    goal = query.get("goal")

    if not isinstance(start, str):
        raise ValueError("Query start must be a string")
    if not isinstance(goal, str):
        raise ValueError("Query goal must be a string")
    if start not in node_ids:
        raise ValueError(f"Query start does not exist: {start!r}")
    if goal not in node_ids:
        raise ValueError(f"Query goal does not exist: {goal!r}")


def _required_mapping(data: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"Missing or invalid required object: {key}")
    return value


def _optional_mapping(data: Dict[str, Any], key: str) -> Optional[Dict[str, Any]]:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"Invalid optional object: {key}")
    return value


def _required_list(data: Dict[str, Any], key: str) -> List[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"Missing or invalid required list: {key}")
    return value
