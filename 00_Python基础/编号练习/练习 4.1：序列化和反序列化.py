import json

data = {
    "agent_name": "WeatherBot",
    "version": 1.0,
    "tools": ["search", "forecast"],
    "config": {"timeout": 10, "retries": 3}
}

# TODO 1: 将 data 转换为格式化的 JSON 字符串（ensure_ascii=False, indent=2）
# TODO 2: 将 JSON 字符串转回 Python 对象（json.loads）
# TODO 3: 将 data 写入文件 config.json
# TODO 4: 从 config.json 读取并验证数据一致

data= json.dumps(data,ensure_ascii=False,indent=2)
print(data)

data = json.loads(data)
print(data)

with open("config.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)

with open("config.json","r",encoding="utf-8") as g:
    loaded=json.load(g)
    print(loaded)
