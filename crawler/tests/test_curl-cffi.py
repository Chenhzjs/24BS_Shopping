from curl_cffi import requests
import json
import os



# 使用 GET 请求
url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=phone&_sacat=0"
# url = "https://www.amazon.com/s?k=phone" 

response = requests.get(url, 
                        headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
                        },
                        impersonate="chrome101")
# print(response.json())
# 检查响应状态码
print("状态码：", response.status_code)
if response.status_code == 200:
    print("请求成功！")
    print("响应内容：", response.text)
else:
    print("请求失败，状态码：", response.status_code)