def test_func(compute):
    result = compute(1,2)
    print(result)

def add(x,y):
    return  x+y
test_func(add)

# 匿名函数
test_func(lambda x,y:x+y)