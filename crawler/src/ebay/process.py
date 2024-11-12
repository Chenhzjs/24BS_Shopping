from bs4 import BeautifulSoup
import re
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
    # # print(len(iterms))
    print(iterms[0])
    # for iterm in iterms:
    #     # print("*****************")
    #     ########### image&title&url ############
    #     _image = iterm.find('span',attrs={'data-component-type':'s-product-image'})
    #     image = _image.find('img')
    #     image_url = image.get('src')
    #     iterm_title = image.get('alt')
    #     iterm_url = "https://www.amazon.com" + _image.find('a').get('href')
    #     # data-cy="reviews-block"
    #     ########### star&customer ############
    #     star_and_customer = iterm.find('div', attrs={'data-cy':'reviews-block'})
    #     if (star_and_customer is None):
    #         star = "No star"
    #         customer = "No evaluation"
    #     else:
    #         star = star_and_customer.find('span', attrs={'class':'a-icon-alt'})
    #         if (star is None):
    #             star = "No star"
    #         else:
    #             star = star.get_text()
    #             star = star.strip()
    #         # class="a-size-base a-color-secondary"
    #         customer = star_and_customer.find('span', string=re.compile("购买"))
    #         if (customer is None):
    #             customer = "No evaluation"
    #         else:
    #             customer = customer.get_text()
    #             customer = customer.strip()
    #     ########### price ############
    #     price = iterm.find('div', attrs={'data-cy':'price-recipe'})
    #     #  <span class="a-offscreen">
    #     price = price.find('span', attrs={'class':'a-offscreen'})
    #     if (price is None):
    #         price = "No price"
    #     else:  
    #         price = price.get_text()
    #         price = price.strip()
    #     # print(price)
    #     # print(iterm_title)
    #     # print(iterm_url)
    #     # print(image_url)
    #     # print(star)
    #     # print(customer)
    #     # print(price)
    #     item_info = {
    #         'title': iterm_title,
    #         'url': iterm_url,
    #         'image_url': image_url,
    #         'star': star,
    #         'customer': customer,
    #         'price': "No price" if price == "No price" else price[2:]
    #     }
    #     yield item_info
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
file_path = 'product_info.txt'
try:
    with open(file_path, 'r') as file:
        content = file.read()
        page_info = BeautifulSoup(content, 'html.parser')
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except IOError:
    print(f"Error reading file '{file_path}'.")

content_list = extract_content(page_info)

# for content in content_list:
#     print(content)
#     print("*****************")