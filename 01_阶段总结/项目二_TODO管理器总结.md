# 📚 项目二总结：命令行 TODO 任务管理器

> **学习人：** 小轩轩
> **完成日期：** 2026年8月10日-8月12日
> **状态：** ✅ 6/6 模块全部完成，可运行、可持久化
> **项目位置：** `C:\Document\todo_project\todo_manager.py`
> **里程碑：** 至此 **14 天学习计划全部完成**（13 练习 + 2 项目）🎉

---

## 📋 项目一句话

**一个在终端里运行的任务清单工具**——像手机里的"待办事项"App，但用键盘命令操作，还能把任务保存到文件（重启不丢）。

**核心流程：** 用户输入命令 → main() 解析 → TaskManager 执行 → 展示结果 →（自动）保存文件

```
> add 学习Python       添加任务
> done 1              标记第1个完成
> pending             只看未完成
> delete 2            删除第2个
> save / load         保存 / 恢复
> quit                退出
```

---

## 🗺️ 项目架构（我给你的介绍，复习用）

### 两个类 + 一个主程序

```
Task 类           → 管"一条任务"（标题 + 完成状态）
TaskManager 类    → 管"一堆任务"（列表 + 增删改查 + 保存加载）
main() 函数       → 管"和用户对话"（接收命令 → 调 TaskManager）
```

### 打个比方

- `Task` = 一张便利贴（写着任务内容和是否完成）
- `TaskManager` = 你的办公桌（整理便利贴：贴新的、划掉、扔掉）
- `main()` = 你（对着办公桌发号施令）

### 会用到你学过的所有知识

| 知识点 | 用途 |
|--------|------|
| 练习 7 类基础 | Task/TaskManager 两个类 |
| 练习 9 魔术方法 | `__call__` 标记完成、容器协议 |
| 练习 12 装饰器 | `@log_action` 操作日志 |
| 练习 4 JSON | save/load 持久化 |
| 练习 8 推导式 | pending/completed 筛选、批量转换 |
| 练习 13 循环 | main() 的 while True 交互 |

---

## 🧩 6 个模块拆解

### 模块 1：Task 类（8/10）
**功能：** 单条任务：标题、完成状态、可调用标记、转字典
**知识点：** `__init__`、`__str__`/`__repr__`、`__call__`、`to_dict`/`from_dict`（`@classmethod`）
**产出：**
```python
t = Task("学习Python")
t()                  # __call__ → 标记完成
t.to_dict()          # {'title': '学习Python', 'done': True}
Task.from_dict({...})  # 字典 → Task 对象
```

### 模块 2：TaskManager 容器协议（8/10）
**功能：** 让 TaskManager 用起来"像列表"
**知识点：** `__len__`、`__getitem__`、`__iter__`、`__str__`（+ enumerate + join）
```python
manager = TaskManager()
len(manager)      # 数量
manager[0]        # 下标访问
for t in manager: # 遍历
print(manager)    # 带序号列表
```

### 模块 3：业务方法（8/10）
**功能：** 增删改查 + 边界检查
**知识点：** 推导式筛选、列表删除、边界检查
```python
add_task("标题")     # 添加
mark_done(1)         # 标记完成（越界返回 False）
delete_task(2)       # 删除（序号从 1 开始）
pending_tasks()      # 未完成（推导式）
completed_tasks()    # 已完成
```

### 模块 4：装饰器日志（8/11）
**功能：** 操作自动记日志
**知识点：** 装饰器、`@wraps`、`func.__name__`
```python
[日志] add_task -> 成功 (共3个任务)
[日志] mark_done -> 成功 (共3个任务)
```

### 模块 5：文件持久化（8/12）
**功能：** save/load——"永久记忆"
**知识点：** `json.dump/load`、推导式批量转换、**编码一致性**
```python
manager.save()   # 对象 → to_dict → json.dump → tasks.json
manager.load()   # tasks.json → json.load → from_dict → 对象
```

### 模块 6：命令行交互（8/12）
**功能：** 用户用命令操作整个程序
**知识点：** `while True`、`input`、`split`、`int()` + 异常处理
```python
cmd = input("\n> ").strip()
parts = cmd.split(" ", 1)   # "add 标题" → ["add", "标题"]
```

---

## 🚨 本项目踩坑清单（全部真实经历，重点复习！）

### 1. `to_dict` 属性遮蔽方法（隐蔽 bug！）
```python
# ❌ 错误：self.to_dict = {...} 把方法名覆盖成字典！
def to_dict(self) -> dict:
    self.to_dict = {"title": ..., "done": ...}   # 第二次调用就崩！
    return self.to_dict

# ✅ 正确：用局部变量或直接 return
def to_dict(self) -> dict:
    return {"title": self.title, "done": self.done}
```
**教训：方法名是"动作"，别用 `self.方法名 = 数据` 覆盖它！**

### 2. `data["done", False]` 语法错误
```python
# ❌ 下标里塞逗号：data["done", False]（用元组当 key！）
# ✅ 应该用 .get()：data.get("done", False)
```
**教训：`dict["key"]` 是下标，`dict.get("key", 默认)` 是方法——别混！**

### 3. 装饰器名字不一致 + 定义位置错误
```python
# ❌ 类里用 @log_action，却定义了个 task_decorator！→ NameError
# ❌ 装饰器定义在类"之后"——用的时候还没定义！
# ✅ 装饰器定义在文件顶部（import 后），名字统一
```
**教训：装饰器定义要放在使用它的类之前；名字必须一致。**

### 4. `delete_task` 忘了 `index-1`
```python
# ❌ del self._tasks[index]      → 删错对象！
# ✅ del self._tasks[index - 1]  → 序号(1开始)→下标(0开始) 减1
```
**教训：mark_done 写了 -1，delete 漏了——一致性 bug！**

### 5. load 的推导式结果丢了！
```python
# ❌ [Task.from_dict(item) for item in data]  → 创建了但没保存！
# ✅ self._tasks = [Task.from_dict(item) for item in data]  → 赋值！
```
**教训：推导式是"表达式"，结果要赋值才有意义（练习 8 的收集模式）！**

### 6. `input("/n")` 写错
```python
# ❌ input("/n")  → 提示符显示字面量 /n
# ✅ input("\n> ") → 换行 + > 提示符
```
**教训：`\n` 是换行符（反斜杠 n），`/n` 是斜杠+字母！**

### 7. done/delete 交互方式不一致
```python
# done 用 parts[1]（命令里的序号），delete 却二次 input → 下一条命令被误读成序号！
# ✅ 统一：都用 parts[1] + try-except
```
**教训：同类命令的交互方式必须一致！**

### 8. Windows 编码陷阱（UnicodeDecodeError）
```python
# ❌ save 写 utf-8，load 默认 gbk 读 → UnicodeDecodeError！
with open(filepath, "w", encoding="utf-8") as f:   # 写入 utf-8
with open(filepath, "r") as f:                      # ❌ 读取默认 gbk！

# ✅ 读写编码必须一致：
with open(filepath, "r", encoding="utf-8") as f:
```
**教训：Windows 上 open() 默认 gbk！读写文件永远显式写 `encoding="utf-8"`！**

### 9. "uf-8" 拼写错误
```python
# ❌ encoding="uf-8" → LookupError: unknown encoding
# ✅ encoding="utf-8"（u-t-f-8，中间的 t 别丢）
```

---

## 🧠 本项目最大的概念突破（三个"啊哈时刻"）

### 突破 1：方法跟着"对象"走（跨类调用）

**问题：Task 的 to_dict 为什么能在 TaskManager 里被调用？**

**答案：因为 `_tasks` 里装的是 Task 对象，`task.to_dict()` 是"Task 对象自己调用自己的方法"，不是 TaskManager 的方法！**

```python
[task.to_dict() for task in self._tasks]
#     ↑ task 是 Task 对象 → to_dict 是 Task 自带的技能
```

**类比：老板（TaskManager）指挥员工（Task），但"做报表"是员工自己的技能。**

### 突破 2：连接不是"注解"产生的，是"运行时"产生的

**问题：`self._tasks: list[Task] = []` 是连接吗？**

**答案：不是！`list[Task]` 只是给 IDE 看的门牌标签，Python 运行时完全忽略它。**

```python
# 注解：list[Task] = "门牌标签"（Python 不看）
# 真实连接：add_task 里 Task(title) + append（运行时放进列表）
```

**所以写不写 `list[Task]` 都不影响运行**——真正的连接发生在 `add_task` 把 Task 对象放进去的那一刻。

### 突破 3：`@classmethod` 和 `cls`（还原工厂）

**问题：from_dict 为什么必须用 @classmethod？**

**答案：因为它要"创建新对象"，创建对象需要"类本身"（cls）而不是"已有实例"（self）。**

```python
@classmethod
def from_dict(cls, data):       # cls = Task（类自己）
    return cls(title=..., ...)  # cls(...) = Task(...) = 新对象
# 调用：Task.from_dict({...})  ← 不需要先有对象！
```

**类比：`self` 是"实例自己"，`cls` 是"类自己"；`self.xxx` 访问属性，`cls(...)` 创建新对象。**

---

## 📖 新学会的语法速查

### enumerate —— "带着号码牌的遍历"
```python
for i, task in enumerate(self._tasks, 1):
    # i=1, task=第一个; i=2, task=第二个...
# enumerate(列表, 起始数字)  → 产生 (序号, 元素) 配对
```

### join —— "胶水拼字符串"
```python
"\n".join(lines)     # 胶水.join(列表) → "行1\n行2\n行3"
", ".join(["a","b"]) # "a, b"
# 注意：join 是"字符串的方法"（胶水在前），不是列表的方法！
```

### 列表推导式批量转换（贯穿全项目）
```python
[task.to_dict() for task in self._tasks]        # 批量：对象 → 字典
[Task.from_dict(item) for item in data]          # 批量：字典 → 对象
[t for t in self._tasks if not t.done]           # 批量：筛选未完成
```

---

## ✅ 项目验收清单（全部通过）

- [x] Task 对象创建、`__call__` 标记完成
- [x] to_dict / from_dict 双向转换
- [x] len() / 下标 / for 遍历（容器协议）
- [x] add / mark_done / delete（含边界检查返回 False）
- [x] pending / completed 筛选
- [x] 操作日志自动记录（装饰器）
- [x] save → tasks.json（中文正常、缩进 2）
- [x] 重启后 load 恢复任务（持久化！）
- [x] 命令行完整交互（增删改查 + 保存 + 退出）
- [x] 编码统一（utf-8 读写）

---

## 🤖 与 AI Agent 开发的联系

**TODO 管理器就是 Agent "记忆能力"的核心模型！**

| Agent 概念 | 本项目对应 |
|-----------|-----------|
| 任务/记忆单元 | `Task` 类 |
| 记忆管理 | `TaskManager`（增删改查）|
| 记忆持久化 | `save`/`load`（JSON 文件）|
| 操作日志 | `@log_action` 装饰器 |
| 交互接口 | main() 命令行循环 |

**Agent 需要记住用户让它做的事、管理任务状态——TODO 管理器就是这种能力的基础实现。** 你以后做的真正的 Agent（任务执行、记忆管理、工具调用）都是这个模式的扩展！

---

## 🏆 最终成果（14 天学习计划全部完成！）

```
P0 练习 1-7   ✅ 7/7     f-string / 字典列表 / 网络请求 / JSON / 异常 / 类型注解 / 面向对象
P1 练习 8-10  ✅ 3/3     推导式 / 魔术方法 / 上下文管理器
P2 练习 11-13 ✅ 3/3     生成器 / 装饰器 / 异步编程
项目一 天气工具 ✅ 6/6    真实 API 调用 + 类封装 + 持久化
项目二 TODO    ✅ 6/6    完整命令行程序 + 记忆持久化
──────────────────────────────────────
全部通关！你已经具备 AI Agent 开发的完整 Python 基础！
```

> **下一步建议：**
> 1. 对照 `C:\Document\` 下的笔记参考答案，检查两个项目
> 2. 把项目放上 GitHub，作为编程生涯的第一个作品
> 3. 开始真正的 Agent 开发之旅（接 LLM API）！
>
> 恭喜你，小轩轩！🎉🎉🎉
