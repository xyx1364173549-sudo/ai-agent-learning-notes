import requests

def safe_divide(a: float, b: float) -> float | None:
    """
    - ZeroDivisionError: 打印 "错误: 除数不能为零"，返回 None
    - TypeError: 打印 "错误: 必须是数字"，返回 None
    - 正常: 返回 a / b
    """
    # ↓ 在这里写你的代码
    try:
        return a/b
    except ZeroDivisionError:
        print("错误: 除数不能为零")
        return None
    except TypeError:
        print("错误: 必须是数字")
        return None


# 测试代码
print(safe_divide(10, 2))    # 期望 5.0
print(safe_divide(10, 0))    # 期望 None + "错误: 除数不能为零"
print(safe_divide("a", 2))   # 期望 None + "错误: 必须是数字"
