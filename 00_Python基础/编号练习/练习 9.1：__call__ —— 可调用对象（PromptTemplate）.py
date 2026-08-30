class PromptTemplate:
    """
    TODO: 实现 PromptTemplate 类
    - __init__(template: str): 保存模板，如 "你好 {name}，我是 {role}"
    - __call__(**kwargs): 用 kwargs 填充模板并返回结果

    示例:
        t = PromptTemplate("你好 {name}，我是 {role}")
        t(name="小轩轩", role="助手")  # → "你好 小轩轩，我是 助手"
    """
    # ↓ 在这里写你的代码
    def __init__(self,template:str):
        self.template = template

# 我好像还是没有理解，上面的段代码的含义，好像是面向对象，封装的原因吧,是初始化字符串吗🥲


    def __call__(self,**kwargs):
        return self.template.format(**kwargs)

# 测试代码
t = PromptTemplate("你好 {name}，我是 {role}")
print(t(name="小轩轩", role="助手"))
print(callable(t))
