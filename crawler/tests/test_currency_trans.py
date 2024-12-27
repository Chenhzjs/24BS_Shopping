import requests

api_key = "651c433434b3404fb08de0f7f9e6e14b"  # 替换为实际的API密钥
base_currency = "USD"  # 设定基准货币
target_currency = "CNY"  # 设定目标货币

url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base={base_currency}"
response = requests.get(url)
data = response.json()
print(data['rates'])
exchange_rate = data['rates'][target_currency]

print(f"1 {base_currency} = {exchange_rate} {target_currency}")