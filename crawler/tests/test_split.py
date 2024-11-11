from bs4 import BeautifulSoup
import re
def extract_content(content, title):
    length = len(title)

    prev_start = content.find(title)
    print(prev_start)
    content = content[prev_start:]
    # print(content[:200])
    # exit(1)
    while content[length:].find(title) != -1:
        start = content[length:].find(title) + length
        yield content[:start]
        prev_start = start
        content = content[prev_start:]

    yield content

    
file_path = 'product_info.txt'
try:
    with open(file_path, 'r') as file:
        content = file.read()
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except IOError:
    print(f"Error reading file '{file_path}'.")

title = '<a class="doubleCardWrapper--'
start = content.find('div class="contentInner--')
end = content.find('<!-- js 禁用提示 -->')
content = content[start:end]
content_list = extract_content(content, title)
iterms = []
for iterm in content_list:
    iterms.append(iterm)
    # print(iterm[:200])

def soup_find(tag, str, *args):
    find_temp = soup.find(tag, class_=re.compile(str))
    print(find_temp)
    print("******")
    find_res = soup.find(tag, class_=re.compile(str))
    if (tag == 'img' and find_res is None): exit(111)
    # print(find_res)
    if find_res:
        if (args):
            return find_res.get(args[0])
        else:
            return find_res.get_text().strip()
    else:
        return None

for iterm in iterms:
    soup = BeautifulSoup(iterm, 'html.parser')

    # print(soup.prettify())
    # 使用BeautifulSoup解析HTML


    # 提取商品名称
    # title = soup.find("span", class_="").get_text().strip()
    title = soup_find("span", "")

    # url = soup.find("a", class_=re.compile("doubleCardWrapper"))["href"]
    url = soup_find("a", "doubleCardWrapper--........", "href")
    # exit(1)
    
    # image_url = soup.find("img", class_=re.compile("mainPic--"))["src"]
    image_url = soup_find("img", "mainPic--........", "src")

    # views = soup.find("div", class_=re.compile("summaryADWrapper")).get_text().strip()
    views = soup_find("div", "summaryADWrapper--........")

    # 提取价格信息
    # price = soup.find("span", class_=re.compile("priceInt")).get_text().strip()
    price = soup_find("span", "priceInt--........")

    # 提取付款人数
    # sales = soup.find("span", class_=re.compile("realSales")).get_text().strip()
    sales = soup_find("span", "realSales--........")

    # 提取商品销售地
    # location = soup.find("div", class_=re.compile("procity")).get_text().strip()
    location = soup_find("div", "procity--........")

    # 提取促销信息
    # promotion = [span.get_text().strip() for span in soup.find_all("span", style="color: rgb(255, 98, 0);")]

    # 打印提取的内容
    print(f"商品名称: {title}")
    print(f"商品链接: {url}")
    print(f"商品图片: {image_url}")
    print(f"观看人数: {views}")
    print(f"价格: ¥{price}")
    print(f"付款人数: {sales}")
    print(f"销售地: {location}")
    print('---')
    # print(f"促销信息: {', '.join(promotion)}")
    # exit(1)