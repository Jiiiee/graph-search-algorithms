from src.graph import Graph, bfs, dfs


def build_demo_graph() -> Graph:
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    return graph


def main() -> None:
    graph = build_demo_graph()

    print("BFS from A:", bfs(graph, "A"))
    print("DFS from A:", dfs(graph, "A"))


if __name__ == "__main__":
    main()
