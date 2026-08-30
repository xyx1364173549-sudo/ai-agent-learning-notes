"""echo_server.py - 本地模拟服务器（替代 httpbin.org）

作用：接收 POST 请求，把收到的数据原样返回。
运行：python echo_server.py  （监听 8000 端口）
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class EchoHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. 读取请求体
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8")

        # 2. 打印服务器视角：收到了什么
        print("\n===== [服务器] 收到请求 =====")
        print(f"路径: {self.path}")
        print(f"Content-Type: {self.headers.get('Content-Type')}")
        print(f"请求体: {raw_body}")

        # 3. 构造响应：把请求体原样返回给客户端
        response = {
            "status": "ok",
            "message": "服务器已收到你的数据！",
            "echo": json.loads(raw_body),   # 原样返回收到的 JSON
        }
        body = json.dumps(response, ensure_ascii=False).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # 静默默认日志，避免刷屏


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), EchoHandler)
    print("本地模拟服务器已启动: http://127.0.0.1:8000/post")
    print("按 Ctrl+C 停止")
    server.serve_forever()
