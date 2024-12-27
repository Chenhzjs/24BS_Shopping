import requests

class CurrencyConverter:
    def __init__(self, api_key="651c433434b3404fb08de0f7f9e6e14b"):
        self.api_key = api_key
        self.base_url = "https://openexchangerates.org/api/latest.json"
        self.data = None

    def get_exchange_rate(self, base_currency, target_currency):
        try:
            url = f"{self.base_url}?app_id={self.api_key}&base={base_currency}"
            if self.data is None:
                self.data = {}
            if base_currency not in self.data:
                self.data[base_currency] = {}
            if (self.data[base_currency] is not None) and (target_currency in self.data[base_currency]):
                return self.data[base_currency][target_currency]
            response = requests.get(url)
            
            if response.status_code != 200:
                raise Exception(f"API请求失败，状态码: {response.status_code}")
            
            data = response.json()

            # 保存返回的数据
            for key, value in data.items():
                data[base_currency][key] = value
            print(data)
            # 检查目标货币是否在返回的汇率中
            if target_currency not in data['rates']:
                raise Exception(f"目标货币 {target_currency} 不存在于返回的汇率中。")
            return data['rates'][target_currency]
        except Exception as e:
            print(f"获取汇率时出错: {e}")
            return None
        
