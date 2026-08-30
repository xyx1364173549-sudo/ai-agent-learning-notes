


def fun1():
    print("fun1开始执行")
    num = 1/0
    print("fun1结束")

def fun2():
    print("fun2开始执行")
    fun1()
    print("fun2开始结束")

def main():
    try:
        fun2()
    except Exception as e:
        print(f"出现异常,异常信息是：{e}")


main()