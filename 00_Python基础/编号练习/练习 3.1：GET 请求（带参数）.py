import requests




def search_duckduckgo(query: str) -> dict | None:
    """
    用 requests.get 搜索 DuckDuckGo API
    URL: https://api.duckduckgo.com/
    参数: q=query, format=json, no_html=1
    返回: 解析后的 JSON dict；失败返回 None
    """
    # ↓ 在这里写你的代码
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
    }
    try:
        response = requests.get(url, params=params,timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
        return None
if __name__ == "__main__":
    result = search_duckduckgo("python")
    print(result)
# 在练习3.1.py 的任意位置加一行：
print("__name__ 的值是:", __name__)
