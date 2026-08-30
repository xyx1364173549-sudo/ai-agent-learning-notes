import time
from functools import wraps

def timer(func):
    """
    TODO: 实现计时装饰器
    - 打印函数执行耗时
    - 不改变原函数的返回值
    - 用 @wraps 保留原函数元信息
    """
    @wraps(func)
    # wraps 他的作用用就是保存好被引录的函数的值不丢失是吧，比如下面的 3和4
    def wrapper(*args, **kwargs):
        # 我忘记*args, **kwargs 这连个参数是什么意思了，好好帮我解释一下
        # *args  = 把所有"位置参数"打包成元组 (3, 4)
        # **kwargs = 把所有"关键字参数"打包成字典 {"name": "xx"}
        
        # ① 记录开始时间
        start = time.time()
        # ② 调用原函数，保存结果
        result = func(*args, **kwargs)
        # ③ 计算耗时并打印
        end = time.time()
        print(f"耗时{end-start:.6f}秒")
        # ④ 返回结果
        return result
        # 似乎本质上就是，给他套上了一个计时工具（用@timer）用func(*args, **kwargs)调回原函数的内容，在这里运行，后返回结果
        pass
    return wrapper


# 测试代码
@timer
def slow_add(a, b):
    time.sleep(0.5)     # 模拟耗时操作
    return a + b

result = slow_add(3, 4)
# 这里调用 slow_add ，slow_add传到timer，再传到warpper里面运行，之后再把结果换回去
print("结果:", result)   # 期望: 先打印耗时，再打印 结果: 7
