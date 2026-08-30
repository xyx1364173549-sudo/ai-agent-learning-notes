messages = [
    {"role": "user", "content": "hello"},
    {"role": "assistant", "content": "hi there"},
    {"role": "user", "content": "how are you"},
    {"role": "system", "content": "be helpful"}
]

# TODO 1: 提取所有 user 的 content → ["hello", "how are you"]
# TODO 2: 生成 [(role, content_length), ...] → [("user", 5), ("assistant", 8), ...]
# TODO 3: 统计各 role 的数量 → {"user": 2, "assistant": 1, "system": 1}
#         （提示：先取 roles 列表，再用 .count() 或推导式统计）


t_1 = [m["content"] for m in messages if m["role"] == "user"]
print(t_1)

t_2 = [(m["role"],len(m["content"]))for m in messages]
print(t_2)

t_3 = [m["role"] for m in messages ]
print(t_3)
t_4 = {m["role"]:t_3.count(m["role"])for m in messages }
print(t_4)

# 你现在的写法：对每条消息都 count 一遍整个列表（重复计算）
# 更高效的写法：先 set 去重，再统计
t_4 = {role: t_3.count(role) for role in set(t_3)}
