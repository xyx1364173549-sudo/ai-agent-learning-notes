import json


def build_prompt(system_msg: str, user_msg: str, temperature: float = 0.7) -> str:
    """
    返回格式化的 JSON 字符串，像这样:
    {
      "system": "你是一个助手",
      "user": "你好",
      "temperature": 0.70
    }

    要求:
    1. 使用 ensure_ascii=False 保留中文
    2. 使用 indent=2 美化缩进
    """
    # ↓ 在这里写你的代码

    data = {
        "system":"system_msg",
        "user": "user_msg",
        "temperature": temperature
    }
    return json.dumps(data,ensure_ascii=False,indent=2)


a = build_prompt("你是一个助手", "你好", 0.7)
print(a)
