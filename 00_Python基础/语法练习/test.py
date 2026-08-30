# 注释
print('Hello Python!')  # 注释
'''
多行
注释

'''
item_one = 1
item_two = 2
item_three = 3

total = item_one + \
    item_two + \
    item_three

print(total)

totals = ['item_1', 'item_2', 'item_3',
          'item_4', 'item_5']
print(totals)


'''
数字类型
int（整数）
bool（布尔）
float（浮点数）
complex（复数）

'''


word = '字符串'
sentence = "这是一个句子。"
paragraph = """这是一个段落，
可以由多行组成"""


str = '123456789'
print(str)
print(str[0:-1])
print(str[0])
print(str[3:])
print(str * 2)
print(str[::2])  # 步长为二
print('\n')  # 输出空行
print(r'\n')  # 输出 \n


# input('\n\n 按下 enter 键后退出')


# print默认换行
# 不换行输出
# print (x,end='')
print(str, end='')


a, b, c = 1, 2, "nb"
print(a)
print(b)
print('nb')
