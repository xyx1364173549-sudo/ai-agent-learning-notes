from turtledemo.chaos import line

# f = open("C:/AI Document/CS2性能优化报告.txt","r",encoding="utf-8")
# print(type(f))

# 读取文件read（）
# print({f.read()})

# readlines（）
# lines = f.readlines()
# print(lines)

# for 循环读取文件行
# for line in f:
#     print(line)
#
# # 关闭文件
# f.close()

# with open ,会自动的将文件关闭
with open("C:/AI Document/CS2性能优化报告.txt","r",encoding="utf-8") as f:
   f.readline()
   print(f.readline())