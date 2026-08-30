# 类


class Student:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address


total = 10

for i in range(1, total + 1):
    print(f"\n当前录入第{i}位学生信息，共需录入{total}位学生信息")
    name = input("请输入姓名")
    age = input("请输入年龄")
    address = input("请输入地址")
    student = Student(name, age, address)
print(f"学生{i}信息录入完成，信息为：【学生姓名：{student.name}，"
      f"年龄：{student.age}，地址：{student.address}】")
