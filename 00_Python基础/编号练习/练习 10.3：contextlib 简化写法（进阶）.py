from contextlib import contextmanager
import time

# TODO: 用 @contextmanager 装饰器实现 timer
# 用法和 10.2 一样，但不用写类！
# 结构：
#   @contextmanager
#   def timer():
#       start = time.time()    # yield 之前 = __enter__
#       yield                  # 这里是 with 代码块
#       print(...)             # yield 之后 = __exit__
@contextmanager
def timer():
    start = time.time()
    yield
    print(f"耗时 {time.time() - start:.3f} 秒")
    # end = time.time()
    # print(end - start)

# 用@contextmanager，其实就是让函数更加的精简易看是吧，本质上就是__enter__和__exit__的精简版
# 测试代码
with timer():
    sum(range(1000000))
