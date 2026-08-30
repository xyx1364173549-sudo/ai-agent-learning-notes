# 一般写法
# def outer(func):
#     def inner():
#         print("我要睡觉了")
#         func()
#         print("我要起床了")
#
#     return inner
#
#
# def sleep():
#     import random
#     import time
#     print("睡眠中......")
#     time.sleep(random.randint(1, 3))
#
#
# fun = outer(sleep)
# fun()

# 快捷写法
def outer(func):
    def inner():
        print("我要睡觉了")
        func()
        print("我要起床了")

    return inner


@outer
def sleep():
    import random
    import time
    print("睡眠中......")
    time.sleep(random.randint(1, 3))


sleep()
