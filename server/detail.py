import threading
import time
import mysql.connector
from curl_cffi import requests
from bs4 import BeautifulSoup
import platform
from index.mail import send_email_to
import re

if platform.system() == "Windows":
    db_password = "Hz040719"  # Windows 下的密码
else:
    db_password = ""    # macOS 下的密码
def extract_numbers(input_string):
    # 使用正则表达式匹配整数和小数
    numbers = re.findall(r'-?\d+\.?\d*', input_string)
    return [float(num) if '.' in num else int(num) for num in numbers]

def fetch_marked_items():
    """
    从 MySQL 的 marked_items 表中获取平台和 UUID，并处理商品 URL。
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",      
            user="root",      
            password=db_password, 
            database="user"   
        )

        cursor = conn.cursor(dictionary=True)

        # 查询 marked_items 表
        query = "SELECT platform, uuid FROM marked_items"
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        conn.close()

        for item in items:
            platform = item["platform"]
            uuid = item["uuid"]

            if platform == 0:
                database = "Amazon"
            else:
                database = "ebay"
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=db_password,
                database=database
            )
            cursor = conn.cursor(dictionary=True)

            product_query = f"SELECT url, price FROM products WHERE id = %s"
            cursor.execute(product_query, (uuid,))
            product = cursor.fetchall()
            print(len(product))
            if (len(product) != 0):
                product = product[-1]

            cursor.close()
            conn.close()
            if product:
                url = product["url"]
                price = product["price"]
                print(f"商品 URL: {url}")
                scrape_product_info(platform,url,price, uuid)
            else:
                print(f"商品未找到，平台: {platform}, UUID: {uuid}")
    except mysql.connector.Error as e:
        print(f"MySQL 错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")


def scrape_product_info(platform, url, price, uuid):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        page_info = requests.get(url, 
                    headers={
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
                    },
                    impersonate="chrome101")
        if page_info.status_code == 200:
            soup = BeautifulSoup(page_info.content, "html.parser")
            if platform == 0:
                price_span = soup.find("span", attrs={'class': 'aok-offscreen'})
                with open("product_info.txt", "w") as file:
                    file.write(soup.prettify())
                if price_span:
                    new_price = price_span.get_text(strip=True)
                    # insert into db
                    database = "Amazon"
                    conn = mysql.connector.connect(
                        host="localhost",
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
                    new_price = extract_numbers(new_price)
                    prices = extract_numbers(price)
                    print(f"商品价格: {price} -> {new_price}")
                    if (prices <= new_price):
                        # query all users who has marked this item
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password=db_password,
                            database="user"
                        )
                        cursor = conn.cursor(dictionary=True)
                        cursor.execute("SELECT id FROM marked_items WHERE uuid = %s", (uuid))
                        users = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        for user in users:
                            cursor.execute("SELECT email FROM users WHERE id = %s", (user["id"],))
                            email = cursor.fetchone()["email"]
                            title = "你标记的商品正在降价销售"
                            body = f"你标记的商品正在降价销售，原价为 {price}，现价为 {new_price}，请尽快查看！"
                            send_email_to(email, title, body, 1)
                else:
                    print("价格信息未找到")
            else:
                price_span = soup.find("span", attrs={'class': 'x-price-approx__price'})
                if price_span:
                    new_price = price_span.get_text(strip=True)
                    # insert into db
                    database = "ebay"
                    conn = mysql.connector.connect(
                        host="localhost",
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
                    print(f"商品价格: {price} -> {new_prices}")
                    if (prices <= new_prices):
                        # query all users who has marked this item
                        conn = mysql.connector.connect(
                            host="localhost",
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
                            send_email_to(email, title, body, 1)
                        cursor.close()
                        conn.close()
                        
                        

                else:
                    print("价格信息未找到")
                
        else:
            print(f"请求失败，状态码: {page_info.status_code}")
    except Exception as e:
        print(f"抓取网页信息时出错: {e}")


def background_task():
    """
    持续运行的子线程任务，每隔固定时间检查数据库。
    """
    while True:
        time.sleep(3600*24)  # 每 1 天检查一次
        print("开始检查 marked_items...")
        fetch_marked_items()


def start_background_task():
    # 启动子线程
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
    print("子线程已启动")

# if __name__ == "__main__":
#     fetch_marked_items()