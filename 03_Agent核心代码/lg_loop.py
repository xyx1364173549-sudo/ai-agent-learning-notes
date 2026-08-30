"""LangGraph 条件边：答错重学循环"""

from typing import TypedDict
from langgraph.graph import StateGraph,START,END
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
    base_url="https://api.deepseek.com"
)

class State(TypedDict,total=False):
    topic : str
    lesson : str
    answer : str# 学生答案（你输入）
    correct : bool# 是否答对（判题节点产出）
    retry_count:int


def generate_lesson(state:State)->State:
    chain = (
        ChatPromptTemplate.from_messages[("user","用一句话讲解：{topic}")]
        | llm
        | StrOutputParser()
    )
    lesson = chain.invoke({"topic":state["topic"]})
    return {"lesson":lesson}


# 节点2：判题（简化：answer 是"懂了"就算对，真实项目用 LLM 判断）
def judge(state:State)->State:
    correct = (state.get("answer") == "懂了")
    retry_count = state.get("retry_count",0)+1#.get(key, 默认值
    return {"correct":correct,"retry_count":retry_count}

def route(state:State)->str:
    if state.get("correct"):
        return "pass"# 答对
    if state.get("retry_count",0) >=3:   # ③ 重试3次还错 → 放
        return "give_up"
    return "retry" #答错

graph = StateGraph(State)
graph.add_node("generate_lesson",generate_lesson)
graph.add_node("judge",judge)
graph.add_edge(START,"generate_lesson")
graph.add_edge("generate_lesson","judge")


# 条件边：从 judge 分叉
graph.add_conditional_edges(
    "judge",    # ① 从判题节点出发
    route,   # ② 路由函数
    {"pass":END,
     "retry":"generate_lesson",
     "give_up":END,
     } , # ③ 映射表：答对→结束，答错→重学
)
app = graph.compile()
result = app.invoke({"topic": "递归", "answer": "不懂"})
print(result)
