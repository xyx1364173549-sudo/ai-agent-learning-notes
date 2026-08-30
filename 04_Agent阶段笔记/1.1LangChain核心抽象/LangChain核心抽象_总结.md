# LangChain 核心抽象（任务 1.1）学习总结

> **学习人：** 小轩轩
> **日期：** 2026-08-20
> **前置知识：** 原生 Function Calling（tools / tool_calls / role=tool，已掌握）
> **状态：** ✅ 完成
> **项目位置：** `C:\Document\agent_project\lc_demo.py`、`lc_tool.py`

---

## 一、一句话总结

**LangChain 用三个"零件"，封装了你手写 FC 时的三个环节：**

| 零件             | 封装了手写的什么               | 类比          |
| -------------- | ---------------------- | ----------- |
| ChatModel      | `requests.post` + 解析响应 | 万能插座        |
| PromptTemplate | f-string 拼 prompt      | 填空题         |
| Tool           | 手写 JSON Schema + 执行工具  | 自动印刷机 / 文件袋 |

---

## 二、三大核心抽象详解

### 2.1 ChatModel —— 万能插座

**作用：** 统一 LLM 接口，换模型只改 `model` / `base_url` 两个参数。

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-v4-flash",            # 用什么模型（对应 json={"model":...}）
    api_key=API_KEY,                      # 身份凭证（对应 headers 的 Authorization）
    base_url="https://api.deepseek.com",  # 模型地址（对应 BASE_URL）
)

reply = llm.invoke("用一句话介绍你自己")  # invoke = 发一次请求
print(reply.content)                      # AIMessage 对象，用 .content 取文本
```

**三个参数对照手写 requests：**

| 手写 requests                                      | ChatOpenAI 参数 |
| ------------------------------------------------ | ------------- |
| `json={"model": MODEL}`                          | `model=`      |
| `headers={"Authorization": f"Bearer {API_KEY}"}` | `api_key=`    |
| `f"{BASE_URL}/chat/completions"`                 | `base_url=`   |

**关键：** `invoke` 返回的是 `AIMessage` 对象（不是字符串），里面带 token 用量、模型名等元信息，用 `.content` 取正文。对比手写的 `resp.json()["choices"][0]["message"]["content"]`。

---

### 2.2 PromptTemplate —— 填空题

**作用：** 把"固定文字"和"变量"分开，固定文字写模板，变量挖成空位 `{变量}`。

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，回答风格要{style}"),   # 元组：(角色, 内容)
    ("user", "{question}"),
])

prompt = template.format_messages(
    role="编程老师",
    style="通俗易懂，多用类比",
    question="什么是递归？",
)
```

**关键：** `from_messages` 里的元组 `(角色, 内容)` 等价于手写的 `{"role": ..., "content": ...}`。`format_messages` 返回**带角色的 messages 列表**，正好是 `llm.invoke()` 要吃的格式——两个零件无缝衔接。

---

### 2.3 Tool —— 自动印刷机（三自动）

**作用：** 用 `@tool` 装饰器，把普通函数变成工具，自动生成工具说明书。

```python
from langchain_core.tools import tool

@tool
def get_weather_tool(city: str) -> str:
    """查询指定城市的天气"""
    return f"{city} 今天晴天，20°C"
```

**"三自动"：** `@tool` 自动从函数抄三样信息，拼成 JSON Schema：

| 函数里的信息                 | 自动变成说明书的      | 对应手写 FC                |
| ---------------------- | ------------- | ---------------------- |
| 函数名 `get_weather_tool` | `name`        | `"name": "..."`        |
| docstring `查询指定城市的天气`  | `description` | `"description": "..."` |
| 类型注解 `city: str`       | `parameters`  | 那段 properties/required |

**关键认知：** docstring 不是注释！它是 Python 保存到 `函数.__doc__` 的元数据。`@tool` 读的是 `__doc__` 属性，不是"AI 读注释"。

---

## 三、完整闭环（两次调用）

```python
from langchain_core.messages import HumanMessage, ToolMessage

llm_with_tools = llm.bind_tools([get_weather_tool])   # 创建"带工具箱"的模型副本

human_msg = HumanMessage(content="北京天气怎么样")

# 第 1 次调用：AI 决定调工具（content 为空，只有 tool_calls）
msg = llm_with_tools.invoke([human_msg])

# 执行工具 + 回传结果
tool_messages = []
for tool_call in msg.tool_calls:
    result = get_weather_tool.invoke(tool_call["args"])
    tool_messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))

# 第 2 次调用：AI 组织最终回答（传完整历史）
final = llm_with_tools.invoke([human_msg, msg, *tool_messages])
print(final.content)
```

**完整流程：**

```
用户输入 → PromptTemplate 拼话 → ChatModel(第1次) 下令 tool_calls
→ Tool 执行 → 回传 ToolMessage → ChatModel(第2次) 组织语言 → 回答
```

---

## 四、难点澄清（7 个，理解这些才算真懂）

### 4.1 docstring 为什么能被 @tool 读到？

docstring 不是注释，是 Python 保存到 `函数.__doc__` 的元数据。`# 注释` 才会被忽略。`@tool` 读的是 `__doc__` 属性，AI 从头到尾看不到你的源代码，只看到 HTTP 请求里的 JSON。

### 4.2 invoke 是什么意思？

`invoke(输入)` = 传参 + 执行 + 返回，三合一（榨汁机：放原料→运转→出果汁）。它是 LangChain 统一的"运行开关"，`llm.invoke` / `tool.invoke` / `chain.invoke` 都用它。

### 4.3 @tool 之后函数变了吗？

变了。`get_weather_tool` 不再是函数，而是 `StructuredTool` 对象（文件袋）：

- `.name` ✅ 工具名 / `.description` ✅ 描述 / `.func` ✅ 原始函数
- `.__name__` ❌ 报错（对象没这个属性）

### 4.4 bind_tools 是什么意思？

`bind_tools` 是"创建带工具箱的模型副本"。`llm` 不变（还是裸的），`llm_with_tools` 是新的、每次 invoke 都带工具清单的副本。

### 4.5 为什么第二次调用还用 llm_with_tools？

保留 AI"继续调工具"的能力。单工具场景第二次会直接回答，但多工具场景 AI 可能还想调第二个工具。

**content 空值 = AI 在下令**：第一次调用 content 为空、只有 tool_calls，正是"大脑和手分离"的证据——AI 只下令不开口。

### 4.6 数据是怎么流动的？（template 和 prompt 怎么到 llm）

template 和 prompt 不是两个并列的东西，是**一条流水线上的两站**：

```
template（带空位） → format_messages 填空 → prompt（填好的 messages）→ invoke(prompt) 传参 → llm
```

**连接靠"函数传参"**（`llm.invoke(prompt)` 里的 prompt 就是传进去的参数），不是 from_messages。`from_messages` 只负责"造模板"，跟"数据怎么流到 llm"完全无关。

**点外卖类比**：template=空白菜单 → format_messages=你在菜单上填 → prompt=填好的菜单 → invoke(prompt)=把菜单递给厨师。

### 4.7 消息类型（HumanMessage / ToolMessage）

LangChain 把手写 FC 的四种 role 字典，做成了四个"消息类"：

| 类               | 对应 role       | 是谁说的   |
| --------------- | ------------- | ------ |
| `SystemMessage` | `"system"`    | 系统/程序员 |
| `HumanMessage`  | `"user"`      | 用户     |
| `AIMessage`     | `"assistant"` | AI     |
| `ToolMessage`   | `"tool"`      | 工具结果   |

`ToolMessage` 比 `HumanMessage` 多一个 `tool_call_id` 字段，用于"对号入座"（告诉 AI 这个结果对应哪次工具调用）。

```python
你之前手写的（字典）：
messages = [
    {"role": "user", "content": "北京天气怎么样"},
    {"role": "tool", "tool_call_id": "call_xxx", "content": "晴天20°C"},
]



from langchain_core.messages import HumanMessage, ToolMessage

messages = [
    HumanMessage(content="北京天气怎么样"),
    ToolMessage(content="晴天20°C", tool_call_id="call_xxx"),
]

```

---

## 五、踩坑清单（本任务新增）

| #   | 坑                                  | 教训                                                     |
| --- | ---------------------------------- | ------------------------------------------------------ |
| 49  | `os.getenv("deepseek_api_key")` 小写 | Windows 大小写不敏感碰巧能跑，Linux 会返回 None；应用大写与 .env 一致        |
| 50  | 第二次调用缩进进 for 循环                    | 多工具时会"每执行一个就调一次 AI"；应退回 for 外                          |
| 51  | 用 `函数.__name__` 访问 @tool 对象        | 报 AttributeError；应用 `.name` / `.description` / `.func` |

---

## 六、类比速记

| 概念             | 类比                                                              |
| -------------- | --------------------------------------------------------------- |
| ChatModel      | 万能插座（换模型只改一行）                                                   |
| PromptTemplate | 填空题（挖空填变量）                                                      |
| @tool          | 文件袋（函数装进袋子，标签=name/description）                                 |
| invoke         | 榨汁机（放原料→运转→出果汁）                                                 |
| bind_tools     | 给手机装 App（返回新副本）                                                 |
| 老板-秘书          | human_msg=客户需求 / tool_calls=老板指令 / tool_messages=秘书结果           |
| 点外卖            | template=空白菜单 / format_messages=填单 / prompt=填好的菜单 / invoke=递给厨师 |

---

## 七、自测清单（答得上来 = 过关）

- [ ] 手写 FC 的"发请求"这一步，LangChain 用什么替代？（ChatModel 的 invoke）
- [ ] `@tool` 之后 `get_weather_tool` 是什么类型？怎么访问描述和原始函数？
- [ ] `invoke` 和 `requests.post` 是什么关系？
- [ ] 第二次调用为什么要传 `[human_msg, msg, *tool_messages]`？
- [ ] `bind_tools` 会不会改变原来的 `llm`？
- [ ] 第一次调用为什么 content 是空的？
