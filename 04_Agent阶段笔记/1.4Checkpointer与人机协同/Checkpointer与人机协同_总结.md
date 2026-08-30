# LangGraph Checkpointer 与人机协同（任务 1.4）学习总结

> **学习人：** 小轩轩
> **日期：** 2026-08-24
> **前置知识：** LangGraph 状态图 + 条件边（1.3）
> **状态：** ✅ 完成
> **案例：** `lg_checkpoint.py`（状态持久化）+ `lg_human.py`（人机协同）

---

## 一句话总结

**Checkpointer 让流水线"记住"状态（多轮对话不失忆）；人机协同（interrupt_before）让流水线在关键节点暂停，等人工确认后再继续。两者配合实现"断点续传"。**

---

## 知识点 1：Checkpointer —— 状态持久化（档案柜）

**说明**：默认每次 `invoke` 都是独立运行（跑完就失忆）。挂上 Checkpointer 后，每次运行的状态被存下来，下次用同一个会话 ID 能续上。

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()                        # 创建"档案柜"
app = graph.compile(checkpointer=memory)      # 编译时挂上
```

> 类比：Checkpointer=档案柜；MemorySaver 是内存版（重启就丢）。

---

## 知识点 2：thread_id —— 会话隔离（档案编号）

**说明**：`thread_id` 区分不同会话，同一个 thread_id 的连续 invoke 共享状态，不同 thread_id 互相独立。

```python
config = {"configurable": {"thread_id": "会话1"}}
```

> 格式是 LangGraph 规定的（字典套字典=给配置分类）：config=总容器，configurable=用户自定义配置类，thread_id=具体一项。

---

## 知识点 3：多轮 invoke 续状态 —— 记忆的活证据

**说明**：同一个 thread_id，每次 invoke 传空，但状态能续上（counter 递增）。

```python
r1 = app.invoke({}, config)   # counter=1
r2 = app.invoke({}, config)   # counter=2（记得上次的1）
r3 = app.invoke({}, config)   # counter=3（记得上次的2）
```

> 没有 Checkpointer 时，每次 invoke({}) 都从 0 开始，输出会是 1、1、1（失忆）。

---

## 知识点 4：interrupt_before —— 人机协同（质检关卡）

**说明**：在指定节点**之前**设"质检关卡"，流水线跑到关卡就暂停，把当前状态交给人工检查。

```python
app = graph.compile(checkpointer=memory, interrupt_before=["human_review"])
```

> 类比：质检关卡——流水线到关卡停，质检员检查，检查完按"继续"。

---

## 知识点 5：断点续传 —— 暂停后恢复

**说明**：第 1 次 invoke 跑到关卡就停（返回当前 state），第 2 次 invoke(None) 从暂停点继续。配合 Checkpointer（同一 thread_id）实现断点续传。

```python
result1 = app.invoke({"topic": "递归"}, config)
# 暂停：{'topic': '递归', 'lesson': '...'}   ← 没有 approved

result2 = app.invoke(None, config)
# 继续：{'topic': '递归', 'lesson': '...', 'approved': True}   ← 有 approved
```

> `None` 表示"没有新输入，继续执行"。关键：暂停时前面的节点已执行完（有 lesson），后面的还没执行（无 approved）。

---

## 知识点 6：MemorySaver vs SqliteSaver —— 对应论文分层记忆

**说明**：MemorySaver 存内存（重启丢），SqliteSaver 存数据库（持久保存）。对应论文第 4 章的工作记忆（短期）和情景记忆（长期 SQLite）。

```python
from langgraph.checkpoint.memory import MemorySaver   # 内存版（工作记忆）
from langgraph.checkpoint.sqlite import SqliteSaver   # 数据库版（情景记忆）
```

| | MemorySaver | SqliteSaver |
|---|---|---|
| 存哪 | 内存 | SQLite 文件 |
| 重启后 | 丢 | 还在 |
| 对应论文 | 工作记忆 | 情景记忆 |

---

## 自测清单

- [ ] Checkpointer 的类比是什么？（档案柜）
- [ ] thread_id 的作用？（区分会话，同一 id 共享记忆）
- [ ] 没有 Checkpointer 时，连续 invoke({}) 输出什么？（1、1、1 失忆）
- [ ] interrupt_before 的作用？（节点前设质检关卡）
- [ ] 第 2 次 invoke 为什么传 None？（继续上次没跑完的）
- [ ] MemorySaver 和 SqliteSaver 对应论文哪两层记忆？
