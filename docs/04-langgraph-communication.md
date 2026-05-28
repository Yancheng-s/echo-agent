# 05 - LangGraph 通信机制

## 核心机制：共享状态（黑板模式）

节点之间**不直接通信**，全部通过 state 中转：

```
planner ──写──→ state ←──读── researcher
                    ↕
analyzer ──读──→ state ←──写── reporter
```

### 黑板模式（Blackboard Pattern）

1. 节点只做两件事：**读 state** → **写部分 state**
2. 节点之间不知道彼此存在，只看 state 里的数据
3. 框架负责按图定义把 state 传给下一个节点

### 对比

```
节点间通信:  A → state → B    （解耦，靠 state 隐式传递）
函数间通信:  A(args) → return → B(result)    （耦合，直接传参）
```

## 优势

- **加新节点容易** — 不用改任何现有节点代码，只需要改 graph.py 的连边定义
- **改顺序容易** — 只改连边，节点代码不动
- **节点独立可测** — 每个节点只依赖 state，可以单独传入测试数据

## 示例

analyzer 写 `gaps`，researcher 下一轮读 `gaps` 定向搜索，两者没有任何直接引用：

```python
# analyzer 写
def analyzer(state: AgentState) -> dict:
    return {
        "analysis": [AnalysisResult(gaps=["缺少技术细节"], ...)],
        "iteration": state.iteration + 1,
    }

# researcher 读
def researcher(state: AgentState) -> dict:
    last_analysis = state.analysis[-1] if state.analysis else None
    queries = last_analysis.gaps if last_analysis and last_analysis.gaps else state.sub_questions
    ...
```

## 可视化

LangGraph 支持 `graph.stream(stream_mode="updates")` 逐步输出每个节点的变更，配合 LangSmith 可以看到完整的调用链、输入输出和耗时。
