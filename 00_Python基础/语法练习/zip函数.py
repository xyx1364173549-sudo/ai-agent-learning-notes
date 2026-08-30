names = ["Alice", "Bob", "Charlie"]
ages = [20, 30, 40]

# zip 写法
# zip 把两个列表按位置配对，每对组成一个元组。for 循环自动解包到 name 和 age。
# for name, age in zip(names, ages):
#     print(f"{name}今年{age}岁")
result = zip(names, ages)
print(result)
# 转成列表看清楚结构
print(list(result))

# 核心规则：以最短的为准；
# zip 永远以最短的那个列表为准。 多出来的元素直接丢弃。
# 如果想保留所有元素：用 itertools.zip_longest
