class Agent:
    """
    TODO: 实现 Agent 类
    - __init__: 接收 name, version, model 三个参数
    - __str__: 返回 "Agent(name=v{version})"
    - __repr__: 返回 "Agent(name='xxx', version='x.x', model='xxx')"
    - greet(): 返回 f"我是 {name}，很高兴为您服务"
    """
    # ↓ 在这里写你的代码
    def __init__(self,name:str,version:str,model:str):
        self.name = name
        self.version = version
        self.model = model
    def __str__(self):
        return f"Agent({self.name}=v{self.version})"
    def __repr__(self):
        return f"Agent(name={self.name!r}, version={self.version!r}, model={self.model!r})"
    def greet(self):
        return f"我是 {self.name}，很高兴为您服务"

# 测试代码
agent = Agent("小助手", "1.0", "gpt-3.5")
print(agent)              # Agent(小助手=v1.0)
print(repr(agent))        # Agent(name='小助手', version='1.0', model='gpt-3.5')
print(agent.greet())      # 我是 小助手，很高兴为您服务
