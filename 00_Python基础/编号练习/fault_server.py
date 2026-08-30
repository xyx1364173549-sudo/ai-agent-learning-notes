"""fault_server.py - 故障模拟服务器（用于测试异常处理）

提供 5 个测试路径:
  /ok         → 200 正常 JSON
  /notfound   → 404 错误
  /error500   → 500 错误
  /html       → 200 但返回 HTML（非 JSON，测试解析异常）
  /slow       → 故意延迟 12 秒（超过 timeout，测试超时）
"""

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class FaultHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/ok'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            body = json.dumps({'status': 'ok', 'data': [1, 2, 3]}, ensure_ascii=False)
            self.wfile.write(body.encode('utf-8'))

        elif self.path.startswith('/notfound'):
            self.send_response(404)
            self.end_headers()

        elif self.path.startswith('/error500'):
            self.send_response(500)
            self.end_headers()

        elif self.path.startswith('/html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = '<html><body>这是一个HTML页面，不是JSON</body></html>'
            self.wfile.write(html.encode('utf-8'))

        elif self.path.startswith('/slow'):
            time.sleep(12)  # 故意延迟，超过客户端 timeout
            self.send_response(200)
            self.end_headers()

        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{}')

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8001), FaultHandler)
    print('故障模拟服务器已启动: http://127.0.0.1:8001')
    print('可用路径: /ok, /notfound, /error500, /html, /slow')
    server.serve_forever()
