

# 定义一个列表 List
my_list = ["happy", "happy", "happy"]
print (my_list)
print(type(my_list))

# 定义一个嵌套列表
my_lsits = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(my_lsits)
print(type(my_lsits))

mylist = ["python", "java", "ruby","c++","css"]
index = mylist.index("java")
print(index)
mylist[0] = "html"
print(mylist)
mylist.insert(1,"JS")
mylist.append("C")
print(mylist)

mylist2 = [1,2,3,4,5,6,7,8,9]
mylist.extend(mylist2)
print(mylist)