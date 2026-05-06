# A* Heuristic 学习笔记

`astar(graph, start, goal, heuristic)` 使用调用方传入的 `heuristic`
函数估算当前节点到目标节点的剩余成本。函数签名应接收当前节点和目标节点，
并返回一个数值：

```python
heuristic(current_node, goal_node) -> float
```

## Zero heuristic

Zero heuristic 始终返回 `0`。

```python
def zero_heuristic(_node, _goal):
    return 0
```

适用场景：

- 节点没有坐标信息。
- 只想根据真实边权搜索最短路径。
- 需要一个最保守、最容易理解的 A* 示例。

当 heuristic 永远为 `0` 时，A* 的行为接近 Dijkstra 算法。

## Manhattan distance

Manhattan distance 计算两个坐标点横向距离和纵向距离之和。

```python
def manhattan_distance(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
```

适用场景：

- 节点是 `(x, y)` 坐标。
- 移动方式限制为上下左右四个方向。
- 网格地图中不允许斜向移动。

## Euclidean distance

Euclidean distance 计算两个坐标点之间的直线距离。

```python
def euclidean_distance(node, goal):
    x_distance = node[0] - goal[0]
    y_distance = node[1] - goal[1]
    return (x_distance**2 + y_distance**2) ** 0.5
```

适用场景：

- 节点是 `(x, y)` 坐标。
- 直线距离是合理的剩余成本估计。
- 地图或问题允许任意方向移动，或需要一个几何距离近似。

## 注意事项

- 当前项目不会自动保存坐标；坐标节点只是普通的 hashable tuple。
- Heuristic 不应高估真实剩余成本，否则 A* 不一定返回最优路径。
- 本轮 heuristic 函数是学习示例，不是 `src.graph` 的正式 API。
