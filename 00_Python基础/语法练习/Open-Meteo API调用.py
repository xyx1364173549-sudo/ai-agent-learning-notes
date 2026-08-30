import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 39.90,
    "longitude": 116.41,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "Asia/Shanghai"
}
r = requests.get(url, params=params, timeout=30)
print("1.状态码：", r.status_code)
print("2.类型：", r.headers.get("Content-Type"))
data = r.json()
print(data)

print("3.湿度：", data["current"]["relative_humidity_2m"], "%")
print("4. 温度:", data["current"]["temperature_2m"], "°C")
# 逗号隔开  print("a","b","c") abc
#
print(f"4.温度：{data["current"]["temperature_2m"]}°C")
