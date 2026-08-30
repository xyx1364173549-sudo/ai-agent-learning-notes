class Agent:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def __str__(self):
        return f"{self.name} (v{self.version})"

    def __repr__(self):
        # 最佳实践：返回能重建对象的代码字符串
        return f"Agent(name={self.name!r}, version={self.version!r})"


a = Agent("助手", "1.0")
print(a)  # 助手 (v1.0)          —— 走 __str__
print(repr(a))  # Agent(name='助手', version='1.0')  —— 走 __repr__
a  # 在 REPL 里直接显示 __repr__ 的结果
