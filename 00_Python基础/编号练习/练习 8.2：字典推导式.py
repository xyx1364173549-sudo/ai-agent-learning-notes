words = ["apple", "banana", "cherry", "date"]

# TODO 1: 生成长度映射 {"apple": 5, "banana": 6, ...}
# TODO 2: 生成首字母映射 {"a": "apple", "b": "banana", ...}
# TODO 3: 筛选长度 > 5 的单词 {"banana": 6, "cherry": 6}

T_1 = {n:len(n) for n in words}
print(T_1)

T_2 = {n[0]:n for n in words}
print(T_2)

T_3 = {n : len(n) for n in words if len(n) > 5 }
print(T_3)
