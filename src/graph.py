import heapq
from collections import deque
from collections.abc import Callable, Hashable


class Graph:
    """A minimal undirected weighted graph backed by an adjacency list."""

    def __init__(self) -> None:
        self._adjacency: dict[Hashable, dict[Hashable, float]] = {}

    def add_node(self, node: Hashable) -> None:
        self._adjacency.setdefault(node, {})

    def add_edge(self, first: Hashable, second: Hashable, weight: float = 1) -> None:
        if weight < 0:
            raise ValueError("Edge weight must be non-negative")

        self.add_node(first)
        self.add_node(second)
        self._adjacency[first][second] = weight
        self._adjacency[second][first] = weight

    def nodes(self) -> list[Hashable]:
        return list(self._adjacency)

    def neighbors(self, node: Hashable) -> list[Hashable]:
        self._ensure_node_exists(node)
        return list(self._adjacency[node])

    def edge_weight(self, first: Hashable, second: Hashable) -> float:
        self._ensure_node_exists(first)
        if second not in self._adjacency[first]:
            raise ValueError(f"Edge does not exist: {first!r} -> {second!r}")
        return self._adjacency[first][second]

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


def bfs_path(graph: Graph, start: Hashable, goal: Hashable) -> list[Hashable]:
    """Return the shortest path by edge count from start to goal."""

    graph._ensure_node_exists(start)
    graph._ensure_node_exists(goal)

    if start == goal:
        return [start]

    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        for neighbor in graph.neighbors(node):
            if neighbor in visited:
                continue

            next_path = [*path, neighbor]
            if neighbor == goal:
                return next_path

            visited.add(neighbor)
            queue.append((neighbor, next_path))

    return []


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


def dfs_path(graph: Graph, start: Hashable, goal: Hashable) -> list[Hashable]:
    """Return the first depth-first path from start to goal."""

    graph._ensure_node_exists(start)
    graph._ensure_node_exists(goal)

    if start == goal:
        return [start]

    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        if node == goal:
            return path

        for neighbor in reversed(graph.neighbors(node)):
            if neighbor not in visited:
                stack.append((neighbor, [*path, neighbor]))

    return []


def astar(
    graph: Graph,
    start: Hashable,
    goal: Hashable,
    heuristic: Callable[[Hashable, Hashable], float],
) -> list[Hashable]:
    """Return the lowest-cost path from start to goal using A* search."""

    graph._ensure_node_exists(start)
    graph._ensure_node_exists(goal)

    if start == goal:
        return [start]

    counter = 0
    open_set = [(heuristic(start, goal), counter, start)]
    came_from: dict[Hashable, Hashable] = {}
    g_score = {start: 0.0}
    closed = set()

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in closed:
            continue

        if current == goal:
            return _reconstruct_path(came_from, current)

        closed.add(current)

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph.edge_weight(current, neighbor)
            if tentative_g_score >= g_score.get(neighbor, float("inf")):
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            counter += 1
            f_score = tentative_g_score + heuristic(neighbor, goal)
            heapq.heappush(open_set, (f_score, counter, neighbor))

    return []


def astar_with_cost(
    graph: Graph,
    start: Hashable,
    goal: Hashable,
    heuristic: Callable[[Hashable, Hashable], float],
) -> tuple[list[Hashable], float]:
    """Return the lowest-cost path and total cost from start to goal."""

    graph._ensure_node_exists(start)
    graph._ensure_node_exists(goal)

    if start == goal:
        return [start], 0

    counter = 0
    open_set = [(heuristic(start, goal), counter, start)]
    came_from: dict[Hashable, Hashable] = {}
    g_score = {start: 0.0}
    closed = set()

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in closed:
            continue

        if current == goal:
            return _reconstruct_path(came_from, current), g_score[current]

        closed.add(current)

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph.edge_weight(current, neighbor)
            if tentative_g_score >= g_score.get(neighbor, float("inf")):
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            counter += 1
            f_score = tentative_g_score + heuristic(neighbor, goal)
            heapq.heappush(open_set, (f_score, counter, neighbor))

    return [], float("inf")


def _reconstruct_path(
    came_from: dict[Hashable, Hashable],
    current: Hashable,
) -> list[Hashable]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
