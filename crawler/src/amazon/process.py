from bs4 import BeautifulSoup
from currency_converter import converter
import re

currency_keys = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'YER', 'ZAR', 'ZMW', 'ZWL']
def extract_numbers(input_string):
    numbers = re.findall(r'-?\d+\.?\d*', input_string)
    return [float(num) if '.' in num else int(num) for num in numbers]

def extract_content(page_info):
    shops = page_info.find('span', attrs={'data-component-type': 's-search-results'})
    iterms = shops.find_all('div', attrs={'data-component-type': 's-search-result'})
    # print(len(iterms))
    for iterm in iterms:
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
                price = price.get_text().strip()
                price = price.replace(",", "")
                # print(price)
                prices = extract_numbers(price)
                price_num = prices[0]
                price_index = price.find(str(price_num))
                price_currency = price[:price_index]
                # print(price_currency)
                if price_currency == '':
                    price_currency = '$'
                if price_currency != '$' and price_currency != 'USD' and price_currency != 'US$':
                    # print(price_currency)
                    if "元" in price or "¥" in price:
                        price_currency = "CNY"
                    print(price_currency)
                    if price_currency not in currency_keys:
                        continue
                    rate = converter.get_exchange_rate(price_currency, 'USD')
                    price_num = price_num * rate
                price = '$' + str(price_num)
                # print(price)
        else: 
            price = "No price"
            
        if price == "No price":
            continue

        item_info = {
            'id': iterm_id,
            'title': iterm_title,
            'url': iterm_url,
            'image_url': image_url,
            'star': star,
            'customer': customer,
            'price': price
        }
        yield item_info

def process_page_info(page_info):
    content_list = extract_content(page_info)
    return content_list
