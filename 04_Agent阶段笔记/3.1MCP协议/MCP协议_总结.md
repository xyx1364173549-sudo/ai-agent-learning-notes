# 3.1 MCP 协议（能写一个简单 MCP Server）· 详细版

> 本节是阶段三"工程化"的第一枪：把我们 2.5b 亲手写的情景记忆（SQLite）**包成标准工具**，让任何 MCP 客户端（调试台、AI 应用）都能"插上就用"。学完你要能回答三件事——为什么 LLM 应用需要一套"工具接口标准"？`@server.tool()` 到底把你的函数怎么了？你写的东西凭什么能被"别人"（Inspector / Client）直接调用？

---

## 一、总结

**一句话概括**：

> **MCP（Model Context Protocol）= 给 Agent 的"工具 + 数据"定的一套通用接口协议。我们用 `MCPServer` 把 2.5b 的 `save_episode` / `search_episodes` 包成两个标准工具（`add_episode` / `query_memory`），函数一旦被 `@server.tool()` 装饰，就自带"说明书"（参数签名 + docstring）暴露到协议层——任何客户端都能先"看菜单"（list_tools）再"点单"（call_tool），不写一行对接代码。**

### 痛点：你的函数很好，但"别人"没法用

| 没有 MCP 的世界 | 有了 MCP 之后 |
|---|---|
| 函数写在项目里，只有自己能 `import` | 函数变成**工具**，任何 MCP 客户端即插即用 |
| 想给另一个 AI 应用用？得自己写 HTTP 接口 + 文档 + 鉴权 | 协议帮你把"接口、文档、参数校验"全标准化 |
| 每个应用一套对接方式，N 个应用 N 套代码 | **一次实现，处处连接**（Claude / Cursor / 自研应用…） |

**类比**：没有 MCP 前，每个家电都自带专属充电口，你得为每台机器配一根线；MCP 之后，全行业统一成 **USB-C**——你写的 server 只认"MCP 这个口"，任何客户端拿标准线一插就能用。`@server.tool()` 就是"把自家插座改装成国标"的那一步。

### 为什么 Agent 时代这事特别重要

LLM 本身不会"干活"，它靠**调工具**干活（查库、发邮件、调 API…）。如果每个工具的接入方式都不一样，模型、开发者、宿主应用三方都会疯掉。MCP 把工具调用统一成一套 **JSON-RPC 消息**（stdio 传输），等于给"模型 ↔ 世界"之间修了一条标准公路。

---

## 二、对应知识点

### 3.1.1 MCP 三件套：谁是谁

```
┌─────────────────────────────────────────────┐
│  Host（宿主应用）                             │
│  例：Claude Desktop、Cursor、MCP Inspector    │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐  │
│  │ Client A │   │ Client B │   │ Client C │  │  ← 每个 server 配一个专属 Client
│  └────┬─────┘   └────┬─────┘   └────┬─────┘  │
└───────┼──────────────┼──────────────┼────────┘
        │ JSON-RPC     │              │
   ┌────▼─────┐   ┌────▼─────┐   ┌────▼─────┐
   │ Server 1 │   │ Server 2 │   │ Server 3 │   ← 轻量进程，暴露工具/资源/提示
   └──────────┘   └──────────┘   └──────────┘
```

| 角色 | 是谁 | 干什么 |
|---|---|---|
| **Host** | 你正在用的 AI 应用（桌面软件/IDE） | 负责 UI、模型、多 Client 管理 |
| **Client** | 与某个 Server **一对一**的连接 | 发请求、收响应（协议对话） |
| **Server** | 我们的 `mcp_server.py`（一个进程） | **暴露能力**：Tools（可执行动作）/ Resources（可读数据）/ Prompts（提示模板） |

**关键关系**：一个 Host 可挂多个 Server；但**一个 Client 只服务一个 Server**（一对一）。我们的 server 是轻量进程，跑起来就干一件事——等别人来调。

### 3.1.2 传输通道：stdio（本阶段主角）

- 客户端 `spawn` 一个 python 进程跑你的 server
- 双方通过**标准输入 / 标准输出**互发 JSON-RPC 消息（注意：**不是**终端里的 print，那是 stderr 演示用的）
- `server.run()` = 启动一个"读 stdin → 干活 → 写 stdout"的循环

这就是为什么测试客户端里要传 `command=python.exe, args=[mcp_server.py]`——告诉系统"用哪个解释器跑哪个文件"。

### 3.1.3 ⚠️ 时效大坑：mcp 2.x 改名风暴（本节最大的记忆点）

你装的是 `mcp 2.1.1`，而网上绝大多数教程还停留在 1.x。**API 已经换代**：

| 事情 | 1.x 老教程写法 | 2.x 真实写法（本项目） |
|---|---|---|
| 导入容器 | `from mcp.server.fastmcp import FastMCP` | `from mcp.server.mcpserver import MCPServer` |
| 创建实例 | `server = FastMCP("名")` | `server = MCPServer("名")` |
| 注册工具 | `@server.tool()` | `@server.tool()`（**没变**） |
| 启动 | `server.run()` | `server.run()`（**没变**） |
| 客户端 | `stdio_client + Client` 两段式 | `Client(server_params)` **一站式** |
| 列工具 | `result.tools` | 仍是 `result.tools`，但 `result` 类型变了 |

**教训**：装完包先确认版本（`pip show mcp`），**教程看不懂先怀疑"版本不对"**，别硬套 1.x 代码。

### 3.1.4 `@server.tool()` 把你的函数怎么了？（核心顿悟）

```python
@server.tool()          # ① 装饰器：登记为"工具"
def add_episode(topic: str, summary: str, score: float, difficulty: str = "中") -> str:
    """记录一次学习会话。
    参数:topic 知识点, summary 会话摘要, score 练习得分(0~1), difficulty 难度(易/中/难)。
    返回:写入成功提示,含新记录的 id。"""
    ...  # 函数体还是那个函数体,2.5b 的 save_episode 照用
```

装饰的那一刻发生了三件事：
1. **函数签名 → 参数说明**：`topic: str` 变成工具的"必填参数 topic，类型字符串"；`difficulty: str = "中"` 变成"选填参数，默认'中'"
2. **docstring → 工具说明书**：客户端（乃至模型）靠它决定"这工具干嘛的、怎么用"
3. **函数被登记到 server 的工具清单**：于是 `list_tools()` 能列到它

> **一句话钉死：你写的是普通 Python 函数，`@server.tool()` 帮它办了"营业执照 + 菜单"——从此别人不 import 也能按菜单调用。**

### 3.1.5 为什么 `DB_PATH` 要用 `__file__` 钉死（工程思维）

```python
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.db")
```

你的 server 是**被客户端 spawn 的子进程**，它的"当前工作目录"≠ `agent_project`（可能是桌面、终端启动目录……）。如果用 `DB_PATH = "memory.db"`（相对路径），它会在**错误的地方**建库/找库——这就是"Inspector 里 add 成功、query 却查不到"的头号嫌疑。`__file__` 是"本文件在哪"，钉死到脚本所在目录，**无论谁在哪儿启动都找对库**。

### 3.1.6 调试台：MCP Inspector（你亲眼看到的那个网页）

`mcp dev mcp_server.py` 一键拉起三样东西（**依赖 uv**，没装会红点 Failed）：

| 组件 | 干什么 |
|---|---|
| 你的 server 子进程 | 被拉起、等调用 |
| 代理服务器（端口 6274） | 中转消息 |
| Web UI（http://localhost:5173） | 可视化调试台（Inspector） |

Inspector 界面对照：

| 面板 | 作用 |
|---|---|
| 左侧 Tools 列表 | 你的工具清单（`query_memory` / `add_episode`）——= 自动调了 `list_tools()` |
| 中间参数区 | 填参数 → 点测试 → = 自动调了 `call_tool()` |
| 下方 Results | 返回的字符串 |
| 右侧 **Messages** | 协议黑匣子：实时打印 CLIENT → SERVER 的原始 JSON-RPC 报文（TOOLS/LIST、TOOLS/CALL…），排错靠它 |

### 3.1.7 用代码当客户端（test_mcp_client.py，三段式）

```python
from mcp import Client, StdioServerParameters

server_params = StdioServerParameters(command=python, args=[mcp_server.py], cwd=项目目录)

async with Client(server_params) as client:   # 2.x 一站式:spawn 进程 + 接管 stdio + JSON-RPC
    result = await client.list_tools()        # ① 看菜单
    for t in result.tools:                    #    2.x:result 是对象,要 .tools
        print(t.name)

    result = await client.call_tool("add_episode", {...})   # ② 点单
    print(result.is_error)                                 #    出错标志
    print([c.text for c in result.content])                #    真实内容在 .content[].text

    result = await client.call_tool("query_memory", {})    # ③ 读回验证
```

**2.x 返回值套路（记死）**：`list_tools()` → `.tools` 拿列表；`call_tool()` → `.content`（列表，元素是 TextContent，取 `.text`）+ `.is_error` 判成败。忘了这步会拿到一个"看不懂的 Pydantic 对象"。

---

## 三、测试验收

### 验收 1：Inspector 网页可见工具（✅ 截图确认）

`mcp dev mcp_server.py` → 浏览器自动打开 Inspector → 左侧看到两个工具 + 右侧 Messages 完整打印 TOOLS/LIST、NOTIFICATIONS/INITIALIZED → **server 与调试台握手成功**。

### 验收 2：query_memory 空库分支（✅ 截图确认）

填 `stu001` / `limit=5` 点测试 → Results 返回：

```
该学生暂无学习记录
```

（31ms 完成，协议报文 TOOLS/CALL query 打印在 Messages。）

### 验收 3：add_episode 写入 + query_memory 读回（✅ 截图确认）

点 `add_episode` 填 `一元二次方程 / 今天学了求根公式 / 0.8` → 返回 `已记录 #1:一元二次方程(得分 0.8)`；切回 `query_memory` 再查 → 返回：

```
- [一元二次方程] 0.0天前 强度0.80
```

**全链路闭环：写 → 存 → 衰减排序 → 读回，一次跑通。**

### 验收 4：Python 客户端三步（✅ 已跑通）

`test_mcp_client.py`：① list_tools 列出两工具 → ② call `add_episode`（is_error=False）→ ③ call `query_memory` 读回写入内容。**证明不靠 Inspector 也能以纯代码方式调用你的 server**——这就是未来 AI 应用接它的方式。

---

## 四、本节踩坑清单

| # | 坑 | 表现 | 根治 |
|---|---|---|---|
| 1 | **版本换代没察觉**（FastMCP → MCPServer） | 照 1.x 教程写，import 直接报错 | 装完先 `pip show mcp` 看版本；报错先怀疑"版本语法变了"，查官方文档而非旧教程 |
| 2 | `mcp dev` 红点 Failed | Inspector 起不来 | 它强制依赖 uv（`pip install uv`）——工具链前置条件要装齐 |
| 3 | `rows[2]` 当单行用 | IndexError | `rows` 是**多行元组**的列表，必须 `for r in rows:` 逐行取 `r[2]`（第 3 次踩"列表套元组"） |
| 4 | `return` 缩进进 for 里 | 只输出最后 1 行 | 拼接要循环内 append、循环外 return（老熟人了，第 5 次） |
| 5 | 函数忘了 return | 工具返回 None | 工具函数**必须有返回值**，否则客户端拿到空 |
| 6 | 用 `STUDENT` 常量"代替"参数 | 参数失效，写死 stu001 | 想"默认给 stu001 但允许覆盖"→ 用默认值 `student_id: str = STUDENT`，别把参数删了 |
| 7 | 相对路径 DB_PATH | 子进程找不到库/建错库 | 用 `os.path.join(os.path.dirname(os.path.abspath(__file__)), ...)` 钉死 |
| 8 | `conn.close()` 忘关 | 连接泄漏（小库无感，量大卡死） | 用完即关；server 每次调用都开新连接，务必配对关闭 |

---

## 五、论文定位（答辩话术）

- **第 6 章 RAG / 记忆系统可无缝升级**：本系统（学习伴侣）的记忆读写、RAG 检索本质都是"工具"，论文第 6 章可以把检索链路包成 MCP Server，**对接任意 LLM 宿主（Claude/Cursor/自研 Web）**——"我的记忆模块是标准协议服务，即插即用"。
- **工程化亮点**：用 `mcp dev` + Inspector 做协议级调试（不是 print 猜），Messages 面板展示 JSON-RPC 原始报文 = 工程规范性的实证素材。
- **面试话术**：能说出"我写过 MCP Server，理解 Host/Client/Server 三角色、stdio 传输、list_tools/call_tool 生命周期，踩过 2.x 改名坑"——这在 Agent 应用岗是**硬通货**（大模型应用都在谈 MCP 生态）。

---

## 六、代码骨架速查

```python
# mcp_server.py —— 把 2.5b 情景记忆包成标准工具
from mcp.server.mcpserver import MCPServer        # 2.x 写法(FastMCP 已改名)
from memory_episodic import init_db, save_episode # 复用 2.5b
from memory_decay import search_episodes

server = MCPServer("learning-memory")             # 容器实例
STUDENT = "stu001"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.db")

@server.tool()                                    # ① 登记工具(带签名+docstring=菜单)
def query_memory(student_id: str = STUDENT, limit: int = 5) -> str:
    """查询某学生的最近学习记录(情景记忆,按时间衰减排序)。"""
    conn = init_db(DB_PATH)
    rows = search_episodes(conn, student_id, limit)
    conn.close()
    if not rows:
        return "该学生暂无学习记录"
    lines = []
    for r in rows:                                 # r = (strength, id, topic, days, weight)
        lines.append(f"- [{r[2]}] {r[3]:.1f}天前 强度{r[0]:.2f}")
    return "\n".join(lines)                        # 循环外 return

@server.tool()
def add_episode(topic: str, summary: str, score: float, difficulty: str = "中") -> str:
    """记录一次学习会话(情景记忆写入)。"""
    conn = init_db(DB_PATH)
    new_id = save_episode(conn, STUDENT, topic, summary, difficulty, score)
    conn.close()
    return f"已记录 #{new_id}:{topic}(得分 {score})"

if __name__ == "__main__":
    server.run()                                   # 读 stdin → 干活 → 写 stdout
```

```bash
# 一条命令拉起调试台(自动开浏览器,依赖 uv)
mcp dev mcp_server.py
# 浏览器手动访问 http://localhost:5173
```

```python
# test_mcp_client.py —— 纯代码客户端(将来 AI 应用就是这样接你的 server)
async with Client(server_params) as client:
    await client.list_tools()            # → .tools
    await client.call_tool("add_episode", {...})   # → .is_error / .content[].text
    await client.call_tool("query_memory", {})     # → .content[].text
```

完整代码：`agent_project/mcp_server.py`、`agent_project/test_mcp_client.py`（依赖 2.5b 的 `memory_episodic.py` / `memory_decay.py`）。
