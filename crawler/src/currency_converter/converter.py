import requests

class CurrencyConverter:
    def __init__(self, api_key="651c433434b3404fb08de0f7f9e6e14b"):
        self.api_key = api_key
        self.base_url = "https://openexchangerates.org/api/latest.json"
        self.data = {}

    def get_exchange_rate(self, base_currency, target_currency):
        try:
            if (base_currency, target_currency) in self.data:
                return self.data[(base_currency, target_currency)]

            url = f"{self.base_url}?app_id={self.api_key}&base={base_currency}"

            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"API请求失败，状态码: {response.status_code}")
            
            data = response.json()
            
            if target_currency not in data['rates']:
                raise Exception(f"目标货币 {target_currency} 不存在于返回的汇率中。")
            
            rate = data['rates'][target_currency]
            
            self.data[(base_currency, target_currency)] = rate
            
            return rate

        except Exception as e:
            print(f"获取汇率时出错: {e}")
            return None