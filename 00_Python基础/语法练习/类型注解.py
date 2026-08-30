# 基础数据类型注解
import json_demo
import random

from pandas._libs import json


# var_1: int = 1
# var_2: str = "xyx"
# var_3: bool = True


# 类对象类型注解
class Student:
    pass


stu: Student = Student()

# 基础容器类型注解
# my_list: list = [1, 2, 3]
# my_tuple: tuple = (1, 2, 3)
# my_dict: dict = {'a': 1}

# 容器类型详细注解
my_list: list[int] = [1, 2, 3]
my_tuple: tuple[int, str, bool] = (1, "xyx", True)
my_dict: dict[str, int] = {"xyx": 222}

# 在注释中进行类型注释
var_1 = random.randint(1, 10)  # type:int
var_2 = json.ujson_loads('{"name":"xyx"}')  # type:dict[str,str]


def func():
    return 10


var_3 = func()  # type:int
