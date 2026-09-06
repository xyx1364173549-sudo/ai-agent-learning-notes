# 3.3 Agent 评测体系 · 详细版

> 本节是阶段三"工程化"的第三枪：解决"**你的 Agent 到底有多好？**"这个问题。学完你要能回答——评测和手工测试差在哪？两个指标各考什么？为什么"满分"反而要警惕？怎么从 LLM 返回里抠出它选了哪个工具？

---

## 一、总结

**一句话概括**：

> **评测（evaluation）= 把"写死几个场景、肉眼盯输出"的土办法，升级成"出一张固定卷子 + 机器自动批改 + 算出分数"。核心是三个标准动作：① 固定输入（题目写死，不靠 LLM 随机出题）② 多轮取平均（跑 N 次，对抗 LLM 随机性）③ 微妙用例（造"难判"的题，考真实判断力）。**

### 痛点：手工测试的三个致命伤

| 手工测试 | 后果 |
|---|---|
| 在 `__main__` 写死 3 个场景，肉眼盯输出 | **不可重复**：改一行代码又得重新肉眼确认 |
| "我感觉还行" | **没数字**：别人问"你这 Agent 多好"，说不出一个百分比 |
| 只测了 3 个场景 | **会漏**：还有几十种情况没试 |

**类比**：手工测试 = 老师一次出一道题，肉眼看对错（累死）；自动评测 = 出一张卷子（20 道），机器自动批改，算出**分数**。

### 为什么 Agent 时代这事重要

大厂 Agent 岗面试必问"你怎么证明你的 Agent 好？"——答案不是"我感觉挺准"，而是"我做了 14 条评测集，端到端成功率 100%（3 轮取平均），工具选择准确率 8/8"。**有数字 = 工程能力的直接证明**，这也是论文第 7 章"实验"的地基。

---

## 二、对应知识点

### 3.3.1 评测三件套

| 三件套 | 作用 | 类比 |
|---|---|---|
| **评测集（试卷）** | 一堆用例，每条 = 固定输入 + 期望结果 | 老师出的卷子 |
| **执行器（做题）** | 把每条用例喂给 Agent，拿到实际输出 | 学生做题 |
| **打分器（批改）** | 对比"期望 vs 实际"，算成功率 | 老师批卷子 |

关键设计：**评测集里题目和答案是写死的**，不靠 LLM 随机出题——评测要的是"可重复"，随机性会污染结果。

### 3.3.2 两个指标，各考一件事

| 指标 | 评谁 | 通俗问法 | 怎么算 |
|---|---|---|---|
| **端到端成功率** | 数学辅导 Agent（`multi_agent.py` 的 `eval_node`） | "整张卷子做对几道？" | 判对的用例 ÷ 总用例 |
| **工具选择准确率** | 天气/计算 Agent（`mini_agent.py`） | "该用锤子还是扳手，选对几道？" | 选对工具的用例 ÷ 总用例 |

更细：**端到端看"结果"**（答案最终对不对），**工具选择看"过程里选工具这一步"**（该动手时选对工具没）。

### 3.3.3 固定输入（评测的"可重复"前提）

评测集里题目写死，不靠 LLM 随机出题。这跟你 2.6 里"场景 C 固定题目才能稳定走通 plan 分支"是同一个道理——**评测要可重复，随机性会污染结果**。

### 3.3.4 ⭐ 多轮取平均（对抗 LLM 随机性）

`eval_node` 内部调 LLM，而 LLM 有随机性（temperature 采样）。所以：

> **跑 1 次 = 得到一个"数字"；跑 N 次 = 得到一个"可信的数字"。前者是彩票，后者是数据。**

**骰子类比**：掷 1 次出 6，不能说"这骰子总出 6"；掷 30 次，才能说"概率约 1/6，骰子公平"。

代码：

```python
def evaluate(rounds=3):
    rates = []
    for i in range(rounds):
        correct = 0
        total = len(CASES)
        for topic, question, answer, expected in CASES:
            actual = run_case(topic, question, answer)
            if actual == expected:
                correct += 1
        rate = correct / total
        rates.append(rate)
        print(f"第 {i+1} 轮：{correct}/{total}")
    avg = sum(rates) / len(rates)
    print(f"平均成功率：{avg:.0%}（{rounds} 轮取平均）")
```

**关键认知**：跑 N 次不是要改变数字（可能还是 100%），而是给你"**这个数字可不可信**"的判断力。你的数学判对错任务确定性高（对就是对错就是错），3 轮都满分正常；但换成"作文写得好不好"这类主观题，随机性就大了，多轮取平均从"多余"变成"必须"。

### 3.3.5 ⭐ 微妙用例（考真实判断力，别只考"1+1=2"）

**满分有两种可能：① 学生真是学霸 ② 卷子只考了"1+1=2"。**

你最初的 10 条用例全是"非黑即白"（正确答案写满过程，错误答案错得离谱），LLM 闭眼都能满分——**测不出真实判断力**。要构造"难判"的边界用例：

| 类型 | 例子 | 考什么 |
|---|---|---|
| **漏根** | `x²-4=0` 只写 `x=2`，漏了 `x=-2` | 会不会被"部分正确"蒙骗 |
| **符号反** | `(x+2)(x+3)`（数字 2+3=5、2×3=6 都对，符号全错） | 会不会被"过程像模像样"蒙骗 |
| **方法不同** | 用求根公式而非因式分解，结果对 | 会不会误杀"非标准解法" |
| **过程简略** | 答案对，没写展开过程 | 会不会误杀"过程太短" |

工具选择的微妙用例同理——考的是**模糊边界**：

| 用例 | 陷阱 | 考什么 |
|---|---|---|
| `明天适合去爬山吗` | 没提"天气"，但爬山要看天气 | 能不能透过字面看意图 |
| `今天出门要带伞吗` | "带伞"隐含"下雨" | 能不能做语义联想 |
| `北京到上海有多远` | 两个工具都不匹配 | 会不会没工具也硬凑 |

**前两类考"该调时联想到"，后一类考"不该调时忍住"**——这是工具选择的两个对立方向。加进去后成功率会掉，**掉下来的那几题，才是你 Agent 真正的短板**。

### 3.3.6 ⭐ tool_calls 三层嵌套解析（工具选择的关键）

LLM 选工具时，返回的 `msg` 长这样（嵌套很深）：

```python
msg = {
    "role": "assistant",
    "content": None,              # 调工具时不写正文
    "tool_calls": [               # 第①层：列表（可能调多个工具）
        {
            "id": "call_xxx",
            "type": "function",
            "function": {         # 第②层：字典（函数信息）
                "name": "get_weather_tool",   # 第③层：字符串（工具名）
                "arguments": '{"city": "北京"}'
            }
        }
    ]
}
```

**为什么三层？** 因为 OpenAI 协议规定：一次回复可能**并行调多个工具**（所以最外层用**列表**装）；每个工具调用又有一堆属性 id/type/function（所以用**字典**）；function 里又有 name/arguments（所以再套一层**字典**）。

**核心口诀**：看它是列表还是字典，决定用什么符号取——

- 遇到**列表** → 用 `[数字]` 下标
- 遇到**字典** → 用 `["字符串"]` 键

所以 `tool_calls[0]["function"]["name"]` = **「下标 → 键 → 键」交错钻三层**。

**你代码里的保护**：

```python
tool_calls = msg.get("tool_calls")   # 没调工具时拿到 None
if tool_calls:                        # None 是"假"，跳过
    return tool_calls[0]["function"]["name"]
else:
    return None                       # 闲聊，没调工具
```

`if tool_calls:` 是"先确认有包裹，才拆箱"——因为"你好"这种闲聊，`msg` 里压根没有 `tool_calls` 这个 key，`.get()` 返回 None，直接 `[0]` 会报 `TypeError`。

**三个易错点**：

| 错误写法 | 报错 | 原因 |
|---|---|---|
| `tool_calls["name"]` | `TypeError: list indices must be integers` | 列表不能用字符串下标 |
| `tool_calls[0]["name"]` | `KeyError: 'name'` | `[0]` 那层没有 name，它藏在 function 里 |
| 不判断直接 `tool_calls[0]` | `TypeError: 'NoneType'...` | 没调工具时是 None |

---

## 三、测试验收

### 验收 1：端到端成功率（✅ 跑通，3 轮取平均 100%）

```powershell
cd C:\Document\agent_project
python eval_agent.py
```

输出：

```
第 1 轮：14/14
第 2 轮：14/14
第 3 轮：14/14
平均成功率：100%（3 轮取平均）
```

14 条用例（10 条基础 + 4 条微妙），3 轮全对 → **端到端成功率 100% 可信**。

### 验收 2：工具选择准确率（✅ 单次 8/8，⚠️ 3 轮平均待补）

```powershell
python eval_tool.py
```

输出：

```
√ 北京天气怎么样 -> get_weather_tool
√ 帮我算 3 * 5 -> calculator_tool
√ 你好 -> None
...
工具选择准确率：100%（8/8）
```

8 条用例（天气 3 + 数学 3 + 闲聊 2）单次全对。**但这是单次结果 + 含送分题（"你好/谢谢"闭眼都对）**，有水分的数字。已提供"加 3 条微妙用例 + evaluate 跑 3 轮"的改造代码，⚠️ **待补跑**（本节收尾时选择直接进入下一任务，此步留作课后补跑）。

---

## 四、本节踩坑清单

| # | 坑 | 表现 | 根治 |
|---|---|---|---|
| 1 | **PythonWin 编辑器偷偷加脏代码** | 文件里冒出 `from pywin.debugger import fail`，import 失败**静默退出**（啥也不打印） | 别在 PythonWin 写代码，用 PyCharm；运行用 `python 文件名.py` 或 PyCharm 的 ▶ |
| 2 | **TODO 判定缺 else** | `if mastery>=0.7 ... elif mastery<0.5`，中间 `[0.5,0.7)` 返回 None，被误判成 fail | 阈值判定要**兜底**：`>=0.7 算 pass，其余一律 fail`（用 else） |
| 3 | **满分要警惕** | 10/10、8/8 全对，其实用例都是"非黑即白"送分题 | 加**微妙用例**（漏根/符号反/方法不同/模糊指令），看成功率会不会掉 |
| 4 | **单次结果不可信** | 一次 14/14 就下结论 | 跑 **N 轮取平均**，对抗 LLM 随机性 |
| 5 | **tool_calls 三层嵌套抠错** | 列表用字符串下标、漏 function 层、None 不判断 | 口诀：列表用 `[0]`、字典用 `["key"]`，先 `if tool_calls` 判断 |
| 6 | **双击 .py 弹出 PythonWin** | 双击文件不是运行，是打开 PythonWin IDE | 用 PowerShell 跑 `python 文件名.py`，或 PyCharm 点 ▶ |

---

## 五、论文定位（答辩话术）

- **第 7 章实验的地基**：消融实验、量化指标全靠评测体系——"我做了一套评测集（端到端成功率 + 工具选择准确率），3 轮取平均，结果可复现"，这是论文"实验"章节的规范性核心。
- **简历硬通货**：能说出"我用评测集量化了 Agent 质量，而不是'我感觉还行'"，证明你是**工程化**的人，不是只会写 demo。
- **面试话术**：能答出"评测三件套""为什么满分要警惕（送分题）""为什么跑 N 次取平均（LLM 随机性）""tool_calls 是列表套字典套字典"，这是大厂 Agent 岗评测方向的真实考点。

---

## 六、代码骨架速查

```python
# eval_agent.py —— 端到端成功率（评 multi_agent 的 eval_node）
from multi_agent import eval_node

CASES = [  # 固定输入 + 期望（含微妙用例）
    ("因式分解", "把 x²-4 因式分解", "x²-4 = (x+2)(x-2)...", "pass"),
    ("二次方程", "解方程 x²-4=0", "x=2", "fail"),   # 漏根
    # ...
]

def run_case(topic, question, answer):
    result = eval_node({"topic": topic, "question": question,
                        "student_answer": answer, "round": 0})
    return "pass" if result["mastery"] >= 0.7 else "fail"

def evaluate(rounds=3):   # 跑 N 轮取平均
    ...
```

```python
# eval_tool.py —— 工具选择准确率（评 mini_agent 的 Function Calling）
from mini_agent import chat_with_tools, SYSTEM_PROMPT

NO_TOOL = None
CASES = [("北京天气怎么样", "get_weather_tool"), ("你好", NO_TOOL), ...]

def run_case(user_input):
    msg = chat_with_tools([{"role": "system", "content": SYSTEM_PROMPT},
                           {"role": "user", "content": user_input}])
    tool_calls = msg.get("tool_calls")
    if tool_calls:
        return tool_calls[0]["function"]["name"]   # 三层嵌套：列表→dict→dict
    return None
```

完整例子：`agent_project/eval_agent.py`、`agent_project/eval_tool.py`。
