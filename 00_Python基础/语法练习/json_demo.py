# 带S的操作字符串，不带S的操作文件
# 序列化：Python->字符串
import json

User = {
    "name": "小明",
    "age": 25,
    "vip": True,
    "余额": None,
    "tags": ["python", "ai"]
}
# 转换成为Json字符串
# ✅ 加 ensure_ascii=False 保留中文
# ✅ 加 indent=2 美化输出
# ✅ 加 sort_keys=True 让键按字母排序
json_str = json.dumps(User, ensure_ascii=False, indent=2, sort_keys=True)

print(json_str)

# 反序列化：json字符串->python对象
User_1 = json.loads(json_str)
print(User_1)
# json.loads() 自动完成类型转换：true → True、null → None。
