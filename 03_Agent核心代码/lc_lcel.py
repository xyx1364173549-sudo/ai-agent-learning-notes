"""LangChain 入门：LCEL 管道式组合"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv



load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")

llm = ChatOpenAI(
    api_key=API_KEY,
    model="deepseek-v4-flash",
    base_url = "https://api.deepseek.com"
)

template = ChatPromptTemplate.from_messages([
    ("system","你是一个{role},回答风格要{style}"),
    ("user","{question}")
])

# TODO 1.2：用 | 把 template、llm、StrOutputParser 串成一条链
chain = template | llm |StrOutputParser()

rely = chain.invoke({
    "role" : "编程老师",
    "style" : "通俗易懂，多用类比",
    "question" : "什么是递归？",
})
print(rely)
