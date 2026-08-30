response = {
    "choices": [
        {"message": {"role": "assistant", "content": "你好！"}},
        {"message": {"role": "assistant", "content": "有什么可以帮您？"}}
    ],
    "usage": {"total_tokens": 100}
}

# TODO 1: 提取第一条回复的 content（应该是 "你好！"）
# TODO 2: 提取 total_tokens（应该是 100）
# TODO 3: 在 choices 末尾追加一条新消息
#         {"message": {"role": "user", "content": "谢谢"}}
a = response["choices"][0]["message"]["content"]
print(a)
b = response["usage"]["total_tokens"]
print(b)

# new_message = {"message": {"role": "user", "content": "谢谢"}}
# response["choices"].append(new_message)
# c = response["choices"][-1]
# print(c)

response["choices"].append({"message": {"role": "user", "content": "谢谢"}})
print(response["choices"][-1])
