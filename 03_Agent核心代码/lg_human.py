"""LangGraph 人机协同：关键节点暂停等人工确认"""

from typing import TypedDict


from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict,total=False):
    topic: str
    lesson: str
    approved: bool   # 是否人工通过

def generate_lesson(state:State)->State:
    return {"lesson":f"{state['topic']}的讲解的内容"}

def human_review(state:State)->State:
    return {"approved":True}    # 模拟：人工审核点了"通过"

graph = StateGraph(State)

graph.add_node("generate_lesson",generate_lesson)
graph.add_node("human_review",human_review)

graph.add_edge(START,"generate_lesson")
graph.add_edge("generate_lesson","human_review")
graph.add_edge("human_review",END)

memory = MemorySaver()
# 关键：interrupt_before 在 human_review 前设"质检关卡"
app = graph.compile(checkpointer=memory,interrupt_before=["human_review"])

config = {"configurable":{"thread_id":"会话1"}}

result1 = app.invoke({"topic":"递归"},config)
print("第1次（暂停）：", result1)

result2 = app.invoke(None,config)#None = 继续上次没跑完的；暂停时前面节点已执行
print("第2次（继续）：", result2)
