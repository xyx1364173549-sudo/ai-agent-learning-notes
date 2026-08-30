"""迷你 Agent：能查天气的 AI 助手
架构：LLM 判断意图 → 调用工具 → 把结果给 LLM 组织回答
"""
import sys

import json
import requests

sys.path.insert(0,r"C:\Document\weather_tool")#告诉 Python"去另一个文件夹找模块"
from weather_tool import WeatherClient, format_weather

from llm_client import chat,API_KEY,BASE_URL,MODEL

weather = WeatherClient()
# 天气获取函数
def get_weather_tool(city:str)->str:
    data = weather.get_weather(city)
    # 调用API查询天气
    try:
        return format_weather(data)
    # 查询到的天气数据后将字典格式改成字符串
    except (Exception):
        return "查询天气失败"
# 计算工具函数
def calculator_tool(expression: str) -> str:
    try:
        result = str(eval(expression))
        return f"[calc工具计算] {result}"
    except Exception as e:
        return f"非法输入：{e}"

tools = [
    {
    "type":"function",
    "function":{
        "name":"get_weather_tool",
        "description":"查询指定城市的天气",
        "parameters":{
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
        }
    }
},
     {
        "type":"function",
        "function":{
            "name":"calculator_tool",
            "description":"完成算数",
            "parameters":{
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "expression"}
                    },
                    "required": ["expression"]
            }
        }
    },
]

def chat_with_tools(messages:list[dict])->dict:
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": messages, "tools": tools},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]



# def ask_llm_for_action(user_input:str)->dict:
#     # 构造 prompt
#     prompt =f"""你是一个意图分析器。分析用户输入，判断需要是用那个工具。
#
#     用户输入：{user_input}
#     可用工具：
#     - weather：查天气，参数是城市名
#     - calc：算数学题，参数是算式
#
#     请只输出一个 JSON，不要输出任何其他文字，格式如下：
#     {{"tool": "weather", "arg": "城市名"}}     （查天气时）
#     {{"tool": "calc", "arg": "算式"}}          （算数学题时）
#     {{"tool": null, "arg": null}}              （其他情况，如闲聊）
#
#     规则：
#     - 问天气（如"天气""热吗""带伞"）→ tool 填 "weather"，arg 填城市名
#     - 问数学（如"1+1""3*5"）→ tool 填 "calc"，arg 填算式
#     - 都不是 → tool 填 null，arg 填 null
#
#     """
#     # {{"tool":...}}--- 注意是双大括号 {{ }}，因为在 f-string 里，{} 是"插值"的意思，{{ 会转义成真正的 {。如果你只写一个 {，Python 会以为你要插值，直接报错
#     # 调用chat()让LLM回答（复用你写的llm_client.chat）
#
#     rely = chat ([{"role":"user","content":prompt}])
#     import json
#
#     return json.loads(rely)#字符串转字典


TOOLS = {
    "get_weather_tool":get_weather_tool,
    "calculator_tool":calculator_tool
}

def execute_tool(name:str,arg:str)->str:
    if name in TOOLS:
        return TOOLS[name](arg) # arg是参数吗
    else:
        return "工具不存在"




SYSTEM_PROMPT = """你是一个智能助手，可以调用以下工具：
- 查天气: 当用户问天气时，调用 get_weather_tool(城市名)，把结果转述给用户
你只能使用提供的工具，不要编造数据。"""

def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("=== 迷你 Agent v3（原生 Function Calling）===")

    while True:
        user_input = input("\n你:").strip()
        if user_input == "quit":
            break
        messages.append({"role": "user", "content": user_input})
        # 第一次调用：让 LLM 决定调不调工具
        msg = chat_with_tools(messages)
        messages.append(msg)

        # 判断 返回的的结果里有没有tool_call
        tool_calls = msg.get("tool_calls")

        if tool_calls:
            for tool_call in tool_calls:
                name = tool_call["function"]["name"]
                arge = json.loads(tool_call["function"]['arguments'])
                arg = arge.get("expression")or arge.get("city")
                result = execute_tool(name, arg)#execute_tool 返回的是裸数据 result。要给 AI，必须包装成 AI 认识的标准消息格式：role="tool"（声明这是工具结果）+ tool_call_id（对应哪次调用）+ content（结果内容）
                messages.append({  # 修 Bug 6：回传结果
                "role": "tool",
                "tool_call_id": tool_call["id"],#AI 可能一次要求调多个工具。所以有必要有这个参数
                "content": result,
                })
            final_msg = chat_with_tools(messages)
            messages.append(final_msg)

        print("AI:", messages[-1]["content"])
        # messages = [{"role":"system","content":SYSTEM_PROMPT}]
    # print("=== 迷你 Agent（试试问：北京天气怎么样）===")
    # while True:
    #     user_input = input("\n你:").strip()
    #     # 用户输入
    #     if user_input.lower() == "quit":# 退出
    #         break
    #
    #     messages.append(({"role":"user","content":user_input}))
    #
    #     # 问llm 拿意图指令，就是ask_llm_for_action中返回的json数据
    #     action = ask_llm_for_action(user_input)
    #
    #     tool_name = action.get("tool")
    #     if tool_name:
    #         arg = action.get("arg")
    #         tool_result = execute_tool(tool_name, arg)
    #         messages.append({
    #             "role": "user",
    #             "content": f"工具返回的数据:\n{tool_result}\n请转述给用户",
    #         })
    #     # if action.get("tool") == "weather":
    #     #     city = action.get("city")
    #     #     tool_result = get_weather_tool(city)
    #     #     messages.append({
    #     #         "role":"user",
    #     #         "content":f"工具返回的天气数据:\n{tool_result}\n请转述给用户",
    #     #     })
    #     reply = chat(messages) # 调用chat 让AI返回数据给用户
    #     messages.append({"role":"assistant","content": reply})  # 保存上下文
    #     print(f"AI: {reply}")

# def extract_city(text:str)->str:
#     for word in ["天气", "怎么样", "怎么样？", "如何", "如何？", " ", "？", "?"]:
#         text = text.replace(word,"")# 将常见词去掉，变成“ ”
#     return text.strip() or "Beijing" # 返回城市名，没有的话返回Beijing

if __name__ == "__main__":

    main()
