import time

# 打开文件 ,文件不存在，W 模式会帮忙创建,文件存在 会覆盖文件里原有的内容
f = open("C:/Document/ruabbish.txt","w",encoding="utf-8")
# wirte 写入
f.write("Hello Python !!!")
# time.sleep()

# flush 刷新
f.flush()
# clos关闭
f.close()

