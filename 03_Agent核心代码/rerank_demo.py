"""2.4 检索 + 重排序：LLM 精排纠正向量召回"""

import chromadb



from llm_client import chat # 复用你的 DeepSeek 客户端


# 1. Chroma 粗召回（复用 2.3 的数据）

client = chromadb.Client()
collection = client.create_collection("study_materials")
collection.add(
    documents=[
        "二次方程的求根公式是 x = (-b ± √(b²-4ac)) / 2a",
        "Python 是一种解释型编程语言",
        "勾股定理：直角三角形两直角边平方和等于斜边平方",
    ],
    ids=["math1", "python1", "math2"],
)


# 2. 粗召回 top-2（英文模型召回不准，勾股定理会排前面）
query = "怎么解一元二次方程"
result = collection.query(
    query_texts=[query],
    n_results=2
)
candidates = result["documents"][0]

print("=== 粗召回结果（英文模型，可能不准）===")
for i, c in enumerate(candidates):     # enumerate = 带着号码牌的遍历
    print(f"  {i+1}. {c}")

# 3. LLM 精排：让 DeepSeek 判断哪个候选最相关
#    prompt 用 f-string 拼：f 前缀在引号前，变量用 {} 包
prompt = f"""用户问题：{query}
候选答案：
1.{candidates[0]}
2.{candidates[1]}
请判断哪个候选答案最能回答用户问题，只输出编号（1 或 2）。
"""
reply = chat([
    {"role": "system", "content": "你是检索排序助手，只输出最相关候选的编号。"},
    {"role": "user", "content": prompt},
])
print("\n=== LLM 精排结果 ===")
print("最相关候选编号：", reply)
