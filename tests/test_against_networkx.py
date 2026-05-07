from collections.abc import Hashable
from pathlib import Path

import networkx as nx
import pytest

from main import zero_heuristic
from src.graph import Graph, astar_with_cost, bfs_path
from src.graph_io import load_graph_from_json


EXAMPLE_DIR = Path("examples/graph_data")


def to_networkx_graph(graph: Graph) -> nx.Graph:
    oracle_graph = nx.Graph()

    for node in graph.nodes():
        oracle_graph.add_node(node)

    added_edges: set[frozenset[Hashable]] = set()
    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            edge_key = frozenset((node, neighbor))
            if edge_key in added_edges:
                continue

            oracle_graph.add_edge(
                node,
                neighbor,
                weight=graph.edge_weight(node, neighbor),
            )
            added_edges.add(edge_key)

    return oracle_graph


def path_cost(graph: Graph, path: list[Hashable]) -> float:
    return sum(
        graph.edge_weight(first, second)
        for first, second in zip(path, path[1:])
    )


def assert_valid_path(
    graph: Graph,
    path: list[Hashable],
    start: Hashable,
    goal: Hashable,
) -> None:
    assert path
    assert path[0] == start
    assert path[-1] == goal

    for first, second in zip(path, path[1:]):
        assert second in graph.neighbors(first)


def test_astar_with_cost_matches_networkx_weighted_shortest_path_cost() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 2)
    graph.add_edge("B", "D", 3)
    graph.add_edge("A", "C", 1)
    graph.add_edge("C", "D", 8)
    graph.add_edge("A", "D", 10)
    oracle_graph = to_networkx_graph(graph)

    path, cost = astar_with_cost(graph, "A", "D", zero_heuristic)
    oracle_cost = nx.shortest_path_length(
        oracle_graph,
        "A",
        "D",
        weight="weight",
    )

    assert_valid_path(graph, path, "A", "D")
    assert cost == oracle_cost
    assert path_cost(graph, path) == oracle_cost


def test_bfs_path_matches_networkx_shortest_path_edge_count() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 10)
    graph.add_edge("B", "D", 10)
    graph.add_edge("A", "C", 1)
    graph.add_edge("C", "E", 1)
    graph.add_edge("E", "D", 1)
    oracle_graph = to_networkx_graph(graph)

    path = bfs_path(graph, "A", "D")
    oracle_edge_count = nx.shortest_path_length(oracle_graph, "A", "D")

    assert_valid_path(graph, path, "A", "D")
    assert len(path) - 1 == oracle_edge_count


def test_no_path_results_match_networkx_no_path() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 2)
    graph.add_node("Z")
    oracle_graph = to_networkx_graph(graph)

    assert bfs_path(graph, "A", "Z") == []
    assert astar_with_cost(graph, "A", "Z", zero_heuristic) == ([], float("inf"))
    with pytest.raises(nx.NetworkXNoPath):
        nx.shortest_path(oracle_graph, "A", "Z")
    with pytest.raises(nx.NetworkXNoPath):
        nx.shortest_path_length(oracle_graph, "A", "Z", weight="weight")


@pytest.mark.parametrize(
    "file_name",
    [
        "warehouse_route.json",
        "learning_path.json",
        "file_dependency.json",
    ],
)
def test_example_graph_data_paths_are_valid_against_networkx(file_name: str) -> None:
    data = load_graph_from_json(EXAMPLE_DIR / file_name)
    graph = data.graph
    oracle_graph = to_networkx_graph(graph)
    start = data.query["start"]
    goal = data.query["goal"]
    expected_result = data.expected_result or {}
    algorithm = data.query.get("algorithm")

    if algorithm == "astar":
        path, cost = astar_with_cost(graph, start, goal, zero_heuristic)
        oracle_path = nx.shortest_path(
            oracle_graph,
            start,
            goal,
            weight="weight",
        )
        oracle_cost = nx.shortest_path_length(
            oracle_graph,
            start,
            goal,
            weight="weight",
        )

        assert_valid_path(graph, path, start, goal)
        assert_valid_path(graph, oracle_path, start, goal)
        assert cost == oracle_cost
        assert path_cost(graph, path) == oracle_cost
        assert expected_result.get("cost") == oracle_cost
        return

    if algorithm == "bfs_path":
        path = bfs_path(graph, start, goal)
        oracle_edge_count = nx.shortest_path_length(oracle_graph, start, goal)

        assert_valid_path(graph, path, start, goal)
        assert len(path) - 1 == oracle_edge_count
        assert path_cost(graph, path) == expected_result.get("cost")
        return

    assert nx.has_path(oracle_graph, start, goal)
    expected_path = expected_result["path"]
    assert_valid_path(graph, expected_path, start, goal)
    assert path_cost(graph, expected_path) == expected_result.get("cost")
