"""LangChain 入门：用 ChatModel 替换手写 requests"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate# 新零件：填空模板
import os  # 这个包是干什么的，从别的文件里提取变量吗
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")


# TODO 1.1a：创建 ChatModel 实例
# 提示：ChatOpenAI 需要 3 个参数：model / api_key / base_url
#       base_url 指向 DeepSeek 的地址 https://api.deepseek.com
# 1. 模型
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=API_KEY,
    base_url="https://api.deepseek.com",
)
# 2. 填空模板：固定文字 + 挖好的空位 {变量}
template = ChatPromptTemplate.from_messages([ #from_messages 用元组定义角色
    ("system","你是一个{role},回答风格要{style}"),# 元组第一个元素 = 角色
    ("user","{question}"),# 元组第二个元素 = 内容（含占位符）
])
# 3. 填空：把变量填进空位，返回带角色的 messages 列表
prompt = template.format_messages(
    role = "编程老师",
    style = "严谨简洁，一句话说清，不要任何类比",
    question = "什么是递归？"
)


# TODO 1.1b：用 invoke 发一条消息，拿到回复文本
# 提示：llm.invoke("用一句话介绍你自己") 返回的不是字符串，而是一个 AIMessage 对象
#       要用 .content 属性取出里面的文本
reply = llm.invoke("用一句话介绍你自己")#invoke 返回的不是字符串，而是一个 AIMessage 对象
#print(reply)
print(reply.content)#我是DeepSeek，由深度求索公司创造的AI助手，随时乐意为你解答问题！

reply2 = llm.invoke(prompt)
print(reply2.content)
