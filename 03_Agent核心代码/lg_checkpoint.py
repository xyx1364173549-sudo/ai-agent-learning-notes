"""LangGraph Checkpointer：状态持久化（多轮记住状态）"""
from typing import TypedDict

from langgraph import graph
from langgraph.graph import StateGraph,END,START
from langgraph.checkpoint.memory import MemorySaver # 新，内存版记忆存储


class State(TypedDict, total=False):
    counter:int

def increment(state:State)->State:
    return {"counter": state.get("counter",0) + 1}# 每次 +1

graph = StateGraph(State)
graph.add_node("increment",increment)
graph.add_edge(START,"increment")
graph.add_edge("increment",END)


# 关键1：创建"记忆存储"（档案柜）
memory = MemorySaver()


# 关键2：compile 时挂上 checkpointer（告诉流水线"记得存档"）
app = graph.compile(checkpointer=memory)#checkpointer=memory 告诉 LangGraph："每次运行完，把状态存进这个档案柜。"


# 关键3：thread_id 是"档案编号"，同一个 thread_id 共享记忆
config1 = {"configurable":{"thread_id":"会话1"}}
config2 = {"configurable":{"thread_id":"会话2"}}


# 连续调用 3 次，传空 {}，但同一个 thread_id
r1 = app.invoke({}, config1)
r2 = app.invoke({}, config2)
r3 = app.invoke({}, config1)

print(r1["counter"])   # 期望：1
print(r2["counter"])   # 期望：2
print(r3["counter"])   # 期望：3
