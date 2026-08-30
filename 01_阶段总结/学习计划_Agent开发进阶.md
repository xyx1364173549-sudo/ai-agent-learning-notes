# 🚀 Agent 开发进阶学习计划（14 天基础后的下一站）

> **学习人：** 小轩轩
> **开始日期：** 2026年8月12日
> **前置基础：** Python 13 练习 + 2 项目全部完成 ✅
> **本阶段目标：** 接真实 LLM API（DeepSeek），做出"迷你 Agent"，同时学会 Git 上传作品集

---

## 🗺️ 学习路线总览

```
阶段 1（第 1-2 天）  接 DeepSeek API → 对话程序 → 迷你 Agent（带天气工具）
阶段 2（第 3 天）    Git/GitHub 入门 → 三个项目推上 GitHub
阶段 3（第 4-7 天）  按需补进阶 → .env / 流式输出 / 多工具注册
```

**核心思路：** 每一步都在"做东西"，遇到什么学什么——不做纯理论。

---

# 📅 阶段 1（第 1-2 天）：接 DeepSeek API，做出迷你 Agent

## 🎯 阶段目标

1. 学会用 DeepSeek API（OpenAI 兼容格式）发对话请求
2. 做出一个"命令行对话程序"
3. **把天气工具接进去**——做出"迷你 Agent"

## 第 1 天：基础对话

### 步骤 1：准备 API Key（5 分钟）

1. 登录 [DeepSeek 开放平台](https://platform.deepseek.com)
2. 创建 API Key（复制保存，**别发给别人**）
3. 充值（新用户一般有赠送额度，个人测试几块钱够用）

> ⚠️ **API Key 就是你"账户的钱包钥匙"**——别写死在代码里（阶段 3 教你放 .env），更别传到 GitHub！

### 步骤 2：创建项目 + 安装依赖（5 分钟）

```bash
mkdir "C:\Document\agent_project"
cd "C:\Document\agent_project"
python -m venv .venv
source .venv/Scripts/activate        # Git Bash
pip install requests
pip freeze > requirements.txt
```

### 步骤 3：第一个 LLM 调用（30 分钟）⭐

创建 `llm_client.py`：

```python
"""DeepSeek LLM 客户端 —— 第一步：能发对话请求"""
import requests

API_KEY = "sk-你的key"               # ⚠️ 临时写这里，阶段3改放到.env
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"              # 通用对话模型（还有 deepseek-reasoner 推理模型）


def chat(messages: list[dict], api_key: str = API_KEY) -> str | None:
    """发送对话请求，返回 AI 的回复文本"""
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,     # ← 消息历史！后面用得到
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # 测试：单个问题
    reply = chat([
        {"role": "system", "content": "你是一个乐于助人的助手"},
        {"role": "user", "content": "用一句话介绍你自己"},
    ])
    print("AI:", reply)
```

### ✅ 第 1 天验收

- [ ] 运行后能打印出 DeepSeek 的回复
- [ ] 理解 `messages` 结构（system/user/assistant 三元组——你在练习 4.3 见过！）
- [ ] 理解返回结构 `["choices"][0]["message"]["content"]`（练习 4.2 的 API 响应结构！）

---

## 第 2 天：对话循环 + 迷你 Agent

### 步骤 1：对话循环程序（45 分钟）⭐

创建 `chat_cli.py`：

```python
"""命令行对话程序 —— 像 ChatGPT 一样连续聊天"""
from llm_client import chat


def main():
    messages = [
        {"role": "system", "content": "你是一个乐于助人的助手，回答要简洁"},
    ]
    print("=== 命令行 ChatGPT（输入 quit 退出）===")

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() == "quit":
            break

        messages.append({"role": "user", "content": user_input})   # 1. 加用户消息

        reply = chat(messages)                                     # 2. 发给 API

        messages.append({"role": "assistant", "content": reply})   # 3. 存 AI 回复
        print(f"AI: {reply}")                                       # 4. 显示


if __name__ == "__main__":
    main()
```

**核心：`messages` 列表就是"对话记忆"**——每次都把整个历史发给 API，AI 才能"记得"前面说了啥。

### 步骤 2：接入天气工具 → 迷你 Agent（1-2 小时）⭐⭐ 本阶段压轴

创建 `mini_agent.py`——**把项目一的 WeatherClient 变成 Agent 的工具**：

```python
"""迷你 Agent：能查天气的 AI 助手
架构：LLM 判断意图 → 调用工具 → 把结果给 LLM 组织回答
"""
import sys
sys.path.insert(0, r"C:\Document\weather_tool")   # 导入项目一的天气客户端
from weather_tool import WeatherClient
from llm_client import chat

weather = WeatherClient()


def get_weather_tool(city: str) -> str:
    """天气工具：输入城市名，返回天气文本"""
    data = weather.get_weather(city)
    if data:
        # 复用项目一的格式化函数！(它返回城市/温度/天气/湿度)
        from weather_tool import format_weather
        return format_weather(data)
    return "查询天气失败"


SYSTEM_PROMPT = """你是一个智能助手，可以调用以下工具：
- 查天气: 当用户问天气时，调用 get_weather_tool(城市名)，把结果转述给用户
你只能使用提供的工具，不要编造数据。"""


def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("=== 迷你 Agent（试试问：北京天气怎么样）===")

    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() == "quit":
            break

        messages.append({"role": "user", "content": user_input})

        # 简单意图判断：包含"天气"就调用工具（第 4 天升级为 LLM 判断）
        if "天气" in user_input:
            city = extract_city(user_input)          # 提取城市名
            tool_result = get_weather_tool(city)     # ← 调用真实工具！
            messages.append({
                "role": "user",
                "content": f"工具返回的天气数据:\n{tool_result}\n请转述给用户",
            })

        reply = chat(messages)
        messages.append({"role": "assistant", "content": reply})
        print(f"AI: {reply}")


def extract_city(text: str) -> str:
    """从"北京天气怎么样"里提取城市名（简单版：去掉常见词）"""
    for word in ["天气", "怎么样", "怎么样？", "如何", "如何？", " ", "？", "?"]:
        text = text.replace(word, "")
    return text.strip() or "Beijing"


if __name__ == "__main__":
    main()
```

### ✅ 第 2 天验收

- [ ] 对话循环能连续聊天（AI 记得前文）
- [ ] 输入"北京天气怎么样"→ 真实调用天气 API → AI 转述天气
- [ ] 输入普通问题（如"1+1等于几"）→ 正常回答
- [ ] 理解整体架构：LLM（大脑）+ 工具（手）+ 消息历史（记忆）

---

# 📅 阶段 2（第 3 天）：Git/GitHub 入门

## 🎯 目标

把三个项目（天气工具、TODO、Agent）推上 GitHub，成为你的**作品集**。Git 不用学全，会 6 条命令就够开始。

## 步骤 1：准备（10 分钟）

1. 注册 [GitHub](https://github.com)（有账号跳过）
2. 下载安装 [Git for Windows](https://git-scm.com/download/win)
3. 配置身份（命令行执行一次，永久生效）：

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

## 步骤 2：6 条核心命令（30 分钟）

| 命令 | 作用 | 类比 |
|------|------|------|
| `git init` | 把文件夹变成仓库 | 开一个新账本 |
| `git add .` | 把改动放进"暂存区" | 把货物搬上推车 |
| `git commit -m "说明"` | 把暂存区存成"快照" | 封箱贴标签 |
| `git log` | 查看历史提交 | 翻账本 |
| `git push` | 推到 GitHub | 把箱子运到仓库 |
| `git pull` | 从 GitHub 拉最新 | 把仓库的新货搬下来 |

**工作流（每次改代码循环）：**
```bash
git add .                # 1. 装车
git commit -m "加了对话功能"   # 2. 封箱
git push                 # 3. 运走
```

## 步骤 3：推送第一个项目（30 分钟）⭐

以天气工具为例：

```bash
cd "C:\Document\weather_tool"

# 1. 创建 .gitignore（告诉 Git 别上传哪些文件）⭐ 重要！
echo ".venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.json" >> .gitignore        # 天气数据文件不上传

# 2. 初始化仓库
git init

# 3. 提交所有代码
git add .
git commit -m "智能天气查询工具 v1.0"

# 4. 在 GitHub 网页上新建仓库（不勾选 README），复制仓库地址
git remote add origin https://github.com/你的用户名/weather_tool.git
git branch -M main
git push -u origin main
```

**完成后**：浏览器打开 GitHub 页面，你的代码就在上面了！🎉

## 步骤 4：推送另外两个项目（各 15 分钟）

TODO 管理器（`todo_project`）、Agent 项目（`agent_project`）同样操作。**注意每个项目单独 `git init`**（一个仓库一个项目）。

### ⚠️ Git 常见坑

| 坑 | 解决 |
|----|------|
| 把 `.venv` 传上去了 | .gitignore 写 `.venv/`（必须做！）|
| `git push` 报错认证失败 | 用 GitHub Token 代替密码（Settings → Developer settings → Tokens）|
| commit 完发现忘改文件 | `git add .` 后再 `git commit --amend` |
| 想回到之前的版本 | `git log` 看历史，`git checkout <版本号> -- 文件名` |

### ✅ 阶段 2 验收

- [ ] `git config` 配置成功
- [ ] 三个项目都在 GitHub 上可见
- [ ] `.venv` 没有被上传
- [ ] 会执行 `add → commit → push` 循环

---

# 📅 阶段 3（第 4-7 天）：按需补进阶

**原则：做 Agent 时遇到什么学什么。** 下面按优先级排列，不一定要全学。

## 第 4 天：密钥管理（.env）⭐⭐ 必学

**问题：** API Key 写死在代码里，传 GitHub 就泄露！

```bash
pip install python-dotenv
```

创建 `.env` 文件（**加入 .gitignore！**）：
```
DEEPSEEK_API_KEY=sk-你的key
```

改 `llm_client.py`：
```python
import os
from dotenv import load_dotenv

load_dotenv()                              # 读取 .env
API_KEY = os.getenv("DEEPSEEK_API_KEY")    # 从环境拿，不再写死
```

**为什么重要：** 这是软件工程的安全底线——密钥进仓库 = 账户被盗风险。

## 第 5 天：智能意图判断（升级迷你 Agent）⭐⭐

**问题：** 现在用"if 天气 in 输入"判断，太笨。让 LLM 自己决定调不调工具！

**方案 A：让 LLM 输出 JSON 指令（你练过 JSON！）**

```python
def ask_llm_for_action(user_input: str) -> dict:
    """让 LLM 判断：要不要调工具、调哪个、传什么参数"""
    prompt = f"""分析用户请求，输出 JSON：
{{"tool": null 或 "weather", "city": "城市名"}}
用户请求: {user_input}"""
    reply = chat([{"role": "user", "content": prompt}])
    import json
    return json.loads(reply)              # JSON → 字典（练习 4！）
```

然后主循环根据返回的 `tool` 字段决定调不调工具——**这就是"LLM 驱动的工具调用"雏形**（正式叫 Function Calling，DeepSeek 支持原生版）。

## 第 6 天：流式输出（打字机效果）⭐

**你学过异步（练习 13）！** DeepSeek 支持流式：

```python
def chat_stream(messages: list[dict]) -> str:
    """流式对话：AI 边生成边返回（打字机效果）"""
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={...},
        json={"model": MODEL, "messages": messages, "stream": True},
        timeout=60,
        stream=True,                      # 流式响应
    )
    full = ""
    for line in resp.iter_lines():        # 逐行读取（生成器！练习11）
        if not line:
            continue
        # 解析 SSE 格式（data: {...}）
        text = parse_sse(line)
        if text:
            print(text, end="", flush=True)   # 边收边打
            full += text
    return full
```

**这就是 ChatGPT 逐字输出的原理**——你练习 11 的 stream_response 终于派上真用场！

## 第 7 天：多工具注册（复用你的 ToolBox！）

**你项目二已经写了 ToolBox 模式！** 现在扩展成 Agent 版：

```python
TOOLS = {
    "weather": {"func": get_weather_tool, "desc": "查询天气，参数：城市名"},
    # 以后加：{"func": calculator, "desc": "计算器"}...
}

def execute_tool(name: str, arg: str) -> str:
    """根据工具名调用对应函数（练习 7.3 ToolBox 模式！）"""
    tool = TOOLS.get(name)
    if tool:
        return tool["func"](arg)
    return "工具不存在"
```

---

# ✅ 本阶段最终验收（全部打勾 = Agent 开发入门成功）

- [ ] DeepSeek API 调用成功（`llm_client.py`）
- [ ] 命令行对话程序能连续聊天
- [ ] 迷你 Agent 能调用天气工具并转述结果
- [ ] Git 三条核心命令熟练（add/commit/push）
- [ ] 三个项目推上 GitHub（.venv 没上传）
- [ ] API Key 放在 .env（没泄露）
- [ ] LLM 判断意图调用工具（Function Calling 雏形）
- [ ] 流式输出打字机效果
- [ ] 多工具注册（ToolBox 模式扩展）

---

# 🚨 本阶段可能遇到的问题

| 问题 | 解决 |
|------|------|
| `401 Unauthorized` | API Key 错了或没充值 |
| `429 Too Many Requests` | 调用太频繁，加 `time.sleep(1)` |
| 回复很长很啰嗦 | system prompt 里加"回答要简洁" |
| 中文乱码 | 确认文件保存为 UTF-8 |
| `git push` 失败 | 检查 Token / 网络 / `git remote -v` |
| 天气工具导入失败 | `sys.path.insert` 路径写对，或用包结构 |

---

# 📚 推荐学习资源（遇到不懂的再查）

- **DeepSeek API 文档**：https://api-docs.deepseek.com （中文文档，清晰）
- **Git 教程**：廖雪峰 Git 教程（中文经典，免费）
- **Python 官方文档**：https://docs.python.org/zh-cn/3/
- **遇到问题**：先自己 print 调试 → 再搜报错信息 → 最后问 AI

---

> **最后的话：**
> 你已经从"看不懂代码"走到了"能调真实 AI"——这一步之后，你就是**真正在做 Agent 开发**了。
> 学完这个阶段，把项目推上 GitHub，你的简历/作品集就有东西了！
>
> 加油，小轩轩！🚀🎉
