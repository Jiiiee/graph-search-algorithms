# graph-search-algorithms 项目状态记录

## 1. 项目名称

graph-search-algorithms

## 2. 当前阶段状态

- 当前阶段：v0.6-path-variants 冻结状态
- 当前主分支：master
- MVP v0.1 已完成
- A* MVP 已完成
- Heuristic 学习示例已完成
- BFS / DFS / A* 算法对比文档已完成
- A* path cost support 已完成
- BFS / DFS path search variants 已完成
- 当前工作区应为 clean

## 3. 已完成内容

### v0.1-mvp

- 建立了基础无向图数据结构 `Graph`
- 实现了广度优先搜索 `bfs`
- 实现了深度优先搜索 `dfs`
- 添加了最小 pytest 测试
- 添加了最小命令行演示入口
- 添加了 pytest 基础配置
- 更新了项目 README，记录运行和测试方式

### v0.2-astar

- 将 `Graph` 扩展为支持边权重的 weighted Graph
- 保持 `add_node`、`add_edge`、`neighbors`、`nodes`、`bfs`、`dfs` 的公开接口兼容
- 新增 `edge_weight(first, second)`，用于读取无向边权重
- 新增 A* 搜索函数 `astar(graph, start, goal, heuristic)`
- 新增 A* pytest 测试，覆盖路径返回、加权路径选择、无路径、缺失节点和起终点相同等场景
- 扩展 `main.py`，增加 A* 命令行演示
- 更新 README，记录 weighted Graph 和 A* 的用法

### v0.3-heuristics

- 新增 `zero_heuristic` 示例函数，说明 A* 在零启发式下接近 Dijkstra 的搜索方式
- 新增 `manhattan_distance` 示例函数，用于四方向网格坐标场景
- 新增 `euclidean_distance` 示例函数，用于平面坐标直线距离估计场景
- 扩展 `main.py`，增加坐标图 A* demo
- 新增 heuristic pytest 测试，覆盖三种 heuristic 的数值结果和坐标图 A* 调用
- 新增 `docs/HEURISTICS.md`，记录 heuristic 学习说明、适用场景和注意事项
- 更新 README，补充 heuristic 使用方式和 demo 输出

### v0.4-comparison

- 新增 `docs/ALGORITHM_COMPARISON.md`，系统记录 BFS、DFS、A* 的算法对比
- 补充 BFS / DFS / A* 的当前功能边界对比，明确遍历函数和路径搜索函数的区别
- 补充三种算法的适用场景对比
- 补充三种算法的主要优缺点说明
- 补充当前 A* 优化评估，明确本阶段优先补文档和测试，不重构 `Graph` 或 `astar`
- 更新 README，增加 algorithm comparison 文档入口
- 新增 algorithm comparison tests，验证 BFS / DFS 遍历与 A* 路径搜索的差异，以及 zero heuristic 与 Manhattan heuristic 在简单坐标图上的一致最优路径

### v0.5-path-cost

- 新增 `astar_with_cost(graph, start, goal, heuristic)`，在不改变 `astar()` 旧行为的前提下返回路径和路径总成本
- 支持找到路径时返回 `(path, total_cost)`
- 支持无路径时返回 `([], float("inf"))`
- 支持 `start == goal` 时返回 `([start], 0)`
- 保持起点或终点不存在时与 `astar()` 一致，抛出 `ValueError`
- 新增相关 pytest 测试，覆盖 path + cost、旧 `astar()` 兼容性、起终点相同、无路径和缺失节点场景
- 更新 README，说明 `astar()` 返回 path only，`astar_with_cost()` 返回 path + cost
- 更新 `docs/ALGORITHM_COMPARISON.md`，记录 A* 路径成本能力和后续优化方向

### v0.6-path-variants

- 新增 `bfs_path(graph, start, goal)`，在不改变 `bfs()` 遍历行为的前提下返回从起点到目标的路径
- 新增 `dfs_path(graph, start, goal)`，在不改变 `dfs()` 遍历行为的前提下返回从起点到目标的路径
- `bfs_path` 返回最少边数路径，不考虑边权重
- `dfs_path` 返回按当前 DFS 邻居顺序找到的第一条深度优先路径，不考虑边权重
- 支持无路径时返回 `[]`
- 支持 `start == goal` 时返回 `[start]`
- 保持起点或终点不存在时抛出 `ValueError`
- 新增相关 pytest 测试，覆盖 BFS 最少边数路径、DFS 第一条深度优先路径、旧 `bfs()` / `dfs()` 兼容性、起终点相同、无路径和缺失节点场景
- 更新 README，说明 traversal API 和 path search variants 的区别
- 更新 `docs/ALGORITHM_COMPARISON.md`，记录 BFS / DFS path variants 的功能边界、适用场景和限制

## 4. 已验证命令

```bash
python3 main.py
pytest
```

验证结果：

- `python3 main.py` 可以输出 BFS、DFS、A* 和坐标图 A* 示例结果
- `pytest` 通过全部 v0.6-path-variants 测试，当前结果为 28 passed

## 5. Git / GitHub 状态

- 当前主分支：master
- PR #1 已合并
- tag 已创建：v0.1-mvp
- 本地 `codex-graph` 分支已删除
- 远程 `codex-graph` 分支已删除
- PR #2 已合并
- tag 已创建：v0.2-astar
- 本地 `astar-mvp` 分支已删除
- 远程 `astar-mvp` 分支已删除
- PR #3 已合并
- tag 已创建：v0.3-heuristics
- 本地 `heuristic-examples` 分支已删除
- 远程 `heuristic-examples` 分支已删除
- PR #4 已合并
- tag 已创建：v0.4-comparison
- 本地 `algorithm-comparison` 分支已删除
- 远程 `algorithm-comparison` 分支已删除
- PR #5 已合并
- tag 已创建：v0.5-path-cost
- 本地 `astar-path-cost` 分支已删除
- 远程 `astar-path-cost` 分支已删除
- PR #6 已合并
- tag 已创建：v0.6-path-variants
- 本地 `path-search-variants` 分支已删除
- 远程 `path-search-variants` 分支已删除
- 当前工作区应为 clean

## 6. 当前冻结点

v0.6-path-variants 冻结在 weighted Graph、BFS、DFS、BFS / DFS path search variants、A*、A* path cost support、heuristic 学习示例、算法对比文档、测试、命令行演示、README、`docs/HEURISTICS.md` 和 `docs/ALGORITHM_COMPARISON.md` 全部完成后的状态。

该冻结点适合作为后续扩展图搜索算法、有向图能力、更多 heuristic 示例、A* 教学统计、图可视化、更多测试用例或项目结构完善的稳定起点。

## 7. 后续任务候选

- 增加有向图支持
- 为 A* 增加访问节点数量或扩展顺序统计，用于教学对比
- 增加 Dijkstra 算法
- 增加更多 heuristic 示例，例如 Chebyshev distance 或自定义业务成本估计
- 增加更多边界测试，例如重复边权重更新、非连通图、零权重边、孤立节点、空图
- 增加简单图可视化功能
- 清理历史中已被 Git 跟踪的 `.DS_Store`

## 8. 下次恢复项目的建议起点

建议下次从 v0.6-path-variants 冻结状态开始，先确认是否继续扩展算法能力、有向图能力、A* 教学统计、heuristic 示例或图可视化能力，而不是直接修改代码。

推荐恢复顺序：

1. 确认当前分支是 `master`
2. 确认工作区 clean
3. 查看 tag `v0.6-path-variants`
4. 阅读当前状态文档
5. 选择下一阶段目标，并单独制定开发计划

## 9. 暂停说明

项目已在 v0.6-path-variants 阶段暂停。

暂停时不需要继续修改代码、不需要提交新的 commit、不需要推送远程分支。后续恢复时，应先基于当前冻结状态确认目标，再开启新的计划和实现步骤。
