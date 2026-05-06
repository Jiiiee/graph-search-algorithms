from src.graph import Graph, astar, bfs, dfs


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


def main() -> None:
    graph = build_demo_graph()
    weighted_graph = build_weighted_demo_graph()

    print("BFS from A:", bfs(graph, "A"))
    print("DFS from A:", dfs(graph, "A"))
    print("A* from A to D:", astar(weighted_graph, "A", "D", lambda _node, _goal: 0))


if __name__ == "__main__":
    main()
