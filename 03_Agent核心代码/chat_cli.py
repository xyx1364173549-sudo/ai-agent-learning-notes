

from llm_client import chat


def main():
    messages = [{"role":"system","content":"你是一个乐于助人的助手，回答要简洁"}]
    print("=== 命令行 DeepSeek（输入 quit 退出）===")

    while True:
        user_input = input("\n你:").strip()
        if user_input.lower() == "quit":
            break
        messages.append({"role":"user","content":user_input})
        reply = chat(messages)
        messages.append({"role":"assistant","content":reply})
        print(f"AI: {reply}")
if __name__ == "__main__":
    main()
# 你:你好
# AI: 你好！有什么可以帮你的吗？
