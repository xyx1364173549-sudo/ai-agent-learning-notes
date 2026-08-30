# 构造方法__init__()

class Student:
    # name = None
    # age = None
    # tel = None

    def __init__(self, name, age, tel):
        self.name = name
        self.age = age
        self.tel = tel
        print("已自动运行")


stu = Student("xyx", 24, 13119580451)
