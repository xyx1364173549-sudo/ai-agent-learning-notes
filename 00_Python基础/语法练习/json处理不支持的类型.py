# JSON 不支持datatime，set，自定义类

# A方案
from datetime import datetime
import json

User = {
    "name": "小明",
    "注册时间": datetime.now()
}
# Object of type datetime is not JSON serializable
# 如果没有手动转换字符串就是出现上面的报错
User["注册时间"] = User["注册时间"].isoformat()

try:
    a = json.dumps(User, ensure_ascii=False)
    print(a)
    # Object of type datetime is not JSON serializable
except Exception as e:
    print(e)


# 方案B 自定义defaul函数

def ota(obj):
    if isinstance(obj, datetime):
        # isinstance()函数-来判断一个对象是否是一个已知的类型，返回bool值
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    raise TypeError(f"不支持序列化的类型：{type(obj)}")


MyUser = {
    "标签": {"python", "ai"},
    "注册时间": datetime.now()
}

b = json.dumps(MyUser, ensure_ascii=False, default=ota)
print(b)
