# # 版本 A：没有标注
# def mystery():
#     return None
#
#
# result = mystery()
# result.upper()  # PyCharm 不警告，运行时崩溃
# 版本 B：有标注
from typing import Optional


def typed() -> Optional[str]:
    return None


# result.upper()  # ⚠️ PyCharm 黄色警告！
result = typed()
if result:  # 先判空
    print(result.upper())  # 再使用
