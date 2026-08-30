
"""LangGraph 入门：状态图（工厂流水线）"""
from typing import  TypedDict

from langgraph import graph
from langgraph.graph import StateGraph,START,END


# 定义状态；（工件规格：有个text字段，是文字）
class State(TypedDict): #TypedDict 是什么：Python 的一个工具，用来定义"一个字典有哪些字段、各是什么类型"。
    text: str

# 定义节点（工位：读state，返回更新）
def step1(state:State):
    return {"text":state["text"]+"->步骤1"}
def step2(state:State):
    return {"text":state["text"]+"->步骤2"}

# 3.建图（画流水线图纸）
graph = StateGraph(State)#StateGraph 是什么：创建一个"流水线图纸"对象，括号里的 State 告诉它"这个流水线上流转的工件是什么类型"

# 4.添加工位（名字，函数）
graph.add_node("step1",step1)
graph.add_node("step2",step2)


# 5.铺传送带（起点，终点）——三条边把流水线接起来
graph.add_edge(START,"step1")
graph.add_edge("step1","step2")
graph.add_edge("step2",END)

# 6.编译（图纸->流水线）+ 运行（放工件）
app = graph.compile()#compile：把"图纸"编译成"能跑的流水线"（一个可调用对象 app）
result = app.invoke({"text":"开始"})#传入初始状态 {"text": "开始"}（放工件），流水线自动跑完，返回最终状态
print(result)
