# AI Research Copilot

AI Research Copilot 是一个面向投资研究、产业链分析和技术趋势判断的个人研究操作系统。

项目目标不是一次性做出复杂平台，而是通过分阶段实现，把以下能力逐步串起来：

1. AI 工程能力：FastAPI、RAG、Memory、LangGraph、Tool Calling、多 Agent、Eval、部署。
2. Research 方法论：研究问题、假设账本、证据矩阵、研究日志、反证搜索、失败复盘、预测追踪、认知更新。

---

## 0. 项目原则

本项目遵循三个原则：

### 0.1 先做最小闭环，再做架构升级

不要一开始就做完整系统。

错误方式：

```text
FastAPI + Streamlit + PostgreSQL + Redis + pgvector + LangGraph + 多 Agent + Skill + Eval 一次性全做
```

正确方式：

```text
每一阶段只增加一个核心能力，并且保证系统始终可以运行。
```

### 0.2 README 是主线文档

每次做完一个阶段，必须更新 README 中的三部分：

```text
1. 当前功能进度
2. 当前架构变化
3. 当前代码路径
```

这样 README 不只是项目介绍，而是学习路线图和开发日志。

### 0.3 先用简单组件，后面再替换

MVP 阶段优先使用轻量组件：

| 模块       | MVP 选择             | 后续升级                           |
| -------- | ------------------ | ------------------------------ |
| 元数据存储    | SQLite             | PostgreSQL                     |
| 向量库      | Chroma / FAISS 本地版 | pgvector / Qdrant              |
| 缓存       | 暂不引入               | Redis                          |
| 前端       | Streamlit          | React / Next.js                |
| Agent 编排 | 普通 Python Pipeline | LangGraph                      |
| 多 Agent  | 暂不引入               | Supervisor + Specialist Agents |

---

## 1. 项目最终形态

最终目标是构建一个支持以下流程的 AI 研究系统：

```text
研究问题输入
  ↓
问题价值判断
  ↓
生成初始假设
  ↓
规划预期证据
  ↓
检索资料
  ↓
构建证据矩阵
  ↓
搜索反向证据
  ↓
生成研究结论
  ↓
Red Team 审查
  ↓
记录研究日志
  ↓
更新长期记忆
  ↓
生成后续研究任务
```

系统最终要回答的不只是：

```text
这家公司怎么样？
```

而是要回答：

```text
这个研究问题是否值得做？
我的初始假设是什么？
支持证据是什么？
反向证据是什么？
证据强度如何？
我的判断应该上调还是下调？
下一步该查什么？
```

---

## 2. 双线 Roadmap 总览

项目分为两条线。

### 2.1 AI 工程能力线

| 阶段  | 工程能力          | 目标                            |
| --- | ------------- | ----------------------------- |
| E0  | 项目骨架          | 创建最小可运行项目                     |
| E1  | FastAPI 后端    | 提供基础 API                      |
| E2  | Streamlit 前端  | 提供可操作 UI                      |
| E3  | 文档上传与解析       | 支持上传 PDF / Markdown / TXT     |
| E4  | RAG 最小闭环      | 支持基于资料问答                      |
| E5  | 会话与记忆         | 支持跨会话保存和摘要                    |
| E6  | LangGraph 状态机 | 用状态图管理 Agent 流程               |
| E7  | Tool Calling  | 支持财务指标和引用检查                   |
| E8  | 多 Agent       | 支持 Research / Risk / Red Team |
| E9  | Eval 评测       | 评估检索、引用、回答质量                  |
| E10 | Docker 部署     | 支持本地和云服务器部署                   |

### 2.2 Research 方法论线

| 阶段 | Research 能力             | 目标          |
| -- | ----------------------- | ----------- |
| R0 | 研究日志模板                  | 开始记录研究过程    |
| R1 | Research Question       | 管理研究问题      |
| R2 | Hypothesis Ledger       | 记录初始假设      |
| R3 | Expected Evidence       | 记录预期证据      |
| R4 | Evidence Matrix         | 区分支持证据和反向证据 |
| R5 | Research Journal        | 记录研究过程和认知变化 |
| R6 | Counter-evidence Search | 主动搜索反证      |
| R7 | Failure Review          | 复盘系统失败案例    |
| R8 | Forecast Tracker        | 追踪长期预测      |
| R9 | Belief Update           | 记录信念更新      |

---

## 3. 推荐实现顺序

不要按所有工程模块做完再做 Research 模块。

推荐采用“工程线 + 研究线交叉推进”的方式：

```text
Phase 0：项目骨架
Phase 1：FastAPI + Research Question
Phase 2：Streamlit + Hypothesis Ledger
Phase 3：文档上传 + Source Registry
Phase 4：RAG 问答 + Evidence Matrix
Phase 5：会话存储 + Research Journal
Phase 6：LangGraph + Counter-evidence Search
Phase 7：Tool Calling + Financial Metrics
Phase 8：Red Team Agent + Failure Review
Phase 9：Eval + Forecast Tracker
Phase 10：Docker 部署 + Progress Dashboard
```

每个阶段都必须满足：

```text
1. 有明确功能
2. 有对应代码路径
3. 有验收标准
4. 有 README 进度记录
```

---

# Phase 0：项目骨架

## 目标

创建一个最小项目结构，不做复杂功能。

本阶段只解决一个问题：

```text
项目能不能被正常启动和维护？
```

## 需要创建的目录

```text
ai-research-copilot/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── apps/
│   ├── api/
│   │   └── main.py
│   └── web/
│       └── streamlit_app.py
├── src/
│   └── research_copilot/
│       ├── __init__.py
│       ├── core/
│       │   ├── config.py
│       │   └── logging.py
│       ├── research_os/
│       │   ├── schemas.py
│       │   └── journal.py
│       └── services/
│           └── health_service.py
├── data/
│   ├── uploads/
│   └── examples/
├── tests/
│   └── test_health.py
└── docs/
    └── architecture.md
```

## 本阶段代码路径

| 功能           | 文件                                            |
| ------------ | --------------------------------------------- |
| FastAPI 入口   | `apps/api/main.py`                            |
| Streamlit 入口 | `apps/web/streamlit_app.py`                   |
| 配置管理         | `src/research_copilot/core/config.py`         |
| 日志管理         | `src/research_copilot/core/logging.py`        |
| 研究日志基础结构     | `src/research_copilot/research_os/journal.py` |
| 数据结构定义       | `src/research_copilot/research_os/schemas.py` |

## 验收标准

运行：

```bash
uvicorn apps.api.main:app --reload
```

访问：

```text
http://127.0.0.1:8000/health
```

返回：

```json
{
  "status": "ok",
  "service": "ai-research-copilot"
}
```

## 当前状态

| 项目                   | 状态          |
| -------------------- | ----------- |
| 目录结构                 | Todo        |
| README               | In Progress |
| FastAPI health check | Todo        |
| Streamlit 空页面        | Todo        |
| 基础配置                 | Todo        |

---

# Phase 1：FastAPI + Research Question

## 目标

实现第一个真正的业务对象：

```text
Research Question
```

研究系统的起点不是文档，也不是模型，而是问题。

本阶段要支持用户创建一个研究问题，例如：

```text
X-FAB 是否是 AI 时代被低估的特色工艺 fab？
```

## 新增目录和文件

```text
src/research_copilot/
├── research_os/
│   ├── question_manager.py
│   ├── schemas.py
│   └── storage.py
├── services/
│   └── research_question_service.py
apps/api/routes/
└── research_questions.py
```

## 数据结构

```python
class ResearchQuestion:
    id: str
    title: str
    description: str
    company: str | None
    theme: str | None
    importance_score: int | None
    non_consensus_score: int | None
    evidence_availability_score: int | None
    status: str
    created_at: str
```

## API 设计

### 创建研究问题

```http
POST /research-questions
```

请求：

```json
{
  "title": "X-FAB 是否是 AI 时代被低估的特色工艺 fab？",
  "description": "研究 X-FAB 是否受益于 AI 基础设施、特色工艺产能和光通信相关需求。",
  "company": "X-FAB",
  "theme": "AI infrastructure / specialty foundry"
}
```

响应：

```json
{
  "id": "rq_001",
  "title": "X-FAB 是否是 AI 时代被低估的特色工艺 fab？",
  "status": "open"
}
```

## Research 方法论对应关系

本阶段对应文章中的：

```text
Pick your own problems
```

也就是主动选择研究问题，而不是被新闻、推文、热门观点牵着走。

## 验收标准

1. 可以通过 API 创建研究问题。
2. 可以通过 API 查询研究问题列表。
3. 每个研究问题有唯一 ID。
4. README 中记录该阶段进度。

## 当前状态

| 项目                      | 状态   |
| ----------------------- | ---- |
| ResearchQuestion schema | Todo |
| 创建研究问题 API              | Todo |
| 查询研究问题 API              | Todo |
| 本地 JSON / SQLite 存储     | Todo |

---

# Phase 2：Streamlit + Hypothesis Ledger

## 目标

实现一个简单前端，让用户可以：

```text
1. 创建研究问题
2. 为研究问题添加初始假设
3. 记录当前置信度
```

## 新增文件

```text
apps/web/
├── streamlit_app.py
└── pages/
    ├── 1_Research_Questions.py
    └── 2_Hypothesis_Ledger.py

src/research_copilot/research_os/
├── hypothesis_manager.py
└── schemas.py
```

## Hypothesis 数据结构

```python
class Hypothesis:
    id: str
    research_question_id: str
    content: str
    belief_before: float
    expected_evidence: list[str]
    status: str
    created_at: str
```

## 示例

研究问题：

```text
8012 是否符合 AI 光通信 bottleneck 投资逻辑？
```

初始假设：

```text
8012 的潜在投资价值不来自传统贸易业务，而来自子公司 Nagase ChemteX 在光学封装材料、热管理材料或半导体材料中的供应链位置。
```

预期证据：

```text
1. 公司材料中出现 optical communication、photonics、semiconductor packaging 等关键词。
2. 子公司产品用于 optical alignment、thermal management 或 advanced packaging。
3. 下游客户与光模块、半导体封装、数据中心产业链相关。
4. 相关业务毛利率或增长率高于集团平均。
```

## Research 方法论对应关系

本阶段对应文章中的：

```text
Predict the result before you run it.
Keep a log: hypothesis, setup, expectation, result, updated belief.
```

## 验收标准

1. Streamlit 可以展示研究问题列表。
2. 用户可以为某个研究问题添加假设。
3. 用户可以填写 belief_before，例如 0.65。
4. 用户可以填写 expected evidence。
5. 数据可以保存到本地。

## 当前状态

| 项目                   | 状态   |
| -------------------- | ---- |
| Streamlit 首页         | Todo |
| Research Question 页面 | Todo |
| Hypothesis Ledger 页面 | Todo |
| 假设保存逻辑               | Todo |

---

# Phase 3：文档上传 + Source Registry

## 目标

实现文档上传和信息源登记。

本阶段还不做 RAG，只做资料管理。

## 新增文件

```text
apps/api/routes/
└── documents.py

src/research_copilot/rag/
├── loaders/
│   ├── pdf_loader.py
│   ├── markdown_loader.py
│   └── text_loader.py
└── document_parser.py

src/research_copilot/research_os/
├── source_registry.py
└── source_quality.py

data/uploads/
```

## Source 数据结构

```python
class ResearchSource:
    id: str
    filename: str
    source_type: str
    company: str | None
    year: int | None
    primary_source: bool
    source_quality_score: float
    bias_risk: str
    uploaded_at: str
```

## Source Quality 规则

| 信息源类型     | 默认质量分 |
| --------- | ----- |
| 年报        | 0.95  |
| 财报电话会原文   | 0.90  |
| 公司公告      | 0.88  |
| 专利        | 0.90  |
| 产品手册      | 0.85  |
| 行业报告      | 0.75  |
| 新闻        | 0.60  |
| 推文 / 社交媒体 | 0.35  |
| 二手总结      | 0.30  |

## Research 方法论对应关系

本阶段对应文章中的：

```text
Upgrade your inputs.
Read the paper itself, not the thread summarizing it.
The appendix is where the bodies are buried.
```

## API 设计

### 上传文档

```http
POST /documents/upload
```

### 查询文档列表

```http
GET /documents
```

## 验收标准

1. 可以上传 PDF / Markdown / TXT。
2. 文件保存在 `data/uploads/`。
3. 系统记录 source_type。
4. 系统给出初始 source_quality_score。
5. Streamlit 可以看到已上传资料列表。

## 当前状态

| 项目                | 状态   |
| ----------------- | ---- |
| 文档上传 API          | Todo |
| 本地文件保存            | Todo |
| Source Registry   | Todo |
| Source Quality 评分 | Todo |
| Streamlit 文档页面    | Todo |

---

# Phase 4：RAG 问答 + Evidence Matrix

## 目标

实现第一个 AI 问答闭环：

```text
上传资料 → 文档切分 → embedding → 检索 → 回答 → 引用 → 证据矩阵
```

## 新增文件

```text
src/research_copilot/rag/
├── splitters/
│   └── text_splitter.py
├── embeddings/
│   └── embedding_client.py
├── vectorstores/
│   └── local_vector_store.py
├── retrievers/
│   └── vector_retriever.py
├── citation.py
└── pipeline.py

src/research_copilot/research_os/
└── evidence_matrix.py

apps/api/routes/
└── chat.py
```

## Evidence 数据结构

```python
class EvidenceItem:
    id: str
    research_question_id: str
    hypothesis_id: str | None
    source_id: str
    chunk_id: str
    evidence_type: str  # support / counter / neutral
    content: str
    strength_score: float
    source_quality_score: float
    citation: str
```

## Evidence Matrix 输出格式

| 命题              | 支持证据         | 反向证据            | 证据强度 | 结论     |
| --------------- | ------------ | --------------- | ---- | ------ |
| 8012 受益于 AI 光通信 | 子公司有电子材料相关业务 | 未披露 AI/CPO 收入占比 | 中低   | 需要继续验证 |

## Research 方法论对应关系

本阶段对应文章中的：

```text
Writing finds gaps your head papers over.
Write down facts that cut against your theory.
```

## API 设计

### RAG 问答

```http
POST /chat
```

请求：

```json
{
  "research_question_id": "rq_001",
  "query": "请判断 8012 是否符合 AI 光通信 bottleneck 投资逻辑。",
  "use_rag": true,
  "return_evidence_matrix": true
}
```

响应：

```json
{
  "answer": "...",
  "citations": [],
  "evidence_matrix": []
}
```

## 验收标准

1. 上传文档后可以进行问答。
2. 回答必须包含引用。
3. 系统可以生成支持证据和反向证据。
4. 证据必须关联 source_id 和 chunk_id。
5. README 记录 RAG pipeline。

## 当前状态

| 项目              | 状态   |
| --------------- | ---- |
| 文档切分            | Todo |
| Embedding       | Todo |
| 本地向量库           | Todo |
| 检索器             | Todo |
| RAG 回答          | Todo |
| 引用生成            | Todo |
| Evidence Matrix | Todo |

---

# Phase 5：会话存储 + Research Journal

## 目标

保存每一次研究过程。

系统不只要保存最终答案，还要保存：

```text
1. 研究问题
2. 初始假设
3. 预期证据
4. 实际证据
5. 研究前置信度
6. 研究后置信度
7. 下一步行动
```

## 新增文件

```text
src/research_copilot/memory/
├── conversation_store.py
├── summarizer.py
└── memory_store.py

src/research_copilot/research_os/
├── research_journal.py
└── belief_tracker.py

apps/api/routes/
├── sessions.py
└── research_logs.py
```

## Research Journal 数据结构

```python
class ResearchLog:
    id: str
    research_question_id: str
    hypothesis_id: str | None
    query: str
    expectation: str
    observed_result: str
    belief_before: float
    belief_after: float
    lesson_learned: str
    next_actions: list[str]
    created_at: str
```

## Research 方法论对应关系

本阶段对应文章中的：

```text
Keep a log: hypothesis, setup, expectation, result, updated belief.
Rereading last month's entries is humbling.
```

## 验收标准

1. 每次问答后生成一条 ResearchLog。
2. ResearchLog 可以在 Streamlit 页面查看。
3. 用户可以手动修改 belief_after。
4. 用户可以记录 lesson learned。
5. 系统可以展示某个研究问题的所有历史日志。

## 当前状态

| 项目                           | 状态   |
| ---------------------------- | ---- |
| 会话保存                         | Todo |
| ResearchLog schema           | Todo |
| ResearchLog API              | Todo |
| Streamlit 日志页面               | Todo |
| belief_before / belief_after | Todo |

---

# Phase 6：LangGraph 状态机 + Counter-evidence Search

## 目标

把普通 Python Pipeline 升级为 LangGraph 状态机。

引入明确流程：

```text
START
  ↓
Load Research Question
  ↓
Load Hypothesis
  ↓
Retrieve Supporting Evidence
  ↓
Retrieve Counter Evidence
  ↓
Build Evidence Matrix
  ↓
Generate Draft Answer
  ↓
Update Research Journal
  ↓
END
```

## 新增文件

```text
src/research_copilot/agents/
├── state.py
├── graph.py
└── nodes/
    ├── load_question_node.py
    ├── hypothesis_node.py
    ├── support_evidence_node.py
    ├── counter_evidence_node.py
    ├── evidence_matrix_node.py
    ├── final_answer_node.py
    └── journal_update_node.py
```

## Agent State

```python
class ResearchAgentState(TypedDict):
    research_question_id: str
    hypothesis_id: str | None
    query: str
    supporting_evidence: list
    counter_evidence: list
    evidence_matrix: list
    draft_answer: str
    final_answer: str
    belief_before: float
    belief_after: float
    errors: list
```

## Research 方法论对应关系

本阶段对应文章中的：

```text
Run the disposable version of every idea first.
Ablate until you know which component carries the result.
```

这里对应到系统设计就是：

```text
不要让 LLM 一次性自由发挥，而是把研究流程拆成可观察、可替换、可调试的节点。
```

## 验收标准

1. 问答流程由 LangGraph 执行。
2. 每个节点有明确输入输出。
3. 支持证据和反向证据分开检索。
4. 状态中可以看到每一步结果。
5. 系统出现错误时可以定位到具体节点。

## 当前状态

| 项目                    | 状态   |
| --------------------- | ---- |
| Agent State           | Todo |
| LangGraph graph.py    | Todo |
| support evidence node | Todo |
| counter evidence node | Todo |
| final answer node     | Todo |
| journal update node   | Todo |

---

# Phase 7：Tool Calling + Financial Metrics

## 目标

加入工具调用能力，让系统可以计算财务指标，而不是让 LLM 猜。

## 新增文件

```text
src/research_copilot/tools/
├── registry.py
├── calculator.py
├── financial_metrics.py
└── citation_checker.py

src/research_copilot/agents/nodes/
└── tool_node.py
```

## 工具列表

| Tool                      | 作用                  |
| ------------------------- | ------------------- |
| calculator                | 通用数学计算              |
| financial_metrics         | 计算 P/B、P/E、毛利率、CAGR |
| citation_checker          | 检查引用是否支持结论          |
| evidence_strength_checker | 检查证据强度              |

## Financial Metrics 示例

```python
def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    return (end_value / start_value) ** (1 / years) - 1
```

## Research 方法论对应关系

本阶段对应文章中的：

```text
Tooling is a first-class research activity.
Launching a run should be one command.
Comparing two runs should take seconds.
```

## 验收标准

1. 系统能识别什么时候需要计算。
2. 财务计算通过工具完成，而不是直接让 LLM 生成。
3. 工具调用结果写入 ResearchLog。
4. 工具调用有 trace 记录。
5. 计算错误可以单独测试。

## 当前状态

| 项目                | 状态   |
| ----------------- | ---- |
| Tool registry     | Todo |
| calculator        | Todo |
| financial_metrics | Todo |
| citation_checker  | Todo |
| tool_node         | Todo |
| 工具调用日志            | Todo |

---

# Phase 8：Red Team Agent + Failure Review

## 目标

加入反方审查和失败案例复盘。

系统每次生成结论后，都要回答：

```text
这个结论最可能错在哪里？
哪些证据不足？
是否有过度推断？
引用是否真的支持结论？
```

## 新增文件

```text
src/research_copilot/agents/specialists/
├── red_team_agent.py
└── risk_agent.py

src/research_copilot/research_os/
├── failure_review.py
└── overconfidence_checker.py

src/research_copilot/agents/nodes/
├── red_team_node.py
└── failure_review_node.py
```

## Failure Case 类型

| 类型                | 含义        |
| ----------------- | --------- |
| Retrieval Failure | 没有召回关键资料  |
| Citation Failure  | 引用不能支撑结论  |
| Reasoning Failure | 从弱证据推出强结论 |
| Memory Failure    | 错误召回历史上下文 |
| Tool Failure      | 工具计算错误    |
| Overconfidence    | 证据不足但语气过强 |

## Research 方法论对应关系

本阶段对应文章中的：

```text
Stare at the outputs.
Pull a hundred failures, read all of them, sort them into piles.
```

## 验收标准

1. 每次最终回答前经过 Red Team 审查。
2. Red Team 输出必须包含证据缺口。
3. 系统能识别至少三类 failure case。
4. Failure case 可以被保存和查看。
5. README 中记录失败类型和改进方案。

## 当前状态

| 项目                        | 状态   |
| ------------------------- | ---- |
| Red Team Agent            | Todo |
| Risk Agent                | Todo |
| failure_review.py         | Todo |
| overconfidence_checker.py | Todo |
| Failure Case 页面           | Todo |

---

# Phase 9：Eval + Forecast Tracker

## 目标

建立评测和预测追踪。

系统不只要回答问题，还要追踪：

```text
1. RAG 是否召回关键资料
2. 引用是否支持结论
3. 回答是否过度自信
4. 用户预测是否被验证
5. 过去判断的命中率如何
```

## 新增文件

```text
evals/
├── datasets/
│   ├── rag_qa_cases.jsonl
│   └── investment_cases.jsonl
├── metrics/
│   ├── retrieval_recall.py
│   ├── citation_accuracy.py
│   ├── answer_faithfulness.py
│   └── overconfidence_rate.py
└── run_eval.py

src/research_copilot/research_os/
└── forecast_tracker.py
```

## Prediction 数据结构

```python
class Prediction:
    id: str
    research_question_id: str
    content: str
    confidence: float
    expected_timeframe: str
    verification_metrics: list[str]
    status: str
    review_due_date: str
    actual_result: str | None
```

## Research 方法论对应关系

本阶段对应文章中的：

```text
Mark down which releases will matter in two years and check your hit rate later.
A forecast plus a correction, repeated a few hundred times, is how taste gets trained.
```

## 验收标准

1. 可以创建预测。
2. 每条预测有 confidence。
3. 每条预测有 review_due_date。
4. 可以运行基础 eval。
5. Eval 结果写入 README 或 docs/progress.md。

## 当前状态

| 项目                | 状态   |
| ----------------- | ---- |
| Eval dataset      | Todo |
| citation_accuracy | Todo |
| retrieval_recall  | Todo |
| forecast_tracker  | Todo |
| Prediction 页面     | Todo |

---

# Phase 10：Docker 部署 + Progress Dashboard

## 目标

将项目整理成可演示版本。

## 新增文件

```text
docker-compose.yml
Dockerfile
scripts/
├── run_api.sh
├── run_web.sh
├── init_db.py
└── ingest_documents.py

apps/web/pages/
└── 9_Project_Progress.py
```

## Progress Dashboard 展示内容

```text
1. 已完成阶段
2. 当前研究问题数量
3. 已上传文档数量
4. 已生成证据数量
5. 已记录研究日志数量
6. 失败案例数量
7. 预测数量
```

## 验收标准

1. 可以通过 Docker Compose 启动。
2. 可以演示完整流程。
3. README 中所有已完成阶段状态更新为 Done。
4. docs/architecture.md 中有最终架构图。
5. 项目可以作为面试展示作品。

## 当前状态

| 项目                 | 状态   |
| ------------------ | ---- |
| Dockerfile         | Todo |
| docker-compose.yml | Todo |
| 启动脚本               | Todo |
| Progress Dashboard | Todo |
| 架构文档               | Todo |

---

# 4. 当前项目进度总表

| Phase    | 工程线            | Research 线              | 状态          |
| -------- | -------------- | ----------------------- | ----------- |
| Phase 0  | 项目骨架           | 研究日志模板                  | In Progress |
| Phase 1  | FastAPI API    | Research Question       | Todo        |
| Phase 2  | Streamlit UI   | Hypothesis Ledger       | Todo        |
| Phase 3  | 文档上传           | Source Registry         | Todo        |
| Phase 4  | RAG 问答         | Evidence Matrix         | Todo        |
| Phase 5  | 会话存储           | Research Journal        | Todo        |
| Phase 6  | LangGraph      | Counter-evidence Search | Todo        |
| Phase 7  | Tool Calling   | Financial Metrics       | Todo        |
| Phase 8  | Red Team Agent | Failure Review          | Todo        |
| Phase 9  | Eval           | Forecast Tracker        | Todo        |
| Phase 10 | Docker 部署      | Progress Dashboard      | Todo        |

---

# 5. 当前架构演进记录

## v0.1.0：项目骨架阶段

当前架构：

```text
FastAPI
  ↓
Service Layer
  ↓
Research OS 基础对象
```

特点：

```text
1. 暂不引入数据库。
2. 暂不引入向量库。
3. 暂不引入 LangGraph。
4. 只搭建最小可运行结构。
```

## v0.2.0：Research Question 阶段

计划架构：

```text
FastAPI
  ↓
ResearchQuestionService
  ↓
Local JSON / SQLite Storage
```

新增能力：

```text
1. 创建研究问题。
2. 查询研究问题。
3. 记录问题状态。
```

## v0.3.0：Hypothesis Ledger 阶段

计划架构：

```text
Streamlit
  ↓
FastAPI
  ↓
HypothesisService
  ↓
Local Storage
```

新增能力：

```text
1. 给研究问题添加初始假设。
2. 记录 belief_before。
3. 记录 expected evidence。
```

## v0.4.0：RAG 阶段

计划架构：

```text
Documents
  ↓
Parser
  ↓
Splitter
  ↓
Embedding
  ↓
Vector Store
  ↓
Retriever
  ↓
Answer with Citation
```

新增能力：

```text
1. 文档解析。
2. 向量检索。
3. 带引用回答。
4. 证据矩阵。
```

---

# 6. 学习路径：每阶段应该重点看哪些代码

| 阶段       | 学习重点                   | 对应代码                                                           |
| -------- | ---------------------- | -------------------------------------------------------------- |
| Phase 0  | Python 项目结构、FastAPI 启动 | `apps/api/main.py`                                             |
| Phase 1  | API 路由、服务层、数据 schema   | `routes/research_questions.py`, `research_question_service.py` |
| Phase 2  | Streamlit 页面与表单        | `apps/web/pages/`                                              |
| Phase 3  | 文件上传、文档解析              | `routes/documents.py`, `rag/loaders/`                          |
| Phase 4  | RAG Pipeline           | `rag/pipeline.py`, `retrievers/`                               |
| Phase 5  | 会话存储、摘要、研究日志           | `memory/`, `research_os/research_journal.py`                   |
| Phase 6  | LangGraph 状态机          | `agents/state.py`, `agents/graph.py`, `agents/nodes/`          |
| Phase 7  | Tool Calling           | `tools/registry.py`, `tools/financial_metrics.py`              |
| Phase 8  | 多 Agent 和 Red Team     | `agents/specialists/`                                          |
| Phase 9  | Eval 评测                | `evals/metrics/`, `evals/run_eval.py`                          |
| Phase 10 | 部署                     | `Dockerfile`, `docker-compose.yml`, `scripts/`                 |

---

# 7. 开发记录模板

每完成一个功能，在 README 中新增一条记录。

## 示例

```text
Date: 2026-06-15
Phase: Phase 1
Change:
- Added ResearchQuestion schema.
- Added POST /research-questions.
- Added GET /research-questions.
- Used local JSON storage for MVP.

Files:
- src/research_copilot/research_os/schemas.py
- src/research_copilot/services/research_question_service.py
- apps/api/routes/research_questions.py

Validation:
- Created a research question through API.
- Listed all research questions successfully.

Next:
- Add Streamlit page for creating research questions.
```

---

# 8. 当前 TODO

## 立即要做

```text
1. 创建项目目录。
2. 保存本 README。
3. 创建 FastAPI health check。
4. 创建 Streamlit 空页面。
5. 创建 ResearchQuestion schema。
```

## 暂时不要做

```text
1. 不要先做多 Agent。
2. 不要先做 LangGraph。
3. 不要先上 PostgreSQL。
4. 不要先做复杂前端。
5. 不要先接实时行情。
6. 不要先做自动交易。
```

---

# 9. 项目完成后的面试表达

当项目完成 Phase 6 之后，可以这样介绍：

```text
我做了一个 AI Research Copilot，不是普通的 RAG 问答系统。

它把研究流程拆成 Research Question、Hypothesis、Expected Evidence、Evidence Matrix、Research Journal 和 Belief Update。

工程上，系统从 FastAPI 和 Streamlit 的最小闭环开始，逐步加入文档解析、RAG 检索、跨会话记忆、LangGraph 状态机、工具调用和 Red Team 审查。

这个项目的重点不是让模型直接生成漂亮结论，而是让 AI 帮我管理研究过程、记录证据、发现反证、复盘失败，并长期训练判断力。
```

---

# 10. 第一阶段启动命令

## 创建项目

```bash
mkdir ai-research-copilot
cd ai-research-copilot
```

## 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

## 安装第一阶段依赖

```bash
pip install fastapi uvicorn streamlit pydantic python-dotenv pytest
```

## 生成 requirements.txt

```bash
pip freeze > requirements.txt
```

## 启动 API

```bash
uvicorn apps.api.main:app --reload
```

## 启动 Web

```bash
streamlit run apps/web/streamlit_app.py
```

---

# 11. 当前版本

```text
Version: v0.1.0
Status: Phase 0 In Progress
Focus: Project Skeleton + README-guided Development
```
