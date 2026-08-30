# 使用Union类型，必须先导包
from typing import Union

my_list: list[Union[int, str]] = [1, 2, "hello"]


def func(data: Union[int, str]) -> Union[int, str]:
    pass


func(1)
func("hello")
