# LangGraph State 与 Checkpoint 机制

## 三个核心概念

| 概念 | 类比 | 说明 |
|------|------|------|
| **State** | 共享白板 | 所有节点都能读写的共享数据 |
| **Node（节点）** | 一个人 | 负责一件事（搜索、分析、生成报告） |
| **Edge（边）** | 传递规则 | 节点间的执行顺序和条件判断 |

```
State（数据）→ Node（处理逻辑）→ Graph（执行流程）
```

## Annotated 与状态合并

`Annotated` 是 Python 3.9+ 内置语法，给类型加元数据：

```python
from typing import Annotated
from operator import add

# 普通字段：节点返回新值 → 覆盖旧的
iteration: int = 0

# Annotated + add：节点返回新值 → 追加到旧列表
search_results: Annotated[list[SearchResult], add] = []
```

当节点返回 `{"search_results": [结果1]}` 时：
- 普通字段：旧值被新值覆盖
- Annotated + add：旧列表 + 新列表 = 追加（`add` 就是 `+` 运算符）

也可以自定义合并函数：

```python
def keep_max(old, new):
    return max(old, new)

score: Annotated[int, keep_max] = 0  # 永远保留最大值
```

## Checkpoint 工作机制

### 存储配置

```python
from langgraph.checkpoint.memory import MemorySaver

graph = builder.compile(checkpointer=MemorySaver())
```

| Checkpointer | 存储位置 | 用途 |
|---|---|---|
| `MemorySaver` | 内存 | 开发调试 |
| `SqliteSaver` | SQLite 文件 | 轻量持久化 |
| `PostgresSaver` | PostgreSQL | 生产环境 |

### 自动存快照

每次节点执行完，LangGraph 自动：
1. 读取当前 checkpoint
2. 执行节点函数，拿到部分更新
3. 用 Annotated 规则合并到完整 state
4. 存新 checkpoint（parent_id 指向上一步）

```
cp_0（初始）→ cp_1（planner后）→ cp_2（researcher后）→ cp_3（结束）
```

### 存储结构

```
thread_id | checkpoint_id | parent_id | state (JSON)
user-123  | cp_0          | NULL      | {"question": "量子计算", ...}
user-123  | cp_1          | cp_0      | {"question": "量子计算", "sub_questions": [...]}
user-123  | cp_2          | cp_1      | {"question": "量子计算", "search_results": [...]}
```

`parent_id` 串成链表，支持回溯到任意节点。

### 核心操作

```python
config = {"configurable": {"thread_id": "user-123"}}

# 读取当前状态
state = graph.get_state(config)
# state.values  → 当前完整 state 数据
# state.next    → 下一步要执行的节点名

# 读取完整历史
history = list(graph.get_state_history(config))

# 回滚到某一步，修改 state 后重新执行
graph.update_state(config, {"sub_questions": ["新问题"]}, as_node="planner")
# 原链：cp_0 → cp_1 → cp_2 → cp_3
# 新链：cp_0 → cp_1 → cp_4 → cp_5（从 cp_1 分叉）

# 暂停：在某个节点前插入断点
graph = builder.compile(checkpointer=checkpointer, interrupt_before=["analyst"])

# 恢复：从断点继续
graph.invoke(None, config)
```

### 底层触发逻辑（伪代码）

```python
def execute_node(node_name, state, checkpointer, config):
    checkpoint = checkpointer.load(config["thread_id"])    # 1. 读当前 checkpoint
    partial_update = node_func(state)                       # 2. 执行节点
    new_state = merge(checkpoint.state, partial_update)     # 3. 合并 state
    checkpointer.save(                                      # 4. 存新 checkpoint
        thread_id=config["thread_id"],
        checkpoint={"id": new_id(), "parent_id": checkpoint.id, "state": new_state}
    )
    return new_state                                        # 5. 传给下一个节点
```
