import json

def read_config(filepath: str) -> dict:
    """
    读取 JSON 配置文件
    - FileNotFoundError: 打印 "配置文件不存在"，返回 {}
    - json.JSONDecodeError: 打印 "配置文件格式错误"，返回 {}
    - 成功: 返回解析后的 dict
    """
    # ↓ 在这里写你的代码
    try:
        with open(filepath,"r",encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("配置文件不存在")
        return {}
    except json.JSONDecodeError:
        print("配置文件格式错误")
        return {}


# 测试代码
print(read_config("不存在.json"))     # 期望 {} + 提示
print(read_config("config.json"))     # 期望 正常读取（config.json 你已经有了！）
