# BFS、DFS、A* 算法对比

本文记录当前项目中 BFS、DFS、A* 的功能边界、适用场景和 A* 优化评估。

## 当前功能边界

| 算法 | 当前函数 | 返回值 | 是否使用 goal | 是否使用边权重 | 是否使用 heuristic |
| --- | --- | --- | --- | --- | --- |
| BFS | `bfs(graph, start)` | 从起点开始的遍历顺序 | 否 | 否 | 否 |
| BFS path | `bfs_path(graph, start, goal)` | 从起点到目标的最少边数路径 | 是 | 否 | 否 |
| DFS | `dfs(graph, start)` | 从起点开始的遍历顺序 | 否 | 否 | 否 |
| DFS path | `dfs_path(graph, start, goal)` | 按 DFS 顺序找到的第一条路径 | 是 | 否 | 否 |
| A* | `astar(graph, start, goal, heuristic)` | 从起点到目标的路径列表 | 是 | 是 | 是 |
| A* with cost | `astar_with_cost(graph, start, goal, heuristic)` | 路径列表和路径总成本 | 是 | 是 | 是 |

当前 BFS 和 DFS 是遍历函数，返回访问顺序。需要路径时使用 `bfs_path` 或 `dfs_path`：`bfs_path` 返回最少边数路径，`dfs_path` 返回按当前 DFS 邻居顺序找到的第一条路径。它们都不考虑边权重。

当前 A* 是路径搜索函数。它会读取 weighted Graph 中的边权重，并通过调用方传入的 `heuristic(current_node, goal_node)` 估算剩余成本。`astar` 保持只返回路径列表；`astar_with_cost` 返回 `(path, cost)`，无路径时返回 `([], float("inf"))`。

## 适用场景

| 算法 | 适合场景 | 主要优点 | 主要限制 |
| --- | --- | --- | --- |
| BFS | 无权图层级遍历、教学中理解队列和逐层扩展 | 顺序稳定，容易理解；`bfs_path` 可返回最少边数路径 | 不考虑权重 |
| DFS | 探索连通结构、理解栈、递归和回溯思想 | 实现紧凑，适合深度优先探索；`dfs_path` 可返回第一条深度优先路径 | 不保证最短路径；不考虑权重 |
| A* | 带权图目标路径搜索，尤其是有合理 heuristic 的坐标图或地图 | 能结合真实成本和估计成本，目标导向更强；可通过 `astar_with_cost` 获取路径总成本 | 依赖 heuristic 质量；当前不返回访问统计 |

## 当前 A* 优化评估

当前 A* 实现适合学习型 MVP：

- 使用 `heapq` 维护 open set。
- 使用 `g_score` 记录从起点到当前节点的真实成本。
- 使用 `came_from` 重建路径。
- 使用 closed set 避免重复扩展已处理节点。
- 使用 counter 作为 heap tie-breaker，避免节点对象不可比较时出错。
- 通过 `astar_with_cost` 支持返回路径总成本，同时保持 `astar` 的旧返回值不变。

本轮不建议重构 `astar`。更合适的优化顺序是：

1. 先补文档，明确 BFS / DFS 遍历函数和 path variants 的区别。
2. 再补测试，验证 A* 在带权图中按低总成本选择路径。
3. 后续如果确实需要更多能力，再考虑继续扩展访问统计或独立 Dijkstra API。

## 后续可选优化

- 为 A* 增加访问节点数量或扩展顺序统计，用于教学对比。
- 新增独立 Dijkstra API，明确 zero heuristic A* 与 Dijkstra 的关系。
- 在项目规模变大后，再考虑轻量 benchmark；当前不需要复杂 benchmark 系统。

## 本轮不做

- 不修改 `Graph`。
- 不重构 `astar`。
- 不修改 `bfs` / `dfs` 的 traversal-order API。
- 不让 `bfs_path` / `dfs_path` 考虑边权重。
- 不新增 Dijkstra 函数。
- 不新增可视化或 benchmark 系统。
