from functools import wraps

def log_calls(func):
    """
    TODO: 实现日志装饰器
    - 记录函数名、参数、返回值
    - 格式: [LOG] 函数名(参数) -> 返回值
    - 不改变原函数行为
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # ① 记录参数（f-string 格式化）
        a = ", ".join( str(a) for a in args )
        # ② 调用原函数
        result = func(*args, **kwargs)
        # ③ 打印日志
        print(f"[LOG] {func.__name__} {a} ->{result!r}")
        #[LOG] greet ('小轩轩',) ->你好 小轩轩 为什么会多一个","，哪里出问题了
        # ④ 返回结果
        return result
        pass
    return wrapper


# 测试代码
@log_calls
def add(a: int, b: int) -> int:
    return a + b

@log_calls
def greet(name: str) -> str:
    return f"你好 {name}"

add(2, 3)         # 期望: [LOG] add(2, 3) -> 5
greet("小轩轩")    # 期望: [LOG] greet('小轩轩') -> 你好 小轩轩


def show_args(*args, **kwargs):
    print("args =", args)
    print("kwargs =", kwargs)

show_args(1, 2, 3)                    # args=(1,2,3)  kwargs={}
show_args(name="小明", age=18)         # args=()       kwargs={'name':'小明','age':18}
show_args(1, "你好", x=5)              # args=(1,'你好') kwargs={'x':5}
