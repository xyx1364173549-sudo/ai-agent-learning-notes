import json


import requests


def call_fake_llm(prompt: str) -> dict | None:
    """
    向 httpbin.org/post 发送 POST 请求
    json body: {"prompt": prompt, "model": "test"}
    headers: {"Content-Type": "application/json"}
    timeout: 5
    返回: 响应 JSON；失败返回 None 并打印错误信息
    """
    # ↓ 在这里写你的代码
    url = "http://httpbin.org/post"
    headers = {"Content-Type": "application/json"}
    body = {"prompt": prompt, "model": "test"}
    try:
        rep = requests.post(url,headers = headers,timeout=10,json=body)
        return rep.json()
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    re = call_fake_llm("AI")
    print(re)
