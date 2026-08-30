import requests

r = requests.get("https://api.github.com/users/python", timeout=30)
print(r.json())
print("1. 状态码:", r.status_code)  # 是否成功（200 = 成功）
print("2. 返回类型:", r.headers.get("Content-Type"))  # 是不是 JSON
print("3. 前 200 字符:", r.text[:200])  # 哪怕出错了看看到底回的是什么
