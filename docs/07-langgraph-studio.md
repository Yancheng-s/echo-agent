# LangGraph Studio 与 LangGraph Server

## 概述

LangGraph Studio 是 LangGraph 官方的可视化调试工具。通过一行命令 `langgraph dev` 自动生成完整的 API 服务 + 可视化界面，开发者只需提供 Graph 代码。

## 启动方式

只需两样东西：

1. `langgraph.json` — 指向你的 Graph
2. `langgraph dev` — 一行启动

```json
{
  "source": { "kind": "uv", "root": "." },
  "graphs": {
    "echo_agent": "./api/engine/graph.py:build_graph"
  },
  "env": "./.env"
}
```

## 架构

```
LangGraph Studio（浏览器，LangChain 服务器）
  ↕ HTTP / SSE（直连本地）
LangGraph API Server（本地，localhost:2024）
  ↕
你的 Graph（build_graph()）
```

Studio UI 托管在 `smith.langchain.com/studio`，通过 `baseUrl` 参数连接本地 API Server。
前端代码从 LangChain 加载，但所有数据请求直连本地服务器，不经过 LangChain。

## 启动流程（底层）

```
1. 读取 langgraph.json → 找到 graph 路径和 env 文件
2. 加载 .env 环境变量（API Key、代理等）
3. import graph.py → 调用 build_graph() → 拿到编译后的 Graph
4. 注册为 "echo_agent"（langgraph.json 里定义的名字）
5. 初始化存储 → 创建 .langgraph_api/ 目录（持久化 checkpoint）
6. 启动 uvicorn → 挂载内置 API 路由
7. 启动 watchfiles → 监听文件变化（热重载）
```

## 自动生成的 API

不需要自己写，LangGraph Server 自动暴露：

```
POST   /threads                     创建会话
GET    /threads                     列出会话
POST   /threads/{id}/runs           执行 Graph
POST   /threads/{id}/runs/stream    流式执行（SSE）
GET    /threads/{id}/state          获取当前 state
GET    /threads/{id}/history        checkpoint 历史
POST   /threads/{id}/runs/cancel    取消执行
GET    /info                        Graph 信息
GET    /docs                        API 文档
```

## SSE 事件流

Studio 通过 SSE 实时接收每步结果：

```
event: metadata       → 开始执行
event: starts         → Graph 启动
event: tasks          → 某个节点开始
event: task_result    → 某个节点完成（含 state 快照）
event: updates        → state 增量更新
event: end            → 全部完成
event: error          → 出错
```

## Checkpoint 持久化

### .langgraph_api/ 目录

`langgraph dev` 自动创建，存：

| 文件 | 内容 |
|------|------|
| `.langgraph_checkpoint.*.pckl` | 每个节点的 state 快照 |
| `store.pckl` | 持久化存储 |

保证重启服务后数据不丢失。

### 和代码里的 Checkpointer 的关系

```
代码里的 Checkpointer（graph.py 中的 MemorySaver）
  → Graph 内部 state 存取

LangGraph Server 的持久化（.langgraph_api/）
  → Server 自己的存储层
```

两层独立。使用 `langgraph dev` 时，Server 会替换你代码里的 Checkpointer。
无论代码里写不写 MemorySaver()，`.langgraph_api/` 都会被创建。

### thread_id

thread_id 是**会话 ID**，不是用户 ID。同一个用户可以有多个研究对话，用不同 thread_id 隔离。

在调用时传入：

```python
graph.invoke(input, config={"configurable": {"thread_id": "session-001"}})
```

同一个 thread_id 共享 state，不同 thread_id 互不影响。

## 前端复用

这些 API 任何前端都能调用，不限于 Studio。用 `@langchain/langgraph-sdk`：

```tsx
import { Client } from "@langchain/langgraph-sdk"

const client = new Client({ apiUrl: "http://localhost:2024" })

const thread = await client.threads.create()

const stream = client.runs.stream(thread.thread_id, "echo_agent", {
  input: { question: "量子计算" }
})

for await (const event of stream) {
  console.log(event.event, event.data)
}
```

不需要自己写 WebSocket、不需要 FastAPI，直接调 LangGraph Server。

## 与 LangSmith 的区别

| | LangGraph Studio | LangSmith |
|---|---|---|
| 阶段 | 开发调试 | 上线监控 |
| 位置 | 本地 | 云服务 |
| 数据 | 关掉就没了（持久化到本地文件） | 永久存储 |
| 谁看 | 开发者自己 | 团队、运维 |

## Windows 编码问题

`langgraph dev` 在 Windows 中文环境下会遇到 GBK 编码错误：

```
UnicodeDecodeError: 'gbk' codec can't decode byte 0x94
```

修复：修改 `venv/Lib/site-packages/langgraph_api/validation.py`：

```python
# 原来
with open(pathlib.Path(__file__).parent.parent / "openapi.json") as f:
# 改为
with open(pathlib.Path(__file__).parent.parent / "openapi.json", encoding="utf-8") as f:
```

## 搜索工具代理配置

DDGS（DuckDuckGo 搜索）在国内需要代理：

```python
from ddgs import DDGS

PROXY = "http://127.0.0.1:7897"

def web_search(query: str, max_results: int = 5) -> list[dict]:
    return list(DDGS(proxy=PROXY).text(query, max_results=max_results))
```
