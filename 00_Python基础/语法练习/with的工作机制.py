# 自定义上下文管理器 —— 让你自己的类支持 with

class MyTimes:
    def __enter__(self):
        import time
        self.start = time.time()
        print("开始计时")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.end = time.time()
        hs_time = self.end - self.start
        print(f"耗时{hs_time:.6f}s")


with MyTimes() as t:
    tol = sum(i ** 2 for i in range(10000))
    print(f"计算完成{tol}")
