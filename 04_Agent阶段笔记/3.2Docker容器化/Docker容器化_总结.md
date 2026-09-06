# 3.2 Docker 容器化 · 详细版

> 本节是阶段三"工程化"的第二枪：解决那个程序员最烦的千古难题——**"我电脑上明明能跑，怎么到你那就不行了？"** 学完你要能回答三件事——Docker 到底把什么"打包"了？镜像和容器是什么关系？为什么 `docker run` 打出来的是 Linux 而不是你的 Windows？

---

## 一、总结

**一句话概括**：

> **Docker = 把"代码 + 运行环境（Python 版本 + 所有依赖包）"打包成一个自给自足的标准箱子（镜像 image），箱子到任何装了 Docker 的机器上都能 `docker run` 原样跑起来（容器 container）。它解决的是"环境地狱"——一次打包，处处运行，代码跑在箱子自己的 Linux 里，跟宿主机的环境彻底隔离。**

### 痛点：换台电脑，环境就崩

| 没有 Docker 的世界 | 有了 Docker 之后 |
|---|---|
| 换机器要重装 Python、重配依赖、版本还可能对不上 | 一行 `docker run 镜像名` 原地跑起来 |
| "我这儿明明是好的啊！"（环境不一致） | 箱子自带环境，跑哪都一样 |
| 部署到服务器 / 给面试官演示 = 从头搭环境 | 把镜像给他，他 `docker run` 就完事 |

**类比**：以前是"带着你的厨房去别人家做饭"（到处装环境）；Docker 是"把整份做好的菜连锅端过去，开火即食"。

### 为什么 Agent 时代这事重要

你的论文系统（学习伴侣 Agent）最终要部署、要给别人跑、要写进简历给面试官验收。如果不 Docker 化，换个人跑就是灾难；Docker 化后，面试官一句 `docker run` 就能看到你的系统活起来——**这是"工程能力"的直接证明**。

---

## 二、对应知识点

### 3.2.1 Docker 三件套（用你计科最熟的"编译"类比钉死）

| Docker 概念 | 你熟悉的类比 | 本质 |
|---|---|---|
| **Dockerfile** | 源码（`.c` 文件） | 一份文字说明书：用什么底子、装什么、跑什么 |
| **镜像 Image** | 编译出的可执行文件（`.exe`） | 按说明书"构建"出的**只读成品**，不可改、可复制千万份 |
| **容器 Container** | 双击 `.exe` 后**跑起来的进程** | 镜像"运行"出来的实例，能启能停、能同时跑多个 |

**面试必考**：镜像和容器的关系 = **程序 vs 进程**。同一个 `.exe` 能开 100 个窗口，同一个镜像也能跑 100 个互不干扰的容器。

```
Dockerfile  --docker build-->  镜像  --docker run-->  容器
   (源码)                     (可执行文件)          (进程)
```

### 3.2.2 Dockerfile 的四条核心指令（本节"知识点"本体）

| 指令 | 作用 | 类比 |
|---|---|---|
| `FROM` | 指定**底子**（基础镜像） | "这房子盖在什么地基上"——`python:3.13-slim` = 自带 Python 3.13 的干净 Linux |
| `WORKDIR` | 设定容器内**工作目录** | "进屋后默认站在哪个房间" |
| `COPY` | 把你电脑的文件**塞进**镜像 | "把我电脑里的东西搬进房子" |
| `CMD` | 容器**启动后跑什么** | "入住后第一件事干什么"（每次 run 都执行） |

**顺序逻辑（背下来）**：先选地基（FROM）→ 定站位（WORKDIR）→ 搬东西（COPY）→ 定好入住干什么（CMD）。

```dockerfile
FROM python:3.13-slim   # ① 地基：自带 Python 的干净 Linux（不是你 Windows！）
WORKDIR /app            # ② 工作目录：容器里的"当前文件夹"
COPY app.py .           # ③ 搬东西：把你的代码复制进 /app
CMD ["python","app.py"] # ④ 启动后干什么：运行这个脚本
```

### 3.2.3 两个核心命令

```powershell
docker build -t my-first-app .   # 读 Dockerfile → "编译"成镜像（-t 起名，. 表示 Dockerfile 在当前目录）
docker run my-first-app          # 用镜像"启动"一个容器（执行 CMD）
```

`build` 成功会看到 `=> naming to docker.io/library/my-first-app:latest`；`run` 就执行你 CMD 里写的那件事。

### 3.2.4 ⭐ 层缓存机制（这次 build 亲眼看到的 `CACHED`）

第二次 build 时出现：

```
=> CACHED [2/3] WORKDIR /app      0.0s
```

`CACHED` = **用了缓存**。Dockerfile 的**每一行是一个"层"**，构建时：

- 某层的内容没变 → 直接拿上次缓存，**不重做**（省时）
- 某层变了（比如你改了 `app.py`，`COPY` 那层就变）→ 该层及之后的层才重做

这就是"改一行代码，重新 build 只要 1 秒"的原因。**面试常问"为什么 build 那么快"——答案就是层缓存。**

**机制再拆细一点（逐层对指纹）**：每一层都算一个"指纹（hash）"，下次 build 时逐层对比：

| 层 | 变了没 | 结果 |
|---|---|---|
| FROM（基础镜像） | 没变 | ✅ CACHED 复用 |
| WORKDIR | 没变 | ✅ CACHED 复用 |
| COPY（代码） | 改了 app.py | ❌ 重做 |
| CMD（在 COPY 后） | 在变层之后 | ❌ 跟着重做 |

所以"快"的本质是 **增量构建**——只重做"变动的层及其之后"，前面的大头（拉基础镜像、装依赖）全命中缓存。计科视角：这就是**增量编译**（没改的 `.c` 不重新编译，只编译改过的 + 重新链接）。

**工程技巧（面试加分）**：既然"变的层及之后全重做"，就把**最不易变的放前面、最易变的放后面**：

```dockerfile
FROM python:3.13.12-slim
WORKDIR /app
COPY requirements.txt .             # ① 先 COPY 依赖清单
RUN pip install -r requirements.txt # ② 装依赖（最慢，但最不常变）
COPY . .                            # ③ 最后才 COPY 代码（最常变）
CMD ["python","app.py"]
```

为什么 `requirements.txt` 要**单独 COPY、放在代码前**？因为 `pip install` 最耗时，若和代码一起 COPY，你每改一行代码都要重装一遍依赖。单独让它占一层 → **改代码时"装依赖"那层命中缓存，不重装**。

### 3.2.5 ⭐ 环境隔离（3.2 的第一性原理，本次实验的核心结论）

`docker run` 打印出：

```
Python 版本：3.13.15
操作系统：  Linux 6.18.33.2-microsoft-standard-WSL2
```

三个铁证证明"代码跑在容器里，不是跑在你 Windows 上"：

| 输出 | 证明 |
|---|---|
| `操作系统：Linux ...WSL2` | 你电脑是 Windows，但代码跑在 Linux 容器里 |
| `Python 版本：3.13.15` | 不是你电脑的 Python（3.13.12 / 3.14.6），是 `python:3.13-slim` 镜像自带的 |
| 报错路径 `/app/app.py` | 容器内部路径，不是 `C:\Document\...` |

> **一句话钉死：Docker 把"代码 + 环境"打包成自给自足的箱子，run 的时候箱子自己带环境跑，跟宿主机（你电脑）彻底隔离。** 所以到任何机器都原样跑，不再有"环境不一致"的坑。

### 3.2.6 WSL2 后端：为什么 Docker 的引擎"看不见"你的 Windows 代理

Docker Desktop 的引擎跑在 **WSL2 的 Linux 虚拟机**里，它有**独立的网络环境**，跟你 Windows 是两个世界。所以：

- 你 Windows 上开的 Clash 系统代理，**管不到虚拟机里的 Docker**
- 必须**单独给 Docker Desktop 配代理**（Settings → Resources → Proxies 填 `http://127.0.0.1:7897`），或配**镜像加速器**（Docker Engine 里加 `registry-mirrors`）

这是国内拉 Docker Hub 镜像最经典的坑（下面踩坑清单详述）。

### 3.2.7 `.venv` vs Docker：一个管"写"，一个管"跑"

两者**不冲突、不替代**，是流水线上的两站：

| | 写代码（开发） | 跑代码（部署） |
|---|---|---|
| 在哪 | 你的电脑（Windows） | 容器（Linux） |
| 用什么 | PyCharm + 本地 Python + .venv | 镜像自带 Python + Linux |
| 靠谁统一环境 | requirements.txt | Docker 镜像 |

- `.venv` + requirements.txt → 统一"开发时写什么版本"
- Docker → 统一"运行时用什么环境"

**类比**：`.venv` 是"调料清单"（写清要哪些料，但每人还得自己买）；Docker 是"把做好的菜连锅打包"（锅和料都装好，端过去就吃）。

> **Docker 主要管"跑"，不管"写"**：写代码时你人在电脑上，靠 PyCharm 的补全/调试（它认本地 Python）；跑代码时才轮到 Docker，在容器里用镜像自带的 Python。所以"拉同一个镜像写代码"不是主流做法（在容器里写很别扭）；真正实现这个想法的是进阶玩法 **Dev Container**。

### 3.2.8 镜像 = 通用基础镜像 + 你的定制层（"拉取"到底拉的是什么）

```
你的镜像 = 基础镜像(通用毛坯) + 你的代码/依赖(COPY/RUN 叠加)
```

- 从 Docker Hub 拉取的 `python:3.13-slim` 是**通用基础镜像**（人人一样的"装了 Python 的干净 Linux"），**不是为你定制的**
- `docker build` 时，在它之上 `COPY` 代码、`RUN` 装依赖，才烧出**属于你的新镜像** `my-first-app`

**"拉取"（pull）= "下载"**：镜像存在云端仓库（Docker Hub），build/run 时下载到本地，这个下载动作就叫"拉取"。

**类比**：基础镜像是开发商统一盖的**毛坯房**（人人一样），你 build 是在毛坯上**装修**（放代码、装依赖），装修完的 `my-first-app` 才是你的**定制精装房**。

### 3.2.9 tag 死活与三层锁版本（为什么本地能跑、容器可能挂）

**隐患**：你本地 Python 3.13.12，但 `FROM python:3.13-slim` 拉下来是 3.13.15——版本不一样，本地能跑的代码打包后可能报错（跨大版本或依赖版本不一致时必挂）。

**根源**：`python:3.13-slim` 这个 tag 是**浮动的**（= "3.13 系列最新版"），会漂移；而你**拉下来的那份镜像**是**死的**（固定的）。所以"没报错"只是运气好（补丁版本兼容），正确做法是**锁死版本**：

| 层 | 做法 | 示例 |
|---|---|---|
| 基础镜像 | 精确到版本号 | `FROM python:3.13.12-slim` |
| 依赖包 | `pip freeze` 导出精确版本 | `langchain==0.2.14` |
| 极致（加分） | 用 digest 锁到具体构建 | `FROM python@sha256:9d2e...` |

> **一句话：Docker 给了你"可复现"的能力，但要不要复现、复现成什么样，取决于你锁不锁版本。** 这是"环境一致性"的正确姿势。

---

## 三、测试验收

### 验收 1：环境通（✅ 跑通）

```powershell
docker --version          # → Docker version 29.7.2
docker run hello-world    # → Hello from Docker!
```

### 验收 2：build 成功（✅ 跑通，截图确认）

```powershell
cd C:\Document\agent_project\docker_demo
docker build -t my-first-app .
```

看到 `=> naming to docker.io/library/my-first-app:latest` → **镜像造出来了**。

### 验收 3：run 输出证明"环境被 Docker 接管"（✅ 跑通）

```powershell
docker run my-first-app
```

输出：

```
我在容器里运行！
Python 版本：3.13.15
操作系统：  Linux 6.18.33.2-microsoft-standard-WSL2
```

**操作系统是 Linux 不是 Windows，Python 版本不是你电脑的 → 环境隔离验证通过。**

### 验收 4：改代码要重新 build（✅ 亲历）

第一次 run 报 `SyntaxError`（app.py 里中文引号撞了三引号），且报错路径是 `/app/app.py`。修复 app.py 后**必须重新 build**，再 run 才正常——因为**镜像是一次性"烧录"的**，改了源码不重新 build，容器里还是旧代码。

---

## 四、本节踩坑清单（Docker 实操坑大合集）

| # | 坑 | 表现 | 根治 |
|---|---|---|---|
| 1 | **Docker Desktop 没启动** | `failed to connect to docker API ... dockerDesktopLinuxEngine ... cannot find the file specified` | 先打开 Docker Desktop，等鲸鱼图标转绿（`docker version` 的 Server 段有版本号才算通） |
| 2 | **Docker Hub 直连超时**（国内墙） | `connectex: A connection attempt failed ... registry-1.docker.io:443` | 配代理或镜像加速器（见 3.2.6） |
| 3 | **Docker 不走系统代理** | Clash 明明开着还是拉不动 | WSL2 独立网络，得**单独给 Docker Desktop 配代理**（`127.0.0.1:7897`） |
| 4 | **DaoCloud 加速器白名单** | `这镜像不在白名单`（中文+emoji 报错） | 公共加速器对自定义镜像限流；本地自定义镜像 build 成功即可，run 用本地镜像不触发拉取 |
| 5 | **cd 错目录** | `open Dockerfile: no such file or directory` | build 的 `.` 指当前目录，先 `cd` 到有 Dockerfile 的目录 |
| 6 | **中文引号撞三引号** | `SyntaxError: unterminated string literal`（docstring 里 `"代码"` 和 `"""` 打架） | docstring 里别内嵌中文双引号，或用单引号/干脆去掉 |
| 7 | **改了代码不重新 build** | run 出来还是旧结果/旧报错 | 镜像一次性固化，改源码必须 `docker build` 重新烧录 |
| 8 | **镜像名拼错** | build 叫 `my-frist-app`、run 找 `my-first-app` | build 和 run 用**同一个名字**，一字不差 |

---

## 五、论文定位（答辩话术）

- **第 6 章 RAG 服务可 Docker 化部署**：把学习伴侣的 RAG 检索 / 记忆系统包成镜像，`docker run` 一键起服务——"我的系统可复现、可交付"，这是工程规范性的实证。
- **工程化亮点**：会用 Docker 把系统打包成镜像 = **简历硬通货**（大厂 Agent 应用岗都要求"能容器化部署"）。
- **面试话术**：能说出"我理解镜像=程序、容器=进程的类比，会写 Dockerfile 四行指令，懂层缓存机制，踩过国内拉镜像的代理/加速器坑"——这证明你不是只会写 demo，而是能**交付可运行系统**的人。

---

## 六、代码骨架速查

```dockerfile
# Dockerfile —— 打包说明书（四行指令）
FROM python:3.13-slim   # ① 地基：自带 Python 的干净 Linux
WORKDIR /app            # ② 容器内工作目录
COPY app.py .           # ③ 搬代码进去
CMD ["python","app.py"] # ④ 启动后干什么
```

```python
# app.py —— 被 Docker 打包运行的最小例子（证明"跑在容器 Linux 里"）
import sys, platform
print(f"Python 版本：{sys.version.split()[0]}")
print(f"操作系统：  {platform.system()} {platform.release()}")
```

```powershell
# 两条命令走完 Docker 全流程
docker build -t my-first-app .   # Dockerfile → 镜像
docker run my-first-app          # 镜像 → 容器（执行 CMD）
```

完整例子：`agent_project/docker_demo/app.py`、`agent_project/docker_demo/Dockerfile`。
