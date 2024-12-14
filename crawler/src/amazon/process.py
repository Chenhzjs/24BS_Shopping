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
    shops = page_info.find('span', attrs={'data-component-type': 's-search-results'})
    # print(shops)
    iterms = shops.find_all('div', attrs={'data-component-type': 's-search-result'})
    print(len(iterms))
    # print(iterms[0])
    for iterm in iterms:
        # print("*****************")
        ########### image&title&url ############
        iterm_id = iterm.get('data-asin')
        # print(iterm_id)
        _image = iterm.find('span',attrs={'data-component-type':'s-product-image'})
        image = _image.find('img')
        image_url = image.get('src')
        # print(image_url)
        iterm_title = image.get('alt')
        iterm_url = "https://www.amazon.com" + _image.find('a').get('href')
        # print(iterm_url)
        # data-cy="reviews-block"
        ########### star&customer ############
        star_and_customer = iterm.find('div', attrs={'data-cy':'reviews-block'})
        if (star_and_customer is None):
            star = "No star"
            customer = "No evaluation"
        else:
            star = star_and_customer.find('span', attrs={'class':'a-icon-alt'})
            if (star is None):
                star = "No star"
            else:
                star = star.get_text()
                star = star.strip()
            # class="a-size-base a-color-secondary"
            customer = star_and_customer.find('span', string=re.compile("购买"))
            if (customer is None):
                customer = "No evaluation"
            else:
                customer = customer.get_text()
                customer = customer.strip()
        ########### price ############
        price = iterm.find('div', attrs={'data-cy':'price-recipe'})
        if price is not None:
            price = price.find('span', attrs={'class':'a-offscreen'})
            if (price is None):
                price = "No price"
            else:  
                price = price.get_text()
                price = price.strip()
        else: 
            price = "No price"
        #  <span class="a-offscreen">
        
        # print(price)
        # print(iterm_title)
        # print(iterm_url)
        # print(image_url)
        # print(star)
        # print(customer)
        # print(price)
        if price == "No price":
            continue

        item_info = {
            'id': iterm_id,
            'title': iterm_title,
            'url': iterm_url,
            'image_url': image_url,
            'star': star,
            'customer': customer,
            'price': "No price" if price == "No price" else price
        }
        yield item_info

def process_page_info(page_info):
    content_list = extract_content(page_info)
    # for content in content_list:
    #     print(content)
    #     print("*****************")
    return content_list

# with open('result.out', 'r') as file:
#     page_info = file.read()
#     page_info = BeautifulSoup(page_info, 'html.parser')
#     # print(page_info.prettify())
#     process_page_info(page_info)