# 04 - LangSmith 追踪原理

## 工作机制

LangSmith 的追踪基于两层机制：

### 第一层 — LangChain 回调系统

LangChain 所有组件在执行时都会触发回调事件：

```
on_llm_start → on_llm_end
on_chain_start → on_chain_end
on_tool_start → on_tool_end
```

这是 LangChain 内建的，开发者不需要写任何代码。

### 第二层 — LangSmith SDK 自动注册

设了 `LANGSMITH_TRACING=true` 后，langsmith SDK 在 import 时自动注册为 LangChain 的回调处理器。

```
你的代码
  → LangGraph 执行节点
    → 触发 LangChain 回调
      → langsmith SDK 捕获
        → 异步发送到 smith.langchain.com
```

## 配置

只需在 `.env` 中添加：

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_xxxxx
LANGSMITH_PROJECT=echo-agent
```

并在代码入口**最早**的位置加载环境变量：

```python
from dotenv import load_dotenv
load_dotenv()  # 必须在 import langchain 之前
```

## 为什么需要 load_dotenv()

`pydantic-settings` 的 `BaseSettings` 读取 `.env` 后只把**类里定义过的字段**存为实例属性，不会写入 `os.environ`。`LANGSMITH_*` 变量没有对应字段，所以被跳过。

| 工具 | 做什么 |
|------|--------|
| `pydantic-settings` | 读 `.env` → 校验 → 存为实例属性（LLM 配置） |
| `load_dotenv()` | 读 `.env` → 全写进 `os.environ`（第三方 SDK 用） |

两者互补：`pydantic-settings` 管自己的字段，`load_dotenv()` 让第三方 SDK 也能读到环境变量。
