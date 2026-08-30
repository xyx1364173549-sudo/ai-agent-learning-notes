"""LangGraph 实战：节点调用 LLM（学习助手流水线）"""

from typing import TypedDict


from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import  StrOutputParser
import os
from dotenv import load_dotenv



load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
llm = ChatOpenAI(
    api_key=API_KEY,
    model="deepseek-v4-flash",
    base_url="https://api.deepseek.com"
                 )

# 状态：三个字段（total=False 表示字段可选，topic 是输入，lesson/quiz 是节点逐步产出的）
class State(TypedDict,total=False):#total=False 你 invoke 时只传了 {"topic": "递归"}，此时 lesson 和 quiz 还是空的（要等节点逐步产出）。如果 total=True，类型检查器会报"State 缺字段"。
    topic:str
    lesson:str
    quiz:str

# 节点1：根据主题生成讲解
def generate_lesson(state:State)->State:
    chain = (
        ChatPromptTemplate.from_messages([("user", "用一句话讲解：{topic}")])
        | llm
        | StrOutputParser()
    )
    lesson = chain.invoke({"topic": state["topic"]})
    return {"lesson": lesson}
# 节点2：根据讲解出一道题
def make_quiz(state:State)->State:
    chain = (
        ChatPromptTemplate.from_messages([("user","根据这段讲解出一道选择题：\n{lesson}")])
        | llm
        | StrOutputParser()
    )
    quiz = chain.invoke({"lesson": state["lesson"]})
    return {"quiz": quiz}

# 建图：生成讲解->出题
graph = StateGraph(State)

graph.add_node("generate_lesson", generate_lesson)# 这两步感觉有点多余，可以这样理解吗，generate_lesson和make_quiz这两个节点像是两个可以干不同工作的两个技工，把这两个技工用graph.add_node调用后这两个才会开始工作
graph.add_node("make_quiz", make_quiz)

graph.add_edge(START,"generate_lesson")
graph.add_edge("generate_lesson","make_quiz")
graph.add_edge("make_quiz",END)

app = graph.compile()
result = app.invoke({"topic":"递归"})

print("讲解：", result["lesson"])
print("题目：", result["quiz"])
