# 🚀 阶段 1 总结：接 DeepSeek API，做出迷你 Agent

> **学习人：** 小轩轩
> **完成日期：** 2026年8月12日（原计划 2 天，1 天完成 🎉）
> **状态：** ✅ 三关全通——llm_client → chat_cli → mini_agent
> **项目位置：** `C:\Document\agent_project\`
> **里程碑：** 你的第一个"会调真实工具的 AI 程序"诞生！

---

## 📋 阶段一句话

**从"会调 API"到"AI 能自己决定调什么工具、再把结果说给你听"——这就是 Agent。**

```
你问"北京天气怎么样"
  ↓
程序发现含"天气"→ 提取城市"北京"
  ↓
调用天气 API（wttr.in）拿到原始数据（温度/湿度/天气）
  ↓
把原始数据塞给 DeepSeek，让它"转述"
  ↓
AI 自己组织语言：北京现在气温23°C，有零星小雨，湿度95%。出门记得带伞。
```

**最震惊的那一刻：AI 不是"传话"，而是"会自己组织语言"。** 这就是 LLM 和普通函数最大的区别——给它数据 + 一句"请转述给用户"，它就能说人话，甚至加一句"记得带伞"。

---

## 🗺️ 三关架构（复习用）

### 第 1 关：llm_client.py —— API 客户端（地基）

| 部件 | 作用 |
|------|------|
| `API_KEY` / `BASE_URL` / `MODEL` | 你是谁、去哪、用哪个模型 |
| `chat(messages)` | 唯一入口：发消息 → 拿回复 |

**核心代码（自己写的）：**
```python
def chat(messages: list[dict], api_key: str = API_KEY) -> str | None:
    url = f"{BASE_URL}/chat/completions"
    data = {"model": MODEL, "messages": messages}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    resp.raise_for_status()
    resp = resp.json()["choices"][0]["message"]["content"]
    return resp
```

**必须背下来的返回结构：** `resp.json()["choices"][0]["message"]["content"]`

### 第 2 关：chat_cli.py —— 对话循环（记忆）

**核心：messages 列表 = 对话记忆。** 每次都把整个历史发给 API，AI 才"记得"前面说了啥。

```python
while True:
    user_input = input("\n你: ").strip()
    if user_input.lower() == "quit":
        break
    messages.append({"role": "user", "content": user_input})    # 加用户消息
    reply = chat(messages)                                      # 发整个历史
    messages.append({"role": "assistant", "content": reply})    # 存 AI 回复
    print(f"AI: {reply}")
```

### 第 3 关：mini_agent.py —— 迷你 Agent（灵魂）

**架构：LLM（大脑）+ 工具（手）+ 消息历史（记忆）**

```python
if "天气" in user_input:                          # 意图判断
    city = extract_city(user_input)               # 提取城市
    tool_result = get_weather_tool(city)          # ← 调用真实工具！
    messages.append({                             # 把工具结果塞进对话
        "role": "user",
        "content": f"工具返回的天气数据:\n{tool_result}\n请转述给用户",
    })
reply = chat(messages)                            # AI 组织语言回复（必经出口！）
messages.append({"role": "assistant", "content": reply})
print(f"AI: {reply}")
```

**为什么 AI 会自己组织语言？** 因为你给它的消息里有两样东西：
1. **工具返回的原始数据**（23°C、95%、Light rain）
2. **指令**："请转述给用户"（在 f-string 里）

AI 看到数据和指令，就自己加工成自然语言——**这就是 LLM 的价值：它不止传话，它"理解 + 表达"。**

---

## 🧩 关键知识点

### 1. messages 三元组结构

| role | 含义 | 类比 |
|------|------|------|
| `system` | 给 AI 定人设/规则 | 给员工发《员工手册》 |
| `user` | 用户说的话 | 顾客下单 |
| `assistant` | AI 说过的话 | 员工的回复记录 |

### 2. sys.path.insert —— 跨文件夹导入

```python
sys.path.insert(0, r"C:\Document\weather_tool")   # 告诉 Python"去这个文件夹找模块"
from weather_tool import WeatherClient, format_weather
```

**原理：** Python 找模块时按 sys.path 里的路径顺序搜索。把项目一目录插到最前面（位置 0），就能 import 它的模块了。

### 3. 模块级函数 vs 实例方法（重要！）

| 类型 | 怎么调用 | 例子 |
|------|---------|------|
| 实例方法 | `对象.方法()` | `weather.get_weather(city)` |
| 模块级函数 | 直接 `函数名()` | `format_weather(data)` |

**错误示范（踩过的坑）：** `weather.format_weather(data)` → AttributeError！
format_weather 是 weather_tool.py 顶层定义的独立函数，不属于 WeatherClient 类。

### 4. 缩进 = 归属（Python 的命门）

```python
while True:
    ...
    if "天气" in user_input:      # 在循环内
        ...
    reply = chat(messages)        # 也在循环内（每轮都执行）✅
```

**踩过的坑：** `if` 缩进少一级 → 天气判断跑到循环外 → 程序只收输入不干活（"你:你:你:"）。

---

## 🪤 踩坑清单（本次新增）

1. **裸函数名调用实例方法**：`get_weather(city)` 缺 `weather.` → NameError
   - 规则：方法跟着对象走，必须有 `对象.` 前缀
2. **模块级函数用 `对象.` 调用**：`weather.format_weather(data)` → AttributeError
   - 规则：独立函数不跟任何对象，直接叫名字；但前提是**先 import 它**！
3. **import 了类忘了 import 函数**：`from weather_tool import WeatherClient` 没带 `format_weather` → 调用时 NameError（被裸 except 吞掉，表现为"查询失败"）
4. **裸 `except:`**：吞掉所有错误，掩盖真相 → 写 `except (Exception):` 至少知道防什么
5. **回复逻辑放在 if 分支里**：普通问题（无"天气"）永远不回复 → 回复是每轮对话的必经出口，必须在 if 外面
6. **extract_city 的 return 在 for 里**：只处理第一个词就返回 → return 要放循环外
7. **IDE 红线≠真错误**：PyCharm 不认识 sys.path.insert 动态路径会标红，运行没问题

---

## ✅ 自测清单（答得上来 = 过关）

- [ ] 为什么 messages 列表要 append assistant 的回复？（答：下轮要把整个历史发给 AI，它才记得）
- [ ] 返回结构 choices[0].message.content 每一步是什么？
- [ ] format_weather 是方法还是函数？怎么调用？为什么？
- [ ] 为什么"北京天气怎么样"能触发天气查询？（if 判断 + extract_city 提取）
- [ ] AI 为什么能"自己组织语言"而不是原样返回数据？
- [ ] 如果用户说"上海热吗"，现在能查吗？（不能，因为没有"热"触发词——这是第 5 天 LLM 意图判断要解决的问题）

---

## 🚀 下一步（阶段 2 & 3）

| 天 | 内容 | 状态 |
|----|------|------|
| 第 3 天 | Git 6 条命令 + 三项目推 GitHub | ⬜ 下一站 |
| 第 4 天 | .env 密钥管理（API Key 移出代码）| ⬜ |
| 第 5 天 | LLM 意图判断（AI 自己决定调不调工具）| ⬜ |
| 第 6 天 | 流式输出（打字机效果）| ⬜ |
| 第 7 天 | 多工具注册（ToolBox 模式）| ⬜ |

> **给未来的自己：** 你已经从"不会 import"走到了"做出会调真实工具的 AI"。这一步，叫 Agent 开发入门。后面的路：让 AI 自己决定调什么（第 5 天）、边生成边输出（第 6 天）、挂更多工具（第 7 天）。加油，小轩轩！🚀
