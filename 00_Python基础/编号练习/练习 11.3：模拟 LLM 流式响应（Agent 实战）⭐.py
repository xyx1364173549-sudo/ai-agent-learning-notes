from pydoc import text


def stream_response(text: str, chunk_size: int = 3):
    """
    TODO: 将文本按 chunk_size 分块逐个 yield
    例: stream_response("hello world", 3)
        产出: "hel", "lo ", "wor", "ld"
    模拟 LLM 的流式输出——每次吐一小段
    """
    # ↓ 在这里写你的代码
    for i in range(0,len(text),chunk_size):
        yield text[i:i+chunk_size]




    # 提示: 用 range(0, len(text), chunk_size) 作为步长
    pass


# 测试代码
print("模拟 LLM 流式输出：")
for chunk in stream_response("你好，我是你的 AI 助手，很高兴为你服务！", 5):
    print(f"[{chunk}]", end=" ")
    # 每次只处理一小段，就像 ChatGPT 逐字输出
