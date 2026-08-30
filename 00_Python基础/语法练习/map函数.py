# map(函数, 可迭代对象)
#      ↑        ↑
#   对每个元素 你要处理的数据
#   调用这个函数
from enumerate函数 import words

data = [1, 2, 3, 4, 5]

Data = list(map(lambda n: n ** 2, data))
print(Data)
# map 返回的不是列表，是迭代器对象。只有当你遍历它（比如 list() 转换）时，才会执行函数计算。这就是"惰性求值"——不急着算，谁要才给谁算。
# map 的真正优势：配合现成函数

# 把字符串列表全转大写
words = ["hello", "word", "python"]
a = list(map(str.upper, words))
print(a)
# 把字符串列表全转成整数
输入 = ["1", "2", "3", "4", "5"]
b = list(map(int, 输入))
print(b)
# 把数字转成字符串
list(map(str, [1, 2, 3]))
# ['1', '2', '3']

# 取每个字符串的长度
list(map(len, ["apple", "banana", "cherry"]))
# [5, 6, 6]
