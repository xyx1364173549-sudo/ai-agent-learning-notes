class Config:
    """
    TODO: 实现 Config 类
    - __init__(data: dict): 保存配置数据
    - __getitem__(key): 支持 config["key"] 访问
    - __setitem__(key, value): 支持 config["key"] = value 赋值
    - __contains__(key): 支持 "key" in config
    - __repr__: 返回格式化的配置内容
    - keys(): 返回所有键
    """
    # ↓ 在这里写你的代码
    def __init__(self,data:dict):
        self.data = data
    def __getitem__(self, key:str):
        return self.data[key]
    def __setitem__(self,key:str,value:int):
        self.data[key] = value
        return self.data[key]
    def __contains__(self,key:str):
        if key in self.data:
            return True
        return False
    def __repr__(self):
        return str(self.data)

    def keys(self):
        return self.data.keys()

# 测试代码
config = Config({"model": "gpt-3.5", "temperature": 0.7})

print(config["model"])        # gpt-3.5
config["max_tokens"] = 1000   # 支持赋值
print(config["max_tokens"])   # 1000
print("model" in config)      # True
print("api_key" in config)    # False
print(config.keys())          # 包含 model, temperature, max_tokens
print(config)                 # 能打印出内容（__repr__）
