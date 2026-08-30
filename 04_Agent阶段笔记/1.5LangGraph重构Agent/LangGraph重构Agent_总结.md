# 用 LangGraph 重构 Agent（任务 1.5）学习总结

> **学习人：** 小轩轩
> **日期：** 2026-08-25
> **前置知识：** LangGraph 状态图 + 条件边（1.3）+ Checkpointer（1.4）
> **状态：** ✅ 完成
> **案例：** `agent_graph.py`（把 mini_agent 的手写循环改造成状态图）

---

## 一句话总结

**把 mini_agent 的手写 `while` 循环，改造成 LangGraph 的状态图——用"节点 + 条件边"表达"下令 → 执行 → 回答"的 Agent 循环（ReAct 模式）。**

---

## 知识点 1：Agent 循环（状态图表达 while 循环）

**说明**：mini_agent 的 `while True` 循环，用状态图的"环"来表达。

```python
# 手写循环（mini_agent.py）
while True:
    用户输入 → 调LLM → 有tool_calls? → 执行工具 → 回传 → 再调LLM → 输出

# 状态图（agent_graph.py）
START → call_model → 有tool_calls? → tool_node → 回到 call_model（环）
                   → 无tool_calls → END
```

---

## 知识点 2：Annotated + add_messages —— 消息累加

**说明**：messages 是对话历史，必须"累加"（往下写），不能"覆盖"（换新纸）。

```python
from typing import Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # 累加，不是覆盖
```

> 类比：默认覆盖=每轮换新纸；add_messages=在同一个本子上往下写。

---

## 知识点 3：call_model 节点 —— 调 LLM

**说明**：调 LLM（带工具），返回 AI 的消息（可能是 tool_calls，也可能是正常回答）。

```python
def call_model(state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}
```

> 第一次调用 content 空（AI 在下令），第二次调用 content 正常（AI 在回答）。

---

## 知识点 4：tool_node 节点 —— 执行工具（按 name 分发）

**说明**：取最后一条消息的 tool_calls，用 TOOLS 注册表按 name 分发到对应工具，返回 ToolMessage。

```python
TOOLS = {
    "get_weather_tool": get_weather_tool,
    "calculator_tool": calculator_tool,
}

def tool_node(state):
    msg = state["messages"][-1]
    tool_messages = []
    for tool_call in msg.tool_calls:
        name = tool_call["name"]
        tool = TOOLS[name]                       # 按 name 找到工具
        result = tool.invoke(tool_call["args"])  # args 是字典
        tool_messages.append(
            ToolMessage(content=result, tool_call_id=tool_call["id"])
        )
    return {"messages": tool_messages}           # 要 return！
```

> 关键：不能硬编码某个工具，要用 TOOLS 注册表按 name 分发（因为有两个工具）。

---

## 知识点 5：should_continue —— 方向代号（不是节点名）

**说明**：路由函数返回"方向代号"（语义），映射表把代号翻译成节点名。

```python
def should_continue(state):
    if state["messages"][-1].tool_calls:
        return "continue"    # 方向代号：继续调工具
    return "finish"          # 方向代号：结束

graph.add_conditional_edges(
    "call_model",
    should_continue,
    {"continue": "tool_node", "finish": END},   # 代号 → 节点
)
```

> 三个名字各司其职：函数名 tool_node（干活）、节点名 "tool_node"（引用）、方向代号 continue/finish（语义）。

---

## 知识点 6：节点名三处一致（本任务最大的坑）

**说明**：add_node、add_edge、映射表里用到的节点名，必须一字不差。

```python
graph.add_node("tool_node", tool_node)        # ① 注册
graph.add_conditional_edges(..., {"continue": "tool_node", ...})  # ② 映射
graph.add_edge("tool_node", "call_model")     # ③ 连边
```

> 三处 "tool_node" 必须完全一致。本任务多次在此踩坑（"tools"/"tool"/"tool_node" 打架）。

---

## 知识点 7：循环自动终止

**说明**：循环不会无限进行，因为第 2 次 call_model 时 AI 已拿到工具结果，就不再"下令"而是"回答"（无 tool_calls），should_continue 返回 finish，结束。

```python
# 第1次 call_model：content空 + tool_calls → continue → tool_node
# 第2次 call_model：content正常 + 无tool_calls → finish → END
```

---

## 自测清单

- [ ] Agent 循环的状态图和 mini_agent 的 while 循环是什么关系？
- [ ] Annotated + add_messages 解决什么问题？（消息累加 vs 覆盖）
- [ ] tool_node 为什么要用 TOOLS 注册表按 name 分发？
- [ ] 路由函数返回的是"方向代号"还是"节点名"？
- [ ] 节点名哪三处必须一致？
- [ ] 循环为什么能自动终止？
