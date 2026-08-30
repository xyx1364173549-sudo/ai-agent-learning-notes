# 两个列表合并成字典
键 = ["name", "age", "city"]
值 = ["小明", 25, "北京"]
# zip 配对后直接转字典
用户 = dict(zip(键, 值))
print(用户)
# 两个列表一拉，直接变字典。

# 同时遍历值值和键
for key, value in zip(用户.keys(), 用户.values()):
    print(f"{key}: {value}")

# 矩阵转置（二维列表行列互换）
矩阵 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
# 用 zip 把行变成列
转置 = list(zip(*矩阵))
# *矩阵 表示把矩阵"展开"成三个独立列表传给 zip
print(转置)
# zip 的反向操作：解压
# zip 配合 * 可以做"解压"——把配对的元组拆回独立列表
lists = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
# *配对 把列表展开成三个元组传给 zip
# 等价于 zip(("Alice", 25), ("Bob", 30), ("Charlie", 35))
名字, 年龄 = zip(*lists)
print(名字)
print(年龄)
# zip 是"合并"，zip(*) 是"拆分"。一个拉链拉上，一个拉开。
