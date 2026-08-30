class Phone:
    __is_5g_enabled = False

    def __check_5g(self):
        if self.__is_5g_enabled:
            print("5G 开启")
        else:
            print("5G 关闭，使用4G")

    def call_by_5g(self):
        self.__check_5g()
        print("正在通话中！")


phone = Phone()
phone.call_by_5g()
