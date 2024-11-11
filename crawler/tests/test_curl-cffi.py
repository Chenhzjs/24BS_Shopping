from curl_cffi import requests
import json
import os
COOKIES_FILE = "taobao_cookies.json"

def load_cookies():
    # 如果本地存在 Cookies 文件，加载到浏览器上下文
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r') as file:
            cookies = json.load(file)
        return convert_cookies_to_string(cookies)

def convert_cookies_to_string(cookies):
    # cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    # print("Cookies = ", cookie_str)
    # return cookie_str
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    print("Cookies 已加载：", cookies_dict)
    return cookies_dict
# 使用 GET 请求
url = "https://s.taobao.com/search?q=手机"

response = requests.get(url, 
                        headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
                        },
                        cookies=load_cookies(),
                        impersonate="chrome101")
# print(response.json())
# 检查响应状态码
print("状态码：", response.status_code)
if response.status_code == 200:
    print("请求成功！")
    print("响应内容：", response.text)
else:
    print("请求失败，状态码：", response.status_code)