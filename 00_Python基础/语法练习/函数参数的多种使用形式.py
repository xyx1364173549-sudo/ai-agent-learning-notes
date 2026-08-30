from os import name


def user_info(name,age,gender):
    print(f"姓名是：{name}，年龄是：{age},性别：{gender}")

# 位置传参
user_info('小明','13','男')
# 关键字传参
user_info(name='小欢',age='14',gender='女')
user_info('小话',age='14',gender='女')

# 缺省传参
def user_info(name,age,gender = '男'):
    print(f"姓名是：{name}，年龄是：{age},性别：{gender}")

user_info('小王',55)


# 不定长——
def user_info(*args):
    print(f"args参数的类型是：{type(args)},内容是：{args}")

user_info(1,2,3,'xjsda',True)

def user_info(**kwargs):
    print(f"args参数的类型是：{type(kwargs)},内容是：{kwargs}")

user_info(name = 'sds',age=45,gender='s4s')
