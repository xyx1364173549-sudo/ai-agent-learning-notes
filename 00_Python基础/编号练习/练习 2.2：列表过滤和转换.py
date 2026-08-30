messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "嗨"},
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "天气如何"}
]

# TODO 1: 筛选出所有 role 为 "user" 的消息
# TODO 2: 提取所有 content 组成一个新列表 → ["你好", "嗨", "你是助手", "天气如何"]
# TODO 3: 构建 {content: role} 的字典 → {"你好": "user", "嗨": "assistant", ...}

User_Messages = [m for m in messages if m["role"] == "user"]
print(User_Messages)

content = [m["content"] for m in messages]
print(content)

content_to_role = [m["role"] : m["content"] for m in messages]
print(content_to_role)
