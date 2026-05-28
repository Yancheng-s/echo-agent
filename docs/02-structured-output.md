# 03 - LLM 结构化输出

## 三种方式对比

### 1. response_format: json_schema

直接约束模型输出的 JSON 结构。

```python
llm.with_structured_output(PlanResult)  # 默认 method
```

底层发送：`response_format: {"type": "json_schema", "json_schema": {...}}`

API 服务端在**解码层面做约束**：每生成一个 token 时，过滤掉不符合 schema 的 token，确保输出能通过校验。

```
普通生成:    模型自由选 token → 可能输出任何内容
json_object: 约束 token 只能构成合法 JSON → 输出一定是有效 JSON
json_schema: 约束 token 必须符合 schema → 输出一定是符合 schema 的 JSON
```

### 2. response_format: json_object

只保证输出合法 JSON，不约束结构。模型可能输出 `[]`、`"hello"`、`{}`，不一定是 `{` 开头。

### 3. function_calling（Echo Agent 使用）

**借工具调用协议的壳**来实现结构化输出。

```python
llm.with_structured_output(PlanResult, method="function_calling")
```

#### 工作原理

**第一步 — Pydantic 模型 → 工具定义**

```json
{
  "type": "function",
  "function": {
    "name": "PlanResult",
    "parameters": {
      "type": "object",
      "properties": {
        "sub_questions": {
          "type": "array",
          "items": {"type": "string"},
          "description": "拆解后的子问题列表，按优先级排列"
        }
      },
      "required": ["sub_questions"]
    }
  }
}
```

**第二步 — LLM 返回工具调用**

```json
{
  "type": "function",
  "function": {
    "name": "PlanResult",
    "arguments": "{\"sub_questions\": [\"问题1\", \"问题2\"]}"
  }
}
```

**第三步 — PydanticToolsParser 解析**

1. 从 `tool_calls` 找 `name == "PlanResult"` 的调用
2. 取出 `arguments` 字符串（JSON）
3. `PlanResult.model_validate_json(arguments)` 反序列化

```
PlanResult (Pydantic类)
   ↓ 转换
工具定义 (发给LLM)
   ↓ LLM返回
tool_call {"name": "PlanResult", "arguments": "..."}
   ↓ PydanticToolsParser按name匹配
PlanResult 实例
```

**本质是一个闭环契约**：定义和解析用的是同一个 Pydantic 类，类名就是匹配的 key。

## 各模型兼容性

| 提供商 | json_object | json_schema | function_calling |
|--------|-------------|-------------|------------------|
| OpenAI | ✅ | ✅ | ✅ |
| Qwen | ✅ | ✅ | ✅ |
| DeepSeek | ✅ | ❌ | ✅ |
| 智谱 | ✅ | ❌ | ✅ |
| 百度 ERNIE | ❌ | ❌ | ✅ |

**function_calling 兼容性最好**，国产模型基本都支持。

## 结构化输出 vs 真实工具调用

如果模型同时需要调真实工具和结构化输出，用**职责分离**：

- 结构化输出 agent（planner、analyzer）→ 不挂真实工具
- 工具调用 agent（researcher）→ 直接调用 Python 函数

避免在同一个 LLM 调用里混合"这是输出格式"和"这是真实工具"。
