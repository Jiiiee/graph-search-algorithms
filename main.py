from src.graph import Graph, astar, bfs, dfs


Point = tuple[float, float]


def zero_heuristic(_node: object, _goal: object) -> float:
    return 0


def manhattan_distance(node: Point, goal: Point) -> float:
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def euclidean_distance(node: Point, goal: Point) -> float:
    x_distance = node[0] - goal[0]
    y_distance = node[1] - goal[1]
    return (x_distance**2 + y_distance**2) ** 0.5


def build_demo_graph() -> Graph:
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    return graph


def build_weighted_demo_graph() -> Graph:
    graph = Graph()
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "D", 1)
    graph.add_edge("A", "D", 5)
    return graph


def build_coordinate_demo_graph() -> Graph:
    graph = Graph()
    graph.add_edge((0, 0), (1, 0), 1)
    graph.add_edge((1, 0), (2, 0), 1)
    graph.add_edge((2, 0), (2, 1), 1)
    graph.add_edge((0, 0), (0, 1), 1)
    graph.add_edge((0, 1), (1, 1), 1)
    graph.add_edge((1, 1), (2, 1), 1)
    return graph


def main() -> None:
    graph = build_demo_graph()
    weighted_graph = build_weighted_demo_graph()
    coordinate_graph = build_coordinate_demo_graph()

    print("BFS from A:", bfs(graph, "A"))
    print("DFS from A:", dfs(graph, "A"))
    print("A* from A to D:", astar(weighted_graph, "A", "D", zero_heuristic))
    print(
        "A* grid path:",
        astar(coordinate_graph, (0, 0), (2, 1), manhattan_distance),
    )


if __name__ == "__main__":
    main()
