"""mytools.py - 一个可被 import 的模块"""

import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError


def search_duckduckgo(query: str) -> dict | None:
    """用 requests.get 搜索 DuckDuckGo API"""
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Timeout:
        print("[超时] 请求超时了")
    except ConnectionError:
        print("[网络] 无法连接服务器")
    except HTTPError as e:
        print(f"[HTTP] 状态码: {e.response.status_code}")
    except ValueError:
        print("[解析] 响应不是合法 JSON")
    return None


def greet(name: str) -> str:
    """一个最简单的函数，用来测试 import"""
    return f"你好，{name}！"


# 如果直接运行本文件，才执行下面的测试代码
if __name__ == "__main__":
    print("===== 我(mytools.py)被直接运行了 =====")
    print("__name__ 的值是:", __name__)
    result = search_duckduckgo("python")
    print("搜索完成，结果条数:", len(result.get("RelatedTopics", [])))
