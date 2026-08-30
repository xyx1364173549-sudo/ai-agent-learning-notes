import json


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

messages = [
    Message("system", "你是助手"),
    Message("user", "你好"),
    Message("assistant", "你好！有什么可以帮您？")
]

# TODO: 将 messages 列表转换为可序列化的 dict 列表
# 然后序列化为 JSON 字符串并写入 messages.json
# 提示: 每个 Message 对象要手动转成 {"role": ..., "content": ...}
result = []
for m in messages:
    a = {"role": m.role, "content": m.content}
    result.append(a)
    print(a)
with open("messages.json","w",encoding="utf-8") as f:
    json.dump(result,f, ensure_ascii=False, indent=2)
