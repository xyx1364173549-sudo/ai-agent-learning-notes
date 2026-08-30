# LangGraph 状态图（任务 1.3）学习总结

> **学习人：** 小轩轩
> **日期：** 2026-08-23
> **前置知识：** LangChain 三大抽象（1.1）+ LCEL 管道（1.2）
> **状态：** ✅ 完成
> **案例：** `lg_llm.py`（线性流水线）+ `lg_loop.py`（条件边循环）

---

## 一句话总结

**LangGraph 把"调用 LLM 的多个步骤"组织成流水线，状态在节点间自动流转；条件边让流水线根据状态分叉，实现"答错重学、超限放弃"的动态流程。**

---

## 知识点 1：State 状态 —— 工件规格

**说明**：State 是节点间共享的数据，用 `TypedDict` 定义字段。`total=False` 表示字段可选（输入字段一开始空着，节点逐步产出）。

```python
from typing import TypedDict

class State(TypedDict, total=False):
    topic: str       # 主题（你输入）
    lesson: str      # 讲解（节点产出）
    answer: str      # 学生答案（你输入）
    correct: bool    # 是否答对（判题节点产出）
    retry_count: int # 重试次数（计数器）
```

> `字段名: 类型` = 练习 6 的"门牌标签"搬到类字段上。TypedDict 只提示不校验（对比 BaseModel 会校验）。

---

## 知识点 2：Node 节点函数 —— 工位（返回"更新"，不原地改）

**说明**：节点读 `state`，`return {"字段": 新值}` 返回更新，LangGraph 自动合并进 state。

```python
def generate_lesson(state: State) -> State:
    lesson = ...                              # 调用 LLM
    return {"lesson": lesson}                 # 返回"更新"，不是原地改 state
```

> 关键：不是 `state["lesson"] = lesson`，而是 `return {"lesson": lesson}`，LangGraph 负责合并。

---

## 知识点 3：节点里复用 LCEL

**说明**：节点内部用 1.2 学的 LCEL（模板 | 模型 | 解析器）调 LLM，串成"读字段 → 调 LLM → 写回"的小任务。

```python
def generate_lesson(state: State) -> State:
    chain = (
        ChatPromptTemplate.from_messages([("user", "用一句话讲解：{topic}")])
        | llm | StrOutputParser()
    )
    lesson = chain.invoke({"topic": state["topic"]})   # 读 state
    return {"lesson": lesson}                          # 写回 state
```

> 注意：`from_messages` 用元组列表 `[("user", "...")]`，不是列表 `["user", "..."]`。

---

## 知识点 4：建图 + 添加工位 + 铺传送带

**说明**：`StateGraph(State)` 建图纸；`add_node(名字, 函数)` 安排工位；`add_edge(起点, 终点)` 铺传送带。START/END 是入口出口。

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)
graph.add_node("generate_lesson", generate_lesson)
graph.add_node("judge", judge)
graph.add_edge(START, "generate_lesson")
graph.add_edge("generate_lesson", "judge")
```

> add_node=安排工位（还没干活）；add_edge=铺传送带（定顺序）。

---

## 知识点 5：compile + invoke —— 开工运行

**说明**：compile 把图纸编译成流水线，invoke 放上初始工件自动跑完。

```python
app = graph.compile()
result = app.invoke({"topic": "递归", "answer": "懂了"})
```

> 真正"开始干活"是 invoke 那一刻，不是 add_node。

---

## 知识点 6：状态流转 —— 核心机制

**说明**：每个节点返回的更新自动合并进 state，后面的节点能读到前面的产出。

```python
# invoke 传入：   {"topic": "递归"}
# 节点1 执行后：  {"topic": "递归", "lesson": "递归是函数调用自身…"}
# 节点2 执行后：  {"topic": "递归", "lesson": "…", "correct": True, "retry_count": 1}
```

> 节点2 用 `state["lesson"]` 读到节点1 的产出——这就是"多 Agent 协作"雏形。

---

## 知识点 7：条件边 add_conditional_edges —— 分拣口

**说明**：条件边让流水线根据状态分叉。三个要素：出发节点、路由函数、映射表。

```python
graph.add_conditional_edges(
    "judge",                       # ① 从判题节点出发
    route,                         # ② 路由函数：读 state，返回方向字符串
    {
        "pass": END,               # ③ 映射表：方向 → 实际节点
        "retry": "generate_lesson",
        "give_up": END,
    },
)
```

> 类比：分拣口——路由函数是分拣员（喊方向代号），映射表是通道表（代号 → 工位）。

---

## 知识点 8：路由函数 —— 分拣员

**说明**：路由函数读 state，返回一个"方向字符串"（不是节点名），由映射表翻译成实际节点。

```python
def route(state: State) -> str:
    if state.get("correct"):
        return "pass"                          # 答对
    if state.get("retry_count", 0) >= 3:
        return "give_up"                       # 答错但超限，放弃
    return "retry"                             # 答错但没超限，重学
```

> 返回值类型是 `str`（方向字符串），不是 `State`。

---

## 知识点 9：循环 + 重试上限 —— 状态驱动的动态规划

**说明**：`retry` 指向前面的节点形成循环；用计数器 `retry_count` 记录循环次数，超限走 `give_up` 分支，避免死循环。这就是"动态任务规划"的内核——**流程根据状态动态调整**。

```python
def judge(state: State) -> State:
    correct = (state.get("answer") == "懂了")
    retry_count = state.get("retry_count", 0) + 1   # 每次判题 +1
    return {"correct": correct, "retry_count": retry_count}
```

> `.get(key, 默认值)` 的安全取值：第一次循环 state 里还没有 retry_count，返回默认值 0。

**流程**：

```
讲解 → 判题 → 答对 → END
            → 答错且 retry_count<3 → 回讲解（循环）
            → 答错且 retry_count>=3 → give_up → END（不崩溃）
```

---

## 自测清单

- [ ] State 为什么用 TypedDict？total=False 是什么意思？
- [ ] 节点为什么 return {"lesson": ...} 而不是原地改 state？
- [ ] 条件边的三个要素是什么？
- [ ] 路由函数返回的是什么？（方向字符串，不是节点名）
- [ ] 计数器解决什么问题？（死循环）
- [ ] `state.get("retry_count", 0)` 的第二个参数作用？
