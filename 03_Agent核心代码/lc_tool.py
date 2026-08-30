"""LangChain 入门：Tool 自动生成工具说明书"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")


llm = ChatOpenAI(
    api_key= API_KEY,
    model="deepseek-v4-flash",
    base_url = "https://api.deepseek.com",
)

# 1. @tool：普通函数 → 工具（自动生成说明书）
@tool#@tool 把你的函数变成 StructuredTool 对象,因为加了 @tool 后，get_weather_tool 已经不是一个函数了。@tool 把你的函数"替换"成了对象
def get_weather_tool(city:str)->str:
    """查询指定城市的天气"""
    return f"{city} 今天晴天，20°C"

# bind_tools：把工具"递给"模型（等价于你手写的 json={"tools": tools}）
llm_with_tools = llm.bind_tools([get_weather_tool])

# 3. 调用，看 AI 决定调什么工具
msg = llm_with_tools.invoke("北京天气怎么样")
print(msg)
print(msg.tool_calls)
print(get_weather_tool.name)         # 工具名 → get_weather_tool
print(get_weather_tool.description)  # 描述   → 查询指定城市的天气（你写的 docstring 在这！）
print(get_weather_tool.func)         # 原始函数 → 你写的那个普通函数


from langchain_core.messages import HumanMessage,ToolMessage
# ── 完整闭环：问天气 → 调工具 → 回传 → AI 组织回答 ──
human_msg = HumanMessage(content="北京天气怎么样") #用户指令信息,HumanMessage 就是"用户消息"

# 第 1 次调用：AI 决定调工具
msg = llm_with_tools.invoke([human_msg])#.invoke这个方法是什么意思啊，难道是把参数传入


# 执行工具 + 回传结果（对应你手写的 for tool_call 那段）
tool_messages = []
for tool_call in msg.tool_calls:# 遍历找到工具,
    result = get_weather_tool.invoke(tool_call["args"])#args': {'city': '北京'}
    tool_messages.append(
        ToolMessage(content=result,tool_call_id = tool_call["id"])#ToolMessage 替代手写的 role: "tool"
        # ToolMessage 就是"工具返回的结果"。
    )

final = llm_with_tools.invoke([human_msg,msg,*tool_messages])# 这三个参数有是（用户的指令，AI要调用的工具，工具字典）是这样吗
print(final.content)
