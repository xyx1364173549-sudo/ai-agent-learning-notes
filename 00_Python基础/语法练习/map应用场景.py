# 数据清洗
data = ["25", "30", "  35  ", "28"]

lists = list(map(int, map(str.strip, data)))
# 内层 map(str.strip, 原始数据)  → ['25', '30', '35', '28']
# 外层 map(int, ...)              → [25, 30, 35, 28]
print(lists)
用户列表 = [
    {"name": "小明", "age": 25},
    {"name": "小红", "age": 30},
    {"name": "小刚", "age": 28},
]

# 提取每个用户的格式化字符串
list(map(lambda u: f"{u['name']}（{u['age']}岁）", 用户列表))
# ['小明（25岁）', '小红（30岁）', '小刚（28岁）']
