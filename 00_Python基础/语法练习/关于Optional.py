# 解决一个具体的问题：函数找不到结果，返回可能找不到结果，喊回None而不是报错

from typing import Optional


class 知识库:
    def __init__(self):
        self.__文档 = {
            "什么是Python": "Python 是一门解释型编程语言...",
            "如何安装": "访问 python.org 下载安装包..."
        }

    def 搜索(self, 问题: str) -> Optional[str]:
        return self.__文档.get(问题)


kb = 知识库()
# 场景 1：找到了
答案 = kb.搜索("什么是Python")
print(答案)  # "Python 是一门解释型编程语言..."

# 场景 2：没找到
答案 = kb.搜索("今天天气怎么样")
print(答案)  # None
