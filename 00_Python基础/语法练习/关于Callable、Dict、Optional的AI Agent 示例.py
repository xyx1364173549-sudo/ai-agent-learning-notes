from typing import Optional, Dict, Callable


class Agent:
    def __init__(self):
        # 工具注册表： 工具名-> 函数
        self._tool: Dict[str, Callable[[str], str]] = {}

    def 注册工具(self, 名称: str, 函数: Callable[[str], str]) -> None:
        self._tool[名称] = 函数

    def 执行(self, 工具名: str, 参数: str) -> Optional[str]:
        函数 = self._tool.get(工具名)
        if 函数 is None:
            return None
        return 函数(参数)


agent = Agent()

agent.注册工具("搜索", lambda q: f"🔍 搜索结果: {q}")
agent.注册工具("计算", lambda q: f"🧮 计算结果: {eval(q)}")
agent.注册工具("翻译", lambda q: f"🌐 翻译: {q}")

# 模拟用户请求
print(agent.执行("搜索", "Python 教程"))  # 🔍 搜索结果: Python 教程
print(agent.执行("计算", "3 + 5"))  # 🧮 计算结果: 8
print(agent.执行("翻译", "hello"))  # 🌐 翻译: hello
print(agent.执行("不存在", "xxx"))  # None
