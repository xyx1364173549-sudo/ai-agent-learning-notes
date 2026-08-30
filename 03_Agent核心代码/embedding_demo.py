"""2.1 Embedding 原理：文本如何变向量 + 相似度如何算（手算版）"""
import math



sentences = [
    ["我", "喜欢", "吃", "苹果"],
    ["我", "喜欢", "吃", "香蕉"],
    ["今天", "天气", "很好"]
]
# ① 构建词表：所有词去重后的列表
# TODO 1：把 sentences 里所有词去重，得到 vocab
# 提示：两层遍历收集所有词，用 set() 去重，再 list() 转回
vocab = []
for sentence in sentences:
    for word in sentence:
        if word not in vocab:
            vocab.append(word)




# ② 句子 → 词频向量（长度 = 词表长度，每个位置 = 该词出现次数）
def sentence_to_vector(sentence, vocab):
    # TODO 2：返回 [词1次数, 词2次数, ...]
    # 提示：先建一个全 0 列表，再遍历 sentence 里的词，在对应位置 +1
    vector = [0]*len(vocab) # 先造一个全是0的向量，长度=词表长度
    for word in sentence:   #在遍历这句话的每一个词
        index = vocab.index(word) #获取每个词在在表里的位置，投射在vector里
        vector[index] += 1  #投影后，位置计数+1
    return vector


def cosine_similarity(vec1, vec2):
    # ① 点积：对应位置相乘，再加起来
    dot = sum(a * b for a,b in zip(vec1, vec2))# zip是干什么的帮我回忆复习一下

    # ② 模长：每个数平方求和，再开根号
    norm1 = math.sqrt(sum(x * x for x in vec1))#v1：2
    norm2 = math.sqrt(sum(x * x for x in vec2))#v2：2
    # ③ 余弦 = 点积 / (模长乘积)
    return dot / (norm1 * norm2)

v1 = sentence_to_vector(sentences[0], vocab)# 苹果句
v2 = sentence_to_vector(sentences[1], vocab)# 香蕉句
v3 = sentence_to_vector(sentences[2], vocab)# 天气句

print("词表：", vocab)
print("苹果句向量：", v1)
print("香蕉句向量：", v2)
print("苹果 vs 香蕉：", cosine_similarity(v1, v2))   # 期望约 0.75
print("苹果 vs 天气：", cosine_similarity(v1, v3))   # 期望 0.0
