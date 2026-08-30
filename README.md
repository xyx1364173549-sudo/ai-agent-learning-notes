# AI Agent 学习笔记（Python → Agent 全链路）

> 小轩轩从零开始学习 Python 与 AI Agent 开发的完整学习笔记与代码。
> 路线：Python 语法基础 → 巩固项目 → DeepSeek API + Function Calling → LangChain / LangGraph → RAG + 分层记忆。
> 时间跨度：2026 年 7 月起。

---

## 目录结构

```
ai-agent-learning-notes/
├── 00_Python基础/          # Python 语法笔记 + 语法练习 + 编号练习（练习1.1~13.3）
│   ├── 语法笔记/            # python.md、python_补充笔记与项目.md
│   ├── 语法练习/            # 50+ 个语法练习 .py
│   └── 编号练习/            # 按知识点编号的系统练习 + P0/P1/P2 阶段复习总结
│
├── 01_阶段总结/            # Python→Agent 衔接的阶段性总结
│   ├── 阶段1_Agent开发入门总结.md      # 接 DeepSeek API，做出迷你 Agent
│   ├── 阶段2_Git与GitHub全流程手册.md
│   ├── 阶段3_Agent进阶收官总结.md
│   ├── 阶段4_原生FunctionCalling总结.md
│   ├── 阶段5_Web化与前后端分离总结.md
│   ├── 项目一_天气查询工具总结.md
│   ├── 项目二_TODO管理器总结.md
│   └── 学习交接.md
│
├── 02_巩固项目/            # 两个综合巩固项目
│   ├── weather_tool/       # 天气查询工具（requests/json/OOP/异常处理）
│   └── todo_project/       # TODO 管理器（装饰器/魔术方法/json 持久化）
│
├── 03_Agent核心代码/       # agent_project 全部源码
│   ├── llm_client.py       # DeepSeek API 封装
│   ├── chat_cli.py         # 命令行对话
│   ├── mini_agent.py       # 迷你 Agent（手写循环）
│   ├── fc_demo.py          # 原生 Function Calling
│   ├── web_agent.py + index.html   # FastAPI Web 化
│   ├── lc_*.py             # LangChain（ChatModel/PromptTemplate/Tool/LCEL）
│   ├── lg_*.py             # LangGraph（状态图/条件边/Checkpointer/人机协同）
│   ├── agent_graph.py      # LangGraph 重构 Agent
│   ├── embedding_demo.py / chroma_demo.py / rerank_demo.py   # RAG
│   ├── chunk_demo.py       # 文档切分
│   └── memory_*.py         # 分层记忆（working / episodic）
│
├── 04_Agent阶段笔记/       # Agent 阶段每任务 .md + .html 双份笔记
│   ├── 1.1LangChain核心抽象/
│   ├── 1.2LCEL管道组合/
│   ├── 1.3LangGraph状态图/
│   ├── 1.4Checkpointer与人机协同/
│   ├── 1.5LangGraph重构Agent/
│   ├── 2.1Embedding与向量化/
│   ├── 2.3Chroma向量数据库/
│   └── 2.4检索与重排序/
│
└── 99_参考资料/            # 非自己写的参考材料（PDF 不上传 GitHub）
```

---

## 学习路线

| 阶段 | 内容 | 状态 |
|---|---|---|
| P0 | Python 语法基础（数据类型/函数/OOP/推导式/魔术方法） | ✅ 完成 |
| P1 | 装饰器、生成器、async/await | ✅ 完成 |
| 阶段1 | DeepSeek API 调用 + 迷你 Agent | ✅ 完成 |
| 阶段2 | Git / GitHub 全流程 | ✅ 完成 |
| 阶段3 | Agent 进阶收官 | ✅ 完成 |
| 阶段4 | 原生 Function Calling | ✅ 完成 |
| 阶段5 | FastAPI Web 化 + 前后端分离 | ✅ 完成 |
| 1.1-1.5 | LangChain 核心抽象 / LCEL / LangGraph / Checkpointer / 重构 Agent | ✅ 完成 |
| 2.1-2.4 | Embedding / Chroma / 检索与重排序 | ✅ 完成 |
| 进行中 | 分层记忆 + 动态任务规划（毕业论文方向） | 🔄 进行中 |

---

## 技术栈

- **语言**：Python
- **LLM 接口**：DeepSeek API（Function Calling / SSE 流式）
- **框架**：LangChain / LangGraph / FastAPI
- **向量库**：Chroma
- **工具**：Git / GitHub / VS Code

---

## 说明

- 本仓库为学习笔记与配套代码，**不包含** `.venv`、`.idea`、`__pycache__` 等环境文件。
- `99_参考资料/` 下的 PDF 按约定不上传 GitHub（体积过大），仅本地保留。
- 每个任务笔记同时提供 `.md`（GitHub 阅读）和 `.html`（本地复习，深色主题）两份。
