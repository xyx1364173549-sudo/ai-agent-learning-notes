def fibonacci(n: int):
    """
    TODO: 生成前 n 个斐波那契数
    序列: 1, 1, 2, 3, 5, 8, 13, ...
    规则: 每个数 = 前两个数之和
    使用 yield 逐个产出
    """
    # ↓ 在这里写你的代码
    a,b= 1,1
    for i in range(n):
        yield a
        a,b = b,a+b

    # 提示:
    # a, b = 1, 1
    # for i in range(n):
    #     yield a
    #     a, b = b, a + b
    pass


# 测试代码
for num in fibonacci(8):
    print(num, end=" ")    # 期望: 1 1 2 3 5 8 13 21
