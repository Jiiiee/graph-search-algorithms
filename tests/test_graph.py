import pytest

from main import euclidean_distance, manhattan_distance, zero_heuristic
from src.graph import (
    Graph,
    astar,
    astar_with_cost,
    bfs,
    bfs_path,
    dfs,
    dfs_path,
    dijkstra_with_cost,
)


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


def test_graph_stores_default_and_explicit_edge_weights() -> None:
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C", 2.5)

    assert graph.edge_weight("A", "B") == 1
    assert graph.edge_weight("B", "A") == 1
    assert graph.edge_weight("A", "C") == 2.5
    assert graph.edge_weight("C", "A") == 2.5


def test_graph_rejects_negative_edge_weight() -> None:
    graph = Graph()

    with pytest.raises(ValueError, match="Edge weight must be non-negative"):
        graph.add_edge("A", "B", -1)


def test_bfs_returns_level_order() -> None:
    graph = build_sample_graph()

    assert bfs(graph, "A") == ["A", "B", "C", "D", "E"]


def test_dfs_returns_depth_first_order() -> None:
    graph = build_sample_graph()

    assert dfs(graph, "A") == ["A", "B", "D", "C", "E"]


def test_bfs_path_returns_shortest_path_by_edge_count() -> None:
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("E", "D")

    assert bfs_path(graph, "A", "D") == ["A", "B", "D"]


def test_dfs_path_returns_first_depth_first_path() -> None:
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("E", "D")

    assert dfs_path(graph, "A", "D") == ["A", "B", "D"]


def test_path_search_keeps_bfs_and_dfs_traversal_order_unchanged() -> None:
    graph = build_sample_graph()

    assert bfs(graph, "A") == ["A", "B", "C", "D", "E"]
    assert dfs(graph, "A") == ["A", "B", "D", "C", "E"]


def test_path_search_returns_start_when_start_is_goal() -> None:
    graph = build_sample_graph()

    assert bfs_path(graph, "A", "A") == ["A"]
    assert dfs_path(graph, "A", "A") == ["A"]


def test_path_search_returns_empty_path_when_goal_is_unreachable() -> None:
    graph = build_sample_graph()
    graph.add_node("Z")

    assert bfs_path(graph, "A", "Z") == []
    assert dfs_path(graph, "A", "Z") == []


def test_path_search_raises_for_missing_start_or_goal_node() -> None:
    graph = build_sample_graph()

    with pytest.raises(ValueError, match="Start node does not exist"):
        bfs_path(graph, "Z", "A")

    with pytest.raises(ValueError, match="Start node does not exist"):
        bfs_path(graph, "A", "Z")

    with pytest.raises(ValueError, match="Start node does not exist"):
        dfs_path(graph, "Z", "A")

    with pytest.raises(ValueError, match="Start node does not exist"):
        dfs_path(graph, "A", "Z")


def test_search_raises_for_missing_start_node() -> None:
    graph = build_sample_graph()

    with pytest.raises(ValueError, match="Start node does not exist"):
        bfs(graph, "Z")

    with pytest.raises(ValueError, match="Start node does not exist"):
        dfs(graph, "Z")


def test_astar_returns_path_in_unweighted_graph() -> None:
    graph = build_sample_graph()

    assert astar(graph, "A", "E", lambda _node, _goal: 0) == ["A", "C", "E"]


def test_astar_prefers_lower_total_weight_over_fewer_edges() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "D", 1)
    graph.add_edge("A", "D", 5)

    assert astar(graph, "A", "D", lambda _node, _goal: 0) == ["A", "B", "D"]


def test_astar_path_search_differs_from_bfs_and_dfs_traversal_order() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 1)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "E", 1)
    graph.add_edge("A", "D", 5)

    assert bfs(graph, "A") == ["A", "B", "C", "D", "E"]
    assert dfs(graph, "A") == ["A", "B", "D", "C", "E"]
    assert astar(graph, "A", "D", zero_heuristic) == ["A", "B", "D"]


def test_astar_returns_start_when_start_is_goal() -> None:
    graph = build_sample_graph()

    assert astar(graph, "A", "A", lambda _node, _goal: 0) == ["A"]


def test_astar_returns_empty_path_when_goal_is_unreachable() -> None:
    graph = build_sample_graph()
    graph.add_node("Z")

    assert astar(graph, "A", "Z", lambda _node, _goal: 0) == []


def test_astar_raises_for_missing_start_or_goal_node() -> None:
    graph = build_sample_graph()

    with pytest.raises(ValueError, match="Start node does not exist"):
        astar(graph, "Z", "A", lambda _node, _goal: 0)

    with pytest.raises(ValueError, match="Start node does not exist"):
        astar(graph, "A", "Z", lambda _node, _goal: 0)


def test_zero_heuristic_always_returns_zero() -> None:
    assert zero_heuristic("A", "B") == 0
    assert zero_heuristic((0, 0), (2, 3)) == 0


def test_manhattan_distance_returns_grid_distance() -> None:
    assert manhattan_distance((0, 0), (2, 3)) == 5
    assert manhattan_distance((2, 3), (0, 0)) == 5


def test_euclidean_distance_returns_straight_line_distance() -> None:
    assert euclidean_distance((0, 0), (3, 4)) == 5
    assert euclidean_distance((3, 4), (0, 0)) == 5


def test_astar_accepts_manhattan_distance_for_coordinate_nodes() -> None:
    graph = Graph()
    graph.add_edge((0, 0), (1, 0), 1)
    graph.add_edge((1, 0), (2, 0), 1)
    graph.add_edge((2, 0), (2, 1), 1)
    graph.add_edge((0, 0), (0, 1), 1)
    graph.add_edge((0, 1), (1, 1), 1)
    graph.add_edge((1, 1), (2, 1), 1)

    assert astar(graph, (0, 0), (2, 1), manhattan_distance) == [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
    ]


def test_astar_returns_same_optimal_path_with_zero_and_manhattan_heuristics() -> None:
    graph = Graph()
    graph.add_edge((0, 0), (1, 0), 1)
    graph.add_edge((1, 0), (2, 0), 1)
    graph.add_edge((2, 0), (2, 1), 1)
    graph.add_edge((0, 0), (0, 1), 1)
    graph.add_edge((0, 1), (1, 1), 1)
    graph.add_edge((1, 1), (2, 1), 1)

    expected_path = [(0, 0), (1, 0), (2, 0), (2, 1)]

    assert astar(graph, (0, 0), (2, 1), zero_heuristic) == expected_path
    assert astar(graph, (0, 0), (2, 1), manhattan_distance) == expected_path


def test_astar_with_cost_returns_path_and_total_cost() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 2)
    graph.add_edge("B", "D", 3)
    graph.add_edge("A", "D", 10)

    assert astar_with_cost(graph, "A", "D", zero_heuristic) == (["A", "B", "D"], 5)


def test_astar_with_cost_keeps_astar_path_only_behavior() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 2)
    graph.add_edge("B", "D", 3)
    graph.add_edge("A", "D", 10)

    assert astar(graph, "A", "D", zero_heuristic) == ["A", "B", "D"]


def test_astar_with_cost_returns_zero_cost_when_start_is_goal() -> None:
    graph = build_sample_graph()

    assert astar_with_cost(graph, "A", "A", zero_heuristic) == (["A"], 0)


def test_astar_with_cost_returns_infinite_cost_when_goal_is_unreachable() -> None:
    graph = build_sample_graph()
    graph.add_node("Z")

    assert astar_with_cost(graph, "A", "Z", zero_heuristic) == ([], float("inf"))


def test_astar_with_cost_raises_for_missing_start_or_goal_node() -> None:
    graph = build_sample_graph()

    with pytest.raises(ValueError, match="Start node does not exist"):
        astar_with_cost(graph, "Z", "A", zero_heuristic)

    with pytest.raises(ValueError, match="Start node does not exist"):
        astar_with_cost(graph, "A", "Z", zero_heuristic)


def test_dijkstra_with_cost_returns_lowest_total_cost_path() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 2)
    graph.add_edge("B", "D", 3)
    graph.add_edge("A", "C", 1)
    graph.add_edge("C", "D", 8)
    graph.add_edge("A", "D", 10)

    assert dijkstra_with_cost(graph, "A", "D") == (["A", "B", "D"], 5)


def test_dijkstra_with_cost_prefers_lower_cost_over_fewer_edges() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 1)
    graph.add_edge("C", "D", 1)
    graph.add_edge("A", "D", 10)

    assert dijkstra_with_cost(graph, "A", "D") == (["A", "B", "C", "D"], 3)
    assert bfs_path(graph, "A", "D") == ["A", "D"]


def test_dijkstra_with_cost_supports_zero_weight_edges() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 0)
    graph.add_edge("B", "D", 2)
    graph.add_edge("A", "D", 5)

    assert dijkstra_with_cost(graph, "A", "D") == (["A", "B", "D"], 2)


def test_dijkstra_with_cost_returns_zero_cost_when_start_is_goal() -> None:
    graph = build_sample_graph()

    assert dijkstra_with_cost(graph, "A", "A") == (["A"], 0)


def test_dijkstra_with_cost_returns_infinite_cost_when_goal_is_unreachable() -> None:
    graph = build_sample_graph()
    graph.add_node("Z")

    assert dijkstra_with_cost(graph, "A", "Z") == ([], float("inf"))


def test_dijkstra_with_cost_raises_for_missing_start_or_goal_node() -> None:
    graph = build_sample_graph()

    with pytest.raises(ValueError, match="Start node does not exist"):
        dijkstra_with_cost(graph, "Z", "A")

    with pytest.raises(ValueError, match="Start node does not exist"):
        dijkstra_with_cost(graph, "A", "Z")


def test_dijkstra_with_cost_matches_zero_heuristic_astar_cost() -> None:
    graph = Graph()
    graph.add_edge("A", "B", 2)
    graph.add_edge("B", "D", 3)
    graph.add_edge("A", "D", 10)

    dijkstra_path, dijkstra_cost = dijkstra_with_cost(graph, "A", "D")
    astar_path, astar_cost = astar_with_cost(graph, "A", "D", zero_heuristic)

    assert dijkstra_path == astar_path
    assert dijkstra_cost == astar_cost
