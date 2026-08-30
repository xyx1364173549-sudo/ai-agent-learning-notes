# 📚 阶段 2 总结：Git + GitHub 全流程手册

> **学习人：** 小轩轩
> **完成日期：** 2026年8月13日-14日
> **状态：** ✅ 三个项目全部推上 GitHub（weather_tool / todo_project / agent_project）
> **用途：** 以后每次要"把项目传上 GitHub"或"更新代码"时，照这份手册操作即可

---

## 📋 一句话总览

**Git 是一个"版本控制"工具，GitHub 是存放代码的云端网站。** 用 Git 把你的代码"打包快照"，再推到 GitHub 上永久保存、对外展示。整个过程只有 6 条命令反复用。

---

## 🗺️ 核心概念：一个文件要走的"四个房间"

```
┌─────────┐  git add   ┌─────────┐  git commit  ┌──────────┐  git push   ┌──────────┐
│  工作区  │ ─────────→ │  暂存区  │ ───────────→ │  本地仓库 │ ──────────→ │ 远程仓库  │
│ 你的文件夹│           │ 装货推车 │             │ 快照存档  │             │  GitHub  │
└─────────┘            └─────────┘              └──────────┘  ←─────────  └──────────┘
                                                                   git pull
```

| 区域 | 是什么 | 类比 |
|------|--------|------|
| **工作区** | 你的项目文件夹，改代码的地方 | 仓库货架 |
| **暂存区** | 你挑出来"准备打包"的改动 | 装货的推车 |
| **本地仓库** | 已保存的历史版本（在 `.git` 文件夹里）| 封箱存档的库房 |
| **远程仓库** | GitHub 上的云端仓库 | 异地总库房 |

> 📦 **记忆锚点**：`add` 搬货上车 → `commit` 封箱贴单 → `push` 运到云端。没 push 之前，GitHub 上什么都没有。

---

## 🔧 一次性准备（每台电脑只做一次）

### 1. 安装 Git

下载安装 [Git for Windows](https://git-scm.com/download/win)，一路下一步即可。

### 2. 配置身份（告诉 Git "你是谁"）

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

> 这两行信息会写进每一次提交的"作者"栏，方便追溯。

### 3. 配置代理（国内访问 GitHub 必备）⚠️ 重要

国内直连 GitHub 常超时（报 `Failed to connect to github.com:443`）。如果你的代理软件是 **Clash Verge**，端口默认可能是 **7897**（不是网上常说的 7890）：

```bash
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
```

> **怎么查端口**：命令行执行 `netstat -ano | grep LISTENING | grep 127.0.0.1`，看代理进程（clash-verge / mihomo / v2ray）监听在哪个端口。
>
> 取消代理（如果以后网络好了）：
> ```bash
> git config --global --unset http.proxy
> git config --global --unset https.proxy
> ```

---

## 🚀 首次推送：完整 8 步流程

> 以下用天气工具为例。**推其他项目时，只需替换第 1 步的目录和第 8 步的仓库地址。**

### 第 0 步：在 GitHub 网页建仓库

1. 打开 https://github.com ，登录
2. 右上角 **「+」→「New repository」**
3. 仓库名填项目名（如 `weather_tool`），选 **Public**
4. **不要勾选** "Add a README file"（勾了会和本地冲突）
5. 点 **Create repository**，记下仓库地址（形如 `https://github.com/用户名/仓库名.git`）

### 第 1 步：进入项目目录

```bash
cd "C:/Document/weather_tool"
```

### 第 2 步：创建 `.gitignore`（排除不该上传的文件）

```bash
echo ".venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo ".idea/" >> .gitignore
echo "*.json" >> .gitignore
```

**`.gitignore` 是"黑名单"**，告诉 Git 这些文件别管：

| 规则 | 排除什么 | 为什么 |
|------|---------|--------|
| `.venv/` | 虚拟环境 | 几百 MB，别人能自己重建 |
| `__pycache__/` | Python 缓存 | 垃圾文件 |
| `.idea/` | PyCharm 配置 | 个人编辑器配置 |
| `*.json` | JSON 数据 | 运行时生成的临时数据 |
| `.env` | 密钥文件 | **绝不能泄露**（见下文专节）|

> **`>` 和 `>>` 的区别**：`>` 覆盖写（第一次），`>>` 追加写（后续）。

### 第 3 步：初始化仓库

```bash
git init
```

> 创建 `.git` 隐藏文件夹 = "开了一本空白账本"。

### 第 4 步：查看状态（可选但推荐）

```bash
git status
```

> 看哪些文件"未被跟踪"（红色）。**确认 `.venv`、`.env` 没出现在列表里**——出现就说明 `.gitignore` 写错了。

### 第 5 步：全部加入暂存区

```bash
git add .
```

> 注意 `add` 和 `.` 之间**有空格**。`.` 代表"当前文件夹所有文件"。

### 第 6 步：再次确认（上传前最后安检）⚠️

```bash
git status
```

> 现在文件应变成绿色 `Changes to be committed`。**仔细看一遍列表，确认没有 `.env`、`.venv`**。这是密钥泄露的最后防线。

### 第 7 步：封箱提交

```bash
git commit -m "第一个版本：智能天气查询工具"
```

> `-m` = message，写清楚"这次改了什么"。消息要具体，别写"改了点东西"。

### 第 8 步：连远程 + 推送

```bash
git remote add origin https://github.com/用户名/weather_tool.git
git branch -M main
git push -u origin main
```

> - `remote add origin` = 登记云端仓库地址，`origin` 是给它起的外号
> - `branch -M main` = 把分支名从 master 改成 main（GitHub 新标准）
> - `push -u origin main` = 推送，`-u` 建立跟踪（以后直接 `git push` 即可）

**成功标志**：看到 `Writing objects: 100%` 和 `main -> main`。

---

## 🔄 以后更新代码：日常 3 步循环

项目已经在 GitHub 上后，每次改完代码只需：

```bash
git add .                                    # 1. 装车
git commit -m "描述这次改了什么"              # 2. 封箱
git push                                     # 3. 运走（已跟踪，无需 -u origin main）
```

> 这是你以后最高频的操作。改完代码 → 这三条 → 完事。

**⚠️ 提交时机（重要习惯）**：每完成一个**独立功能**就提交一次，不要攒好几个功能一起提交。

- ❌ 错误：上午做了"意图判断"、下午做了"流式+多工具"，晚上一次性 `git add .` 全提交 → 历史糊成一团，出 bug 难定位
- ✅ 正确：做完"意图判断"→ 立即 commit；做完"流式"→ 立即 commit；做完"多工具"→ 立即 commit

**为什么**：commit 是"版本快照"，粒度越细，`git log` 越清晰，回滚越精准。

---

## 🔒 专节：`.env` 密钥管理（安全底线）

**绝对不要**把 API Key、密码写进代码后推上 GitHub——一旦推上去，**即使删除文件，密钥也会永久留在 Git 历史里**，等于全网公开你的钱包钥匙。

### 正确做法三步

**1. 建 `.env` 文件存密钥**（注意编码，见下方坑 6）：
```
DEEPSEEK_API_KEY=sk-你的key
```

**2. `.gitignore` 里加一行**：
```bash
echo ".env" >> .gitignore
```

**3. 代码里读取**：
```python
import os
from dotenv import load_dotenv

load_dotenv()                              # 读取 .env 文件
API_KEY = os.getenv("DEEPSEEK_API_KEY")    # 从环境变量取 Key
```

依赖安装：`pip install python-dotenv`

---

## 🧰 6 条核心命令速查表

| 命令 | 作用 | 类比 |
|------|------|------|
| `git init` | 把文件夹变成仓库 | 开新账本 |
| `git add .` | 改动放入暂存区 | 货搬上推车 |
| `git commit -m "说明"` | 存成快照 | 封箱贴标签 |
| `git log` | 看历史提交 | 翻账本 |
| `git push` | 推到 GitHub | 箱子运到仓库 |
| `git pull` | 从 GitHub 拉最新 | 把新货运下来 |

**其他常用**：

| 命令 | 作用 |
|------|------|
| `git status` | 看当前状态（最常用！）|
| `git remote -v` | 看远程仓库地址 |
| `git branch -a` | 看分支 |
| `git rm --cached 文件` | 把误 add 的文件移出暂存区 |

---

## 🪤 踩坑清单（本次实战遇到的）

| # | 坑 | 解决 |
|---|----|------|
| 1 | `.gitignore` 拼成 `gittignore` | 正确是 `.gitignore`（点开头 + git + ignore）|
| 2 | `git add .` 写成 `git add.` | `add` 和 `.` 之间要有空格 |
| 3 | `git remote add` 报 "already exists" | 说明之前已加过，直接跳过这步 |
| 4 | 连不上 github.com:443 | 配代理（见上文"配置代理"）|
| 5 | push 时浏览器被误关 | 重新执行 `git push -u origin main` 即可，会再次弹认证 |
| 6 | `.env` 用 PowerShell `echo >` 创建 → UTF-16 编码报 UnicodeDecodeError | 用 PyCharm 把编码改为 UTF-8（无 BOM），或用 Python 写：`open('.env','w',encoding='utf-8').write(...)` |
| 7 | GitHub 建仓库时勾了 README | 会导致 push 冲突。建仓库时不要勾 README |

---

## ✅ 自测清单（答得上来 = 过关）

- [ ] 四个区域分别是什么？add/commit/push 各自在哪个区域之间搬运？
- [ ] `.gitignore` 为什么要加 `.venv` 和 `.env`？
- [ ] `>` 和 `>>` 的区别？
- [ ] 首次推送为什么要 `-u origin main`，日常更新为什么只要 `git push`？
- [ ] API Key 为什么不能写进代码推 GitHub？
- [ ] `git status` 能帮你发现什么问题？

---

## 📍 你的三个仓库（作品集）

| 项目 | 地址 |
|------|------|
| 天气查询工具 | https://github.com/xyx1364173549-sudo/weather_tool |
| TODO 管理器 | https://github.com/xyx1364173549-sudo/todo_project |
| 迷你 Agent | https://github.com/xyx1364173549-sudo/agent_project |

> **下一步**（第 5 天）：让 LLM 自己判断"要不要调工具、调哪个"——把"if 天气 in 输入"的笨判断，升级成 Function Calling。加油，小轩轩！🚀
