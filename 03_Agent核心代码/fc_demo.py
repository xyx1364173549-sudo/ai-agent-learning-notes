"""原生 Function Calling 最小例子"""


import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"

def get_weather(city:str)->str:
    """真实工具函数：返回天气（这里先用假数据模拟）"""
    return f"{city} 今天26°C，晴"



# TODO 1: 定义 tools 列表（工具说明书）
#         告诉 API：有一个 get_weather 工具，需要一个 city 参数（字符串、必填）

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",# 工具名
        "description":"查询指定城市天气", # 工具是干嘛的（LLM 靠这个决定调不调）
        "parameters":{ # 参数定义（JSON Schema 格式）
            "type":"object",
            "properties":{
                "city":{"type":"string","description":"城市名"},
            },
            "required":["city"]  # 必填参数
        }
    }
}]

def run(messages):
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}","Content-Type": "application/json"},
        json={"model":MODEL,"messages":messages,"tools":tools},
        timeout = 30
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    messages = [{"role":"user","content":"北京天气怎么样？"}]
    resp = run(messages)
    msg = resp["choices"][0]["message"]
    print(msg)


    tools_calls = msg.get("tool_calls")
    if tools_calls:
        tools_call = tools_calls[0]
        # 'tool_calls': [{'index': 0, 'id': 'call_00_lvLLzu8ByNK8lOUOR6Qc2645', 'type': 'function',
        #                 'function': {'name': 'get_weather', 'arguments': '{"city": "北京"}'}}]
        name = tools_call["function"]["name"]
        args = json.loads(tools_call["function"]["arguments"])# 这里为什么要用json.loads 和name一样不行吗
        city = args["city"]

        result = get_weather(city)

        messages.append(msg)  #保存上一次的聊天记录

        messages.append({
            "role": "tool",
            "tool_call_id": tools_call["id"],
            "content":result,
        }) # 在里面加入工具调用的路径

        resp2 = run(messages) # 再次调用API给AI跑一遍
        final = resp2["choices"][0]["message"] # AI返回的结果
        print("AI:",final)
    else:
        print("AI:",msg["content"])
