num = [1, 2, 3, 4, 5, 6, 7, 8]

ou = list(filter(lambda n: n % 2 == 0, num))
print(ou)
# filter(判断函数, 可迭代对象)
#         ↑           ↑
#   返回True就保留   你要筛的数据
#   返回False就丢弃
# filter(None, ...)：快速去假值
# 当第一个参数是 None 时，filter 有特殊行为
数据 = [0, 1, "", "hello", False, True, None, [], [1, 2], {}, {"a": 1}]

# filter(None, ...) 只保留"真值"，自动滤掉所有假值
list(filter(None, 数据))
# [1, 'hello', True, [1, 2], {'a': 1}]
