import json
from pathlib import Path

import pytest

from main import zero_heuristic
from src.graph import astar_with_cost, bfs_path
from src.graph_io import GraphData, load_graph_from_json


EXAMPLE_DIR = Path("examples/graph_data")


def test_load_graph_from_json_returns_graph_data() -> None:
    data = load_graph_from_json(EXAMPLE_DIR / "warehouse_route.json")

    assert isinstance(data, GraphData)
    assert data.metadata["format_version"] == "0.1"
    assert data.metadata["name"] == "warehouse_route"
    assert data.query["start"] == "Entrance"
    assert data.query["goal"] == "Exit"
    assert data.constraints == {"allow_negative_weights": False}
    assert data.expected_result == {
        "path": ["Entrance", "Aisle-1", "Packing", "Exit"],
        "cost": 7,
    }


def test_load_graph_from_json_builds_nodes_and_undirected_edges() -> None:
    data = load_graph_from_json(EXAMPLE_DIR / "warehouse_route.json")

    assert data.graph.nodes() == ["Entrance", "Aisle-1", "Aisle-2", "Packing", "Exit"]
    assert data.graph.neighbors("Entrance") == ["Aisle-1", "Aisle-2"]
    assert data.graph.neighbors("Packing") == ["Aisle-1", "Aisle-2", "Exit"]


def test_load_graph_from_json_reads_default_and_explicit_weights() -> None:
    learning_data = load_graph_from_json(EXAMPLE_DIR / "learning_path.json")
    warehouse_data = load_graph_from_json(EXAMPLE_DIR / "warehouse_route.json")

    assert learning_data.graph.edge_weight("Python Basics", "Data Structures") == 1
    assert learning_data.graph.edge_weight("Graphs", "A Star") == 2
    assert warehouse_data.graph.edge_weight("Entrance", "Aisle-1") == 2
    assert warehouse_data.graph.edge_weight("Aisle-1", "Entrance") == 2


def test_loaded_query_can_be_used_with_existing_algorithms() -> None:
    data = load_graph_from_json(EXAMPLE_DIR / "warehouse_route.json")

    path, cost = astar_with_cost(
        data.graph,
        data.query["start"],
        data.query["goal"],
        zero_heuristic,
    )

    assert path == data.expected_result["path"]
    assert cost == data.expected_result["cost"]


def test_example_json_files_load_and_support_path_queries() -> None:
    expected_paths = {
        "warehouse_route.json": ["Entrance", "Aisle-1", "Packing", "Exit"],
        "learning_path.json": [
            "Python Basics",
            "Data Structures",
            "Graphs",
            "A Star",
        ],
        "file_dependency.json": [
            "tests/test_graph_io.py",
            "src/graph.py",
            "main.py",
        ],
    }

    for file_name, expected_path in expected_paths.items():
        data = load_graph_from_json(EXAMPLE_DIR / file_name)

        assert bfs_path(data.graph, data.query["start"], data.query["goal"]) == expected_path


def test_load_graph_from_json_raises_for_malformed_json(tmp_path: Path) -> None:
    graph_file = tmp_path / "malformed.json"
    graph_file.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_graph_from_json(graph_file)


@pytest.mark.parametrize("missing_field", ["metadata", "nodes", "edges", "query"])
def test_load_graph_from_json_raises_for_missing_required_fields(
    tmp_path: Path,
    missing_field: str,
) -> None:
    graph_data = {
        "metadata": {"format_version": "0.1", "directed": False},
        "nodes": [{"id": "A"}, {"id": "B"}],
        "edges": [{"source": "A", "target": "B"}],
        "query": {"start": "A", "goal": "B"},
    }
    graph_data.pop(missing_field)
    graph_file = tmp_path / "missing-field.json"
    graph_file.write_text(json.dumps(graph_data), encoding="utf-8")

    with pytest.raises(ValueError, match="Missing or invalid required"):
        load_graph_from_json(graph_file)


def test_load_graph_from_json_rejects_non_string_node_ids(tmp_path: Path) -> None:
    graph_file = tmp_path / "non-string-node.json"
    graph_file.write_text(
        json.dumps(
            {
                "metadata": {"format_version": "0.1", "directed": False},
                "nodes": [{"id": 1}],
                "edges": [],
                "query": {"start": "A", "goal": "A"},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Node id at index 0 must be a string"):
        load_graph_from_json(graph_file)


def test_load_graph_from_json_rejects_edges_with_unknown_nodes(tmp_path: Path) -> None:
    graph_file = tmp_path / "unknown-edge-node.json"
    graph_file.write_text(
        json.dumps(
            {
                "metadata": {"format_version": "0.1", "directed": False},
                "nodes": [{"id": "A"}],
                "edges": [{"source": "A", "target": "B"}],
                "query": {"start": "A", "goal": "A"},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Edge target does not exist"):
        load_graph_from_json(graph_file)


def test_load_graph_from_json_rejects_missing_query_nodes(tmp_path: Path) -> None:
    graph_file = tmp_path / "unknown-query-node.json"
    graph_file.write_text(
        json.dumps(
            {
                "metadata": {"format_version": "0.1", "directed": False},
                "nodes": [{"id": "A"}],
                "edges": [],
                "query": {"start": "A", "goal": "B"},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Query goal does not exist"):
        load_graph_from_json(graph_file)


def test_load_graph_from_json_rejects_directed_graphs(tmp_path: Path) -> None:
    graph_file = tmp_path / "directed.json"
    graph_file.write_text(
        json.dumps(
            {
                "metadata": {"format_version": "0.1", "directed": True},
                "nodes": [{"id": "A"}, {"id": "B"}],
                "edges": [{"source": "A", "target": "B"}],
                "query": {"start": "A", "goal": "B"},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Only undirected graph data is supported"):
        load_graph_from_json(graph_file)
