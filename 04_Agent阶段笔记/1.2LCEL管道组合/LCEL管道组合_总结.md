# LCEL 管道式组合（任务 1.2）学习总结

> **学习人：** 小轩轩
> **日期：** 2026-08-21
> **前置知识：** LangChain 三大核心抽象（ChatModel / PromptTemplate / Tool）
> **状态：** ✅ 完成
> **项目位置：** `C:\Document\agent_project\lc_lcel.py`

---

## 一、一句话总结

**LCEL 用 `|`（管道符）把组件串成一条链，一次 `invoke` 跑完整条链，替代"手动三步走"。**

---

## 二、核心概念

### 2.1 之前的三步走（手动流水线）

```python
prompt = template.format_messages(...)   # 第1步：填空
msg = llm.invoke(prompt)                 # 第2步：发给模型
answer = msg.content                     # 第3步：取文本
```

每次都要手动写这 3 步，中间变量手动传。

### 2.2 LCEL 的一步走（自动传送带）

```python
chain = template | llm | StrOutputParser()   # 组装一次（串成链）

answer = chain.invoke({"role": ..., "question": ...})   # 一次跑完
```

---

## 三、三个新零件

| 新东西 | 是什么 | 类比 |
|---|---|---|
| `\|` 管道符 | 把组件串成链，上一个输出自动接下一个输入 | 接水管 / 传送带 |
| `StrOutputParser()` | 把 AIMessage 自动转成纯字符串 | 自动帮你 `.content` |
| `chain` | 串好的链，本身也可 `invoke` | 装好的流水线 |

**关键：** `chain` 是一个**对象**，它记住了"template → llm → parser"的路线，可以像函数一样反复调用。

---

## 四、核心区别：手动流水线 vs 自动传送带

| | 普通写法 | LCEL |
|---|---|---|
| 本质 | 每次手动做 3 步 | 先把 3 步组装成链，以后 1 步跑完 |
| 中间变量 | 手动写 prompt、msg | 不需要（`\|` 自动递） |
| 复用 | 每次重写 3 步 | 组装一次，反复 invoke |

### 复用角度（最能说明问题）

同一个模板问 3 个问题：

```python
# 普通写法：9 行
prompt1 = template.format_messages(question="什么是递归？")
msg1 = llm.invoke(prompt1); a1 = msg1.content
prompt2 = template.format_messages(question="什么是闭包？")
msg2 = llm.invoke(prompt2); a2 = msg2.content
prompt3 = template.format_messages(question="什么是装饰器？")
msg3 = llm.invoke(prompt3); a3 = msg3.content

# LCEL：4 行
chain = template | llm | StrOutputParser()
a1 = chain.invoke({"question": "什么是递归？"})
a2 = chain.invoke({"question": "什么是闭包？"})
a3 = chain.invoke({"question": "什么是装饰器？"})
```

---

## 五、完整代码

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=API_KEY,
    base_url="https://api.deepseek.com",
)

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，回答风格要{style}"),
    ("user", "{question}"),
])

# LCEL：用 | 串成链
chain = template | llm | StrOutputParser()

reply = chain.invoke({
    "role": "编程老师",
    "style": "通俗易懂，多用类比",
    "question": "什么是递归？",
})
print(reply)   # 直接是字符串，不用 .content
```

---

## 六、难点澄清

### 6.1 `|` 到底做了什么？

`|` 是"自动传参"的语法糖：上一个零件的输出，自动变成下一个零件的输入，省掉你手动写中间变量。

### 6.2 StrOutputParser 省掉了什么？

省掉了 `reply.content` 这一步。链的最后接上它，`chain.invoke()` 直接返回字符串。

### 6.3 为什么 invoke 传字典？

因为链的第一个零件是 PromptTemplate，它需要字典来填空（`{"role": ..., "question": ...}`）。

### 6.4 LCEL 和普通写法的本质区别？

普通写法 = 手动流水线（每次自己递数据）；LCEL = 自动传送带（装好一次，自动流）。

### 6.5 LCEL 的三个价值

1. **复用**：链组装一次，反复调用
2. **可读**：`template | llm | parser` 一眼看出数据流向
3. **可组合**：链还能再拼接（`chain_a | chain_b`），是 LangGraph 的基础

---

## 七、自测清单

- [ ] `|` 做了什么？（把上一个输出接到下一个输入）
- [ ] `StrOutputParser()` 省掉了什么？（`.content`）
- [ ] 为什么 `chain.invoke` 传字典？（链第一个是 PromptTemplate）
- [ ] LCEL 和普通写法的本质区别？（手动流水线 vs 自动传送带）
- [ ] LCEL 的三个价值？（复用 / 可读 / 可组合）
