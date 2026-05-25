# Echo Agent — AI Deep Research Agent 开发方案

> *Echo Agent — like sonar in the deep sea of information. Ping, listen, go deeper.*

## 项目定位

通用 AI 深度研究智能体，通过多轮深层"回声探测"，在信息空间中逐步构建完整认知地图。类似 OpenAI Deep Research / Perplexity Pro 的开源实现，覆盖 DeepAgent 核心技术栈。

## 核心隐喻：深海声呐回声探测

| 声呐概念 | DeepAgent 对应 |
|---------|---------------|
| Ping（发射脉冲） | Action — 发出查询/调用工具 |
| Echo（回声信号） | Observation — 返回结果 |
| 深度递进（越探越深） | 多轮迭代推理，逐层深入 |
| 多站点三角定位 | Multi-Agent 协作交叉验证 |
| 回声地图（累积成像） | GraphRAG 知识图谱 |
| 声呐记忆（历史回波） | Agent Memory |
| 调频/变向 | Query 改写 |

## 核心流程

```
用户问题
  ↓
[Planner] 拆解为子问题树
  ↓
[Researcher] 对每个子问题执行 ReAct 循环
  Ping(搜索) → Echo(结果) → Think(分析) → 决定是否继续深挖
  ↓
[Knowledge Builder] 抽取实体关系，构建图谱
  ↓
[Analyst] 交叉验证 + 图上推理 + 发现信息缺口
  ↓ (缺口回传给 Researcher 继续探测)
[Writer] 综合输出研究报告
```

## 技术栈

- 语言：Python
- LLM 框架：LangChain 家族
- 前端：React
- API：FastAPI + WebSocket
- 向量库：Chroma / FAISS
- 图数据库：Neo4j / NetworkX（轻量版）

## 技术点覆盖清单

| 技术点 | 对应 Phase | 对应模块 |
|--------|-----------|---------|
| ReAct 推理循环 | Phase 2 | `engine/react.py` |
| Plan-and-Execute 分步执行 | Phase 2 | `engine/planner.py` + `engine/state.py` |
| Multi-Agent 多智能体协作 | Phase 7 | `agents/` 下 5 个 Agent + Orchestrator |
| Query 改写模块 | Phase 4 | `query/rewriter.py` + `query/decomposer.py` |
| GraphRAG 知识图谱融合检索 | Phase 6 | `knowledge/` 全链路 |
| Agent Memory 短期工作记忆 | Phase 5 | `memory/working.py` |
| Agent Memory 长期向量记忆 | Phase 5 | `memory/vector.py` |
| Agent Memory 摘要缓存 | Phase 5 | `memory/summary.py` |
| 标准化 Tool Calling 接口 | Phase 1 | `core/tools.py` |
| 5 种以上工具集成 | Phase 3 | 6 个工具 |

## 架构总览

```
┌─────────────────────────────────────────────────┐
│  Frontend (React)                                │
│  推理过程可视化 / 知识图谱展示 / 对话界面         │
├─────────────────────────────────────────────────┤
│  API Layer (FastAPI + WebSocket)                  │
├─────────────────────────────────────────────────┤
│  Echo Pipeline — Deep Research 业务逻辑           │
├──────────┬──────────┬───────────────────────────┤
│ Agents   │ Memory   │ Knowledge                  │
│ 多智能体  │ 三级记忆  │ GraphRAG                   │
├──────────┴──────────┴───────────────────────────┤
│  Reasoning Engine (ReAct + Plan-and-Execute)     │
├─────────────────────────────────────────────────┤
│  Foundation (LLM / Tool Interface / Config)       │
└─────────────────────────────────────────────────┘
```

---

## 实施阶段

### Phase 1 — Foundation（地基层）约 1 周

| 模块 | 内容 | 产出 |
|------|------|------|
| `core/llm.py` | LLM 统一调用封装，支持多模型切换，流式输出 | 能调通 LLM |
| `core/tools.py` | Tool Calling 标准接口（BaseTool + ToolRegistry + 参数校验） | 注册工具跑通 |
| `core/schema.py` | 统一数据结构（Message、Step、Plan、ResearchState） | 类型安全 |
| `core/config.py` | 配置管理、日志、异常处理 | 项目可运行 |

### Phase 2 — Reasoning Engine（推理引擎）约 1.5 周

| 模块 | 内容 | 产出 |
|------|------|------|
| `engine/react.py` | ReAct 循环：Thought → Action → Observation → 终止判断 | 能用 ReAct 调工具回答问题 |
| `engine/planner.py` | Plan-and-Execute：问题 → 子问题树 → 动态调整 | 复杂问题自动拆解执行 |
| `engine/state.py` | 研究状态机：tracking 子问题进度、深度、置信度 | 可观测的执行状态 |

### Phase 3 — Tool Suite（工具集）约 1 周

| 工具 | 声呐隐喻 | 用途 |
|------|----------|------|
| `tools/web_search.py` | Ping | 通用搜索（Tavily / SerpAPI / DuckDuckGo） |
| `tools/academic_search.py` | Deep Ping | 论文检索（Semantic Scholar / arXiv） |
| `tools/web_reader.py` | Echo Receiver | 网页正文提取 + 长文档分块 |
| `tools/code_executor.py` | Depth Analyzer | Python 沙箱，数据分析/可视化 |
| `tools/calculator.py` | Signal Processor | 数值计算、单位换算 |
| `tools/note_taker.py` | Echo Logger | 结构化笔记，供后续 Agent 消费 |

### Phase 4 — Query Engine（查询引擎）约 1 周

| 模块 | 内容 |
|------|------|
| `query/decomposer.py` | 复杂问题 → 子问题树（支持层级拆解） |
| `query/rewriter.py` | 多策略改写：同义扩展、子问题拆分、时间限定、对比、反面 |
| `query/router.py` | 根据问题类型路由到合适的工具/检索通道 |

### Phase 5 — Memory System（记忆系统）约 1.5 周

| 模块 | 内容 |
|------|------|
| `memory/working.py` | 短期工作记忆 — 当前 session 的中间状态、已探索线索、待验证假设 |
| `memory/vector.py` | 长期向量记忆 — 历史研究成果存入向量库，语义检索复用 |
| `memory/summary.py` | 摘要缓存 — 长文档压缩摘要，LRU 策略避免重复处理 |
| `memory/manager.py` | 统一调度 — 决定何时读/写哪级记忆 |

### Phase 6 — GraphRAG（知识图谱融合检索）约 2 周

| 模块 | 内容 |
|------|------|
| `knowledge/extractor.py` | 从研究结果中抽取实体 + 关系（概念-证据-来源） |
| `knowledge/graph.py` | 图存储与查询（Neo4j 或 NetworkX），支持增量构建 |
| `knowledge/retriever.py` | 融合检索：图遍历（多跳推理）+ 向量召回 + 交叉排序 |
| `knowledge/gap_detector.py` | 信息缺口检测：发现孤立节点/缺失关系 → 生成补充查询 |

### Phase 7 — Multi-Agent（多智能体协作）约 1.5 周

| Agent | 职责 |
|-------|------|
| `agents/orchestrator.py` | 总调度，管理研究生命周期，Agent 间通信 |
| `agents/planner.py` | 接收用户问题，制定/调整研究计划 |
| `agents/researcher.py` | 执行信息采集，运行 ReAct 循环调用工具 |
| `agents/analyst.py` | 交叉验证、矛盾检测、置信度评估、图谱推理 |
| `agents/writer.py` | 综合所有发现，生成结构化研究报告 |

Agent 间通信：共享 ResearchState + 消息队列。

### Phase 8 — Echo Pipeline（业务组装）约 1 周

将所有模块串成完整的 Deep Research pipeline：

- 深度控制：用户可设定探索深度（1-5 级）
- 实时进度：当前探索哪个子问题、第几轮、发现了什么
- 报告模板：摘要 → 关键发现 → 详细分析 → 来源引用 → 知识图谱可视化
- 中断恢复：支持暂停/继续研究

### Phase 9 — API + Frontend（接口与前端）约 2 周

| 模块 | 内容 |
|------|------|
| `api/main.py` | FastAPI + WebSocket 实时推送推理链 |
| `web/` | React 前端 |

前端核心页面：

- 对话界面：输入研究问题，查看历史
- 推理过程可视化：实时展示 ReAct 循环步骤
- 子问题树：展示 Plan 的分解与执行进度
- 知识图谱：交互式图谱浏览（节点点击展开详情）
- 研究报告：结构化渲染 + 来源链接

---

## 目录结构

```
echo-agent/
├── core/                   # Phase 1: 基础设施
│   ├── __init__.py
│   ├── llm.py
│   ├── tools.py
│   ├── schema.py
│   └── config.py
├── engine/                 # Phase 2: 推理引擎
│   ├── __init__.py
│   ├── react.py
│   ├── planner.py
│   └── state.py
├── tools/                  # Phase 3: 工具实现
│   ├── __init__.py
│   ├── web_search.py
│   ├── academic_search.py
│   ├── web_reader.py
│   ├── code_executor.py
│   ├── calculator.py
│   └── note_taker.py
├── query/                  # Phase 4: 查询引擎
│   ├── __init__.py
│   ├── decomposer.py
│   ├── rewriter.py
│   └── router.py
├── memory/                 # Phase 5: 三级记忆
│   ├── __init__.py
│   ├── working.py
│   ├── vector.py
│   ├── summary.py
│   └── manager.py
├── knowledge/              # Phase 6: GraphRAG
│   ├── __init__.py
│   ├── extractor.py
│   ├── graph.py
│   ├── retriever.py
│   └── gap_detector.py
├── agents/                 # Phase 7: 多智能体
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── planner.py
│   ├── researcher.py
│   ├── analyst.py
│   └── writer.py
├── echo/                   # Phase 8: 业务逻辑
│   ├── __init__.py
│   ├── pipeline.py
│   └── report.py
├── api/                    # Phase 9: 后端
│   ├── __init__.py
│   └── main.py
├── web/                    # Phase 9: React 前端
│   └── (create-react-app)
├── tests/                  # 测试
│   ├── test_react.py
│   ├── test_planner.py
│   ├── test_memory.py
│   └── test_pipeline.py
├── requirements.txt
├── .env.example
├── README.md
└── DEVELOPMENT_PLAN.md     # 本文件
```

---

## 工期估算

| Phase | 内容 | 时间 |
|-------|------|------|
| 1 | Foundation | 1 周 |
| 2 | Reasoning Engine | 1.5 周 |
| 3 | Tool Suite | 1 周 |
| 4 | Query Engine | 1 周 |
| 5 | Memory System | 1.5 周 |
| 6 | GraphRAG | 2 周 |
| 7 | Multi-Agent | 1.5 周 |
| 8 | Echo Pipeline | 1 周 |
| 9 | API + Frontend | 2 周 |
| **总计** | | **约 13 周** |

每个 Phase 结束都有可独立运行的产出，Phase 2 结束即可演示基础研究能力。

---

## 里程碑

- **M1（Phase 1-2 完成）**：能用 ReAct 循环 + 工具调用回答简单研究问题
- **M2（Phase 3-4 完成）**：支持多工具、多角度查询改写的研究能力
- **M3（Phase 5-6 完成）**：具备记忆和知识图谱，能做跨文档多跳推理
- **M4（Phase 7-8 完成）**：完整的多 Agent 协作 Deep Research pipeline
- **M5（Phase 9 完成）**：带 Web UI 的完整产品形态
