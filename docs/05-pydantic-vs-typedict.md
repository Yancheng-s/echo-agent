# 06 - Pydantic vs TypedDict vs dataclass

## 对比总览

| | TypedDict | Pydantic BaseModel | Python dataclass |
|---|---|---|---|
| 本质 | 带 type hint 的 dict | 数据校验容器 | 轻量数据类 |
| 运行时校验 | ❌ | ✅ | ❌ |
| 类型强制转换 | ❌ `"3"` 还是字符串 | ✅ `"3"` → `3` | ❌ |
| 字段约束 | ❌ | ✅ `Field(ge=0, le=10)` `Literal` | ❌ |
| 默认值 | ✅ | ✅ | ✅ |
| 序列化/反序列化 | ❌ | ✅ `.model_dump()` | ❌ |
| JSON Schema 生成 | ❌ | ✅ | ❌ |
| IDE 补全 | ✅ | ✅ | ✅ |
| 性能 | 最好（就是 dict） | 多一步校验 | 中等 |

## TypedDict — 纯类型标注

```python
class AgentState(TypedDict):
    iteration: int

state = AgentState(iteration="hello")  # 运行时不报错，静默通过
```

只有类型提示，运行时就是普通 dict，不做任何校验。

## Pydantic — 运行时校验

```python
class SearchResult(BaseModel):
    url: str
    score: int = Field(ge=0, le=10)
    quality: Literal["low", "medium", "high"]

SearchResult(url="a.com", score=99, quality="high")   # ❌ ValidationError
SearchResult(url="a.com", score=8, quality="invalid") # ❌ ValidationError
SearchResult(url="a.com", score="5", quality="low")   # ✅ score 自动转成 5
```

自动获得：
- `model_dump()` — 序列化为 dict
- `model_dump_json()` — 序列化为 JSON 字符串
- `model_validate_json(str)` — 从 JSON 反序列化
- `model_json_schema()` — 生成 JSON Schema（with_structured_output 用的就是它）

## dataclass — 轻量数据类

```python
@dataclass
class AgentState:
    question: str = ""
    iteration: int = 0
```

介于 TypedDict 和 Pydantic 之间，有默认值但无校验。

## 在 LLM 结构化输出中的差异

`with_structured_output()` 三种都能传入，但效果不同：

```python
# Pydantic — 有 Field description，LLM 知道每个字段填什么
class PlanResult(BaseModel):
    sub_questions: list[str] = Field(description="拆解后的子问题列表")

# TypedDict — 没有描述，LLM 可能理解不准
class PlanResult(TypedDict):
    sub_questions: list[str]
```

Pydantic 生成的工具定义里字段有 `description` 说明，能引导模型更准确地输出。
