# graph-search-algorithms 项目状态记录

## 1. 项目名称

graph-search-algorithms

## 2. 当前阶段状态

- 当前阶段：v0.2-astar 冻结状态
- 当前主分支：master
- MVP v0.1 已完成
- A* MVP 已完成
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

## 4. 已验证命令

```bash
python3 main.py
pytest
```

验证结果：

- `python3 main.py` 可以输出 BFS、DFS 和 A* 示例结果
- `pytest` 通过全部 v0.2-astar 测试

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
- 当前工作区应为 clean

## 6. 当前冻结点

v0.2-astar 冻结在 weighted Graph、BFS、DFS、A*、测试、命令行演示和 README 全部完成后的状态。

该冻结点适合作为后续扩展图搜索算法、路径返回能力、图可视化、更多测试用例或项目结构完善的稳定起点。

## 7. 后续任务候选

- 增加有向图支持
- 为 BFS / DFS 增加路径返回能力
- 为 A* 增加路径成本返回能力
- 增加 Dijkstra 算法
- 增加更多边界测试，例如重复边权重更新、非连通图、零权重边、空图
- 添加更多边界测试，例如孤立节点、重复边、空图
- 增加简单图可视化功能
- 清理历史中已被 Git 跟踪的 `.DS_Store`

## 8. 下次恢复项目的建议起点

建议下次从 v0.2-astar 冻结状态开始，先确认是否继续扩展算法能力、路径返回能力或图可视化能力，而不是直接修改代码。

推荐恢复顺序：

1. 确认当前分支是 `master`
2. 确认工作区 clean
3. 查看 tag `v0.2-astar`
4. 阅读当前状态文档
5. 选择下一阶段目标，并单独制定开发计划

## 9. 暂停说明

项目已在 v0.2-astar 阶段暂停。

暂停时不需要继续修改代码、不需要提交新的 commit、不需要推送远程分支。后续恢复时，应先基于当前冻结状态确认目标，再开启新的计划和实现步骤。
