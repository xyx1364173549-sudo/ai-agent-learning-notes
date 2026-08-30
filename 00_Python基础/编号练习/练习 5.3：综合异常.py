import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

def robust_api_call(url: str) -> dict | None:
    """
    发送 GET 请求，处理所有可能的异常
    - Timeout: 打印 "[超时] 请求超时"
    - ConnectionError: 打印 "[网络] 无法连接"
    - HTTPError: 打印 f"[HTTP] 状态码: {e.response.status_code}"
    - ValueError: 打印 "[解析] 响应不是合法 JSON"
    - 成功: 返回解析后的 dict
    """
    # ↓ 这就是 3.3 的 safe_get！凭记忆写一遍，不许看笔记！
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Timeout as e:
        print("[超时] 请求超时")
    except ConnectionError as e:
        print("[网络] 无法连接")
    except HTTPError as e:
        print(f"[HTTP] 状态码: {e.response.status_code}")
    except ValueError as e:
        print("[解析] 响应不是合法 JSON")


# 测试代码（用我们昨天的故障服务器）
if __name__ == "__main__":
    print(robust_api_call("http://127.0.0.1:8001/ok"))
    print(robust_api_call("http://127.0.0.1:8001/notfound"))
