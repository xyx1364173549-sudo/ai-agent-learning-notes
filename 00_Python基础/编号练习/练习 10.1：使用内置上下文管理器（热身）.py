# TODO 1: 用 with open 读取 config.json 并打印内容（记得 encoding="utf-8"）
# TODO 2: 用 with open 写入一个文件 data.txt，内容 "hello world"
#         然后重新读取验证写入成功


with open("config.json",encoding="utf-8") as f:
    data = f.read()
    print(data)

with open("data.txt","w",encoding="utf-8") as f:
    f.write("hello world")
with open("data.txt","r",encoding="utf-8") as f:
    data = f.read()
    print(data)
