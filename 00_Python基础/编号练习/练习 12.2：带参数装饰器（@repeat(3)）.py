from functools import wraps

def repeat(times:int):


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            for i in range(times):
                print(f"---第{i+1}次执行")
                result = func(*args, **kwargs)
            # 这里似乎不用返回 result 也可以
        return wrapper
    return decorator



@repeat(3)
def say(message):
    print(message)



say("你好")
