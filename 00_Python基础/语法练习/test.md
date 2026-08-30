Python 允许同时为多个变量赋值
# a = b = c = 1
也可以，为多个变量同时指定不同的值
# a,b,c = 1,2,runoob


关于数据类型
有六种
Number（数字）
String（字符串）
bool（布尔类型）
List（列表）
Tuple（元组）
Set（集合）
Dictionary（字典）
不可变数据（4 个）：Number（数字）、String（字符串）、bool（布尔）、Tuple（元组）
可变数据（3 个）：List（列表）、Dictionary（字典）、Set（集合）

type（）函数用来查询变量所指的对象数据类型
还可以用isinstance（）


bool 是int 的子类
True 和 False可以和数字相加 会返回True

反斜杠\可作为续航符，表示下一行是上一行的延续

Python的字符串是不一样的，列表中的元素是可以更改的

元组  与列表类似，不同之处是元组不可以修改 ，元组写在（）里 # 一个元素，需要元素后面加逗号  tup = (20,)


append 添加列表项
del 删除列表元素
len（） 长度
3 in【1,2,3】 元素是否在列中


operator.it(a,b) :a < b
operator.le(a,b) :a <= b
operator.eq(a,b) :a == b
operator.ne(a,b) :a != b 

字典  ，一种可变容器 ，可以存储任意类型的对象
tinydict = {'name': 'runoob', 'likes': 123, 'url': 'www.runoob.com'}

集合  ，无序的不重复元素序列

