import requests

api_key = "651c433434b3404fb08de0f7f9e6e14b"  
base_currency = "USD"  
target_currency = "USD"  

url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}&base={base_currency}"
print(url)
response = requests.get(url)
data = response.json()
print(data)
print(data['rates'])
exchange_rate = data['rates'][target_currency]

print(f"1 {base_currency} = {exchange_rate} {target_currency}")