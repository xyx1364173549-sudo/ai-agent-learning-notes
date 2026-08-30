class Student:
    name = None

    def say(self):
        print(f"大家好，我是{self.name}")

    def say2(self, msg):
        print(f"大家好，我是{self.name},{msg}")


stu = Student()
stu.name = "xyx"
stu.say()

stu2 = Student()
stu2.name = "xyx"
stu2.say2("AAABBB")
