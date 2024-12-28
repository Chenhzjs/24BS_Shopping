import threading
import time
import mysql.connector
from curl_cffi import requests
from bs4 import BeautifulSoup
import platform
from index.mail import send_email_to
from currency_converter import converter
import re
currency_keys = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'YER', 'ZAR', 'ZMW', 'ZWL']

if platform.system() == "Windows":
    db_password = ""  
else:
    db_password = ""    
def extract_numbers(input_string):
    numbers = re.findall(r'-?\d+\.?\d*', input_string)
    return [float(num) if '.' in num else int(num) for num in numbers]

def fetch_marked_items():

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",      
            user="root",      
            password=db_password, 
            database="user"   
        )

        cursor = conn.cursor(dictionary=True)


        query = "SELECT platform, uuid FROM marked_items"
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        # print(f"共有 {len(items)} 个标记商品")
        for item in items:
            platform = item["platform"]
            uuid = item["uuid"]

            if platform == "0":
                database = "Amazon"
            else:
                database = "ebay"
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password=db_password,
                database=database
            )
            print(f"正在处理...\n平台: {database}, UUID: {uuid}")
            cursor = conn.cursor(dictionary=True)

            product_query = f"SELECT url, price FROM products WHERE id = %s"
            cursor.execute(product_query, (uuid,))
            # print(product_query)
            product = cursor.fetchall()
            print(len(product))
            if (len(product) != 0):
                product = product[-1]

            cursor.close()
            conn.close()
            if product:
                url = product["url"]
                price = product["price"]
                # print(f"商品 URL: {url}")
                scrape_product_info(platform,url,price, uuid)
            else:
                print(f"商品未找到，平台: {platform}, UUID: {uuid}")
    except mysql.connector.Error as e:
        print(f"MySQL 错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

def scrape_product_info(platform, url, price, uuid):
    try:
        print("start")
        page_info = requests.get(url, 
                    headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
                    },
                    impersonate="chrome101")
        
        soup = BeautifulSoup(page_info.content, "html.parser")
        print(f"正在处理商品 URL: {url}")
        if platform == "0":
            price_spans = soup.findAll("span", attrs={'class': 'aok-offscreen'})
            # print(len(price_spans))
            for price_span_tmp in price_spans:
                # 如果class只有 aok-offscreen，说明是价格
                if price_span_tmp.get("class") == ['aok-offscreen']:
                    price_span = price_span_tmp
                    break

            # with open("product_info_amazon.txt", "w") as file:
            #     file.write(soup.prettify())
            if price_span:
                new_price = price_span.get_text(strip=True)
                new_price = new_price.replace(",", "")
                # print(price)
                new_prices = extract_numbers(new_price)
                new_price_num = new_prices[0]

                # # find price_num in price
                new_price_index = new_price.find(str(new_price_num))
                new_price = price[:new_price_index + len(str(new_price_num))]
                new_price_currency = new_price[:new_price_index]
                if new_price_currency != '$' and new_price_currency != 'USD' and new_price_currency != 'US$' and new_price_currency != 'US $':
                    if "元" in price or "¥" in price:
                        new_price_currency = "CNY"
                    # print(price_currency)
                    if new_price_currency not in currency_keys:
                        return 
                    rate = converter.get_exchange_rate('USD', new_price_currency)
                    new_price_num = new_price_num / rate
                new_price = '$' + str(new_price_num)
                # print(new_price)
                # insert into db
                database = "Amazon"
                conn = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password=db_password,
                    database=database
                )
                cursor = conn.cursor(dictionary=True)
                # query other info
                cursor.execute("SELECT title, image_url, star, customer FROM products WHERE id = %s", (uuid,))
                product = cursor.fetchall()
                product = product[-1]
                cursor.execute("INSERT INTO products (id, title, url, image_url, star, customer, price) VALUES (%s, %s, %s, %s, %s, %s, %s)", (uuid, product["title"], url, product["image_url"], product["star"], product["customer"], new_price))
                conn.commit()
                cursor.close()
                conn.close()
                new_prices = extract_numbers(new_price)
                prices = extract_numbers(price)
                # print(prices[0], new_prices[0])
                print(f"商品价格: {price} -> {new_price}")
                if (prices[0] > new_prices[0]):
                    # query all users who has marked this item
                    conn = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password=db_password,
                        database="user"
                    )
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT id FROM marked_items WHERE uuid = %s", (uuid, ))
                    users = cursor.fetchall()
                    
                    for user in users:
                        cursor.execute("SELECT email FROM users WHERE id = %s", (user["id"],))
                        email = cursor.fetchone()["email"]
                        title = "你标记的商品正在降价销售"
                        p_title = product["title"]
                        body = f"你标记的商品 {p_title} 正在降价销售，原价为 {price}，现价为 {new_price}，请尽快查看！"
                        # print(email, title, body)
                        send_email_to(email, title, body, 0)

                    cursor.close()
                    conn.close()
            else:
                print("价格信息未找到")
        else:
            price_span = soup.find("div", attrs={'class': 'x-price-primary'})
            if price_span is None:
                price_span = soup.find("span", attrs={'class': 'x-price-approx__price'})
            # with open("product_info_ebay.txt", "w") as file:
            #     file.write(soup.prettify())
            if price_span:
                new_price = price_span.get_text(strip=True)
                new_price = new_price.replace(",", "")
                # print(new_price)
                new_prices = extract_numbers(new_price)
                new_price_num = new_prices[0]
                # # find new_price_num in new_price
                new_price_index = new_price.find(str(new_price_num))
                new_price_currency = new_price[:new_price_index]
                if new_price_currency != '$' and new_price_currency != 'USD' and new_price_currency != 'US$' and new_price_currency != 'US $':
                    if "元" in new_price or "¥" in new_price:
                        new_price_currency = "CNY"
                    # print(new_price_currency)
                    if new_price_currency not in currency_keys:
                        return 
                    rate = converter.get_exchange_rate('USD', new_price_currency)
                    new_price_num = new_price_num / rate
                new_price = '$' + str(new_price_num)
                # insert into db
                database = "ebay"
                conn = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password=db_password,
                    database=database
                )
                cursor = conn.cursor(dictionary=True)
                # query other info
                cursor.execute("SELECT title, image_url, star, customer FROM products WHERE id = %s", (uuid,))
                product = cursor.fetchall()
                product = product[-1]
                print(product)
                cursor.execute("INSERT INTO products (id, title, url, image_url, star, customer, price) VALUES (%s, %s, %s, %s, %s, %s, %s)", (uuid, product["title"], url, product["image_url"], product["star"], product["customer"], new_price))
                conn.commit()
                cursor.close()
                conn.close()
                new_prices = extract_numbers(new_price)
                prices = extract_numbers(price)
                print(f"商品价格: {price} -> {new_price}")
                # print(prices[0], new_prices[0])
                if (prices[0] > new_prices[0]):
                    # query all users who has marked this item
                    conn = mysql.connector.connect(
                        host="127.0.0.1",
                        user="root",
                        password=db_password,
                        database="user"
                    )
                    cursor = conn.cursor(dictionary=True)
                    cursor.execute("SELECT id FROM marked_items WHERE uuid = %s", (uuid, ))
                    users = cursor.fetchall()
                    
                    for user in users:
                        cursor.execute("SELECT email FROM users WHERE id = %s", (user["id"],))
                        email = cursor.fetchone()["email"]
                        title = "你标记的商品正在降价销售"
                        p_title = product["title"]
                        body = f"你标记的商品 {p_title} 正在降价销售，原价为 {price}，现价为 {new_price}，请尽快查看！"
                        # print(email, title, body)
                        send_email_to(email, title, body, 0)
                    cursor.close()
                    conn.close()
            else:
                print("价格信息未找到")
    except Exception as e:
        print(f"抓取网页信息时出错: {e}")


def background_task():
    while True:
        time.sleep(120*1)  
        print("开始检查 marked_items...")
        fetch_marked_items()


if __name__ == "__main__":
    background_task()
