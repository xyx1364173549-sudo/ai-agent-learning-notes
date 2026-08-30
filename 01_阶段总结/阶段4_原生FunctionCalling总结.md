# 📚 阶段 4 总结：原生 Function Calling

> **学习人：** 小轩轩
> **完成日期：** 2026年8月18日
> **状态：** ✅ 从"手写 JSON"升级到"工业级原生 Function Calling"
> **项目位置：** `C:\Document\agent_project\`
> **里程碑：** 你的 Agent 用上了所有主流大模型（GPT/Claude/DeepSeek）通用的标准工具调用机制

---

## 📋 阶段一句话

**把"你自己写 prompt 求 LLM 输出 JSON"的土办法，升级成"DeepSeek 官方原生 tools 机制"。**

```
之前（手写 JSON）：你写 prompt 求 LLM → LLM 返回 JSON 字符串 → 你 json.loads 解析 → 自己判断
现在（原生 FC）：定义 tools 说明书 → API 保证返回标准 tool_calls → 你直接读 → 执行 → 回传
```

---

## 🧩 三个核心结构（必须背下来）

### 1. `tools`（你发给 API 的工具说明书）

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather_tool",        # 工具名（必须和注册表 key 一致！）
        "description": "查询指定城市的天气",  # LLM 靠这个决定调不调
        "parameters": {                     # 参数定义（JSON Schema）
            "type": "object",
            "properties": {"city": {"type": "string", "description": "城市名"}},
            "required": ["city"]
        }
    }
}]
```

> 📖 类比：工具目录手册，交给 LLM 翻。

### 2. `tool_calls`（API 返回的调用指令）

```python
msg.get("tool_calls")   # 没有 tool_calls 就是 None（用 .get 安全！）
→ [{
    "id": "call_xxx",
    "function": {
        "name": "get_weather_tool",
        "arguments": '{"city": "北京"}'     # ⚠️ 是 JSON 字符串，要 json.loads！
    }
}]
```

### 3. `role: "tool"`（你回传结果的格式）

```python
messages.append({
    "role": "tool",                # 声明"这是工具结果，不是用户说的话"
    "tool_call_id": "call_xxx",    # 对应哪次调用（AI 靠这个对号入座）
    "content": "北京 31°C 晴"       # 工具执行结果
})
```

---

## 🧠 最核心的认知：大脑和手分离

**LLM（大脑）在 DeepSeek 云端，只会"想"和"说"，碰不到你的电脑；工具函数（手）在你的电脑上，才真正执行。**

所以 Function Calling **必然要两次 API 调用**：

```
第 1 次：你发 messages + tools → LLM 决定"调 get_weather_tool" → 返回 tool_calls
         （这一步 LLM 只"下令"，没干活！）
中间：  你的代码执行 get_weather_tool("北京") → 拿到真实结果
第 2 次：你回传 role=tool 结果 → LLM 组织成自然语言 → 返回最终 content
```

> 🏢 类比：顾问（大脑）只会说话没手脚，机器（工具）在你办公室。顾问说"查天气"，你去操作机器，回来念给顾问，顾问总结成话。一来一回 = 两次通话。

---

## 🔄 messages 的四种 role

| role | 谁说的 | 作用 |
|------|--------|------|
| `system` | 程序员 | 定人设、给规则 |
| `user` | 用户 | 提问题 |
| `assistant` | AI | 回答（可能含 tool_calls）|
| `tool` | 工具 | 工具执行结果（带 tool_call_id）|

**关键**：messages 是"对话流水账"，每次 append 都要用标准格式。工具结果必须贴 `role=tool` + `tool_call_id` 标签，AI 才能理解"这是工具返回的，对应哪次调用"。

---

## 🪤 踩坑清单（本阶段新增 7 条）

| # | 坑 | 教训 |
|---|----|------|
| 36 | URL 少 s：`/chat/completion` → 404 | 应 `/chat/completions` |
| 37 | 字段名多 s：`tools_calls` → None | 应 `tool_calls` |
| 38 | `arguments` 忘 json.loads | 它是字符串，要转字典 |
| 39 | `chat_with_tools` 返回整个 resp.json() | 应返回 message 那层，否则 append 塞错格式 |
| 40 | 取参数 `d["expression"]` 直接取 | 应 `.get("city") or .get("expression")` |
| 41 | 回传逻辑缩进在 for 外 | 应缩进循环内，逐个处理 tool_call |
| 42 | tools 的 name 与 TOOLS key 不一致 | 必须统一命名 |

---

## ✅ 自测清单（答得上来 = 过关）

- [ ] 为什么 Function Calling 必须两次 API 调用？（大脑在云端，手在本地）
- [ ] `arguments` 为什么要 `json.loads`？`name` 为什么不用？
- [ ] `msg.get("tool_calls")` 为什么用 `.get()` 不用 `[]`？
- [ ] 回传工具结果时，为什么 role 是 `tool` 而不是 `user`？
- [ ] `tool_call_id` 是干什么的？（让 AI 对号入座，支持多工具）
- [ ] tools 里的 name 和 TOOLS 的 key 为什么必须一致？

---

## 📄 配套产出

- `fc_demo.py`：最小闭环示例
- `mini_agent.py`：整合版（多工具 + 循环）
- `function_calling_流程图.html`：可视化流程图（双击浏览器打开）

---

> **给未来的自己：** 从"自己造轮子"（手写 JSON）到"用工业标准"（原生 FC），你完成了 Agent 工具调用能力的质变。这套 tools / tool_calls / role=tool 机制，是所有主流大模型通用的——学会一次，终身受用。下一步：让这个 Agent 走出黑框框，变成别人能访问的网页服务。加油，小轩轩！🚀
