"""2.5a 工作记忆：滑动窗口管理"""
from typing import TypedDict

class Message(TypedDict):
    role:str
    content:str


def sliding_window(messages:list[Message],max_turns:int) -> list[Message]:
    """只保留最近 max_turns 条消息，system 消息始终保留在首位

        参数：
            messages: 完整对话历史（第 0 条通常是 system）
            max_turns: 最多保留多少条（不含 system）

        返回：
            裁剪后的消息列表
        """
    # TODO 1：把 system 消息单独挑出来
    #   提示：判断 messages[0]["role"] == "system"
    #   system_msgs = [m for m in messages if m["role"] == "system"]
    system_msgs = [m for m in messages if m["role"] == "system"]


    # TODO 2：挑出非 system 的消息，只保留最后 max_turns 条
    #   提示：先过滤掉 system，再用切片 [-max_turns:]
    others = [m for m in messages if m["role"] != "system"]
    others_msgs = others[-max_turns:] if max_turns > 0 else []

    # TODO 3：拼回去（system 在前，其余在后）
    return system_msgs+others_msgs


# ── 测试 ──
messages: list[Message] = [
    {"role": "system", "content": "你是一个编程老师"},
    {"role": "user", "content": "什么是递归？"},
    {"role": "assistant", "content": "递归是函数自己调用自己…"},
    {"role": "user", "content": "能举个例子吗？"},
    {"role": "assistant", "content": "比如阶乘…"},
    {"role": "user", "content": "那递归和循环的区别？"},
    {"role": "assistant", "content": "递归是栈，循环是…"},
]

result = sliding_window(messages, max_turns=4)
print(f"裁剪后共 {len(result)} 条：")
for m in result:
    print(f"  [{m['role']}] {m['content']}")
