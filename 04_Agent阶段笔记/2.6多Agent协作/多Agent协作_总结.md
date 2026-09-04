# 2.6 多 Agent 协作（导师 / 出题 / 评估 / 规划）· 详细版

> 本节是阶段二从"单 Agent"跨向"多 Agent 编排"的第一章，也是毕业论文第 5 章"动态任务规划"的前置。学完你要能回答三件事——为什么要把一个全能 Agent 拆成四个？四个 Agent 之间怎么传"接力棒"？怎么保证循环不会死？

---

## 一、总结

**一句话概括**：

> **多 Agent 协作 = 用 LangGraph 把一个"全能 Agent"拆成四个各司其职的 Agent（导师讲 → 出题考 → 评估分 → 规划下一步），节点之间靠结构化的 State 字段传"接力棒"，条件边根据掌握度决定"重讲 / 推进 / 收工"，再用轮次计数器保证循环必然终止。**

### 为什么不能只用一个全能 Agent？

| 痛点 | 单全能 Agent | 四 Agent 分工 |
|---|---|---|
| Prompt 冲突 | 又要讲知识、又要出题、又要批改、又要规划，一套提示词塞四套人设互相打架 | 每人一套专属人设，互不干扰 |
| 状态混乱 | 讲完课顺手出题，出题的人设会"污染"讲课语气 | 各管一段，交接清晰 |
| 难扩展 | 想加个"心理疏导 Agent"要改全图 | 加个节点 + 一条边就行 |

类比：**医院科室**。不会让一个医生既看门诊又做检验又发药——**每个环节专人做，质量才稳**。

### 四 Agent 流水线（对照 `multi_agent.py`）

```
START → tutor(讲解) → quiz(出题) → eval(批改) ─┬─ mastery≥0.7 ──→ plan(规划) ─┐
                                               ├─ 没学会,轮次<3 → 回 tutor 重讲 │
                                               └─ 3轮没学会 / 总轮≥5 → 收工 END ←┘
```

| Agent | 职责 | 产出（写入 State 的字段） |
|---|---|---|
| tutor 导师 | 讲解当前知识点 | `lecture` |
| quiz 出题 | 按知识点出练习题 | `question` |
| eval 评估 | 批改答案、打掌握度（最难） | `feedback` + `mastery` + `round` |
| plan 规划 | 决定下一知识点 | `next_topic`（顺手把 `topic` 也更新） |

---

## 二、对应知识点

### 2.6.1 从 1.5 到 2.6：三处架构升级

| 维度 | 1.5 单 Agent | 2.6 多 Agent |
|---|---|---|
| State | 只有 `messages`（对话流水账） | 一堆**具名字段**（接力棒） |
| 节点 | `llm_with_tools`（带工具） | 带人设的普通 LLM |
| 条件边 | 判断"最后一条有没有 tool_calls" | 判断"学没学会" |
| 循环 | `call_model ↔ tool_node`（技术循环） | `eval ↔ plan/retry`（**业务循环**） |

**关键认知：多 Agent 之间传的不是"聊天记录"，是结构化的接力棒。** 题目、答案、掌握度、下一知识点各有归属——这就是为什么 State 要拆成具名字段而不是一条 messages 走天下。

### 2.6.2 State：接力棒字典（谁写谁读要记牢）

```python
class AgentState(TypedDict, total=False):
    topic: str           # 当前知识点（plan 换新）
    lecture: str         # tutor 写
    question: str        # quiz 写
    student_answer: str  # 外部传入
    feedback: str        # eval 写
    mastery: float       # eval 写（条件边的依据）
    next_topic: str      # plan 写
    round: int           # eval 写（防死循环出口）
```

| 字段 | 写者 | 读者 |
|---|---|---|
| `topic` | plan（换新知识点） | tutor / quiz / eval / plan |
| `question` | quiz | eval |
| `mastery` | **eval** | should_continue / plan |
| `round` | **eval**（每考一次 +1） | should_continue |

**LangGraph 的合并机制**：节点只 `return` 自己改写的字段（一个 dict），LangGraph 自动把返回的字段合并回总 State，没返回的字段原样保留。

### 2.6.3 节点模式：一个节点 = 人设 + 一次 invoke + return dict

```python
def tutor_node(state: AgentState) -> dict:
    resp = llm.invoke([
        SystemMessage(content=TUTOR_PROMPT.format(topic=state["topic"])),
        HumanMessage(content="请开始讲解"),
    ])
    return {"lecture": resp.content}   # 纯文本,不 json.loads!
```

四个节点的套路完全一样，唯一差别在**返回字段**和**是否需要解析 JSON**：

| 节点 | prompt 要求输出 | resp.content 里是 | 处理方式 |
|---|---|---|---|
| tutor | 3 句话讲解 | 普通文本 | 直接用 |
| quiz | 1 道题 | 普通文本 | 直接用 |
| eval | **JSON**（mastery + feedback） | JSON 文本 | `json.loads` 解析（三层兜底见 2.6.5） |
| plan | 只输出知识点名 | 普通文本 | `strip()` 后直接用 |

#### 信封 vs 信纸：`resp.content` 永远是 str

**你踩过的概念坑**：HTTP 响应是 JSON（含 usage/id/choices），那是**信封**；LangChain 拆完信，`resp.content` 是**信纸**——类型恒为 `str`。模型输出的是"人话还是 JSON 文本"，**取决于 prompt 怎么要求**，跟返回值类型无关。

> **判据（可复用工程规矩）：输出格式的契约写在 prompt 里，解析方式跟着契约走。** prompt 没要求 JSON，就绝不 `json.loads`；要求了，才解析。

### 2.6.4 条件边：四段式判定 + 防死循环

#### 两条铁律（本节的灵魂）

> **铁律一：状态修改只发生在节点里，条件边只负责指路。** `round + 1` 在 `eval_node`，绝不在 `should_continue`。
>
> **铁律二：循环计数器必须放在"所有路径的必经节点"上。** plan→quiz 回边**绕过 tutor**，所以 round 放 tutor 会让场景 A 死循环；quiz/eval 是两条回边的汇合点，放 eval 语义也最贴切（考完一次 = 学了一轮）。

#### 死循环推演（round 放 tutor 的后果）

```
1. tutor 进入      round = 0+1 = 1
2. quiz → eval     mastery=0.9 → should_continue 判:≥0.7 → plan
3. plan → quiz     ← 回边不经过 tutor! round 再没机会 +1
4. eval → plan → quiz → eval → ... 无限循环,round 永远 = 1,硬上限失效
```

#### 正确版本

```python
def should_continue(state: AgentState) -> str:
    """只指路、不改状态。四段式判定:"""
    r = state.get("round", 0)
    m = state.get("mastery", 0.0)
    if r >= 5:                  # ① 总轮次硬上限(兜 plan 回边那条路)
        return "end"
    if m >= 0.7:                # ② 学会了 → 去规划
        return "plan"
    if r < 3:                   # ③ 没学会还有机会 → 回导师重讲
        return "retry"
    return "end"                # ④ 学了 3 轮还不会 → 收工
```

`round + 1` 写在 eval_node 的 return 里：

```python
return {
    "feedback": feedback,
    "mastery": mastery,
    "round": state.get("round", 0) + 1,   # 每批改一次 = 一轮
}
```

#### 终止性（论文/答辩素材）

验证循环不会死，必须**枚举所有路径**并给每条路径出口：

| 路径 | 会不会经过 tutor | 出口 |
|---|---|---|
| eval → retry → tutor → quiz → eval | ✅ | round 到 3 收工 |
| eval → plan → quiz → eval | ❌（绕过） | round 到 5 收工（硬上限） |

> 工业做法其实用**两个计数器**：`round`（总轮次，防死循环）+ `retry_count`（当前知识点重讲次数，换知识点清零）。一个 round 顶两个用是教学简化——写论文第 5 章时可展开。

### 2.6.5 eval_node：三层兜底 + 钳制（本节最难的函数）

目标：模型返回的是**文本**，要抠出 `mastery` 这个**数字**。模型可能输出 ```json 代码块、纯文本"掌握度大概 0.8 分"、甚至一坨废话。

```python
def eval_node(state: AgentState) -> dict:
    resp = llm.invoke([SystemMessage(content=EVAL_PROMPT.format(
            topic=state["topic"],
            question=state.get("question", ""),
            answer=state.get("student_answer", ""),
        )), HumanMessage(content="请批改这份答案")])
    # ① 剥壳:模型爱用 ```json ... ``` 裹 JSON,先撕掉这层包装纸
    text = resp.content.strip().replace("```json", "").replace("```", "")

    try:                              # ② 正常路径:json.loads
        data = json.loads(text)
        mastery = float(data["mastery"])
        feedback = data.get("feedback", "")
    except Exception:                 # ③ 备用路径:正则抠第一个数字
        m = re.search(r"\d\.?\d*", text)
        mastery = float(m.group()) if m else 0.0
        feedback = text[:50]

    mastery = max(0.0, min(mastery, 1.0))   # ④ 钳制:不管前面拿到啥,锁进 0~1
    return {"feedback": feedback, "mastery": mastery,
            "round": state.get("round", 0) + 1}
```

#### 三个机制逐个拆

**① 正则 `\d\.?\d*`**：`\d` 一个数字、`\.` 真正的点（`.` 在正则里是"任意字符"要转义）、`?` 可有可无、`\d*` 零个或多个数字。匹配 `8` / `0.8` / `0.85`。`re.search` 找到返回匹配对象，`.group()` 取字符串；找不到返回 `None`。

**② try/except 接异常，不是 if 接**：`json.loads` 解析失败是 **raise（打断程序）**，不是返回空值——所以不能用 `if/elif/else` 分支接它，必须 `try/except`。类比：钥匙卡住就换备用钥匙（正则），还不行就撬锁（默认 0.0）。

**③ 钳制 `max(0.0, min(m, 1.0))`——prompt 是请求，不是保证**：

| 模型实际给的 | 不钳制 | 钳制后 | 说明 |
|---|---|---|---|
| `{"mastery": 0.8}` | 0.8 | 0.8 | 正常值,没被误伤 |
| `{"mastery": 85}`（百分制） | **85.0** | 1.0 | 85 ≥ 0.7 会误判"学会" |
| "我给 85 分"（纯文本抠到） | **85.0** | 1.0 | 同上 |
| "第 3 题答案正确"（抠到题号） | **3.0** | 1.0 | 正则不知道哪个数字是掌握度 |
| `{"mastery": -0.2}` | **-0.2** | 0.0 | 负数会永远走 retry 重讲到天荒地老 |
| `{"mastery": 1.5}` | **1.5** | 1.0 | 超范围 |

> 类比：prompt 里写"0~1"像前台的"请按规范填写"提示牌，`max/min` 像门口安检机——**提示牌防君子，安检机防意外，真实系统两层都要**。
>
> 诚实补充：钳制是"保命不保准"——85 被钳成 1.0 而非 0.85。更严谨的做法是 `if 1 < mastery <= 100: mastery /= 100`（百分制自动换算），留给 2.7 优化。

### 2.6.6 搭图五步

```python
graph = StateGraph(AgentState)
graph.add_node("tutor", tutor_node)          # ① 注册 4 个节点(漏一个 → 编译报
graph.add_node("quiz", quiz_node)            #    "Found edge starting at unknown node")
graph.add_node("plan", plan_node)
graph.add_node("eval", eval_node)
graph.add_edge(START, "tutor")               # ② 固定边
graph.add_edge("tutor", "quiz")
graph.add_edge("quiz", "eval")
graph.add_conditional_edges("eval", should_continue,   # ③ 条件边:返回的 key → 走哪
    {"plan": "plan", "retry": "tutor", "end": END})    #    映射表,跟 1.5 同套路
graph.add_edge("plan", "quiz")               # ④ 循环回边(绕过 tutor!)
app = graph.compile()                        # ⑤ 编译
```

**注意**：`add_node` 注册 ≠ `add_edge` 连边，两个都不能漏。LangGraph 只在 `compile()` 时检查"边指向的节点存在不存在"——漏注册节点会编译时报错。

### 2.6.7 留给 2.7 的设计缺口（本章最有价值的产出）

| 缺口 | 现象 | 2.7 的正解 |
|---|---|---|
| 规划 Agent 没有"结束"信号 | 学完最后一个知识点，plan 输出"无"，图不停止，白烧一轮靠 round≥5 兜底 | 规划输出结构化决策：`推进 / 巩固 / 重学 / 结束`，结束交由条件边直接 END |
| mastery 在 plan 里区分度有限 | should_continue 已用 0.7 分流，进 plan 的 mastery 恒 ≥0.7 | 2.7 里 mastery 才真正决定"推进/巩固/跳级/回退"路径 |

---

## 三、测试与验收

### 三场景走查（真实运行输出）

| 场景 | 输入 | 实际走的路径 | 结果 | 说明 |
|---|---|---|---|---|
| A 随机出题 + 固定答案 | 答案写死但题是随机生成的 → 错配 | retry×…→end | 掌握度 0.0 | **演示数据缺陷，不是代码 bug**——题对不上答案，当然判 0 分 |
| B 答错 | student_answer="不会" | retry×2 → end | 最终掌握度 0.0，**round=3 正常停** | 防死循环出口生效 ✅ |
| C 固定题目 + 正确答案 | 预置 question="x²-4"，答对 | plan 分支 ×…→ round≥5 停 | 掌握度 1.0，推进到下一知识点 | 演示 plan 分支要**固定题目**（quiz_node 加一行：外部已有 question 就不生成） |

### 边界测试 13/13（方法：桩函数替掉 LLM）

**测试思想（面试可讲）**：把 `tutor/quiz/plan` 换成返回固定值的桩函数（stub），只测"图怎么走"，不测"模型说啥"——不烧 API 钱、结果可复现。这就是单元测试里"隔离外部依赖"的思想。

| 场景 | 验证点 | 结果 |
|---|---|---|
| 一直答对（mastery 恒 0.95） | round 到 5 停（不死循环）+ 进 plan + next_topic | ✅ |
| 一直答错（mastery 恒 0.2） | round 到 3 收工 + plan 调用 0 次 + tutor 重讲 3 次 | ✅ |
| 先错两次再对（0.3→0.5→0.9） | 最终 0.9 + plan 调用 2 次 | ✅ |
| eval 返回 ```json 包裹 | 剥壳后解析出 0.85 | ✅ |
| eval 返回纯文本"大概 0.6 分" | 正则兜底抠出 0.6 | ✅ |
| eval 返回无数字文本 | 兜底给 0.0（不崩） | ✅ |
| eval 返回百分制 80 | 钳制到 1.0 | ✅ |
| round 自增 | 每批改一次 +1 | ✅ |

> 排错插曲：场景 3 一度判 FAIL——最后发现**是我测试脚本的期望值算错了**（plan 应被调用 2 次而非 3 次），代码本身是对的。**期望值错 ≠ 代码错，先走查再改代码。**

---

## 四、本节踩坑清单

| # | 坑 | 表现 | 根治 |
|---|---|---|---|
| 1 | `&&` 当逻辑与 | SyntaxError，模块都导不进 | Python 用 `and` |
| 2 | `json.loads` 用在纯文本 | JSONDecodeError | prompt 没要求 JSON 就不解析 |
| 3 | 变量名 `re` 遮蔽 re 模块 | `re.search` 报"dict 没有 search" | 临时变量别用模块/内置名（`re`/`list`/`dict`/`str`/`round`/`id`） |
| 4 | `"mastry"` 拼写 | KeyError | 字段名照抄类定义 |
| 5 | `.format()` 少传占位符 | KeyError | 模板里几个 `{}` 就传几个 |
| 6 | HumanMessage 粘 docstring/TODO 原文 | 模型收到"评估:批改答案…"鬼话 | 写正常指令 |
| 7 | `resp.content["key"]` 拿字符串当字典 | TypeError: string indices | content 是 str，下标只能整数 |
| 8 | `.replace()` 不传参数 | TypeError | `replace(旧, 新)` 两个参数 |
| 9 | 漏注册 `add_node("quiz", ...)` | compile 报 unknown node 'quiz' | 4 节点注册齐，注册≠连边 |
| 10 | `should_continue` 缺 `round>=5` 第一条 | 场景 A 死循环烧钱 | 四段式顺序：硬上限→plan→retry→end |
| 11 | `round+1` 放 tutor | 场景 A round 冻结在 1 死循环 | 放必经节点 eval（铁律二） |
| 12 | 相信 prompt"0~1 之间"不用钳制 | 85/3/-0.2 污染下游判断 | `max/min` 钳制兜底 |
| 13 | 变量名 `round` 遮蔽内置函数 | 后续 `round(3.14)` 炸"int 不可调用" | 改名或内联 |

---

## 五、论文定位（第 5 章动态任务规划的前置）

- **流水线拆分**：把"教学"拆成导师/出题/评估/规划四个工位——第 5 章"动态任务规划"就是在这一章基础上，让规划 Agent 从"输出一个知识点名"升级为"输出完整学习路径策略"。
- **接力棒 State**：多 Agent 传结构化字段而非聊天流水账——这是多 Agent 系统设计的第一原则，可写进论文方法部分。
- **终止性证明**：枚举两条回边 + 各自出口，答辩被问"会不会死循环"直接背这段。
- **双计数器**：round（防死循环）+ retry_count（当前知识点重试）的取舍，第 5 章可展开。
- **规划决策结构化**：plan 输出"无"不结束的缺口 = 第 5 章要解决的第一个真问题。

---

## 六、代码段

完整代码在 `agent_project/multi_agent.py`，四个节点的关键骨架（prompt 略）：

```python
def tutor_node(state): 
    resp = llm.invoke([SystemMessage(content=TUTOR_PROMPT.format(topic=state["topic"])),
                       HumanMessage(content="请开始讲解")])
    return {"lecture": resp.content}          # 纯文本,不解析

def quiz_node(state):
    if state.get("question"):
        return {}                             # 外部已指定题目 → 沿用(演示 plan 分支用)
    resp = llm.invoke([SystemMessage(content=QUIZ_PROMPT.format(topic=state["topic"])),
                       HumanMessage(content="根据知识点出题")])
    return {"question": resp.content}

def eval_node(state):
    resp = llm.invoke([SystemMessage(content=EVAL_PROMPT.format(
        topic=state["topic"], question=state.get("question",""),
        answer=state.get("student_answer",""))), HumanMessage(content="请批改这份答案")])
    text = resp.content.strip().replace("```json","").replace("```","")
    try:
        data = json.loads(text)
        mastery = float(data["mastery"]); feedback = data.get("feedback","")
    except Exception:
        m = re.search(r"\d\.?\d*", text)
        mastery = float(m.group()) if m else 0.0
        feedback = text[:50]
    mastery = max(0.0, min(mastery, 1.0))
    return {"feedback": feedback, "mastery": mastery,
            "round": state.get("round", 0) + 1}   # 计数放必经节点

def plan_node(state):
    resp = llm.invoke([SystemMessage(content=PLAN_PROMPT.format(
        topic=state["topic"], mastery=state.get("mastery", 0.0))),
        HumanMessage(content="请决定下一个知识点")])
    nxt = resp.content.strip()                 # 纯文本知识点名
    return {"next_topic": nxt, "topic": nxt}   # topic 也要换!否则出题还考旧的

def should_continue(state):
    r = state.get("round", 0); m = state.get("mastery", 0.0)
    if r >= 5:  return "end"      # ① 硬上限兜底(plan 回边那条路)
    if m >= 0.7: return "plan"    # ② 学会了
    if r < 3:   return "retry"    # ③ 没学会,再试
    return "end"                  # ④ 3 轮还不会,收工
```

搭图与测试的完整代码见 `multi_agent.py` 本体（含三场景演示：A 随机出题、B 答错循环、C 固定题目走通 plan 分支）。
