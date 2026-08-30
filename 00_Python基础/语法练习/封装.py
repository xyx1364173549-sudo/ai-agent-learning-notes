# 定义一个类，内含只有成员和私有成员方法
# 私有成员无法被类对象使用，但是可以被其他的成员使用
class Phone:
    __current_vol = 0.5  # 电压，私有的成员变量

    def __keep_single_core(self):
        print("让CPU以单核模式运行")

    def call_by_5g(self):
        if self.__current_vol >= 1:
            print("5g通话开始")
        else:
            self.__keep_single_core()
            print("电量不足，无法使用5g通话，并设置为单核模式")


phone = Phone()
# phone.__keep_single_core(
phone.call_by_5g()
# 私有的对象和方法，类对象是不可以直接使用的，类里的其他成员是可以直接使用的
