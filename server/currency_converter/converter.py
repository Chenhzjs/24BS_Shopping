import requests

class CurrencyConverter:
    def __init__(self, api_key="651c433434b3404fb08de0f7f9e6e14b"):
        self.api_key = api_key
        self.base_url = "https://openexchangerates.org/api/latest.json"
        self.data = {}

    def get_exchange_rate(self, base_currency, target_currency):
        try:
            # 检查缓存中是否已经存在该汇率
            if (base_currency, target_currency) in self.data:
                return self.data[(base_currency, target_currency)]

            # 构建API请求URL
            url = f"{self.base_url}?app_id={self.api_key}&base={base_currency}"

            # 发送请求
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"API请求失败，状态码: {response.status_code}")
            
            data = response.json()
            # print(data)
            
            # 检查目标货币是否在返回的汇率中
            if target_currency not in data['rates']:
                raise Exception(f"目标货币 {target_currency} 不存在于返回的汇率中。")
            
            # 获取汇率
            rate = data['rates'][target_currency]
            
            # 缓存汇率数据
            self.data[(base_currency, target_currency)] = rate
            # print(self.data)
            
            return rate

        except Exception as e:
            print(f"获取汇率时出错: {e}")
            return None