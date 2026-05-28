# 02 - State 数据结构设计

## 三种定义方式

LangGraph state 支持三种定义：

```python
# 1. TypedDict（LangGraph 默认推荐）
class AgentState(TypedDict):
    question: str
    search_results: Annotated[list[SearchResult], add]

# 2. Pydantic BaseModel（Echo Agent 使用）
class AgentState(BaseModel):
    question: str = ""
    search_results: Annotated[list[SearchResult], add] = []

# 3. Python dataclass
@dataclass
class AgentState:
    question: str = ""
    search_results: Annotated[list[SearchResult], add] = field(default_factory=list)
```

## Reducer 模式

LangGraph 的 state 更新采用 Reducer 模式（类似前端 Redux）：

- **节点返回部分更新**，不是完整 state
- **框架按规则合并**回完整 state

```python
class AgentState(BaseModel):
    # 普通字段 → 节点返回值直接覆盖
    question: str = ""
    iteration: int = 0

    # Annotated + add → 节点返回值追加到列表
    search_results: Annotated[list[SearchResult], add] = []
    visited_urls: Annotated[list[str], add] = []

    # add_messages → 智能合并（按 ID 去重、更新、删除）
    messages: Annotated[list[AnyMessage], add_messages] = []
```

### 合并规则

| 字段类型 | reducer | 行为 |
|----------|---------|------|
| `str` / `int` | 无（覆盖） | 直接覆盖旧值 |
| `Annotated[list[T], add]` | `operator.add` | 新值追加到列表 |
| `Annotated[list, add_messages]` | `add_messages` | 按 ID 智能合并 |

## Reducer 模式的意义

```
                  ┌─────────────┐
                  │ AgentState  │  ← 完整状态
                  └──────┬──────┘
                         │ 全量传入
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        planner     researcher    analyzer
        返回:        返回:          返回:
        {           {              {
          sub_qs      search_res     analysis,
        }             visited_urls   iteration
                    }              }
            │            │            │
            └────────────┼────────────┘
                         │ 框架按 reducer 合并
                  ┌──────▼──────┐
                  │ AgentState  │  ← 新状态
                  └─────────────┘
```

节点只需要关心"我产出什么"，不需要知道其他节点怎么改 state。

## 设计经验

调研了 LangGraph 源码和 GPT Researcher 后的改进：

| 改进点 | 说明 |
|--------|------|
| `visited_urls` | 跨迭代去重，防止重复抓取同一个 URL |
| `messages` + `add_messages` | 用 LangGraph 官方 reducer 管理 LLM 对话历史 |
| `Literal["low", "medium", "high"]` | 约束枚举值，比纯 `str` 更安全 |
| `max_iterations` | 防止无限循环的安全阀 |
