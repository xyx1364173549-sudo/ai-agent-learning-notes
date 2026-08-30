"""LangGraph 版 Agent：把 mini_agent 的循环改造成状态图"""
import sys


sys.path.insert(0, r"C:\Document\weather_tool")
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage,ToolMessage # 关于这两个的知识点你要和我好好讲一下，我有些生疏了这俩个关键词我忘记了
import os
from dotenv import load_dotenv
from weather_tool import WeatherClient, format_weather # 调用外部文件（获取天气数据）


load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

llm = ChatOpenAI(
    api_key = API_KEY,
    model="deepseek-v4-flash",
    base_url = "https://api.deepseek.com"

)

weather = WeatherClient()

@tool
def get_weather_tool(city:str)->str:
    """查询指定城市的天气"""
    data = weather.get_weather(city)
    try:
        return format_weather(data)
    except Exception :
        return "查询天气失败"


@tool
def calculator_tool(expression:str)->str:
    """完成算数计算"""
    return str(eval(expression))


tools = [get_weather_tool,calculator_tool]
# 把工具传给大模型，让他自己调用这个函数
llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict,total=False):
# ── State：messages 用 add_messages 累加 ──
    messages: Annotated[list,add_messages]
# 默认覆盖 {"messages": [...]},每轮换一张新纸
# Annotated[list, add_messages],在同一个本子上往下写


# ── 节点1：调 LLM ──
def call_model(state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages":[response]}
    # 第一次调用，返回的是工具信息
TOOLS = {
    "get_weather_tool": get_weather_tool,
    "calculator_tool": calculator_tool,
}

# ── 节点2：执行工具 ──
def tool_node(state):
# TODO 2：取最后一条消息的 tool_calls，逐个执行，返回 ToolMessage 列表
# 提示：msg = state["messages"][-1]；遍历 msg.tool_calls；用 get_weather_tool.invoke(args)
    tool_messages = []
    msg = state["messages"][-1]
    for tool_call in msg.tool_calls:
        name = tool_call["name"]
        tool = TOOLS[name]
        result = tool.invoke(tool_call["args"])
        tool_messages.append(
            ToolMessage(content=result,tool_call_id=tool_call["id"])
        )
    return {"messages": tool_messages}

def should_continue(state):
# TODO 3：最后一条消息有 tool_calls 就返回 "tools"，否则返回 "end"
# 提示：state["messages"][-1].tool_calls 为空列表表示没有
    if state["messages"][-1].tool_calls:
        return "continue"  # 用工具返回这个干嘛
    else:
        return "finish"


graph = StateGraph(AgentState)
graph.add_node("call_model",call_model)
graph.add_node("tool_node",tool_node)
graph.add_edge(START,"call_model")
graph.add_conditional_edges("call_model",
                            should_continue,
                            {"continue": "tool_node", "finish": END}
                            )# 为什么这个节点的判断写法和当时学的不一样
graph.add_edge("tool_node","call_model") # 工具执行完，回到 call_model（循环）

app = graph.compile()
# ── 运行 ──
result = app.invoke({"messages": [HumanMessage(content="你好呀")]})
print(result)
print(result["messages"][-1].content)
