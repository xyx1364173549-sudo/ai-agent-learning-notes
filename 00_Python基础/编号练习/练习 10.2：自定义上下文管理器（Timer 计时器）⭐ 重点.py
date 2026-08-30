import time


class Timer:
    """
    TODO: 实现 Timer 类
    - __enter__: 记录开始时间，返回 self
    - __exit__: 计算耗时并打印，返回 False（不吞异常）
    - elapsed: @property，返回耗时（秒）

    使用方式:
        with Timer() as t:
            sum(range(1000000))
        print(f"耗时 {t.elapsed:.3f} 秒")
    """
    # ↓ 在这里写你的代码
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        # print(f"耗时 {self.elapsed:.3f} 秒")
        return False
    @property   # 这三行没有看懂@property，是干什么用的，为什么还要在设置一个这样的函数，没有这个函数也可以啊
    def elapsed(self):
        return self.end - self.start

# 测试代码
with Timer() as t:
    total = sum(range(1000000))
print(f"耗时 {t.elapsed:.3f} 秒")
