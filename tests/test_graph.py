import pytest

from src.graph import Graph, bfs, dfs


def build_sample_graph() -> Graph:
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    return graph


def test_graph_adds_nodes_and_undirected_edges() -> None:
    graph = Graph()
    graph.add_edge("A", "B")

    assert graph.nodes() == ["A", "B"]
    assert graph.neighbors("A") == ["B"]
    assert graph.neighbors("B") == ["A"]


def test_bfs_returns_level_order() -> None:
    graph = build_sample_graph()

    assert bfs(graph, "A") == ["A", "B", "C", "D", "E"]


def test_dfs_returns_depth_first_order() -> None:
    graph = build_sample_graph()

    assert dfs(graph, "A") == ["A", "B", "D", "C", "E"]


def test_search_raises_for_missing_start_node() -> None:
    graph = build_sample_graph()

    with pytest.raises(ValueError, match="Start node does not exist"):
        bfs(graph, "Z")

    with pytest.raises(ValueError, match="Start node does not exist"):
        dfs(graph, "Z")
