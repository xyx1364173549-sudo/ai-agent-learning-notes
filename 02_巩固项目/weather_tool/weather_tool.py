import requests
from requests.exceptions import Timeout, ConnectionError,HTTPError
import json


class WeatherClient:
    def __init__(self, base_url: str = "https://wttr.in"):
        self.base_url = base_url.rstrip("/")
        # "https://wttr.in//Beijing"   ← 双斜杠，服务器可能报错！
       

    def __str__(self) -> str:
        # 返回友好的字符串表示
        return f"WeatherClient(base_url = {self.base_url})"


    def __repr__(self):
        # 返回开发者友好的字符串
        return f"WeatherClient(base_url = {self.base_url!r})"


    def get_weather(self, city: str) -> dict | None:
        url = f"{self.base_url}/{city}"
        params = {"format": "j1"}
        # "请用 JSON 格式（j = json，1 = 第一版）返回天气数据"
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Timeout:
            print("[错误] 请求超时")
        except ConnectionError:
            print("[错误] 网络连接失败")
        except HTTPError as e:
            print(f"[错误] HTTP {e.response.status_code}")
        except ValueError:
            print("[错误] 响应不是合法 JSON")
        return  None

    def save_to_file(self,data:dict,filepath:str)->bool:
        try:
            with open(filepath,"w",encoding="utf-8") as f:
                json.dump(data, f, indent=2,ensure_ascii=False)
                # 我记得有个文件的写入f.write，为什么不用这个，给我和JSON.dump知识点一起讲一下
                print(f"[成功] 已保存到 {filepath}")
                return True
        except Exception as e:
            print(f"[错误] 文件写入失败: {e}")
            return False



def format_weather(data: dict) -> str:
    temp = data.get("current_condition",[{}])[0]["temp_C"]
    city = data.get("nearest_area",[{}])[0]["areaName"][0]["value"]
    desc = data.get("current_condition",[{}])[0]["weatherDesc"][0]["value"]
    humidity = data.get("current_condition",[{}])[0]["humidity"]
    return (
        f"城市: {city}\n"
        f"温度: {temp}°C\n"
        f"天气: {desc}\n"
        f"湿度: {humidity}%"
    )


if __name__ == "__main__":
    client = WeatherClient()
    print(client)

    city = input("请输入城市名（如 Beijing / 北京）: ").strip()#去掉首尾空格（防止用户多打空格）
    if not city:
        print("城市名不能为空")
        exit()
    data = client.get_weather(city)
    if data:
        print("\n=== 天气信息 ===")
        print(format_weather(data))
        client.save_to_file(data, f"weather_{city}.json")
    else:
        print("查询失败，请稍后重试")

    # data_str = json.dumps(data, indent=2)
    # print(data_str)
    # if data:
    #     print(format_weather(data))
    #     client.save_to_file(data, f"weather_Beijing.json")
    # else:
    #     print("查询失败")
