


class MessageHistory:
    """
    TODO: 实现 MessageHistory 类
    - __init__: 初始化空列表 _messages
    - add(role, content): 添加 {"role": ..., "content": ...} 消息
    - __len__: 返回消息数量（支持 len(history)）
    - __getitem__(index): 支持下标访问 history[0]
    - __iter__: 支持 for msg in history 遍历
    """
    # ↓ 在这里写你的代码
    def __init__(self):
        self._messages = []
    def add(self,role:str,content:str):
        self._messages.append({"role":role,"content":content})
        # 为什么这个add函数要加self，我记得不是只有魔术方法要加吗，加self有什么含义吗
    def __len__(self):
        return len(self._messages)
    def __getitem__(self,index):
        return self._messages[index]
    # history 不是字典吗，要下标访问难道要先遍历成为列表？
    def __iter__(self):

        return iter(self._messages)
    # iter()这个函数，忘记了



# 测试代码
history = MessageHistory()
history.add("user", "你好")
history.add("assistant", "你好！有什么可以帮您？")

print(len(history))        # 2
print(history[0])          # {'role': 'user', 'content': '你好'}
for msg in history:        # 能遍历
    print(msg["role"])
