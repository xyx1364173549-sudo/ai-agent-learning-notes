class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # print(stu)  # 结果是内存地址
    # print(str(stu))

    # __str__ 魔术方法
    def __str__(self):
        return f"Student类对象，name:{self.name}, age:{self.age}"

    # __lt__ 魔术方法
    def __lt__(self, other):
        return self.age < other.age
        # 当前的年龄，和被比较的年龄

    # __le__ 魔术方法
    def __le__(self, other):
        return self.age <= other.age

    # __eq__ 魔术方法
    def __eq__(self, other):
        return self.age == other.age
    # 没有这个方法比较的事内存地址


stu = Student("xyx", 18)
stu2 = Student("xyl", 17)
print(stu)
print(stu < stu2)
print(stu >= stu2)
print(stu == stu2)
