"""Agent 的 Web 服务"""
from fastapi import FastAPI
from pydantic import BaseModel   # 用来定义"请求体"的格式
from fastapi.responses import HTMLResponse
# 引入Agent核心能力
from mini_agent import chat_with_tools,execute_tool,SYSTEM_PROMPT,tools
import json

app = FastAPI()  # FastAPI() 是"创建一个 Web 应用对象"。这个 app 就是你整个服务的"主体"——你后面写的所有接口（@app.get、@app.post），都是挂在这个 app 上的。

class ChatRequest(BaseModel):
    message:str # 用户发来的消息;
    # 声明：订单表里必须有一个叫 message 的字段，类型是字符串

# TODO 1: 写 run_agent(user_input) 函数（把上面的核心逻辑搬进来）
#         输入一句话，返回 AI 的最终回答

def run_agent(user_input:str)->str:
    messages = [{"role":"system","content":SYSTEM_PROMPT}]
    # 系统一开始的提示词
    messages.append({"role":"user","content":user_input})
    # 输入用户的提示词
    msg = chat_with_tools(messages)
    # 这里开始调用AI，把上面的提示词打包给AI的同时，告诉它可以调用的函数工具
    messages.append(msg)
    # 再把AI返回的结果装进message

    tool_calls = msg.get("tool_calls")
    # 提取要使用的工具信息
    if tool_calls:
        for tool_call in tool_calls:
            name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])
            arg = args.get("city") or args.get("expression")
            result = execute_tool(name, arg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": result,
            })
        final_msg = chat_with_tools(messages)
        messages.append(final_msg)
    return messages[-1]["content"]
# 返回最终的回答
@app.post("/chat") #@app.get("/") → 访问 http://127.0.0.1:8000/（根路径，就是首页）
                   #@app.post("/chat") → 访问 http://127.0.0.1:8000/chat（聊天窗口）
def chat_api(req: ChatRequest):
    # TODO 2: 调用 run_agent(req.message)，把结果包成 JSON 返回
    reply = run_agent(req.message)
    # 调用run_agent(req.message)；req.message是什么东西，是
    return {"reply":reply}
@app.get("/")
def home():
    with open("index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())
