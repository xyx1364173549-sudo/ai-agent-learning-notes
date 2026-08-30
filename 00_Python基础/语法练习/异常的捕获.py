

# 基本的捕获语法
# try:
#     f = open("C:/Document/演示.txt","r",encoding="utf-8")
# except:
#     f = open("C:/Document/演示.txt", "w", encoding="utf-8")


try:
    print(name)
    # 1/0
except NameError as e:
    print("变量未定义")
    print(e)

try:
    # 1/0
    print(se)
except (NameError,ZeroDivisionError) as e:
    print("出现了变量未定义 或者除以0的异常错误")


# except Exception as e   捕获所有的异常，和
# except:是一样的