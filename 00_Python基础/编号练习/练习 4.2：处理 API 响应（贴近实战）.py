import json

api_response = '''
{
    "id": "chatcmpl-123",
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "Hello! How can I help you?"},
            "finish_reason": "stop"
        }
    ],
    "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18}
}
'''

# TODO 1: 解析 api_response 字符串（json.loads）
# TODO 2: 提取 assistant 的回复内容（应该是 "Hello! How can I help you?"）
# TODO 3: 提取 total_tokens（应该是 18）
api = json.loads(api_response)
print(api)

a = api["choices"][0]["message"]["content"]
# 这里不是和你清楚，虽然跌跌撞撞写出来了
print(a)

b = api["usage"]["total_tokens"]
print(b)
