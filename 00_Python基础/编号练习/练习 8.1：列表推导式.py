numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# TODO 1: 生成 squares = [1, 4, 9, 16, ..., 100]
# TODO 2: 生成 evens = [2, 4, 6, 8, 10]（只保留偶数）
# TODO 3: 生成 labels = ["1-奇", "2-偶", "3-奇", ..., "10-偶"]（if-else 放前面！）

squares = [n**2 for n in numbers]
print(spuares)

evens = [n for n in numbers if n % 2 == 0]
print(evens)

labels = [f"{n}-偶" if n % 2 == 0 else f"{n}-奇" for n in numbers]
print(labels)


# if 放在最后 = 过滤（决定要不要）
# if-else 放在前面 = 选择（决定取哪个值）
