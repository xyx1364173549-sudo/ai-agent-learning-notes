"""2.2 文档切分策略：固定长度 + 重叠窗口"""

# 模拟一份讲义（长文档）
text = ("大语言模型是基于Transformer架构的深度学习模型。"
        "Transformer的核心是自注意力机制，它允许模型并行地捕捉序列中"
        "任意两个位置之间的依赖关系。与传统的循环神经网络相比，"
        "Transformer能够更好地处理长距离依赖，因此成为现代大语言模型的"
        "基础架构。在此基础上，GPT等生成式模型通过海量语料的预训练，"
        "学会了预测下一个词，展现出强大的语言理解和生成能力。")

# TODO：写 chunk_text(text, chunk_size, overlap)
#   按 chunk_size 切分，相邻块重叠 overlap 个字符
#   提示：
#     1. 用 while 循环，start 从 0 开始
#     2. 每次取 text[start : start+chunk_size] 作为一个 chunk
#     3. start 每次前进 (chunk_size - overlap)   ← 关键：步长
#     4. 当 start >= len(text) 时停止
def chunk_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+chunk_size])
        start += (chunk_size - overlap)
        #start = start + chunk_size - overlap

    # 你的代码写这里
    return chunks

# 调用：每块 50 字，重叠 10 字
chunks = chunk_text(text, chunk_size=50, overlap=10)

print(f"共切出 {len(chunks)} 块：")
for i, c in enumerate(chunks):
    print(f"\n[块{i}] (长度{len(c)}): {c}")
