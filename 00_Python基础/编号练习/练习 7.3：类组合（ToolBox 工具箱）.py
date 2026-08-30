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
class ToolBox:
    """
    TODO: 实现工具箱类
    - __init__: 初始化空的 tools 字典
    - register(tool: Tool): 把 tool 存入 self._tools[tool.name]
    - get(name: str): 按名称获取 Tool，不存在返回 None
    - list_tools(): 返回所有工具名称的列表
    - count: @property，返回已注册工具数量
    """
    # ↓ 在这里写你的代码
    def __init__(self):
        # 这个他IED提示_tools前面的的_有什么含义吗，是函数的内部变量的意思吗，报错是因为我没有加_吗
        self.tools = {}
    def register(self, tool:Tool):
        self.tools[tool.name] = tool
    def get(self,name:str):
        if name in self.tools:
            return self.tools[name]
        else:
            return None
    def list_tools(self):
        return list(self.tools.keys())
    @property
    def count(self):
        return len(self.tools)
# 这些代码 勉勉强强可以看懂，但是有报错，我也不知道为什么，请你给我讲解一下
# 测试代码
box = ToolBox()
box.register(tool)                     # 注册刚才的搜索工具
print(box.list_tools())                # ['搜索']
print(box.count)                       # 1
t = box.get("搜索")
print(t.execute("AI Agent"))           # 搜索结果: AI Agent
print(box.get("不存在的工具"))          # None
