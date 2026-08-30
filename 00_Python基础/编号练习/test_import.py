"""test_import.py - 测试从 mytools 导入函数"""

# 从 mytools 模块导入两个函数
from mytools import search_duckduckgo, greet

print("===== 我(test_import.py)被运行了 =====")
print("注意：上面没有打印 mytools 的测试代码，说明它被 import 时跳过了 if __name__ 块\n")

# 使用导入的函数
print(greet("小轩轩"))

result = search_duckduckgo("python")
if result:
    heading = result.get("Heading", "未知")
    print(f"搜索 'python' 的标题是: {heading}")
