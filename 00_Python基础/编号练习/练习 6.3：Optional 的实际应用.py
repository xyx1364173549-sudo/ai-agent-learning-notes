def get_config(key:str, config_dict:dict)->str|int|bool|None:
    """
    从 config_dict 中获取 key 对应的值
    - 存在: 返回值（value 类型可以是 str/int/bool → 用 Any 或 object）
    - 不存在: 返回 None
    注解返回值类型为 Optional[...] 或 ... | None
    """
    return config_dict.get(key)  # dict.get() 找不到就返回 None

# 测试
config = {"model": "gpt-3.5-turbo", "max_tokens": 1000}
print(get_config("model", config))        # gpt-3.5-turbo
print(get_config("temperature", config))  # None
