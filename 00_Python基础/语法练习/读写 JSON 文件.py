import json

data = {"name": "小明", "age": 25, "vip": True}

with open("user.json", "w", encoding="utf-8") as f:
    #  把"用户"这个字典  →  写入到文件对象"f"中
    json.dump(data, f, ensure_ascii=False, indent=2)
with open("user.json", "r", encoding="utf-8") as f:
    data_1 = json.load(f)
    print(data_1["name"])
    print(data_1)
