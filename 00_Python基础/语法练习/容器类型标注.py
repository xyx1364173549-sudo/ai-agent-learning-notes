def process(messages: list[str]) -> dict[str, int]:
    return {msg: len(msg) for msg in messages}


def get_points() -> tuple[float, float]:
    return 3.14, 2.71


a = process(["hello", "xyxyxl", "ai"])
print(a)
b = get_points()
print(b)
# Python 3.9 之后可以不用导入 typing，直接用小写的 list、dict、tuple
