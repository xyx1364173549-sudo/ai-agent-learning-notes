from test import word

Fruits = ["苹果", "香蕉", "橙子"]

# 默认从零开始
for i, fruit in enumerate(Fruits):
    print(i, fruit)
# 从1开始
for i, fruit in enumerate(Fruits, start=1):
    print(i, fruit)

# 根据位置修改列表
data = [10, -5, 20, -8, 30]
for i, num in enumerate(data):
    if num < 0:
        data[i] = 0

print(data)

# 构建“值->索引”查找表

words = ["apple", "banana", "cherry"]

index_map = {word: idx for idx, word in enumerate(words)}

print(index_map["cherry"])
