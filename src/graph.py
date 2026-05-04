from collections import deque
from collections.abc import Hashable


class Graph:
    """A minimal undirected graph backed by an adjacency list."""

    def __init__(self) -> None:
        self._adjacency: dict[Hashable, list[Hashable]] = {}

    def add_node(self, node: Hashable) -> None:
        self._adjacency.setdefault(node, [])

    def add_edge(self, first: Hashable, second: Hashable) -> None:
        self.add_node(first)
        self.add_node(second)
        if second not in self._adjacency[first]:
            self._adjacency[first].append(second)
        if first not in self._adjacency[second]:
            self._adjacency[second].append(first)

    def nodes(self) -> list[Hashable]:
        return list(self._adjacency)

    def neighbors(self, node: Hashable) -> list[Hashable]:
        self._ensure_node_exists(node)
        return list(self._adjacency[node])

    def _ensure_node_exists(self, node: Hashable) -> None:
        if node not in self._adjacency:
            raise ValueError(f"Start node does not exist: {node!r}")


def bfs(graph: Graph, start: Hashable) -> list[Hashable]:
    """Return nodes in breadth-first traversal order."""

    graph._ensure_node_exists(start)

    visited = {start}
    order = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def dfs(graph: Graph, start: Hashable) -> list[Hashable]:
    """Return nodes in depth-first traversal order."""

    graph._ensure_node_exists(start)

    visited = set()
    order = []
    stack = [start]

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        for neighbor in reversed(graph.neighbors(node)):
            if neighbor not in visited:
                stack.append(neighbor)

    return order
