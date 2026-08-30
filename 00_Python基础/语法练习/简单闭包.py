# def outer(loge):
#     def inner(msg):
#         print(f"<{loge}>{msg}<{loge}>")
#
#     return inner
#
#
# fn1 = outer("hello")
# fn1("AAAA")
# fn1("BBBBB")
# fn2 = outer("world")
# fn2("AAAA")
# fn2("BBBBB")

# 使用nonlocal关键字修改外部函数的值

# def outer(num1):
#     def inner(num2):
#         nonlocal num1
#         num1 += num2
#         print(num1)
#
#     return inner
#
#
# fn = outer(10)
# fn(10)
# fn(10)


# 使用闭包实现ATm的小案例
def account_create(amount=0):
    def atm(num, deposit=True):
        nonlocal amount
        if deposit:
            amount += num
            print(f"存款：+{num},账户余额：{amount}")
        else:
            amount -= num
            print(f"存款：-{num},账户余额：{amount}")

    return atm


atm = account_create()
atm(100)
atm(200)
atm(100, deposit=False)
