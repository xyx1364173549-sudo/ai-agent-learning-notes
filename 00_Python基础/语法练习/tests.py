a, b, c, d = 20, 5.5, True, 4+3j
print(type(a), type(b), type(c), type(d))
isinstance(a, int)


var1 = 1
print(var1)
del var1
# print(var1)


my_list = ['abc', '786', 'runboo', 70.2]
tinylist = [123, 'tun']
print(my_list + tinylist)


r = [1, 2, 3, 4, 5, 6, 7]
r[0] = 9
r[2:5] = [13, 14, 15]
print(r)
