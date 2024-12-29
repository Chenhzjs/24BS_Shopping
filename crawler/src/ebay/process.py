from bs4 import BeautifulSoup
from currency_converter import converter
import re
def extract_numbers(input_string):
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
currency_keys = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'YER', 'ZAR', 'ZMW', 'ZWL']
def extract_content(page_info):
    # print(page_info.prettify())
    # <div class="srp-river-results clearfix" id="srp-river-results">
    shops = page_info.find('div', attrs={'id': 'srp-river-results'})

    iterms = shops.find_all('li', attrs={'class':'s-item s-item__pl-on-bottom'})
    iterm_final = shops.find('li', attrs={'class':'s-item s-item__before-answer s-item__pl-on-bottom'})
    iterms = iterms + [iterm_final]
    # iterms = shops.find_all('div', attrs={'data-component-type':'s-search-result'})
    for iterm in iterms:
        if iterm is None:
            continue
    #     ########### image&title&url ############
        id = iterm.get('id')
        title = iterm.find('div', attrs={'class':'s-item__title'}).get_text().strip()
        url = iterm.find('a', attrs={'class':'s-item__link'}).get('href')
        print(title)
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
            price = price.replace(",", "")
            print(price)
            prices = extract_numbers(price)
            price_num = prices[0]
            # # find price_num in price
            price_index = price.find(str(price_num))
            price_currency = price[:price_index].strip()
            if price_currency != '$' and price_currency != 'USD' and price_currency != 'US$':
                if "元" in price or "¥" in price:
                    price_currency = "CNY"
                # print(price_currency)
                # print(price_currency not in currency_keys)
                if price_currency not in currency_keys:
                    continue
                rate = converter.get_exchange_rate('USD', price_currency)
                price_num = price_num / rate
            price = '$' + str(price_num)
            # print(price)
            # index = price_index
            # print(index, price_index)
            # # while price[index] != '>':
            # #     index -= 1
            # print(index, price_index, price[index:price_index])
            # if len(prices) == 2:
            #     price = 'NKD ' + prices[0]
        if price == "No price" :
            continue
        
        item_info = {
            'id': id,
            'title': title,
            'url': url,
            'image_url': image_url,
            'star': star,
            'customer': customer,
            'price': price
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
