import requests
from requests.exceptions import Timeout,ConnectionError,HTTPError


def safe_get(url: str) -> dict | None:
    """
    安全的 GET 请求，处理所有可能的异常:
    - Timeout: 打印 "[超时]"
    - ConnectionError: 打印 "[网络]"
    - HTTPError (4xx/5xx): 打印 f"[HTTP] 状态码: {code}"
    - ValueError (JSON 解析失败): 打印 "[解析]"
    - 成功: 返回解析后的 dict
    """
    # ↓ 在这里写你的代码
    try:
        resp = requests.get(url,timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Timeout:
        print("[超时] 请求超时")
    except ConnectionError:
        print("[网络] 无法连接服务器")
    except HTTPError as e:
        print(f"[HTTP] 状态码: {e.response.status_code}")  # e.response 里能拿到响应对象
    except ValueError:
        print("[解析] 响应不是合法 JSON")
    return None

if __name__ == "__main__":
    for url in [
        "http://127.0.0.1:8001/ok",
        "http://127.0.0.1:8001/notfound",
        "http://127.0.0.1:8001/error500",
        "http://127.0.0.1:8001/html",
        "http://127.0.0.1:8001/slow",
    ]:
        print(f"\n--- 测试 {url} ---")
        result = safe_get(url)
        print("结果:", result)
