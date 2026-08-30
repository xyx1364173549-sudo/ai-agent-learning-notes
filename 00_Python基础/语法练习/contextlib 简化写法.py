from contextlib import contextmanager


@contextmanager
def timer():
    import time
    ks = time.time()
    print("开始")
    yield
    a = time.time() - ks
    print(f"耗时{a:.6f}s")


with timer():
    total = sum(i ** 2 for i in range(1_000_000))
    print(f"计算完成: {total}")
