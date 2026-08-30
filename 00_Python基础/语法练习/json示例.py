import json

# 序列化
data = {"name": "助手", "tools": ["search", "calc"], "enabled": True}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
# ensure_ascii=False: 保留中文（默认会转成 \uXXXX）
# indent=2: 美化缩进，便于阅读
print(json_str)

# 反序列化
parsed = json.loads(json_str)
print(parsed["name"])  # 助手

# 写入文件（配合 with）
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 从文件读取
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded)
