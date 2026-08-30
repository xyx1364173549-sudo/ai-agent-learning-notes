"""DeepSeek LLM 客户端 —— 第一步：能发对话请求"""
import json


import requests
import os
from dotenv import load_dotenv



load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")               # ⚠️ 临时写这里，阶段3改放到.env
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-flash"              # 通用对话模型（还有 deepseek-reasoner 推理模型）


def chat(messages: list[dict], api_key: str = API_KEY) -> str | None:
    """发送对话请求，返回 AI 的回复文本"""
    # TODO 1: 用 requests.post 发请求到 f"{BASE_URL}/chat/completions"
    #          headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    #          json={"model": MODEL, "messages": messages}
    #          timeout=30
    # 上面的参数怎么来的，是api文档里的吗
    url = f"{BASE_URL}/chat/completions"
    data = {"model": MODEL, "messages": messages}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = requests.post(url,headers=headers,json=data,timeout=30)

    # TODO 2: 检查响应状态（HTTP 错误会抛异常）
    resp.raise_for_status()

    # TODO 3: 从返回 JSON 里取出 AI 回复文本
    #          结构: resp.json()["choices"][0]["message"]["content"]
    # 上面的参数怎么来的，是api文档里的吗



    resp = resp.json()["choices"][0]["message"]["content"]
    return resp

def chat_stream(messages: list[dict],api_key: str = API_KEY) -> str :

    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": messages,"stream": True},
        timeout = 60,
        stream=True,
    )
    resp.raise_for_status()

    full_text = ""
    for line in resp.iter_lines(): # 这个是 requests 提供的一个生成器——它把服务器返回的一大串数据，按"行"一条条吐出来。
        if not line: # 这一行没有，进入先一个循环
            continue
        line = line.decode("utf-8")
        if line == "data: [DONE]": # 到最后一行了直接退出
            break
        line = line[6:] # # 去掉 "data: " 前缀
        # line = line.removeprefix("data: ")  # 仅当真以 "data: " 开头时才去掉
        json_data = json.loads(line)
        text = json_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
        if text:
            print(text,end="",flush=True)## ← 流式打印，逐字蹦出来
            full_text += text
    print()
    return full_text



if __name__ == "__main__":
    # 测试：单个问题
    reply = chat_stream([
        {"role": "system", "content": "你是一个乐于助人的助手"},
        {"role": "user", "content": "写一篇 500 字的文章"},
    ])
    # print("AI:", reply)# ← 又把完整的 reply 打印了一遍！(一口气打印出来)
