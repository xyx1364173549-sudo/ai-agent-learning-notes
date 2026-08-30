"""2.3 Chroma 向量数据库：建索引 + 语义检索"""
import chromadb


# 1. 创建客户端（内存版，程序结束就丢；演示够用）
client = chromadb.Client()

# 2. 创建集合（一个 collection = 一个"知识库"）
collection = client.create_collection("study_materials")

# 3. 添加文档（add 时 Chroma 会自动把文本变成向量存进去）
collection.add(
    documents=[
            "二次方程的求根公式是 x = (-b ± √(b²-4ac)) / 2a",
            "Python 是一种解释型编程语言",
            "勾股定理：直角三角形两直角边平方和等于斜边平方",
        ],
        ids=["math1", "python1", "math2"],
    #ids[0] 是 documents[0] 的编号，ids[1] 是 documents[1] 的编号……靠位置对上，不是靠 key 找 value
)

# 4. 检索：问一个"字面不同、但语义相近"的问题
result = collection.query(
    query_texts=["怎么解一元二次方程"],## 注意：这里没有"求根公式"三个字
    n_results=2,
)
print(result)
