import json

try:
    data = json.loads('{"name":"xyx","age":"25"')
    # 缺少右括号
except json.JSONDecodeError as e:
    print(f"JSON格式错误：{e}")
