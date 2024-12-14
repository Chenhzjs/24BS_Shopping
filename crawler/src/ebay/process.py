from bs4 import BeautifulSoup
import re
def extract_numbers(input_string):
    # 使用正则表达式匹配整数和小数
    numbers = re.findall(r'-?\d+\.?\d*', input_string)
    return [float(num) if '.' in num else int(num) for num in numbers]

# def soup_find(soup, tag, str, *args):
#     find_temp = soup.find(tag, class_=re.compile(str))
#     print(find_temp)
#     print("******")
#     find_res = soup.find(tag, class_=re.compile(str))
#     if (tag == 'img' and find_res is None): exit(111)
#     # print(find_res)
#     if find_res:
#         if (args):
#             return find_res.get(args[0])
#         else:
#             return find_res.get_text().strip()
#     else:
#         return None
'''
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    url TEXT,
    image_url TEXT,
    star VARCHAR(50),
    customer VARCHAR(100),
    price VARCHAR(50),
'''
def extract_content(page_info):
    # print(page_info.prettify())
    # <div class="srp-river-results clearfix" id="srp-river-results">
    shops = page_info.find('div', attrs={'id': 'srp-river-results'})

    iterms = shops.find_all('li', attrs={'class':'s-item s-item__pl-on-bottom'})
    iterm_final = shops.find('li', attrs={'class':'s-item s-item__before-answer s-item__pl-on-bottom'})
    iterms = iterms + [iterm_final]
    # print(len(iterms))
    # print(shops)
    # iterms = shops.find_all('div', attrs={'data-component-type':'s-search-result'})
    print(len(iterms))
    # print(iterms[0])
    for iterm in iterms:
        if iterm is None:
            continue
    #     # print("*****************")
    #     ########### image&title&url ############
        id = iterm.get('id')
        title = iterm.find('div', attrs={'class':'s-item__title'}).get_text().strip()
        url = iterm.find('a', attrs={'class':'s-item__link'}).get('href')
        # print(title)
        _image = iterm.find('div',attrs={'class':'s-item__image-wrapper image-treatment'})
        image = _image.find('img')
        image_url = image.get('src')
        star = 'no star' if iterm.find('span', attrs={'class':'s-item__etrs-text'}) is None else iterm.find('span', attrs={'class':'s-item__etrs-text'}).get_text()
        customer = iterm.find('span', attrs={'class':'s-item__seller-info'})
        if customer is None:
            customer = "No evaluation"
        else:
            customer = customer.get_text().strip()
        if "(" in customer:
            customer = customer.split("(")[1].strip()
            customer = customer.replace(",", "")
            customer = customer.split(")")[0].strip()
        price = iterm.find('span', attrs={'class':'s-item__price'})
        if price is None:
            price = "No price"
        else:
            price = price.get_text().strip()
            prices = extract_numbers(price)
            if len(prices) == 2:
                price = 'NKD ' + prices[0]
        if price == "No price" :
            continue
        
        item_info = {
            'id': id,
            'title': title,
            'url': url,
            'image_url': image_url,
            'star': star,
            'customer': customer,
            'price': "No price" if price == "No price" else price
        }
        yield item_info
    #     # print(star)
    #     # print(customer)
    #     # if (iterm == iterms[0]):
    #         # print(star)
            
    #         # print(star_and_customer.prettify())
    #     #     for i in range(len(star)):
    #     #         print(star[i].prettify())
    #     # print(image_url)
    #     # print(iterm_title)
    #     # print(iterm_url)
    #     # print(iterm.prettify())
    #     # print(iterm.find('a', class_=re.compile
    # # length = len(title)

    # # prev_start = content.find(title)
    # # print(prev_start)
    # # content = content[prev_start:]
    # # # print(content[:200])
    # # # exit(1)
    # # while content[length:].find(title) != -1:
    # #     start = content[length:].find(title) + length
    # #     yield content[:start]
    # #     prev_start = start
    # #     content = content[prev_start:]

    # # yield content

def process_page_info(page_info):
    content_list = extract_content(page_info)
    # for content in content_list:
    #     print(content)
    #     print("*****************")
    return content_list

# read process_info.txt file
# file_path = 'product_info.txt'
# try:
#     with open(file_path, 'r') as file:
#         content = file.read()
#         page_info = BeautifulSoup(content, 'html.parser')
# except FileNotFoundError:
#     print(f"File '{file_path}' not found.")
# except IOError:
#     print(f"Error reading file '{file_path}'.")
# # print(page_info.prettify())
# content_list = process_page_info(page_info)

# for content in content_list:
#     print(content)
#     print("*****************")