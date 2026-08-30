class tax:
    def __init__(self, 地区: str):
        self.taxs = {"北京": 0.15, "上海": 0.13, "深圳": 0.10}[地区]

    def __call__(self, 金额: float) -> float:
        return 金额 * self.taxs


BJ = tax("北京")
print(BJ(1000))
# 配置一次，调用多次
