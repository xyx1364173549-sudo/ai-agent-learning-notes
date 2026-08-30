default_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
}
user_config = {
    "temperature": 0.9,
    "max_tokens": 2000
}

# TODO: 用 user_config 覆盖 default_config 中的同名键，保留其他默认值
# 预期结果:
# {"model": "gpt-3.5-turbo", "temperature": 0.9, "max_tokens": 2000}

# 提示: 想想 {**default_config, **user_config} 或者 update() 的用法

# 解包合并
merged = {**default_config,**user_config}
print(merged)
# updata()
default_config.update(user_config)
print(default_config)
