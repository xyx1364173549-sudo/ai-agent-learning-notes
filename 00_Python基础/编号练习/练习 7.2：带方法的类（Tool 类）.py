class Tool:
    """
    TODO: 实现 Tool 类
    - __init__: 接收 name, description, func 三个参数
    - execute(input_data): 调用 self.func(input_data) 并返回结果
    - info(): 返回 f"{name}: {description}"
    - is_available: @property，返回 func is not None
    """
    # ↓ 在这里写你的代码
    def __init__(self, name:str, description:str, func):
        self.name = name
        self.description = description
        self.func = func
    def execute(self, input_data:str):
        return self.func(input_data)
    def info(self):
        return f"{self.name}: {self.description}"
    @property
    # @property 我忘记这个是干什么的，等等为我解释一下
    def is_available(self):
        return self.func is not None

# 测试代码
def search(q):
    return f"搜索结果: {q}"

tool = Tool("搜索", "查询信息", search)
print(tool.info())            # 搜索: 查询信息
print(tool.execute("Python")) # 搜索结果: Python
print(tool.is_available)      # True（property，不带括号）
