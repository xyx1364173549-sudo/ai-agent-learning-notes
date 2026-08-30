class skl:
    def __init__(self, agent):
        self.agent = agent
        self.skjl = []

    def __enter__(self):
        print("开始记录")
        self.agent.jlz = True
        return self

    def jlz(self, nr):
        self.skjl.append(nr)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.agent.jlz = False
        self.agent.ls += self.skjl
        print(f"已保存 {len(self.skjl)} 条思考记录")


class Agent:
    def __init__(self):
        self.jlz = False
        self.ls = []

    def sk(self, wt):
        if self.jlz:
            return f"分析：{wt}"
        return "直接回答"


agent = Agent()

with skl(agent) as chain:
    chain.jlz("用户问了天气")
    chain.jlz("决定调用天气工具")
    result = agent.sk("今天天气")
    print(result)
