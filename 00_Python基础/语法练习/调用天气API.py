import requests

r = requests.get("https://wttr.in/Beijing?format=j1")

r.raise_for_status()
data = r.json()
print(data)

Today = data["current_condition"][0]

print(f"温度：{Today['temp_C']}°C")
print(f"体感: {Today['FeelsLikeC']}°C")
print(f"天气: {Today['weatherDesc'][0]['value']}")
print(f"湿度: {Today['humidity']}%")
print(f"风速: {Today['windspeedKmph']} km/h")
