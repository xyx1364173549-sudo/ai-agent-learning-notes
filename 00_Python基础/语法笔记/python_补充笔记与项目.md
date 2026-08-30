# Python 补充笔记与巩固项目

> 配合 `python.md` 使用，覆盖学习目标中的知识缺口，并附两个综合项目。
> 标注 ⭐ 的为 AI Agent 开发高频知识点。

---

## 目录

1. [控制流（if / elif / else + 三元运算符）](#1-控制流)
2. [推导式（列表 / 字典 / 集合）⭐](#2-推导式)
3. [魔术方法补充（`__repr__`、`__call__`、`__len__`、`__getitem__`）⭐](#3-魔术方法补充)
4. [`venv` 虚拟环境 ⭐](#4-venv-虚拟环境)
5. [`requests` 网络请求 ⭐](#5-requests-网络请求)
6. [`json` 数据处理 ⭐](#6-json-数据处理)
7. [`typing` 模块完整指南 ⭐](#7-typing-模块完整指南)
8. [字符串格式化（f-string）⭐](#8-字符串格式化)
9. [常用内置函数（enumerate / zip / map / filter）](#9-常用内置函数)
10. [生成器与迭代器 ⭐](#10-生成器与迭代器)
11. [上下文管理器原理（`__enter__` / `__exit__`）⭐](#11-上下文管理器原理)
12. [异步编程基础（async / await）⭐](#12-异步编程基础)

---

## 1. 控制流

你的笔记里完全没有 `if/elif/else`，这是最基础的条件分支。

### 1.1 if / elif / else

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:        # elif = else if，可以有多个
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "D"

print(grade)  # B
```

**要点：**

- Python 用**缩进**表示代码块，4 个空格为标准。
- `elif` 和 `else` 可省略；条件后必须有冒号 `:`。
- 条件支持链式比较：`if 60 <= score < 90:` （其它语言做不到）。

### 1.2 三元运算符（条件表达式）

一行写完简单的 if-else，AI Agent 代码里常见：

```python
status = "在线" if is_online else "离线"

# 等价于
if is_online:
    status = "在线"
else:
    status = "离线"
```

### 1.3 match-case（Python 3.10+，模式匹配）

类似其它语言的 switch：

```python
command = "search"

match command:
    case "search":
        print("执行搜索")
    case "exit":
        print("退出")
    case _:                  # _ 是通配符，相当于 default
        print("未知命令")
```

---

## 2. 推导式

**Python 最具标志性的特性之一**，用一行代码生成容器。AI Agent 代码里到处都是。

### 2.1 列表推导式

```python
# 传统写法
squares = []
for i in range(10):
    squares.append(i ** 2)

# 推导式写法（一行）
squares = [i ** 2 for i in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件过滤
evens = [i for i in range(20) if i % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 带条件表达式（if-else 放前面）
labels = ["偶" if i % 2 == 0 else "奇" for i in range(5)]
# ['偶', '奇', '偶', '奇', '偶']
```

**语法模板：**

```
[表达式 for 变量 in 可迭代对象 if 条件]
```

### 2.2 字典推导式

```python
# 把列表转成 {值: 索引} 的查找表（AI 里极常用）
words = ["hello", "world", "ai"]
index_map = {word: idx for idx, word in enumerate(words)}
# {'hello': 0, 'world': 1, 'ai': 2}

# 翻转键值
original = {"a": 1, "b": 2}
flipped = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b'}
```

### 2.3 集合推导式

```python
# 提取句子中所有不重复的单词长度
sentence = "the quick brown fox jumps"
lengths = {len(w) for w in sentence.split()}
# {3, 5}   —— 3 和 5，自动去重
```

> **性能提示：** 推导式比等价的 for 循环 + append 快约 30%，因为是在 C 层执行的。

---

## 3. 魔术方法补充

你笔记里有 `__str__`、`__le__`、`__lt__`、`__eq__`，但目标明确要求 `__repr__` 和 `__call__`，这里补齐。

### 3.1 `__repr__` vs `__str__` ⭐

两者都控制对象的字符串表现，但**用途不同**：

| 方法         | 用途       | 触发场景                                | 目标读者    |
| ---------- | -------- | ----------------------------------- | ------- |
| `__str__`  | 用户友好的显示  | `print(obj)`、`str(obj)`             | 终端用户    |
| `__repr__` | 开发者友好的显示 | 直接在 REPL 输入变量名、`repr(obj)`、`!r` 格式化 | 开发者（调试） |

```python
class Agent:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def __str__(self):
        return f"{self.name} (v{self.version})"

    def __repr__(self):
        # 最佳实践：返回能重建对象的代码字符串
        return f"Agent(name={self.name!r}, version={self.version!r})"

a = Agent("助手", "1.0")
print(a)        # 助手 (v1.0)          —— 走 __str__
print(repr(a))  # Agent(name='助手', version='1.0')  —— 走 __repr__
a               # 在 REPL 里直接显示 __repr__ 的结果
```

**黄金法则：** 如果只实现一个，优先 `__repr__`。因为当 `__str__` 未定义时，Python 会退回使用 `__repr__`。

### 3.2 `__call__` ⭐

让对象变得"可调用"，像函数一样使用。AI Agent 里常用于把配置/状态封装成可调用对象。

```python
class PromptTemplate:
    def __init__(self, template: str):
        self.template = template

    def __call__(self, **kwargs) -> str:
        # 对象像函数一样被调用，填充模板
        return self.template.format(**kwargs)

greet = PromptTemplate("你好，{name}！我是{role}。")

# 直接像函数一样调用对象
result = greet(name="小明", role="助手")
print(result)  # 你好，小明！我是助手。
```

**为什么用 `__call__` 而不是普通方法？** 当一个对象需要"携带状态 + 被反复调用"时，`__call__` 比显式方法调用更自然，也能让对象作为回调传入其它函数。

### 3.3 `__len__` 与 `__getitem__`（强烈建议补上）

让自定义容器支持 `len()` 和下标访问：

```python
class TaskList:
    def __init__(self, tasks: list):
        self._tasks = tasks

    def __len__(self):                 # 支持 len(task_list)
        return len(self._tasks)

    def __getitem__(self, index):      # 支持 task_list[0]、task_list[1:3]
        return self._tasks[index]

    def __iter__(self):                # 支持 for task in task_list
        return iter(self._tasks)

tl = TaskList(["任务A", "任务B", "任务C"])
print(len(tl))      # 3
print(tl[0])        # 任务A
for t in tl:        # 能遍历
    print(t)
```

---

## 4. venv 虚拟环境

你笔记只提了 `pip install`，但**没有虚拟环境**，这是工程化的第一步。AI Agent 项目依赖多、版本冲突频繁，必须隔离。

### 4.1 为什么需要虚拟环境

- 不同项目可能需要**不同版本**的同一个包（项目 A 要 `requests==2.28`，项目 B 要 `2.31`）。
- 全局安装会污染系统 Python，难以清理。
- `venv` 为每个项目创建**独立的 Python 环境**，互不干扰。

### 4.2 标准操作流程（Windows）

```bash
# 1. 创建虚拟环境（在项目目录下执行）
python -m venv .venv

# 2. 激活虚拟环境（Windows Git Bash）
source .venv/Scripts/activate

# 2. 激活（Windows CMD / PowerShell）
.venv\Scripts\activate

# 3. 激活后，命令行前会出现 (.venv) 标记
#    此时的 pip install 只装到 .venv 里，不影响全局

# 4. 安装依赖
pip install requests openai

# 5. 导出当前环境的依赖清单（极其重要，用于他人复现）
pip freeze > requirements.txt

# 6. 退出虚拟环境
deactivate
```

### 4.3 复现他人项目

```bash
# 拿到别人的 requirements.txt 后
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt     # 一键安装所有依赖
```

### 4.4 `.gitignore` 必加

虚拟环境目录 `.venv` **不要**提交到 git，只提交 `requirements.txt`：

```
.venv/
__pycache__/
*.pyc
```

---

## 5. requests 网络请求

**AI Agent 调用 LLM API 的核心工具**。虽然很多框架封装了 HTTP，但理解底层是基本功。

### 5.1 安装

```bash
pip install requests
```

### 5.2 四大请求方法

```python
import requests

# GET —— 获取资源（最常用）
resp = requests.get("https://httpbin.org/get", params={"q": "python"})
print(resp.json())    # 直接解析为 dict / list

# POST —— 提交数据（调用 LLM API 用这个）
resp = requests.post(
    "https://httpbin.org/post",
    json={"message": "你好"},            # json= 会自动序列化并设置 Content-Type
    headers={"Authorization": "Bearer xxx"},
    timeout=10,                          # ⭐ 必须设超时，否则可能永久挂起
)

# PUT / DELETE —— 更新 / 删除（REST API 用）
resp = requests.delete("https://httpbin.org/delete")
```

### 5.3 响应对象的常用属性

```python
resp = requests.get("https://httpbin.org/get")

resp.status_code    # 200（HTTP 状态码）
resp.text           # 响应体文本（str）
resp.json()         # 响应体解析为 Python 对象（dict/list）——最常用
resp.headers        # 响应头（dict）
resp.ok             # True 当 status_code < 400
```

### 5.4 ⭐ 必须配合异常处理

网络请求会失败，**永远要包 try-except**：

```python
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

def safe_get(url: str) -> dict | None:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()      # 4xx/5xx 主动抛异常
        return resp.json()
    except Timeout:
        print("请求超时")
    except ConnectionError:
        print("网络连接失败")
    except HTTPError as e:
        print(f"HTTP 错误: {e}")
    except ValueError:
        print("响应不是合法 JSON")
    return None
```

---

## 6. json 数据处理

API 交互的标准格式。Python 内置 `json` 模块，无需安装。

### 6.1 核心两组函数

| 函数                  | 作用                   | 方向      |
| ------------------- | -------------------- | ------- |
| `json.dumps(obj)`   | Python 对象 → JSON 字符串 | 序列化     |
| `json.loads(str)`   | JSON 字符串 → Python 对象 | 反序列化    |
| `json.dump(obj, f)` | Python 对象 → 写入文件     | 序列化到文件  |
| `json.load(f)`      | 从文件读取 → Python 对象    | 从文件反序列化 |

> **记忆技巧：** `s` 结尾 = string（字符串），不带 `s` = file（文件）。

### 6.2 Python 与 JSON 类型对应

| Python           | JSON        |
| ---------------- | ----------- |
| `dict`           | object `{}` |
| `list` / `tuple` | array `[]`  |
| `str`            | string      |
| `int` / `float`  | number      |
| `True`/`False`   | true/false  |
| `None`           | null        |

### 6.3 示例

```python
import json

# 序列化
data = {"name": "助手", "tools": ["search", "calc"], "enabled": True}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
# ensure_ascii=False: 保留中文（默认会转成 \uXXXX）
# indent=2: 美化缩进，便于阅读
print(json_str)

# 反序列化
parsed = json.loads(json_str)
print(parsed["name"])   # 助手

# 写入文件（配合 with）
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 从文件读取
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 6.4 处理自定义对象（进阶）

`json` 默认不认识自定义类，需提供转换函数：

```python
class Agent:
    def __init__(self, name, version):
        self.name = name
        self.version = version

def agent_to_dict(obj):
    if isinstance(obj, Agent):
        return {"name": obj.name, "version": obj.version}
    raise TypeError(f"无法序列化 {type(obj)}")

a = Agent("助手", "1.0")
json.dumps(a, default=agent_to_dict, ensure_ascii=False)
# '{"name": "助手", "version": "1.0"}'
```

---

## 7. typing 模块完整指南

你笔记有基础类型注解和 `Union`，但 `typing` 模块还有更常用的工具。

### 7.1 常用类型一览

```python
from typing import (
    Optional,    # 可选：可能是 None
    List,        # 列表（Python 3.9+ 可直接用 list）
    Dict,        # 字典
    Tuple,       # 元组
    Set,         # 集合
    Any,         # 任意类型（尽量少用）
    Callable,    # 可调用对象（函数/类）
    Union,       # 联合类型
)
```

### 7.2 Optional —— AI 代码最常见

表示"这个值可能是 None"。AI Agent 里返回值经常是 `Optional`（找不到结果就返回 None）：

```python
from typing import Optional

def find_tool(name: str) -> Optional[dict]:
    # 返回 dict 或 None
    if name in tools:
        return tools[name]
    return None

# Optional[dict] 等价于 Union[dict, None]
# Python 3.10+ 可简写为 dict | None
```

### 7.3 容器类型（泛型注解）

```python
from typing import List, Dict, Tuple

def process(messages: List[str]) -> Dict[str, int]:
    # 参数是字符串列表，返回值是 字符串->整数 的字典
    return {msg: len(msg) for msg in messages}

def get_point() -> Tuple[float, float]:
    return (3.14, 2.71)
```

> **Python 3.9+ 可以直接用小写：** `list[str]`、`dict[str, int]`、`tuple[float, float]`，效果相同，`typing.List` 等是为兼容旧版本保留的。

### 7.4 Callable —— 标注函数/回调 ⭐

AI Agent 里到处是回调（工具函数、处理函数）：

```python
from typing import Callable

# Callable[[参数类型...], 返回值类型]
def run_tool(tool: Callable[[str], str], input: str) -> str:
    return tool(input)

# 实际应用：注册多个工具函数
tools: Dict[str, Callable[[str], str]] = {
    "search": lambda q: f"搜索: {q}",
    "calc":   lambda q: f"计算: {q}",
}
```

### 7.5 联合类型的新写法（Python 3.10+）

```python
# 旧写法
from typing import Union
def parse(x: Union[int, str, None]) -> str: ...

# 新写法（推荐，更简洁）
def parse(x: int | str | None) -> str: ...
```

### 7.6 类型注解的意义

类型注解**不强制运行时检查**，它的价值在于：

1. IDE（PyCharm / VS Code）的**智能提示和补全**。
2. 用 `mypy` 做**静态类型检查**，提前发现 bug。
3. **代码即文档**，队友一看就知道函数要什么、返回什么。

AI Agent 代码库几乎 100% 使用类型注解，这是基本功。

---

## 8. 字符串格式化

你的笔记完全没提，但实际写脚本必用。三种方式：

### 8.1 f-string（Python 3.6+，强烈推荐）⭐

```python
name = "助手"
version = 1.0
tools = ["search", "calc"]

# 变量直接放进 {} 里
msg = f"我是 {name}，版本 {version}，共 {len(tools)} 个工具"

# 支持表达式
print(f"2 的 10 次方 = {2 ** 10}")

# 格式化数字
pi = 3.14159265
print(f"π = {pi:.2f}")          # π = 3.14    （保留 2 位小数）
print(f"{1234567:,}")            # 1,234,567   （千分位）

# !r 用 repr 显示（调试时有用）
word = "hello"
print(f"{word}")     # hello
print(f"{word!r}")   # 'hello'   （带引号）
```

### 8.2 str.format()（旧式，了解即可）

```python
"我是 {}，版本 {}".format("助手", 1.0)
"我是 {name}，版本 {ver}".format(name="助手", ver=1.0)
```

### 8.3 % 格式化（最古老，不推荐）

```python
"我是 %s，版本 %.1f" % ("助手", 1.0)
```

> **结论：永远用 f-string。**

---

## 9. 常用内置函数

推导式的最佳搭档，写脚本时极高频。

### 9.1 enumerate —— 同时拿"索引+值" ⭐

```python
# 传统（错误示范，不要这样写）
for i in range(len(fruits)):
    print(i, fruits[i])

# 正确写法
for idx, fruit in enumerate(fruits):
    print(idx, fruit)

# 指定起始序号
for idx, fruit in enumerate(fruits, start=1):
    print(f"第 {idx} 个: {fruit}")
```

### 9.2 zip —— 并行遍历多个序列

```python
names = ["小明", "小红", "小刚"]
scores = [90, 85, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# 一行构建字典
score_map = dict(zip(names, scores))
# {'小明': 90, '小红': 85, '小刚': 78}
```

### 9.3 map —— 对每个元素套用函数

```python
nums = ["1", "2", "3"]
ints = list(map(int, nums))      # [1, 2, 3]

# 等价推导式（更推荐）
ints = [int(n) for n in nums]
```

### 9.4 filter —— 过滤

```python
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))   # [2, 4, 6]

# 等价推导式（更推荐）
evens = [x for x in nums if x % 2 == 0]
```

> **建议：** 优先用推导式，可读性更好；`map`/`filter` 在函数式风格代码中仍常见，需能看懂。

---

## 10. 生成器与迭代器

处理大数据流、AI 流式响应的基础。

### 10.1 生成器函数（yield）

`return` 返回一个值就结束；`yield` 返回一个值后**暂停**，下次调用继续：

```python
def count_up_to(n: int):
    i = 1
    while i <= n:
        yield i        # 产出值，暂停
        i += 1         # 下次从这里继续

# 生成器不会立即执行，而是"惰性"产出
counter = count_up_to(5)
print(next(counter))   # 1
print(next(counter))   # 2

# 通常用 for 循环消费
for num in count_up_to(3):
    print(num)         # 1, 2, 3
```

**核心价值：不一次性生成所有数据，省内存。**

```python
# 处理 100 万条数据，用列表会占大量内存
# 生成器一次只在内存里放一条
def read_large_file(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()
```

### 10.2 生成器表达式

推导式的"惰性版本"，把 `[]` 换成 `()`：

```python
# 列表推导式：立即生成全部
squares_list = [i ** 2 for i in range(1000000)]   # 占内存

# 生成器表达式：惰性生成
squares_gen = (i ** 2 for i in range(1000000))    # 几乎不占内存

# 配合 sum/max/min 使用，极其优雅
total = sum(i ** 2 for i in range(1000000))       # 不需要先建列表
```

### 10.3 为什么 AI Agent 要懂生成器

LLM 的**流式响应**（streaming）本质就是生成器——API 一边吐 token，你一边接收处理，而不是等整段回复生成完。这是实时打字效果的技术基础。

---

## 11. 上下文管理器原理

你笔记会用 `with open(...)`，但**没讲为什么能自动关闭**。原理是 `__enter__` 和 `__exit__` 两个魔术方法。

### 11.1 with 的工作机制

```python
with open("data.txt") as f:
    data = f.read()

# 等价于
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()
```

`with` 语句保证了**无论是否异常，资源都会被释放**。

### 11.2 自定义上下文管理器

```python
class Timer:
    """计时器：with 代码块结束时打印耗时"""
    def __enter__(self):
        import time
        self.start = time.time()
        return self          # 返回值会赋给 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.time() - self.start
        print(f"耗时 {self.elapsed:.3f} 秒")
        # 返回 False（默认）表示不吞掉异常
        # 返回 True 表示吞掉 with 块内的异常（慎用）
        return False

# 使用
with Timer() as t:
    total = sum(range(1000000))
# 输出: 耗时 0.045 秒
```

### 11.3 contextlib 简化写法（推荐）

不用写类，用装饰器：

```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    yield                  # yield 之前 = __enter__，之后 = __exit__
    print(f"耗时 {time.time() - start:.3f} 秒")

with timer():
    sum(range(1000000))
```

---

## 12. 异步编程基础

你笔记里只有"异步编程"四个字标题，这里补全。这是 AI Agent **并发调用多个 API** 的关键。

### 12.1 为什么要异步

同步：一次只做一件事，等 API 响应时 CPU 干等。
异步：等 API 响应时，CPU 去干别的（发下一个请求）。

**场景：** 要调用 10 个工具查询，同步要 10 秒，异步可能 1 秒搞定。

### 12.2 async / await 基础

```python
import asyncio

async def greet(name: str) -> str:
    print(f"开始招呼 {name}")
    await asyncio.sleep(1)        # 模拟耗时 IO（不阻塞！）
    print(f"完成招呼 {name}")
    return f"你好，{name}"

# async def 定义协程函数
# await 等待另一个协程完成（期间可让出 CPU）

async def main():
    # 串行：约 2 秒
    r1 = await greet("A")
    r2 = await greet("B")

    # 并发：约 1 秒（同时跑两个）
    results = await asyncio.gather(greet("A"), greet("B"))
    print(results)

# 运行事件循环
asyncio.run(main())
```

### 12.3 异步 HTTP 请求（aiohttp）

`requests` 是同步库，异步场景要用 `aiohttp`：

```python
import asyncio
import aiohttp

async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as resp:        # async with！
        return await resp.json()

async def main():
    urls = ["https://httpbin.org/get"] * 5
    async with aiohttp.ClientSession() as session:
        # 并发请求 5 个 URL
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls]
        )
        print(f"完成 {len(results)} 个请求")

asyncio.run(main())
```

### 12.4 何时用同步，何时用异步

| 场景              | 推荐                     |
| --------------- | ---------------------- |
| 单次 API 调用、简单脚本  | `requests`（同步）         |
| 并发调用多个 API、流式响应 | `aiohttp`（异步）          |
| CPU 密集计算        | 多进程（`multiprocessing`） |

> **入门建议：** 先掌握同步 `requests`，理解整个流程后再学异步。多数 Agent 框架（LangChain 等）已封装好异步，你只需理解原理。

---

# 巩固项目

下面两个项目**刻意覆盖了所有缺口知识点**。建议先自己动手写，再看答案。

---

## 项目一：智能天气查询工具

**覆盖知识点：** `venv`、`requests`、`json`、类型注解、异常处理、`with`、面向对象、f-string、`typing`

### 需求

1. 创建虚拟环境，安装 `requests`，生成 `requirements.txt`。
2. 实现一个 `WeatherClient` 类，封装对免费天气 API（`wttr.in`，无需密钥）的调用。
3. 提供 `get_weather(city)` 方法，返回类型注解完整的天气信息。
4. 对网络异常、JSON 解析异常做健壮处理。
5. 用 `__str__` 和 `__repr__` 让对象可读。
6. 支持把查询结果保存为 JSON 文件（用 `with` + `json.dump`）。

### 参考答案

```python
# weather_tool.py
"""智能天气查询工具 —— 巩固练习项目一"""
import json
import requests
from typing import Optional
from requests.exceptions import Timeout, ConnectionError, HTTPError


class WeatherClient:
    """封装 wttr.in 天气 API 的客户端。"""

    def __init__(self, base_url: str = "https://wttr.in") -> None:
        self.base_url = base_url.rstrip("/")

    def __str__(self) -> str:
        return f"WeatherClient(base_url={self.base_url})"

    def __repr__(self) -> str:
        return f"WeatherClient(base_url={self.base_url!r})"

    def get_weather(self, city: str) -> Optional[dict]:
        """
        查询城市天气。
        :param city: 城市名（中文或英文）
        :return: 天气数据字典；失败返回 None
        """
        url = f"{self.base_url}/{city}"
        params = {"format": "j1"}    # j1 = JSON 格式

        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data
        except Timeout:
            print(f"[错误] 请求 {city} 超时")
        except ConnectionError:
            print(f"[错误] 网络连接失败，请检查网络")
        except HTTPError as e:
            print(f"[错误] HTTP 状态异常: {e}")
        except ValueError:
            print(f"[错误] 响应不是合法 JSON")
        return None

    def save_to_file(self, data: dict, filepath: str) -> bool:
        """把天气数据保存为 JSON 文件。"""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[成功] 已保存到 {filepath}")
            return True
        except OSError as e:
            print(f"[错误] 文件写入失败: {e}")
            return False


def format_weather(data: dict) -> str:
    """从原始 JSON 中提取关键信息，格式化为可读字符串。"""
    # wttr.in 的 j1 格式结构：current_condition 是个列表
    current = data.get("current_condition", [{}])[0]
    area = data.get("nearest_area", [{}])[0]

    city = area.get("areaName", [{}])[0].get("value", "未知")
    temp = current.get("temp_C", "?")
    desc = current.get("weatherDesc", [{}])[0].get("value", "未知")
    humidity = current.get("humidity", "?")

    return (
        f"城市: {city}\n"
        f"温度: {temp}°C\n"
        f"天气: {desc}\n"
        f"湿度: {humidity}%"
    )


def main() -> None:
    client = WeatherClient()
    print(client)                # 走 __str__
    print(repr(client))          # 走 __repr__

    city = input("请输入城市名（如 Beijing / 北京）: ").strip()
    if not city:
        print("城市名不能为空")
        return

    data = client.get_weather(city)
    if data is None:
        print("查询失败，请稍后重试")
        return

    print("\n=== 天气信息 ===")
    print(format_weather(data))

    # 保存到文件
    save_path = f"weather_{city}.json"
    client.save_to_file(data, save_path)


if __name__ == "__main__":
    main()
```

### 运行步骤

```bash
# 1. 创建并激活虚拟环境
python -m venv .venv
source .venv/Scripts/activate          # Git Bash
# .venv\Scripts\activate               # CMD / PowerShell

# 2. 安装依赖
pip install requests

# 3. 导出依赖清单
pip freeze > requirements.txt

# 4. 运行
python weather_tool.py
```

### 练习扩展（自行挑战）

- [ ] 增加 `get_forecast(city, days)` 方法，获取未来 N 天预报。
- [ ] 用 `asyncio` + `aiohttp` 改造为异步版本，同时查询多个城市。
- [ ] 把 `WeatherClient` 改造成可调用对象（实现 `__call__`）。

---

## 项目二：命令行 TODO 任务管理器

**覆盖知识点：** 面向对象全套（`__init__`、`__str__`、`__repr__`、`__call__`、`__len__`、`__getitem__`、`__iter__`）、装饰器、闭包、推导式、`json` 文件持久化、`with`、控制流、`typing`、`enumerate`、`f-string`

### 需求

1. `Task` 类：包含标题、完成状态；实现 `__str__`、`__repr__`、`__call__`（调用即标记完成）。
2. `TaskManager` 类：管理任务列表；实现 `__len__`、`__getitem__`、`__iter__`；支持增删改查。
3. 用**装饰器**实现操作日志（每次增删自动打印日志）。
4. 用 `with` + `json` 实现任务持久化（保存/加载）。
5. 命令行交互：`add` / `done` / `list` / `delete` / `save` / `load` / `quit`。
6. 全程类型注解。

### 参考答案

```python
# todo_manager.py
"""命令行 TODO 任务管理器 —— 巩固练习项目二"""
import json
from datetime import datetime
from typing import Optional, Callable
from functools import wraps


# ---------- 装饰器：操作日志 ----------
def log_action(func: Callable) -> Callable:
    """装饰器：在方法调用前后打印日志。"""
    @wraps(func)                          # 保留原函数的元信息
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] {datetime.now():%H:%M:%S} 执行 {func.__name__}")
        result = func(self, *args, **kwargs)
        print(f"[LOG] {func.__name__} 完成")
        return result
    return wrapper


# ---------- Task 类 ----------
class Task:
    """单个任务。"""

    def __init__(self, title: str, done: bool = False) -> None:
        self.title = title
        self.done = done

    def __call__(self) -> "Task":
        """让 Task 对象可调用：调用即标记为完成。"""
        self.done = True
        return self                       # 返回自身，支持链式调用

    def __str__(self) -> str:
        status = "✓" if self.done else "○"
        return f"[{status}] {self.title}"

    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, done={self.done})"

    def to_dict(self) -> dict:
        return {"title": self.title, "done": self.done}

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(title=data["title"], done=data.get("done", False))


# ---------- TaskManager 类 ----------
class TaskManager:
    """任务管理器，支持增删改查与持久化。"""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    # --- 容器协议：让 manager 支持 len()、下标、遍历 ---
    def __len__(self) -> int:
        return len(self._tasks)

    def __getitem__(self, index: int) -> Task:
        return self._tasks[index]

    def __iter__(self):
        return iter(self._tasks)

    def __str__(self) -> str:
        if not self._tasks:
            return "（空，暂无任务）"
        lines = [f"  {i}. {task}" for i, task in enumerate(self._tasks, 1)]
        return "\n".join(lines)

    # --- 业务方法（带装饰器日志）---
    @log_action
    def add(self, title: str) -> Task:
        task = Task(title)
        self._tasks.append(task)
        return task

    @log_action
    def done(self, index: int) -> Optional[Task]:
        """标记第 index 个任务为完成（index 从 0 开始）。"""
        if 0 <= index < len(self._tasks):
            return self._tasks[index]()    # 调用 Task 的 __call__
        print(f"[错误] 索引 {index} 超出范围")
        return None

    @log_action
    def delete(self, index: int) -> bool:
        if 0 <= index < len(self._tasks):
            removed = self._tasks.pop(index)
            print(f"已删除: {removed}")
            return True
        print(f"[错误] 索引 {index} 超出范围")
        return False

    def pending(self) -> list[Task]:
        """返回所有未完成任务（用推导式）。"""
        return [t for t in self._tasks if not t.done]

    def completed(self) -> list[Task]:
        """返回所有已完成任务（用推导式）。"""
        return [t for t in self._tasks if t.done]

    # --- 持久化 ---
    def save(self, filepath: str) -> bool:
        """保存到 JSON 文件。"""
        data = {"tasks": [t.to_dict() for t in self._tasks]}
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[成功] 已保存 {len(self._tasks)} 个任务到 {filepath}")
            return True
        except OSError as e:
            print(f"[错误] 保存失败: {e}")
            return False

    def load(self, filepath: str) -> bool:
        """从 JSON 文件加载。"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
            print(f"[成功] 已加载 {len(self._tasks)} 个任务")
            return True
        except FileNotFoundError:
            print(f"[提示] 文件 {filepath} 不存在，将创建新任务列表")
            return False
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[错误] 文件格式异常: {e}")
            return False


# ---------- 命令行交互 ----------
def show_help() -> None:
    print("""
可用命令:
  add <标题>        添加任务
  done <序号>       标记完成（序号从 1 开始）
  delete <序号>     删除任务
  list              列出所有任务
  pending           只看未完成
  save [文件名]     保存（默认 tasks.json）
  load [文件名]     加载（默认 tasks.json）
  help              显示帮助
  quit              退出
""")


def main() -> None:
    manager = TaskManager()
    print("=== TODO 任务管理器 ===")
    show_help()

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "quit":
            print("再见！")
            break
        elif cmd == "help":
            show_help()
        elif cmd == "add":
            if not arg:
                print("用法: add <标题>")
                continue
            manager.add(arg)
        elif cmd == "done":
            idx = int(arg) - 1            # 用户输入 1-based
            manager.done(idx)
        elif cmd == "delete":
            idx = int(arg) - 1
            manager.delete(idx)
        elif cmd == "list":
            print(f"共 {len(manager)} 个任务：")
            print(manager)
        elif cmd == "pending":
            tasks = manager.pending()
            print(f"未完成 {len(tasks)} 个：")
            for i, t in enumerate(tasks, 1):
                print(f"  {i}. {t}")
        elif cmd == "save":
            filepath = arg if arg else "tasks.json"
            manager.save(filepath)
        elif cmd == "load":
            filepath = arg if arg else "tasks.json"
            manager.load(filepath)
        else:
            print(f"未知命令: {cmd}，输入 help 查看帮助")


if __name__ == "__main__":
    main()
```

### 运行

```bash
python todo_manager.py
```

### 这个项目刻意覆盖的知识点对照

| 知识点                                    | 在代码中的体现                                      |
| -------------------------------------- | -------------------------------------------- |
| 控制流                                    | `main()` 里的 if/elif 链                        |
| 推导式                                    | `pending()`、`completed()`、`save()` 里的列表推导式   |
| `__call__`                             | `Task.__call__`，调用任务即标记完成                    |
| `__str__` / `__repr__`                 | `Task` 和 `TaskManager` 都实现了                  |
| `__len__` / `__getitem__` / `__iter__` | `TaskManager` 支持容器操作                         |
| 装饰器                                    | `@log_action` 给增删方法加日志                       |
| 闭包                                     | 装饰器内部 `wrapper` 就是闭包                         |
| `with` + `json`                        | `save()` / `load()`                          |
| 类型注解                                   | 全程 `-> None`、`Optional[Task]`、`list[Task]` 等 |
| `enumerate`                            | `__str__` 和 `pending` 列表                     |
| f-string                               | 遍布全代码                                        |
| 异常处理                                   | `load()` 的多重 except、`main()` 的键盘中断           |

### 练习扩展（自行挑战）

- [ ] 增加任务优先级（high/medium/low），用 `__lt__` 实现按优先级排序。
- [ ] 用生成器实现 `iter_pending()`，惰性产出未完成任务。
- [ ] 把 `log_action` 改造为支持把日志写入文件（用 `with open` 追加模式）。

---

## 学习路线建议

完成以上两个项目后，你已具备写 Python 脚本、调用 API、做面向对象设计的能力。下一步建议：

1. **强化异步**：用 `aiohttp` 重写项目一为异步并发版本。
2. **接触 Agent 框架**：尝试用 `openai` SDK 调用 LLM（本质就是 `requests` + `json` + 类型注解）。
3. **学习设计模式**：工厂模式、策略模式在 Agent 工具注册中极常用。
4. **代码规范**：安装 `ruff` 或 `black` 做代码格式化，`mypy` 做类型检查。


