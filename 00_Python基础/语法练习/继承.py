# 单继承
class Phone:
    IMEI = None
    producer = "xm"

    def call_by_4g(self):
        print("4G 通话")


class Phone2022(Phone):
    face_id = "1000101"

    def call_by_5g(self):
        print("2022年：5G")


phone = Phone2022()
print(phone.producer)
phone.call_by_5g()
phone.call_by_4g()


# 多继承

class NFCReader:
    nfc_type = "5代"
    pro = "xm"

    def read_card(self):
        print("NFC读卡")

    def write_card(self):
        print("NFC写卡")


class ROMControl:
    rc_ty = "红外遥控"

    def control(self):
        print("打开")


class My_phone(Phone, ROMControl, NFCReader):
    pass  # 不想再添加新功能了，让语法不产生错误，无内容，空的意思


iph = My_phone()
iph.control()
iph.call_by_4g()
iph.write_card()
iph.read_card()
# 谁先继承谁的优先级最高
