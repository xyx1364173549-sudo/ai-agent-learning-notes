# 洗数据

Adata = ["  Alice ", "", "  Bob  ", "\n", "Charlie"]
# 去空格+过滤空值
Bdata = [s.strip() for s in Adata if s.strip()]
print(Bdata)

# s.strip() 去除每个元素首位空白  if s.strip（）筛选哪些去掉空白元素的空元素


# 提取指定字段 API返回数据处理
Json = {
    "list": [
        {"date": "07-27", "temp": 32, "weather": "晴"},
        {"date": "07-28", "temp": 28, "weather": "多云"},
        {"date": "07-29", "temp": 25, "weather": "暴雨"},
    ]
}

my_list = [{"日期": a["date"], "温度": a["temp"]} for a in Json["list"]]
print(my_list)

# 构建ID查找表 - 避免循环查库
UserList = [
    {"id": 101, "name": "小明", "vip": True},
    {"id": 102, "name": "小红", "vip": False},
    {"id": 107, "name": "小刚", "vip": True},
]
# 构建 {id: 用户对象} 查找
id_cz = {u["id"]: u for u in UserList}
print(id_cz[101]["name"])
